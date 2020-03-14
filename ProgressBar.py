# -*- coding: utf-8 -*-
#  @ Date   : 2019/5/20 13:14
#  @ Author : RichardLauCx
#  @ file   : Richard.py
#  @ IDE    : PyCharm

import sys
import time


# 进度条
def progress_bar_1():
    for i in range(1, 101):
        print("\r", end="")
        print("StateOfTranslationTemplate: {}%: ".format(i), "▋" * (i // 2), end="")
        sys.stdout.flush()
        time.sleep(0.5)


def progress_bar_2(total):
   """
   进度条效果
   """
   # 获取标准输出
   _output = sys.stdout
   # 通过参数决定你的进度条总量是多少
   for count in range(0, total + 1):
       # 这里的second只是作为工作量的一种代替
       # 这里应该是有你的主程序,main()
       _second = 0.1
       # 模拟业务的消耗时间
       time.sleep(_second)
       # 输出进度条
       _output.write(f'\rcomplete percent:{count:.0f}%')
   # 将标准输出一次性刷新
   _output.flush()
# progress_bar(100)


if __name__ == '__main__':
    progress_bar_1()