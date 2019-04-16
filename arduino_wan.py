#coding=utf-8
from arduino import Arduino
import time
#初始化

b = Arduino('COM5') #通过COM5来控制Arduino
Tail_left_weak_time = 0.4 #尾巴向左的强度时间定义
Tail_left_medium_time = 0.8
Tail_left_strong_time = 1.2
Tail_right_weak_time = 0.4 #尾巴向右的强度时间定义
Tail_right_medium_time = 0.8
Tail_right_strong_time = 1.2
Tummy_front_weak_time = 0.4 #肚子向前的强度时间定义
Tummy_front_medium_time = 0.8
Tummy_front_strong_time = 1.2
Tummy_back_weak_time = 0.4 #肚子向后的强度时间定义
Tummy_back_medium_time = 0.8
Tummy_back_strong_time = 1.2
K1=22 #输出管脚定义
K2=26
K3=30
K4=34
DELAY_TIME = 0.1 #间隔时间delay
b.output([K1,K2,K3,K4]) #输出管脚设置

def Tail_Left(Time): #尾巴向左摆
    b.setHigh(K1)
    time.sleep(Time)
    b.setLow(K1)
    time.sleep(DELAY_TIME)

def Tail_Right(Time): #尾巴向右摆
    b.setHigh(K2)
    time.sleep(Time)
    b.setLow(K2)
    time.sleep(DELAY_TIME)

def Tummy_Front(Time): #肚子向前摆
    b.setHigh(K3)
    time.sleep(Time)
    b.setLow(K3)
    time.sleep(DELAY_TIME)

def Tummy_Back(Time): #肚子向后摆
    b.setHigh(K4)
    time.sleep(Time)
    b.setLow(K4)
    time.sleep(DELAY_TIME)

def Tail_Medium(K): #肚子向后摆
    if K==K1 :
        b.setHigh(K2)
        time.sleep(0.2)
        b.setLow(K2)
        time.sleep(DELAY_TIME)
    elif K==K2:
        b.setHigh(K1)
        time.sleep(0.2)
        b.setLow(K1)
        time.sleep(DELAY_TIME)

if __name__ == '__main__':
    while True:
        Tail_Left(Tail_left_medium_time)
        Tail_Right(Tail_right_medium_time)
    b.close()

