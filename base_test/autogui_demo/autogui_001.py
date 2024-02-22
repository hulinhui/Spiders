# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         autogui_001
# Description:  
# Author:       hulinhui779
# Date:      2024/2/21 16:38
# -------------------------------------------------------------------------------
import pyautogui

# 查看屏幕尺寸
print(pyautogui.size())

# 查看当前鼠标所在位置
print(pyautogui.position())

# 移动鼠标
x, y = (320, 100)
pyautogui.moveTo(x, y, duration=1)
print(pyautogui.position())

# 使用moveRel函数相对路径移动，将当前位置作为坐标轴原点。
positon = (409, 300)
pyautogui.moveRel(*positon, duration=1)
print(pyautogui.position())

# 鼠标点击
pyautogui.click(1000, 460, clicks=2, interval=1, button='left')
