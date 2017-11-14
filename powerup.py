'''
Created on May 19, 2015

@author: saul

base power up item with animation
'''

from item import Item
import pygame

class PowerUps(Item):
    
    frames = []
    
    def __init__(self, x, y, type):
        super().__init__(x, y)
        self.frame = 0
        if len(PowerUps.frames) == 0: self.setupFrames()
        self.image = PowerUps.frames[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.power = 10
        self.wepons = [1000, 50, 5]
        self.radius = self.image.get_width() -10 // 2
        
    def update(self):
        super().update()
        scale = 3
        self.frame += 1
        if self.frame >= scale * len(PowerUps.frames): self.frame = 0
    
        self.image = PowerUps.frames[self.frame//scale]
        
    def setupFrames(self):
        
        i = pygame.image.load("./res/blue.png").convert_alpha()
        PowerUps.frames.append(i)
        i = pygame.image.load("./res/green.png").convert_alpha()
        PowerUps.frames.append(i)
        i = pygame.image.load("./res/yellow.png").convert_alpha()
        PowerUps.frames.append(i)
        i = pygame.image.load("./res/orange.png").convert_alpha()
        PowerUps.frames.append(i)
        i = pygame.image.load("./res/red.png").convert_alpha()
        PowerUps.frames.append(i)
        i = pygame.image.load("./res/pink.png").convert_alpha()
        PowerUps.frames.append(i)
        i = pygame.image.load("./res/purple.png").convert_alpha()
        PowerUps.frames.append(i)
        
        
        