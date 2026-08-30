import paramiko
import time
import socket
from typing import Tuple, Optional
import logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
from openhtf.core import base_plugs

import threading

dict_for_connect = \
{
    "host": "172.31.180.199",
    "port": 22,
    "username": "root",
    "password": "12345678"
}

class ControllerConnectErr(Exception):
    pass

class ControllerSSHConnector(base_plugs.BasePlug):
    """
    Controller SSH远程控制类
    针对 ESP32/WolfSSH 优化：
    1. 使用 Transport 直连，强制指定 KEX 算法。
    2. 使用无 PTY 的 Interactive Shell 进行命令交互。
    """

    def __init__(self, dict_for_connect=dict_for_connect):
        super().__init__()

        # 基础配置
        self.ssh_client: Optional[paramiko.SSHClient] = None
        self.interactive_shell: Optional[paramiko.Channel] = None
        self.host = dict_for_connect["host"]
        self.port = dict_for_connect["port"]
        self.username = dict_for_connect["username"]
        self.password = dict_for_connect["password"]
        self.timeout = 10
        self.encoding = "utf-8"
        self.shell_timeout = 30

        # SSH核心对象
        self.sock: Optional[socket.socket] = None
        self.transport: Optional[paramiko.Transport] = None
        self.interactive_channel: Optional[paramiko.Channel] = None

        # 连接状态
        self.connected = False
        self.shell_active = False

        self.motion_complete = True

    def _connect(self) -> bool:
        """
        内部方法: 建立SSH连接 (使用 Transport 直连模式)
        """
        if self.connected and self.transport and self.transport.is_active():
            return True

        try:
            # 1. 创建 Socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.timeout)
            self.sock.connect((self.host, self.port))

            # 2. 创建 Transport
            self.transport = paramiko.Transport(self.sock)

            # 3. 禁用不兼容算法，强制使用 diffie-hellman-group-exchange-sha256
            self.transport.disabled_algorithms = {
                "kex": [
                    "ecdh-sha2-nistp256",
                    "ecdh-sha2-nistp384",
                    "ecdh-sha2-nistp521",
                    "diffie-hellman-group16-sha512",
                    # "diffie-hellman-group-exchange-sha256",
                    "diffie-hellman-group14-sha256",
                    "diffie-hellman-group-exchange-sha1",
                    "diffie-hellman-group14-sha1",
                    "diffie-hellman-group1-sha1",
                ]
            }

            # 4. 握手
            self.transport.start_client(timeout=self.timeout)

            # 5. 认证
            self.transport.auth_password(username=self.username, password=self.password)

            if not self.transport.is_authenticated():
                raise Exception("认证失败！")

            self.connected = True
            self.logger.info(f"SSH 连接到 {self.host}")
            return True

        except Exception as e:
            self.logger.error(f"连接失败: {str(e)}")
            self.connected = False
            return False

    def connect(self, retry_times: int = 3) -> None:
        """
        建立连接，支持重试
        """
        if not self.connected:

            for _ in range(retry_times):
                if self._connect():
                    break
                time.sleep(1)
            else:
                raise ControllerConnectErr(f"连接Controller失败, 重试 {retry_times} 次依然失败，请检查网络和设备状态")

            self.logger.info(f"连接Controller成功: {self.host}:{self.port}")
            return True

    def start_interactive_shell(self) -> bool:
        """
        启动交互式 Shell (无 PTY 模式，适配 WolfSSH)
        """
        try:
            # 打开一个新会话通道
            self.interactive_channel = self.transport.open_session()

            # 直接 invoke_shell，不调用 get_pty()，避免了 WolfSSH 对 PTY 请求的处理错误
            self.interactive_channel.invoke_shell()

            self.interactive_channel.settimeout(self.shell_timeout)
            self.shell_active = True

            # 等待欢迎语
            time.sleep(1)
            self._clear_buffer()  # 清空初始欢迎语，避免干扰后续命令解析

            self.logger.info("交互式shell启动成功(无PTY)")
            return True

        except Exception as e:
            self.logger.error(f"交互式shell启动失败: {str(e)}")
            self.shell_active = False
            self.interactive_channel = None
            return False

    def _clear_buffer(self):
        """清空通道缓冲区"""
        if self.interactive_channel and self.interactive_channel.recv_ready():
            try:
                self.interactive_channel.recv(4096)
            except:
                pass

    def _send_and_receive(self, command: str, timeout: int = 10) -> Tuple[str, str, int]:
        """
        通过交互式通道发送命令并读取输出
        返回: (stdout, stderr, exit_code)
        注意：嵌入式设备通常没有明确的 exit_code, 这里主要靠输出判断
        """
        if not self.shell_active or not self.interactive_channel:
            if not self.start_interactive_shell():
                return "", "Shell交互未激活", -1

        try:
            # 1. 发送命令，确保命令以换行符结尾
            if not command.endswith("\n"):
                command += "\n"

            self.interactive_channel.send(command)

            # 2. 读取输出
            start_time = time.time()
            output_buffer = ""

            # 等待一小段时间让命令开始执行
            time.sleep(0.2)

            while time.time() - start_time < timeout:
                if self.interactive_channel.recv_ready():
                    try:
                        data = self.interactive_channel.recv(4096).decode(self.encoding, errors="ignore")
                        output_buffer += data
                        # 如果收到数据，重置超时计时器的一小部分，防止长输出被切断
                        # 但这里我们主要依赖总超时
                    except Exception as e:
                        self.logger.info(f"Error reading from channel: {e}")
                        break

                # 检查是否还有数据在途中
                if not self.interactive_channel.recv_ready():
                    # 如果连续一段时间没数据，认为命令执行完毕
                    time.sleep(0.1)
                    if not self.interactive_channel.recv_ready():
                        break

            # 简单的错误判断：如果输出中包含 "error" 或 "fail" (根据实际设备调整)
            # 这里假设只要执行了就是成功，除非抛出异常
            exit_code = 0
            if "error" in output_buffer.lower() or "fail" in output_buffer.lower():
                exit_code = 1

            return output_buffer.strip(), "", exit_code

        except Exception as e:
            err_msg = f"命令执行出错：{str(e)}"
            self.logger.error(err_msg)
            return "", err_msg, -1

    def exec_command(self, command: str) -> Tuple[str, str, int]:
        """
        兼容原有接口的命令执行方法
        优先使用交互式通道，因为 exec_command 在 WolfSSH 上可能不稳定
        """
        # 尝试使用交互式通道发送命令
        return self._send_and_receive(command, timeout=15)
    
    def read_shell_output(self, timeout: int = 10) -> str:
        """
        读取交互式Shell的输出缓冲区(单独调用, 获取当前所有可用输出）

        :return: 读取到的输出字符串（忽略编码错误）
        """
        if not self.shell_active or not self.interactive_channel:
            if not self.start_interactive_shell():
                return "", "Shell交互未激活", -1

        # 2. 读取输出
        start_time = time.time()
        output_buffer = ""

        # 等待一小段时间让命令开始执行
        time.sleep(0.2)

        while time.time() - start_time < timeout:
            if self.interactive_channel.recv_ready():
                try:
                    data = self.interactive_channel.recv(4096).decode(self.encoding, errors="ignore")
                    output_buffer += data
                    # 如果收到数据，重置超时计时器的一小部分，防止长输出被切断
                    # 但这里我们主要依赖总超时
                except Exception as e:
                    self.logger.info(f"Error reading from channel: {e}")
                    break

            # 检查是否还有数据在途中
            if not self.interactive_channel.recv_ready():
                # 如果连续一段时间没数据，认为命令执行完毕
                time.sleep(0.1)
                if not self.interactive_channel.recv_ready():
                    break

        return output_buffer.strip()
    
    def tearDown(self) -> None:
        """
        关闭连接，释放资源
        """
        if self.interactive_channel:
            try:
                self.interactive_channel.close()
            except:
                pass
            self.interactive_channel = None
            self.shell_active = False

        if self.transport:
            try:
                self.transport.close()
            except:
                pass
            self.transport = None

        if self.sock:
            try:
                self.sock.close()
            except:
                pass
            self.sock = None

        self.connected = False
        self.logger.info("已关闭Controller连接")