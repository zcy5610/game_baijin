#!/usr/bin/env python
# -*- coding: utf-8 -*-

#游戏的配置文件

#游戏中使用的图像

banana_image ='image/baijin.bmp'                #底部操作小人图片，白金
weight_image = 'image/hong.png'                 #下落小人图片，红
splash_image = 'image/begin.jpg'                #进入游戏图片
beijing_image = 'image/beijing.jpg'             #游戏背景图片
introduction_image ='image/introduction.jpg'    #游戏说明图像
nextlevel_image = 'image/nextlevel.png'         #进入下一关卡显示图片
over_image = 'image/game_over.jpg'              #游戏结束图片

#游戏的总体外观
screen_size = 800,600                           #屏幕大小
background_color = 255,255,255                  #填充背景颜色，白色
margin = 20                                     #限制移动范围
full_screen = 1                                 #全屏
notfull_screen = 0                              #非全屏
font_size = 48                                  #字体大小

#设置游戏的行为
drop_speed = 20                                 #红初始下落速度
banana_speed = 5                                #移动小人的速度
speed_increase = 5                              #关卡的加速
weights_per_level =16                           #每关要躲的红各商户
banana_pad_top = 10
banana_pad_side =20
