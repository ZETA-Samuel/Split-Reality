# /// script
# dependencies = [
#     "pygame-ce",
#     "pytmx",
# ]
# ///
import pygame
import asyncio
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

portal_sheet = pygame.image.load(GAME_DIR/"assets"/"portal.png").convert_alpha()

portal_frames = [
    portal_sheet.subsurface((0,0,60,80)),
    portal_sheet.subsurface((60,0,60,80))
]

portal_frames = [
    pygame.transform.scale_by(frame,2)for frame in portal_frames
]

# Map-space portal rectangles; each spawn rests on solid ground in both realms.
CHECKPOINTS = [
    {"portal": pygame.Rect(12, 105, 48, 64), "spawn": (15, 59)},
    {"portal": pygame.Rect(1350, 121, 48, 64), "spawn": (1320, 75)},
]
current_checkpoint = CHECKPOINTS[0]["spawn"]

portal_frame = 0
portal_timer = 0
portal_animation_speed = 0.5

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
async def main():
    global dt,running,game_state,player,realm_type,teleport_index,portal_timer,portal_frame,current_checkpoint
    while running:
        screen.fill(screen_color)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:

                if game_state == "menu":
                    if event.key == pygame.K_RETURN:
                        player = Player(*START_POSITION)
                        current_checkpoint = CHECKPOINTS[0]["spawn"]
                        game_state = "playing"

                elif game_state == "ending" or game_state == "play_again":
                    if event.key == pygame.K_r:
                        player = Player(*START_POSITION)
                        current_checkpoint = CHECKPOINTS[0]["spawn"]
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

            portal_timer += dt

            if portal_timer >= portal_animation_speed:
                portal_timer = 0
                portal_frame = (portal_frame + 1) % 2

            player.update(dt, active_walls)
            if player.rect.top >= tilemap.height:
                player = Player(*current_checkpoint)

            for checkpoint in CHECKPOINTS:
                if player.rect.colliderect(checkpoint["portal"]):
                    current_checkpoint = checkpoint["spawn"]

            camera.update(player, tilemap.zoom)
            if realm_type == 1:
                background_overworld.draw(screen,camera)
            else:
                background_ruins.draw(screen,camera)
            tilemap.draw(screen,camera,realm_type)

            for checkpoint in CHECKPOINTS:
                portal = checkpoint["portal"]
                screen.blit(
                    portal_frames[portal_frame],
                    (portal.x * tilemap.zoom - camera.x, portal.y * tilemap.zoom - camera.y),
                )
            player.draw(screen, camera, tilemap.zoom)

            if player.rect.colliderect(END_RECT):
                game_state = "ending"


        if game_state == "ending":
            draw_ending()

        if game_state == "play_again":
            play_again()


        dt = clock.tick(60) / 1000

        pygame.display.update()

        await asyncio.sleep(0)

asyncio.run(main())