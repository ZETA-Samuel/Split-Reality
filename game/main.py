import pygame
import sys

pygame.init()
clock = pygame.time.Clock()

width,height = 800,600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Split Reality')

x,y = 30,30
player = pygame.Rect(x,y,60,60)
player_color = 'white'
screen_color = 'black'

dt = 0

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
                player_color = 'black'
                screen_color = 'white'
                surf_color = 'blue'
            elif event.key == pygame.K_w:
                player_color = 'white'
                screen_color = 'black'
                surf_color = 'green'

    if player.bottom >= surf_rect.y and player.colliderect(surf_rect):
        player.bottom = surf_rect.y

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a]:
        player.x -= 10

    elif keys[pygame.K_d]:
        player.x += 10

    player.y += 300 * dt

    pygame.draw.rect(screen,player_color,player)
    pygame.draw.rect(screen,surf_color,surf_rect)
    dt = clock.tick(60) / 1000
    pygame.display.update()

pygame.quit()
sys.exit()