import step_controller
import time
import threading

dict_for_connect_custom = \
{
    "host": "172.31.180.199",
    "port": 22,
    "username": "root",
    "password": "12345678"
}
controller = step_controller.ControllerSSHConnector(dict_for_connect_custom)

def motor1_ccw_cw_360():
    status = 0
    while(1):
        time.sleep(1.3)
        controller.exec_command("query status")
        log = controller.read_shell_output().strip()
        if "move_1: 0" in log: 
            print("电机1已空闲")
        else:
            print("电机1未空闲")
            continue

        if status == 0:
            controller.exec_command("ccw motor 1 degrees 360.0 speed 60.0")
            status = 1
            continue
        else:
            controller.exec_command("cw motor 1 degrees 360.0 speed 60.0")
            status = 0
            continue

def motor2_ccw_cw_360():
    status = 0
    while(1):
        time.sleep(1.3)
        controller.exec_command("query status")
        log = controller.read_shell_output().strip()
        if "move_2: 0" in log: 
            print("电机2已空闲")
        else:
            print("电机2未空闲")
            continue

        if status == 0:
            controller.exec_command("ccw motor 2 degrees 360.0 speed 60.0")
            status = 1
            continue
        else:
            controller.exec_command("cw motor 2 degrees 360.0 speed 60.0")
            status = 0
            continue

def motor3_ccw_cw_360():
    status = 0
    while(1):
        time.sleep(1.3)
        controller.exec_command("query status")
        log = controller.read_shell_output().strip()
        if "move_3: 0" in log: 
            print("电机3已空闲")
        else:
            print("电机3未空闲")
            continue

        if status == 0:
            controller.exec_command("ccw motor 3 degrees 360.0 speed 60.0")
            status = 1
            continue
        else:
            controller.exec_command("cw motor 3 degrees 360.0 speed 60.0")
            status = 0
            continue

def motor4_ccw_cw_360():
    status = 0
    while(1):
        time.sleep(1.3)
        controller.exec_command("query status")
        log = controller.read_shell_output().strip()
        if "move_4: 0" in log: 
            print("电机4已空闲")
        else:
            print("电机4未空闲")
            continue

        if status == 0:
            controller.exec_command("ccw motor 4 degrees 360.0 speed 60.0")
            status = 1
            continue
        else:
            controller.exec_command("cw motor 4 degrees 360.0 speed 60.0")
            status = 0
            continue

def motor5_ccw_cw_360():
    status = 0
    while(1):
        time.sleep(1.3)
        controller.exec_command("query status")
        log = controller.read_shell_output().strip()
        if "move_5: 0" in log: 
            print("电机5已空闲")
        else:
            print("电机5未空闲")
            continue

        if status == 0:
            controller.exec_command("ccw motor 5 degrees 360.0 speed 60.0")
            status = 1
            continue
        else:
            controller.exec_command("cw motor 5 degrees 360.0 speed 60.0")
            status = 0
            continue

def motor6_ccw_cw_360():
    status = 0
    while(1):
        time.sleep(1.3)
        controller.exec_command("query status")
        log = controller.read_shell_output().strip()
        if "move_6: 0" in log: 
            print("电机6已空闲")
        else:
            print("电机6未空闲")
            continue

        if status == 0:
            controller.exec_command("ccw motor 6 degrees 360.0 speed 60.0")
            status = 1
            continue
        else:
            controller.exec_command("cw motor 6 degrees 360.0 speed 60.0")
            status = 0
            continue

def motor5_ccw_cw_to_intr1_2():
    status = 0
    while(1):
        time.sleep(1)
        controller.exec_command("query status")
        log = controller.read_shell_output().strip()
        if "move_5: 0" in log: 
            print("电机5已空闲")
        else:
            print("电机5未空闲")
            continue

        if status == 0:
            controller.exec_command("ccw motor 5 to intr 1 speed 60.0")
            status = 1
            continue
        else:
            controller.exec_command("cw motor 5 to intr 2 speed 60.0")
            status = 0
            continue

def motor6_ccw_cw_to_intr7_8():
    status = 0
    while(1):
        time.sleep(1)
        controller.exec_command("query status")
        log = controller.read_shell_output().strip()
        if "move_6: 0" in log: 
            print("电机6已空闲")
        else:
            print("电机6未空闲")
            continue

        if status == 0:
            controller.exec_command("ccw motor 6 to intr 7 speed 60.0")
            status = 1
            continue
        else:
            controller.exec_command("cw motor 6 to intr 8 speed 60.0")
            status = 0
            continue

def motor1_ccw_cw_freq_time():
    status = 0
    while(1):
        time.sleep(1)
        controller.exec_command("query status")
        log = controller.read_shell_output().strip()
        if "move_1: 0" in log: 
            print("电机1已空闲")
        else:
            print("电机1未空闲")
            continue

        if status == 0:
            controller.exec_command("ccw motor 1 freq 1562.5 time 2.0")
            status = 1
            continue
        else:
            controller.exec_command("cw motor 1 freq 1562.5 time 2.0")
            status = 0
            continue

