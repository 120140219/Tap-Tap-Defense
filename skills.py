import pygame
from pygame import mixer
import os
from player import Player,player


class Skill1:
    def __init__(self):
        self.cost = 100
        self.knockback = 100
        self.effect = 15
        self.sound = mixer.Sound(os.path.join("game_assets", "skill1.mp3"))

    def active(self, list, mana):
        if mana >= self.cost:
            Player.use_skill(player, self.cost)
            self.sound.play()
            for i in list:
                if i.name == "NB":
                    i.x += self.knockback
                elif i.name == 'GB':
                    i.stun(self.effect)

class Skill2:
    def __init__(self):
        self.cost = 150
        self.dmg = 5
        self.effect = 30
        self.sound = mixer.Sound(os.path.join("game_assets", "skill1.mp3"))

    def active(self, list, mana):
        if mana >= self.cost:
            player.use_skill(self.cost)
            self.sound.play()
            for i in list:
                i.take_damage(self.dmg)
                i.stun(self.effect)

class Skill3:
    def __init__(self):
        self.cost = 300
        self.dmg = 999
        self.sound = mixer.Sound(os.path.join("game_assets", "skill1.mp3"))

    def active(self, list, mana):
        if mana >= self.cost:
            player.use_skill(self.cost)
            self.sound.play()
            for i in list:
                i.take_damage(self.dmg)