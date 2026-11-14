import pygame
from pytmx.util_pygame import load_pygame
from pathlib import Path

class TileMap:

    def __init__(self,filename):
        self.filename = Path(filename)
        self.tmx_data = load_pygame(str(self.filename))

        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tileheight

        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight

        self.zoom = 2.5

        self.scaled_tile_width = int(self.tile_width * self.zoom)
        self.scaled_tile_height = int(self.tile_height * self.zoom)

    def draw(self, surface, camera):

        for layer in self.tmx_data.visible_layers:

            if hasattr(layer, "tiles"):

                for x, y, image in layer.tiles():

                    world_x = x * self.tile_width
                    world_y = y * self.tile_height

                    screen_x = world_x * self.zoom - camera.x 
                    screen_y = world_y * self.zoom - camera.y

                    if (screen_x + self.scaled_tile_width < 0 or screen_x > surface.get_width() or screen_y + self.scaled_tile_height < 0 or screen_y > surface.get_height()):
                        continue

                    scaled_image = pygame.transform.scale(image,(self.scaled_tile_width, self.scaled_tile_height))

                    surface.blit(scaled_image,(round(screen_x), round(screen_y)))



