import pygame
import os
pygame.init()

width = 700
height = 300
screen = pygame.display.set_mode((width, height))
bgImage = pygame.image.load(os.path.join("game_assets", "background.jpg"))
rescaledBackground = pygame.transform.scale(bgImage, (width, height))

mob = []
font_size = 20
font = pygame.font.Font("freesansbold.ttf", font_size)
font_color = (255, 255, 255)