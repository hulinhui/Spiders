# 引入time包
import os
import time


def adb_input(*parameter):
    params = ' '.join([str(i) for i in parameter])
    # print(f"adb shell input {params}")
    os.system(f"adb shell input {params}")


def adb_operate(*parameter):
    params = ' '.join([str(i) for i in parameter])
    info_data = os.popen(f'adb shell {params}')
    return info_data.read().strip()


def AutoDing():
    product_model = adb_operate('getprop', 'ro.product.model')
    android_version = adb_operate('getprop', 'ro.build.version.release')
    print(f'正在手机型号为:{product_model},安卓系统为:{android_version}上进行打卡')
    # 点亮屏幕
    adb_input('keyevent', 224)
    time.sleep(1)

    # 滑动屏幕
    adb_input('swipe', 220, 1110, 218, 644)
    time.sleep(1)

    # #密码解锁
    adb_input('tap', 720, 1771)
    adb_input('tap', 720, 1500)
    adb_input('tap', 720, 2254)
    adb_input('tap', 341, 2030)
    adb_input('tap', 720, 1500)
    adb_input('tap', 720, 1771)
    time.sleep(2)

    # #找到应用位置并点击进入钉钉
    adb_input('tap', 437, 2483)
    time.sleep(1)

    # 悬浮窗点击应用
    adb_input('tap', 371, 1848)
    time.sleep(5)

    # #钉钉应用内布局
    adb_input('tap', 1269, 546)  # 跳转打卡页面
    time.sleep(6)

    adb_input('tap', 715, 1910)   #打卡
    time.sleep(4)

    # # # 返回首页按钮
    adb_input('keyevent', 3)
    time.sleep(1)

    adb_operate('am', 'force-stop', 'com.alibaba.android.rimet')
    time.sleep(2)

    adb_input('keyevent', 223)

    print('打卡成功！')


# 执行
AutoDing()
