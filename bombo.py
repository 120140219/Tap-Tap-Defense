import pygame
from pygame import mixer
import time, os, random, math
from abc import ABC, abstractmethod
from player import Player,player
from function import remove
from variabels import mob,screen

class BomboSapiens(ABC):
    spawn_rate = 60
    add_mob = 0
    mob_pos = [15, 75, 135, 195, 255]
    explodeImage = []
    for i in range(9):
        tempImage = pygame.image.load(os.path.join("game_assets", "explosion0" + str(i) + ".png"))
        tempImage = pygame.transform.scale(tempImage, (80, 80))
        explodeImage.append(tempImage)
    explodeSound = mixer.Sound(os.path.join("game_assets", "explosion.mp3"))
    explodeDuration = 8

    def __init__(self, name, hp, spd, image):
        self.name = name
        self.image = image
        self.hp = hp
        self.__spd = spd
        self.move = self.__spd
        self.ISexplode = False
        self.ISstun = False
        self.time = 0
        self.x = 700
        self.y = random.choice(BomboSapiens.mob_pos)

    @abstractmethod
    def maju(self):
        self.x -= self.move

    @abstractmethod
    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.explode()
            Player.get_kill(player)

    @abstractmethod
    def explode(self):
        self.move = 0
        self.time = 0
        BomboSapiens.explodeSound.play()
        self.ISexplode = True

    @abstractmethod
    def stun(self, time):
        self.time = 0
        self.move = 0
        self.stun_duration = time
        self.ISstun = True

    @abstractmethod
    def update(self,index):
        self.maju()
        screen.blit(self.image, (self.x, self.y))
        if self.x < Player.base and not self.ISexplode:
            self.explode()
            Player.take_damage(player)
        if self.ISexplode:
            self.time += 1
            self.image = BomboSapiens.explodeImage[self.time]
            if self.time == BomboSapiens.explodeDuration:
                remove(mob, index)
                self.time = 0
        if self.ISstun and not self.ISexplode:
            self.time += 1
            if self.time == self.stun_duration:
                self.ISstun = False
                self.move = self.__spd
                self.time = 0

class NormalBombo(BomboSapiens):
    def __init__(self):
        name = "NB"
        image = pygame.image.load(os.path.join("game_assets", "Normal Bombo.png"))
        hp = 10
        spd = 1
        super().__init__(name, hp, spd, image)

    def maju(self):
        super().maju()

    def take_damage(self, dmg):
        super().take_damage(dmg)

    def explode(self):
        super().explode()

    def stun(self, time):
        super().stun(time)

    def update(self,index):
        super().update(index)

class GiantBombo(BomboSapiens):
    def __init__(self):
        name = "GB"
        image = pygame.image.load(os.path.join("game_assets", "Giant Bombo.png"))
        self.angry_sound = mixer.Sound(os.path.join("game_assets", "Giant Bombo Angry.mp3"))
        hp = 30
        spd = 0.5
        super().__init__(name, hp, spd, image)

    def maju(self):
        super().maju()

    def take_damage(self, dmg):
        self.angry_sound.play()
        self.move += 0.5
        super().take_damage(dmg)

    def explode(self):
        self.angry_sound.stop()
        super().explode()

    def stun(self, time):
        super().stun(time)

    def update(self,index):
        super().update(index)