import pygame
import sys

pygame.init()
clock = pygame.time.Clock()

width,height = 800,600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Split Reality')

gravity = 1200
jump_strength = -900
move_speed = 350

velocity_x = 0
velocity_y = 0

x,y = 30,30
player = pygame.Rect(x,y,60,60)
player_color = 'white'
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

on_ground = False

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
                if on_ground:
                    velocity_y = jump_strength
                    on_ground = False

    # changing realm
    if realm_type == -1:
        player_color = 'black'
        screen_color = 'white'
        surf_color = 'blue'
        active_walls = plain_walls
        
    else:
        player_color = 'white'
        screen_color = 'black'
        surf_color = 'green'
        active_walls = ruin_walls


    all_walls = active_walls + [surf_rect]

    velocity_y += gravity * dt

    if player.colliderect(surf_rect):
        if velocity_y > 0 and player.bottom + velocity_y * dt >= surf_rect.top:
            player.bottom = surf_rect.top
            velocity_y = 0
            on_ground = True

    keys = pygame.key.get_pressed()

    velocity_x = 0
    
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        velocity_x = -move_speed 

    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        velocity_x = move_speed

    player.x += round(velocity_x * dt)

    for wall in all_walls:

        if player.colliderect(wall):

            if velocity_x > 0:
                player.right = wall.left

            elif velocity_x < 0:
                player.left = wall.right

    # screen boundaries
    if player.left < 0:
        player.left = 0

    if player.right > width:
        player.right = width

    # Y-axis collision
    velocity_y += gravity * dt

    on_ground = False

    # move vertically
    player.y += round(velocity_y * dt)

    for wall in all_walls:
        if player.colliderect(wall):

            if velocity_y > 0:
                player.bottom = wall.top
                on_ground = True

            elif velocity_y < 0:
                player.top = wall.bottom

            velocity_y = 0

    if player.top < 0:
        player.y = 0
        velocity_y = 0

    if player.bottom > height:
        player.bottom = height
        velocity_y = 0
        on_ground = True
        
    for wall in all_walls:
        pygame.draw.rect(screen,surf_color,wall)
    
    pygame.draw.rect(screen,player_color,player)
    pygame.draw.rect(screen,surf_color,surf_rect)
    dt = clock.tick(60) / 1000
    pygame.display.update()

pygame.quit()
sys.exit()