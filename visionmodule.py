import cv2
import numpy as np
from math import *
import time


class VisionModule:
    def __init__(self):
        self.d_h = 0
        self.d_alpha = 0
        self.alpha = 45
        self.h = 300
        self.h_record = []
        self.alpha_record = []
        pass

    def get_d_h(self):
        return self.d_h

    def get_d_alpha(self):
        return self.d_alpha

    def vision(self):
        # 打开视频捕获设备
        video_capture = cv2.VideoCapture(0)
        kernel = np.ones((7, 7), np.float32) / 49
        dis_low = 20
        dis_high = 100
        # 假设机器人从左往右运动
        t0 = time.time()
        while True:
            # print("In while1")
            alpha = self.alpha
            h = self.h
            angle = []
            height = []
            loop = 1
            count = 0
            while count < loop:  # 取十个图像做一次中值滤波
                # print("In while2")
                if not video_capture.isOpened():
                    print('Unable to load camera.')
                    time.sleep(1)
                    break
                # 读视频帧
                ret, img = video_capture.read()
                # 转为灰度图像
                # img = cv2.medianBlur(img, 3)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度图像
                dst = cv2.filter2D(gray, -1, kernel)
                circles1 = cv2.HoughCircles(dst, cv2.HOUGH_GRADIENT, 1, 50, param1=100, param2=20, minRadius=12,
                                            maxRadius=20)
                # 已知检测圆圈，直至有图像中出现圆圈
                while circles1 is None:
                    # print("In while3")
                    ret, img = video_capture.read()
                    # 转为灰度图像
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度图像
                    dst = cv2.filter2D(gray, -1, kernel)
                    circles1 = cv2.HoughCircles(dst, cv2.HOUGH_GRADIENT, 1, 50, param1=100, param2=20, minRadius=12,
                                                maxRadius=20)
                circles = circles1[0, :, :]  # 提取为二维
                circles = np.int16(np.around(circles))  # 四舍五入,circles[[x1,y1,r1],[x2,y2,r2],...]

                # # 根据圆灰度阈值进行第二次过滤
                # color_circles = []
                # for ele in circles:
                #     p_value = 0
                #     minx = max((ele[0] - ele[2] // 5), 0)
                #     maxx = min((ele[0] + ele[2] // 5), 640)
                #     miny = max((ele[1] - ele[2] // 5), 0)
                #     maxy = min((ele[1] + ele[2] // 5), 480)
                #     for i in range(minx, maxx):
                #         for j in range(miny, maxy):
                #             p_value = p_value + dst[j][i] / ((maxx - minx) * (maxy - miny))
                #     if p_value > 100:
                #         color_circles.append(list(ele))
                # #            print(p_value)
                # color_circles = np.array(color_circles)
                color_circles = np.array(circles)
                # # 根据圆心距离，第一次过滤检测圆
                # temp_circles = []
                # num = color_circles.shape[0]  # 检测到的圆个数
                # for i in range(num):
                #     for j in range(i + 1, num):
                #         dis = sqrt(((color_circles[i][0] - color_circles[j][0]) / 100) ** 2 + (
                #                 (color_circles[i][1] - color_circles[j][1]) / 100) ** 2) * 100
                #         if dis > dis_low and dis < dis_high:
                #             temp_circles.append(list(color_circles[i]))
                #             temp_circles.append(list(color_circles[j]))
                # temp_circles = np.array(temp_circles)
                temp_circles = color_circles

                if temp_circles.shape[0] > 1:
                    retain_circles = np.unique(temp_circles, axis=0)

                    for i in retain_circles[:]:
                        cv2.circle(img, (i[0], i[1]), i[2], color=[0, 0, 0], thickness=2)  # 画圆
                        cv2.circle(img, (i[0], i[1]), 2, color=[0, 255, 0], thickness=2)  # 画圆心
                    for i in range(retain_circles.shape[0]):
                        for j in range(i + 1, retain_circles.shape[0]):
                            dx = retain_circles[i][1] - retain_circles[j][1]
                            dy = retain_circles[i][0] - retain_circles[j][0]
                            temp_angle = atan2(abs(dx), abs(dy)) * 180 / pi
                            temp_height = 0.5 * (retain_circles[i][1] + retain_circles[j][1])
                            if dx * dy / 10000 > 0:
                                temp_angle = -temp_angle
                            angle.append(temp_angle)
                            height.append(temp_height)
                    count = count + 1
            angle = sorted(angle)
            height = sorted(height)
            if len(angle) == 0:
                return_angle = False
                return_height = False
            else:
                return_angle = angle[len(angle) // 2]
                return_height = 480 - height[len(height) // 2]
            self.d_h = h - return_height
            self.d_alpha = alpha - return_angle
            # print('d_h:', self.d_h)
            # print('alpha', alpha)
            # print('d_alpha', self.d_alpha)
            self.alpha_record.append([return_angle, time.time() - t0])
            self.h_record.append([return_height, time.time() - t0])
            np.savetxt('h_record.csv', self.h_record, delimiter=',')
            np.savetxt('alpha_record.csv', self.alpha_record, delimiter=',')
            # cv2.putText(img=img, text='h'+str(return_height), org=(50, 300))
            cv2.imshow('video', img)
            cv2.waitKey(1)


if __name__ == '__main__':
    vision = VisionModule()
    print(vision.get_d_h())
