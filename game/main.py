import pygame
import sys
from player import Player

pygame.init()
clock = pygame.time.Clock()

width,height = 800,600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Split Reality')

player = Player(30,30)
screen_color = 'black'

dt = 0

# Realm Type
realm_type = 1

# Surface
surf_rect = pygame.Rect(0,500,800,100)
surf_color = 'green'

# surface for plain world
plain_walls = [
    pygame.Rect(10,10,300,25),
    pygame.Rect(50,50,300,25),
    pygame.Rect(100,100,300,25),
    pygame.Rect(200,200,300,25)
]
# surface for ruin world
ruin_walls = [
    pygame.Rect(400,400,35,25),
    pygame.Rect(600,300,90,45),
    pygame.Rect(500,25,26,67),
    pygame.Rect(36,76,89,98)
]

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


    # changing realm
    if realm_type == -1:
        player_color = 'black'
        screen_color = 'blue'
        surf_color = 'pink'
        active_walls = plain_walls
        
    else:
        player_color = 'white'
        screen_color = 'black'
        surf_color = 'green'
        active_walls = ruin_walls


    all_walls = active_walls + [surf_rect]

    for wall in all_walls:
        pygame.draw.rect(screen,surf_color,wall)
        
    player.update(dt,all_walls)
    player.draw(screen)
    dt = clock.tick(60) / 1000
    
    pygame.display.update()

pygame.quit()
sys.exit()