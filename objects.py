#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame,config,os
from random import randrange

#模块包括游戏使用的游戏对象

class SquishSprite(pygame.sprite.Sprite):  #所有sprite超类，设置精灵的外接矩形和移动范围
    def __init__(self,image):
        super().__init__()      #super机制里可以保证公共父类仅被执行一次
        self.image = pygame.image.load(image).convert_alpha()           #使用convert_alpha，去除透明白色部分
        self.rect = self.image.get_rect()
        screen = pygame.display.get_surface()
        shrink = -config.margin * 2
        self.area = screen.get_rect().inflate(shrink,shrink)

class Weight(SquishSprite):     #从天而降的铁锤，红哥，以指定速度下降
    def __init__(self,speed):
        super().__init__(config.weight_image)
        self.speed =speed
        self.reset()

    def reset(self):  #移动到屏幕顶端，随机水平位置
        x = randrange(self.area.left,self.area.right)
        self.rect.midbottom = x,0

    def update(self): #根据速度垂直向下移动距离。通知设置是否到达底部的属性landed
        self.rect.top += self.speed
        self.landed = self.rect.top >= self.area.bottom

class Banana(SquishSprite):         #绝望的香蕉，白金，停留在屏幕底部附近，且水平位置由鼠标当前文职决定
    def __init__(self):
        super().__init__(config.banana_image)
        self.rect.bottom = self.area.bottom    #固定底部？
        #内边距，表示图像中不属于白金的部分
        self.pad_top = config.banana_pad_top
        self.pad_side = config.banana_pad_side

    def update(self):
        self.rect.centerx = pygame.mouse.get_pos()[0]   #香蕉的中心坐标X设置为鼠标当前x坐标
        self.rect = self.rect.clamp(self.area)          #矩形clamp确保香蕉位于允许的移动范围内

    def touches(self,other):
        #碰撞判断，去除顶部及两边的空白区域
        bounds = self.rect.inflate(-self.pad_side,-self.pad_top)  #去除内边距
        bounds.bottom = self.rect.bottom
        return bounds.colliderect(other.rect)