def motor2_ccw_cw_freq_time():
    status = 0
    while(1):
        time.sleep(1)
        controller.exec_command("query status")
        log = controller.read_shell_output().strip()
        if "move_2: 0" in log: 
            print("电机2已空闲")
        else:
            print("电机2未空闲")
            continue

        if status == 0:
            controller.exec_command("ccw motor 2 freq 1562.5 time 2.0")
            status = 1
            continue
        else:
            controller.exec_command("cw motor 2 freq 1562.5 time 2.0")
            status = 0
            continue

def motor3_ccw_cw_freq_time():
    status = 0
    while(1):
        time.sleep(1)
        controller.exec_command("query status")
        log = controller.read_shell_output().strip()
        if "move_3: 0" in log: 
            print("电机3已空闲")
        else:
            print("电机3未空闲")
            continue

        if status == 0:
            controller.exec_command("ccw motor 3 freq 1562.5 time 2.0")
            status = 1
            continue
        else:
            controller.exec_command("cw motor 3 freq 1562.5 time 2.0")
            status = 0
            continue

def motor4_ccw_cw_freq_time():
    status = 0
    while(1):
        time.sleep(1)
        controller.exec_command("query status")
        log = controller.read_shell_output().strip()
        if "move_4: 0" in log: 
            print("电机4已空闲")
        else:
            print("电机4未空闲")
            continue

        if status == 0:
            controller.exec_command("ccw motor 4 freq 1562.5 time 2.0")
            status = 1
            continue
        else:
            controller.exec_command("cw motor 4 freq 1562.5 time 2.0")
            status = 0
            continue

def motor5_ccw_cw_freq_time():
    status = 0
    while(1):
        time.sleep(1)
        controller.exec_command("query status")
        log = controller.read_shell_output().strip()
        if "move_5: 0" in log: 
            print("电机5已空闲")
        else:
            print("电机5未空闲")
            continue

        if status == 0:
            controller.exec_command("ccw motor 5 freq 1562.5 time 2.0")
            status = 1
            continue
        else:
            controller.exec_command("cw motor 5 freq 1562.5 time 2.0")
            status = 0
            continue

def motor6_ccw_cw_freq_time():
    status = 0
    while(1):
        time.sleep(1)
        controller.exec_command("query status")
        log = controller.read_shell_output().strip()
        if "move_6: 0" in log: 
            print("电机6已空闲")
        else:
            print("电机6未空闲")
            continue

        if status == 0:
            controller.exec_command("ccw motor 6 freq 1562.5 time 2.0")
            status = 1
            continue
        else:
            controller.exec_command("cw motor 6 freq 1562.5 time 2.0")
            status = 0
            continue

if __name__ == "__main__":
    controller.connect()
    controller.exec_command("ls")

    # 示例1，所有电机同时循环360°往复
    # 启动各电机线程
    threading.Thread(target=motor1_ccw_cw_360, daemon=True).start()
    threading.Thread(target=motor2_ccw_cw_360, daemon=True).start()
    threading.Thread(target=motor3_ccw_cw_360, daemon=True).start()
    threading.Thread(target=motor4_ccw_cw_360, daemon=True).start()
    threading.Thread(target=motor5_ccw_cw_360, daemon=True).start()
    threading.Thread(target=motor6_ccw_cw_360, daemon=True).start()

    # # 示例2，电机1至电机4以60r/min的速度作360°往复，电机5和电机6以60r/min的速度分别循环往复至两边的中断传感器位置
    # threading.Thread(target=motor1_ccw_cw_360, daemon=True).start()
    # threading.Thread(target=motor2_ccw_cw_360, daemon=True).start()
    # threading.Thread(target=motor3_ccw_cw_360, daemon=True).start()
    # threading.Thread(target=motor4_ccw_cw_360, daemon=True).start()
    # threading.Thread(target=motor5_ccw_cw_to_intr1_2, daemon=True).start()
    # threading.Thread(target=motor6_ccw_cw_to_intr7_8, daemon=True).start()

    # # 示例3，所有电机分别接受（1562.5HZ脉冲2秒往复信号）的控制
    # threading.Thread(target=motor1_ccw_cw_freq_time, daemon=True).start()
    # threading.Thread(target=motor2_ccw_cw_freq_time, daemon=True).start()
    # threading.Thread(target=motor3_ccw_cw_freq_time, daemon=True).start()
    # threading.Thread(target=motor4_ccw_cw_freq_time, daemon=True).start()
    # threading.Thread(target=motor5_ccw_cw_freq_time, daemon=True).start()
    # threading.Thread(target=motor6_ccw_cw_freq_time, daemon=True).start()

    # 主线程保持运行
    while True:
        time.sleep(1)

