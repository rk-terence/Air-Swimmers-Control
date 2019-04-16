#coding=utf-8
class PidController:
    def __init__(self,kp,ki,kd,ref,componentKi_Max,output_Max):
        '''
        :param kp:
        :param ki:
        :param kd:
        :param ref: 输入的参考值
        :param componentKi_Max: I部分的限幅
        :param output_Max: PID控制器输出的限幅
        '''
        self.kp = kp
        self.ki = 0
        self.kd = kd
        self.ref = ref #参考输入
        self.inte = 0 #积分值
        self.componentKi_Max = componentKi_Max #I部分的输出最大值
        self.output_Max = output_Max #PID总输出的最大值
        self.err_bef = 0 #上一个时刻的err
        self.err_now = 0 #当前时刻的err
        self.componentKp = 0
        self.componentKi = 0
        self.componentKd = 0
        self.output = 0

    def pid_calc(self,err_NOW):
        '''
        :param err_NOW: 现在的误差值
        :return: pid控制器的输出
        '''
        self.err_bef = self.err_now
        self.err_now = err_NOW
        self.inte+=self.err_now #PID的积分值+=现在的e
        self.componentKp = self.kp * self.err_now #计算pid的三个部分的输出
        self.componentKi = self.ki * self.inte
        self.componentKd = self.kd * (self.err_now - self.err_bef)

        if self.componentKi > self.componentKi_Max : #I部分的限幅
            self.componentKi = self.componentKi_Max
        elif self.componentKi < -self.componentKi_Max :
            self.componentKi = -self.componentKi_Max

        self.output = self.componentKp + self.componentKi + self.componentKd

        if self.output > self.output_Max : #PID输出的限幅
            self.output = self.output_Max
        elif self.output < -self.output_Max :
            self.output = -self.output_Max

        return self.output

    def main_control(self, d_h):
        alpha_0 = self.pid_calc(d_h)
        return alpha_0

    def sub_control(self, d_alpha):
        '''
        :param d_alpha:
        :return: 1->应该抬头，肚子往尾巴移动
                 0->应该低头，肚子往头部移动
                 2->肚子不变
        '''
        #d_alpha是alpha_0 - alpha_sensor
        if d_alpha >= 10: #目前的角度小于reference，应该抬头
            return 1
        elif d_alpha <= -10: #应该低头
            return 0
        else:
            return 2

