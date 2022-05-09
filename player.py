import pygame
from pygame import mixer
import time, os
from variabels import font,font_color

#initialize the pygame
pygame.init()

#settings
FPS = 60
fpsClock = pygame.time.Clock()

width = 700
height = 300
screen = pygame.display.set_mode((width, height))
bgImage = pygame.image.load(os.path.join("game_assets", "background.jpg"))
rescaledBackground = pygame.transform.scale(bgImage, (width, height))

mixer.music.load(os.path.join("game_assets", "music.mp3"))
gvSound = mixer.Sound(os.path.join("game_assets", "gameover.mp3"))
mixer.music.play(-1)

class Player():
    textX = 10
    textY = 10
    base = 280

    def __init__(self):
        self.play = True
        self.score = 0
        self.damage = 0
        self.mana = 0

    def get_kill(self):
        self.score += 1
        if self.mana != 300:
            self.mana += 10

    def take_damage(self):
        self.damage += 1

    def game_over(self):
        mixer.music.stop()
        gvSound.play()
        self.play = False
        time.sleep(3)

    def use_skill(self, cost):
        self.mana -= cost

    def update(self):
        self.x, self.y = pygame.mouse.get_pos()
        crosshair = pygame.image.load(os.path.join("game_assets", "crosshair.png")).convert_alpha()
        score = font.render("Score : " + str(self.score), True, font_color)
        lives = font.render("Lives : " + str(5 - self.damage), True, font_color)
        mana = font.render(str(self.mana) + "/300", True, font_color)
        screen.blit(crosshair, (self.x, self.y))
        screen.blit(score, (Player.textX, Player.textY))
        screen.blit(lives, (Player.textX, Player.textY + 35))
        screen.blit(mana, (Player.textX, Player.textY + 260))
        if self.damage >= 5:
            self.game_over()

player = Player()