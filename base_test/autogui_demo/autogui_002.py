# -*- coding: utf-8 -*-
# !/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:         autogui_002
# Description:  
# Author:       hulinhui779
# Date:      2024/2/21 16:39
# -------------------------------------------------------------------------------
import pyautogui


def click_operate(position_x, position_y):
    num_of_clicks = 1
    secs_between_clicks = 1
    pyautogui.click(position_x, position_y, clicks=num_of_clicks, interval=secs_between_clicks, button='left')


# 点击微信页面的公众号，显示公众号内容
wx_position_x_y = (860, 473)
click_operate(*wx_position_x_y)

# 点击第一个公众号图标
gz_positions_x_y = (1090, 305)
click_operate(*gz_positions_x_y)

text_localtion = pyautogui.locateOnScreen(image='1.png', confidence=0.7)
click_operate(text_localtion.left + 25, text_localtion.top + 23)

# text_localtion = pyautogui.locateOnScreen(image='3.png', confidence=0.7)
# click_operate(text_localtion.left + 25, text_localtion.top + 23)
#
# xx_positions_x_y = (1221, 214)
# click_operate(xx_positions_x_y)

if __name__ == '__main__':
    pass
