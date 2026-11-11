import pygame
import sys

pygame.init()

width,height = 800,600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Split Reality')

running = True
while running:
    screen.fill((255,255,255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
sys.exit()