import pygame

class Camera:

    def __init__(self,width,height,map_width,map_height):

        self.x = 0
        self.y = 0

        self.width = width
        self.height = height

        self.map_width = map_width
        self.map_height = map_height

    def update(self,target,zoom):

        self.x = target.rect.centerx * zoom - self.width // 2
        self.y = target.rect.centery * zoom - self.height // 2

        self.x = max(0,min(self.x, self.map_width - self.width))
        self.y = max(0, min(self.y, self.map_height - self.height))