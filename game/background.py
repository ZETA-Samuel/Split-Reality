import pygame
from pathlib import Path

class Background:
    def __init__(self,image_path,zoom):
        self.image = pygame.image.load(str(image_path)).convert()

        self.zoom = zoom

        self.image = pygame.transform.scale(self.image,(int(self.image.get_width() * zoom), int(self.image.get_height() * zoom)))

    def draw(self,surface,camera):
        x = -camera.x 
        y = -camera.y

        surface.blit(self.image, (round(x), round(y)))

        