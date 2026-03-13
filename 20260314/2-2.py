# 2-2.py例
import time

def timer(count_time):
    for i in range(1, count_time + 1):
        print(i)
        time.sleep(1)

#test
timer(10)