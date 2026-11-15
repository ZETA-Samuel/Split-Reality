import pygame
import sys
from player import Player
from tilemap import TileMap
from pathlib import Path
from camera import Camera

pygame.init()
clock = pygame.time.Clock()

width,height = 800,600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Split Reality')

GAME_DIR = Path(__file__).resolve().parent

tilemap = TileMap(GAME_DIR / "map.tmx")

camera = Camera(width,height,tilemap.width * tilemap.zoom,tilemap.height * tilemap.zoom)



player = Player(30,30)
screen_color = 'black'

dt = 0

# Realm Type
realm_type = 1

# Surface
surf_rect = pygame.Rect(0,500,800,100)
surf_color = 'green'

running = True
while running:
    screen.fill(screen_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                realm_type *= -1

            if event.key == pygame.K_SPACE:
                player.jump()

    if realm_type == 1:
        active_walls = tilemap.collisions["overworld"]
    else:
        active_walls = tilemap.collisions["ruins"]

    player.update(dt, active_walls)
    camera.update(player, tilemap.zoom)
    tilemap.draw(screen,camera,realm_type)
    player.draw(screen, camera, tilemap.zoom)
    dt = clock.tick(60) / 1000

    pygame.display.update()

pygame.quit()
sys.exit()