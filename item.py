'''
Created on Apr 28, 2015

@author: saul
'''
import pygame
     

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__();

        self.image = pygame.Surface([50, 50])
        self.image = pygame.image.load("./res/a1.png").convert_alpha()
        # self.image.fill(pygame.Color(0,200,100))
 
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0
        self.speed = 0
        self.explode = False
        self.eFrame = 0
        self.eFrames = []
       
    def setEframe(self, frames): self.eFrames = frames   
        
    def getRect(self):
        return self.rect
       
    def getCenter(self):
        return (self.rect.x + self.image.get_width()//2, 
                self.rect.y + self.image.get_height()//2)
          
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

    def bang(self): self.explode = True
    
    def update(self):
        
       
        if not self.explode:
            self.rect.x += self.vx
            self.rect.y += self.vy
        else:
            scale = 1   #control the speed of the explosion.
            self.eFrame += 1
            if self.eFrame >= scale * len(self.eFrames): 
                self.eFrame = 0
                self.kill()
            self.image = self.eFrames[self.eFrame// scale]
          
            
        