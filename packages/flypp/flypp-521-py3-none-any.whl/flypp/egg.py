# _*_ coding:utf-8 _*_
import pygame   
import sys
import pyautogui
import os

def run_egg():
    pygame.init()
    pygame.display.set_caption('Love Fly PP')

    screen_size = pyautogui.size()
    size = width, height = screen_size # 获取窗口分辨率
    screen = pygame.display.set_mode(size)  # 显示窗口
    color = (0,0,0)                         # 设置颜色

    pig = pygame.image.load(os.path.join(os.path.dirname(__file__), "flypp.gif"))
    # pig = pygame.movie.Movie('flypp.mov')

    pigrect = pig.get_rect()
    speed = [3, 3] 
    clock = pygame.time.Clock() 

    while True:
        clock.tick(60) #每秒执行60次
        for event in pygame.event.get():    #遍历所有事件
            if event.type == pygame.QUIT:   #如果点击关闭窗口，则退出
                sys.exit()

        pigrect = pigrect.move(speed) #移动   
        #碰到左右边缘
        if pigrect.left < 0 or pigrect.right > width:
            pig = pygame.transform.flip(pig, True, False)
            speed[0] = -speed[0]
        #碰到上下边缘
        if pigrect.top < 0 or pigrect.bottom > height:
            pig = pygame.transform.flip(pig, False, True)
            speed[1] = -speed[1]
        screen.fill(color)  #填充颜色
        screen.blit(pig,pigrect)  #显示在窗口上
        pygame.display.flip() #更新全部显示
    pygame.quit() #退出Pygame