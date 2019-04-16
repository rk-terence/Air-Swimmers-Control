from fish import Fish
from fish import TimeConfig
from visionmodule import VisionModule
import threading
import time
import numpy as np

from pid_controller import PidController

H = 300  # The control object of h


class GetVision(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        vision.vision()


class Demo(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            fish.tail_DEMO()


if __name__ == "__main__":
    # 主控制器初始化
    kp_main = 0.2
    ki_main = 0.1
    kd_main = 0
    h_ref = 20
    I_main_Max = 3
    Output_main_Max = 90
    controller = PidController(kp_main, ki_main, kd_main, h_ref, I_main_Max, Output_main_Max)

    # Initialize
    fish = Fish(com='COM4')
    time_config = TimeConfig()
    vision = VisionModule()

    d_h = vision.get_d_h()
    alpha = controller.main_control(d_h)

    d_alpha = vision.get_d_alpha()
    cmd = controller.sub_control(d_alpha)
    last_cmd = cmd
    run_flag = True

    # Start the threading:
    thread_get_vision = GetVision()
    thread_get_vision.start()
    # thread_fish_demo = Demo()
    # thread_fish_demo.start()
    control_alpha_signal = []
    control_cmd_signal = []
    t0 = time.time()
    vision.h = H

    while run_flag:
        # fish.tail_DEMO()
        d_h = vision.get_d_h()
        # print('d_h:', d_h)
        vision.alpha = controller.main_control(d_h)
        # print('alpha in main:', vision.alpha)
        d_alpha = vision.get_d_alpha()
        # print('d_alpha:', d_alpha)
        cmd = controller.sub_control(d_alpha)

        if cmd == 0:
            fish.tummy_back_end()
            fish.tummy_front_start()
        elif cmd == 1:
            fish.tummy_front_end()
            fish.tummy_back_start()
        control_alpha_signal.append([vision.alpha, time.time() - t0])
        np.savetxt('control_alpha_signal.csv', control_alpha_signal, delimiter=',')
        control_cmd_signal.append([cmd, time.time() - t0])
        np.savetxt('control_cmd_signal.csv', control_cmd_signal, delimiter=',')
        # time.sleep(0.1)

    fish.terminate()
