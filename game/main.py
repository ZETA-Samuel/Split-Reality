import pygame
import sys
from player import Player
from tilemap import TileMap
from pathlib import Path
from camera import Camera
from background import Background

pygame.init()
clock = pygame.time.Clock()

START_POSITION = (30,30)
END_RECT = pygame.Rect(1550,130,64,64)

game_state = "menu"
title_font = pygame.font.SysFont("arial",64,bold=True)
menu_font = pygame.font.SysFont("arial", 30)



width,height = 800,600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Split Reality')

GAME_DIR = Path(__file__).resolve().parent

tilemap = TileMap(GAME_DIR / "map.tmx")

camera = Camera(width,height,tilemap.width * tilemap.zoom,tilemap.height * tilemap.zoom)

background_overworld = Background(GAME_DIR/"assets"/"background_overworld.png", zoom=0.48)

background_ruins = Background(GAME_DIR/"assets"/"background_ruins.png",zoom=0.48)

player = Player(30,30)
screen_color = 'black'

dt = 0

# Realm Type
realm_type = 1
teleport_index = 0

teleport_animations = [
    "teleport","teleport_2","teleport_3"
]

# Surface
surf_rect = pygame.Rect(0,500,800,100)
surf_color = 'green'

def draw_menu():
    screen.fill((15,18,30))

    title = title_font.render("SPLIT REALITY", True, (255,255,255))
    start = menu_font.render("Press ENTER to Start", True, (200,200,200))
    controls = menu_font.render("A / D - Move | SPACE - Jump | Q - Switch Reality", True, (150,150,150))

    screen.blit(title,title.get_rect(center=(400,220)))
    screen.blit(start, start.get_rect(center=(400,350)))
    screen.blit(controls, controls.get_rect(center=(400,430)))

def draw_ending():
    screen.fill((15,18,30))

    title = title_font.render("MORE COMING SOON", True, (255,255,255))
    subtitle = menu_font.render("Thank you for playing!", True,(180,180,180))
    clue = menu_font.render("Press 'R' to play again", True, (130,130,130))

    screen.blit(title,title.get_rect(center=(400,220)))
    screen.blit(subtitle,subtitle.get_rect(center=(400,350)))
    screen.blit(clue,clue.get_rect(center=(400,430)))

def play_again():
    screen.fill((15,18,30))

    title = title_font.render("GAME OVER",True,(255,255,255))
    subtitle = menu_font.render("Press 'R' to play again", True,(255,255,255))

    screen.blit(title, title.get_rect(center=(400,220)))
    screen.blit(subtitle, subtitle.get_rect(center=(400,350)))

running = True
while running:
    screen.fill(screen_color)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if game_state == "menu":
                if event.key == pygame.K_RETURN:
                    player = Player(*START_POSITION)
                    game_state = "playing"

            elif game_state == "ending" or game_state == "play_again":
                if event.key == pygame.K_r:
                    player = Player(*START_POSITION)
                    game_state = "playing"

            if game_state == "playing":
                if event.key == pygame.K_q:
                    realm_type *= -1
                    player.play_animation(teleport_animations[teleport_index])

                    teleport_index = (teleport_index + 1) % len(teleport_animations)
    
                if event.key == pygame.K_SPACE:
                    player.jump()

    if realm_type == 1:
        active_walls = tilemap.collisions["overworld"]
    else:
        active_walls = tilemap.collisions["ruins"]

    if game_state == "menu":
        draw_menu()

    if game_state == "playing":

        player.update(dt, active_walls)
        camera.update(player, tilemap.zoom)
        if realm_type == 1:
            background_overworld.draw(screen,camera)
        else:
            background_ruins.draw(screen,camera)
        tilemap.draw(screen,camera,realm_type)
        player.draw(screen, camera, tilemap.zoom)

        end_screen_rect = pygame.Rect(
            round(END_RECT.x * tilemap.zoom - camera.x),
            round(END_RECT.y * tilemap.zoom - camera.y),
            round(END_RECT.width * tilemap.zoom),
            round(END_RECT.height * tilemap.zoom)
        )

        pygame.draw.rect(screen, "red", end_screen_rect ,2)
        if player.rect.y >= 600:
            game_state = "play_again"

        if player.rect.colliderect(END_RECT):
            game_state = "ending"


    if game_state == "ending":
        draw_ending()

    if game_state == "play_again":
        play_again()


    dt = clock.tick(60) / 1000

    pygame.display.update()

pygame.quit()
sys.exit()