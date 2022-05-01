#!/usr/bin/env/python3
# -- coding=utf-8 --
import pygame

def main():
    # 创建窗体
    screen = pygame.display.set_mode((300,500),0,32)
    # 加载背景
    bg = pygame.image.load("bg.png")

    while True:
        # 设置背景
        screen.blit(bg,(0,0))
        # 更新显示
        pygame.display.update()

        pass

if __name__ == "__main__":
    main()
    pass

