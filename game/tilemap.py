import pygame
from pytmx.util_pygame import load_pygame
from pathlib import Path

class TileMap:

    def __init__(self,filename):
        self.filename = Path(filename)
        self.tmx_data = load_pygame(str(self.filename))

        self.collisions = {
            "overworld": self.load_collision_layer("collision_overworld"),
            "ruins": self.load_collision_layer("collision_ruins")
        }

        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tileheight

        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight

        self.zoom = 2.5

        self.scaled_tile_width = int(self.tile_width * self.zoom)
        self.scaled_tile_height = int(self.tile_height * self.zoom)

    def load_collision_layer(self,layer_name):

        collision_shapes = []

        layer = self.tmx_data.get_layer_by_name(layer_name)

        for obj in layer:

            points = [(round(p.x), round(p.y)) for p in obj.points]

            bounds = pygame.Rect(
                min(p[0] for p in points),
                min(p[1] for p in points),
                max(p[0] for p in points) - min(p[0] for p in points),
                max(p[1] for p in points) - min(p[1] for p in points)
            )

            local_points = [
                (x - bounds.x, y - bounds.y) for x,y in points
            ]

            polygon_surface = pygame.Surface(bounds.size, pygame.SRCALPHA)
            pygame.draw.polygon(polygon_surface, (0,255,0), local_points)

            collision_mask = pygame.mask.from_surface(polygon_surface)

            collision_shapes.append({
                "rect": bounds,
                "mask": collision_mask
            })

        return collision_shapes

    def draw(self, surface, camera, realm_type):

        for layer in self.tmx_data.visible_layers:

            if layer.name in ("background1", "background2"):
                pass

            elif realm_type == 1 and layer.name not in ("world",):
                continue

            elif realm_type == -1 and layer.name not in ("hell",):
                continue

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



