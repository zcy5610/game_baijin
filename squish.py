#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,pygame
from pygame.locals import *
import objects,config
from random import randrange



class State:     #游戏状态超类，能够处理事件以及在指定表面上显示自己
    def handle(self,event):   #只处理退出事件的默认事件处理
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:  #按下backspace键，退出
            sys.exit()

    def first_display(self,screen):
        #首次显示时使用，使用背景色填充屏幕

        # screen.fill(config.background_color)
        background = pygame.image.load(config.beijing_image).convert()
        screen.blit(background,(0,0))
        pygame.display.flip()

    def display(self,screen):
        #后续显示状态时使用，默认行为是什么都不做
        pass

class Level(State): #关卡
    #游戏关卡
    def __init__(self,number=1):
        self.number = number
        self.remaining = config.weights_per_level

        speed = config.drop_speed  #初始速度

        speed += (self.number-1)*config.speed_increase      #每关提升的速度

        # self.weight = objects.Weight(speed)
        # self.banana = objects.Banana()
        # both = self.weight, self.banana #可能含有更多精灵
        # self.sprites = pygame.sprite.RenderUpdates(both)

        self.weight1 = objects.Weight(speed)                    #第一个红
        self.weight2 = objects.Weight(speed+randrange(2,5))     #第二个红，随机速度变化
        self.banana = objects.Banana()
        both = self.weight1, self.weight2,self.banana
        self.sprites = pygame.sprite.RenderUpdates(both)

    def update(self,game):  #更新游戏状态
        self.sprites.update()

        #发生碰撞
        if self.banana.touches(self.weight1) or self.banana.touches(self.weight2):
            game.next_state = GameOver()
        #红下落到底部
        if self.weight1.landed:
            self.weight1.reset()
            self.remaining -= 1

        if self.weight2.landed:
            self.weight2.reset()
            self.remaining -= 1
        #通关关卡
        if self.remaining == 0:
            game.next_state = LevelCleared(self.number)

    def display(self,screen):  #第一个显示（清屏）后显示状态

        # screen.fill(config.background_color)
        background = pygame.image.load(config.beijing_image).convert()
        screen.blit(background, (0, 0))

        #显示当前关卡和通关所需剩余躲避红数量
        level_text = 'Level: %d' % (self.number)
        quantity_text = 'Remaining hong  quantity: %d' % (self.remaining)
        ft_font = pygame.font.SysFont("Arial", 20)  # 设置第一行文字字体
        ft1_surf = ft_font.render(level_text, 1, (0, 0, 0))  # 设置第一行文字颜色
        ft2_surf = ft_font.render(quantity_text, 1, (0, 0, 0))  # 设置第二行文字颜色
        screen.blit(ft1_surf, [20, 30])  # 设置第一行文字显示位置
        screen.blit(ft2_surf, [20, 80])  # 设置第二行文字显示位置
        # pygame.display.flip()

        #更新精灵状态
        updates = self.sprites.draw(screen)
        pygame.display.update(updates)
        pygame.display.flip()

class Paused(State):  #暂停状态，点击鼠标或按任何键盘结束这种状态
    finished = 0   #用户暂停了么
    image = None   #如需显示图像，将这个属性设置成一个文件名
    text = ''      #说明性文本

    def handle(self,event):
        #按键和鼠标单击做出响应，将self.finished设置为Ttue
        State.handle(self,event)
        if event.type in [MOUSEBUTTONDOWN,KEYDOWN]:
            self.finished =1

    def update(self,game): #更新关卡
        if self.finished:
            game.next_state = self.next_state()

    def first_display(self,screen): #首次显示暂停状态时调用
        #背景色填充屏幕来清屏
        screen.fill(config.background_color)

        font = pygame.font.SysFont("Arial",config.font_size)
        #获取文本行
        lines = self.text.strip().splitlines()
        #获取每行文本的高度，并计算文本总高度
        height = len(lines)*font.get_linesize()
        #计算文本的位置（在屏幕上居中）
        center,top = screen.get_rect().center
        top -= height//2

        #如果有图像要显示
        if self.image:
            image = pygame.image.load(self.image).convert()
            r = image.get_rect()
            top += r.height//2             #文本下移图像高度一半的距离
            r.midbottom = center,top -20   #图像放在文本上方20像素处
            screen.blit(image,r)

        antialias =1 #消除文本的锯齿
        black =0,0,0 #使用黑色渲染文本
        #渲染文本
        for line in lines:
            text = font.render(line.strip(),antialias,black)
            r = text.get_rect()
            r.midtop = center,top
            screen.blit(text,r)
            top += font.get_linesize()
        pygame.display.flip() #显示修改

class Info(Paused): #显示一些游戏信息的简单暂停状态，紧跟后面是第一关的状态

    next_state = Level
    image = config.introduction_image
    text = '''
        Press any key to continue
        '''

class StartUP(Paused):   #显示启动图像和欢迎消息的暂停状态，紧跟在它后面的是Info状态
    next_state = Info
    image = config.splash_image
    text ='''
    Welcome to the Game
    '''

class LevelCleared(Paused): #指出用户已过关的暂停状态,紧跟后面的是下一关状态
    def __init__(self,number):
        self.number = number
        self.text = '''
        Level {} cleared
        Click to start next level
        '''.format(self.number)
        self.image = config.nextlevel_image
    def next_state(self):
        return Level(self.number + 1)

class GameOver(Paused):   #游戏结束状态，紧跟后面是第一关的状态
    next_state = Level
    image = config.over_image
    text = '''
    Game OVer!
    Click to Restart, Esc to Quit...
    '''
class Game:     #负责主事件循环的游戏对象
    def  __init__(self,*args):     #获取游戏和图像所在的目录
        path = os.path.abspath(args[0])
        dir = os.path.split(path)[0]

        os.chdir(dir)
        self.state = None   #最初不在任何状态
        self.next_state = StartUP()

    def run(self):
        """
        这个方法设置一些变量。它执行一些重要的初始化任务，并进入主事件循环
        """
        pygame.init() #初始化所有Pygame模块

        flag = 0 #默认在窗口中显示游戏

        # if config.full_screen:
        #     flag = FULLSCREEN #全屏模式

        screen_size = config.screen_size
        screen = pygame.display.set_mode(screen_size,flag)

        pygame.display.set_caption('BaiJin Disco')
        pygame.mouse.set_visible(False)
        pygame.time.Clock().tick(60)  # 设置时钟
    #主事件循环
        while True:
            #（1）如果next_state被修改，就切换到修改后的状态并显示它（首次）
            if self.state != self.next_state:
                self.state = self.next_state
                self.state.first_display(screen)
            #（2）将事件处理工作委托给当前状态：
            for event in pygame.event.get():
                self.state.handle(event)
            #（3）更新当前状态
            self.state.update(self)
            #（4）显示当前状态
            self.state.display(screen)
        pygame.quit()

if __name__ == '__main__':
    game = Game(*sys.argv)
    game.run()















