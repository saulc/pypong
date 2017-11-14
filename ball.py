import pygame
from item import Item


class Ball(Item):
    def __init__(self, serv):
        super().__init__(0, 300)
        self.vmax = 10
        self.ymax = 10


    def update(self):
            self.vx = self.vmax
            self.vy = self.ymax
            self.rect.x += self.vx
            self.rect.y += self.vy

       