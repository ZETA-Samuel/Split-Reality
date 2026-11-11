import pygame
import sys

pygame.init()
clock = pygame.time.Clock()

width,height = 800,600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Split Reality')

gravity = 1200
jump_strength = -1000

velocity_y = 0

x,y = 30,30
player = pygame.Rect(x,y,60,60)
player_color = 'white'
screen_color = 'black'

dt = 0

# Surface
surf_rect = pygame.Rect(0,500,800,100)
surf_color = 'green'

on_ground = False

running = True
while running:
    screen.fill(screen_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                player_color = 'black'
                screen_color = 'white'
                surf_color = 'blue'
            elif event.key == pygame.K_w:
                player_color = 'white'
                screen_color = 'black'
                surf_color = 'green'
            if event.key == pygame.K_SPACE:
                if on_ground:
                    velocity_y = jump_strength
                    on_ground = False

    velocity_y += gravity * dt

    if player.colliderect(surf_rect):
        if velocity_y > 0 and player.bottom - velocity_y * dt <= surf_rect.top:
            player.bottom = surf_rect.top
            velocity_y = 0
            on_ground = True

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a]:
        player.x -= 10

    elif keys[pygame.K_d]:
        player.x += 10

    player.y += velocity_y * dt

    pygame.draw.rect(screen,player_color,player)
    pygame.draw.rect(screen,surf_color,surf_rect)
    dt = clock.tick(60) / 1000
    pygame.display.update()

pygame.quit()
sys.exit()