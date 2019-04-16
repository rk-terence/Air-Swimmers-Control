#coding=utf-8
from arduino import Arduino
import time


class TimeConfig:
    """
    Some parameters of our fish
    """
    def __init__(self):
        self.Tail_left_weak_time = 0.4  # 尾巴向左的强度时间定义
        self.Tail_left_medium_time = 0.8
        self.Tail_left_strong_time = 1.2
        self.Tail_right_weak_time = 0.4  # 尾巴向右的强度时间定义
        self.Tail_right_medium_time = 0.8
        self.Tail_right_strong_time = 1.2
        self.Tummy_front_weak_time = 0.4  # 肚子向前的强度时间定义
        self.Tummy_front_medium_time = 0.8
        self.Tummy_front_strong_time = 1.2
        self.Tummy_back_weak_time = 0.4  # 肚子向后的强度时间定义
        self.Tummy_back_medium_time = 0.8
        self.Tummy_back_strong_time = 1.2


class Fish:
    def __init__(self, com=None):
        """
        :param com: 设备管理器中的com号。
        """
        self.board = Arduino(com)
        self.K1 = 22
        self.K2 = 26
        self.K3 = 30
        self.K4 = 34
        self.K_demo = 38
        self.keys = [self.K1, self.K2, self.K3, self.K4,self.K_demo]
        self.board.output(self.keys)
        for key in self.keys:
            self.board.setLow(key)
        self.delay_time = 0.1
        self.config = TimeConfig()

    def terminate(self):
        for key in self.keys:
            self.board.setLow(key)
        self.board.close()

    def tummy_front_start(self):  # 开启肚子向前摆
        self.board.setHigh(self.K3)

    def tummy_front_end(self):  # 关闭肚子向前摆
        self.board.setLow(self.K3)

    def tummy_back_start(self):  # 开启肚子向后摆
        self.board.setHigh(self.K4)

    def tummy_back_end(self):  # 关闭肚子向后摆
        self.board.setLow(self.K4)

    def tail_left(self, action_time):  # 尾巴向左摆
        self.board.setHigh(self.K1)
        time.sleep(action_time)
        self.board.setLow(self.K1)
        time.sleep(self.delay_time)

    def tail_right(self, action_time):  # 尾巴向右摆
        self.board.setHigh(self.K2)
        time.sleep(action_time)
        self.board.setLow(self.K2)
        time.sleep(self.delay_time)

    def tail_DEMO(self):  # 尾巴取demo一直左右摇摆，因为前进目前暂时不用控制
        self.tail_left(0.45)
        self.tail_right(0.8)


if __name__ == '__main__':
    time_config = TimeConfig()
    fish = Fish(com='COM5')
    for i in range(10):
        fish.tummy_front_start()
        fish.tummy_front_end()

    fish.terminate()
