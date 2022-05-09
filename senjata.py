import pygame
from pygame import mixer
import os
from abc import ABC, abstractmethod
from player import Player
from variabels import font,font_color,screen

class Senjata(ABC):
    def __init__(self, name, mag, dmg, time, start, reload, shoot):
        self.name = name
        self.mag = mag
        self.ammo = self.mag
        self.dmg = dmg
        self.reload_time = time
        self.time = 0
        self.ISshoot = True
        self.ISreload = False
        self.Sstart = start
        self.Sreload = reload
        self.Sshoot = shoot

    @abstractmethod
    def start(self):
        self.Sstart.play()

    @abstractmethod
    def shoot(self):
        if self.ISshoot:
            self.ammo -= 1
            self.Sshoot.play()

    @abstractmethod
    def reload(self):
        self.Sreload.play()
        self.ISreload = True
        self.ISshoot = False

    @abstractmethod
    def update(self):
        ammo = font.render(str(self.ammo) + "/" + str(self.mag), True, font_color)
        screen.blit(ammo, (Player.textX, Player.textY + 225))
        if self.ammo == 0 and not self.ISreload:
            self.reload()
        if self.ISreload:
            self.time += 1
        if self.time == self.reload_time:
            self.ammo = self.mag
            self.ISshoot = True
            self.ISreload = False
            self.time = 0

class Glock(Senjata):
    def __init__(self):
        name = 'G'
        mag = 15
        dmg = 10
        time = 90
        start = mixer.Sound(os.path.join("game_assets", "glock_start.mp3"))
        reload = mixer.Sound(os.path.join("game_assets", "glock_reload.mp3"))
        shoot = mixer.Sound(os.path.join("game_assets", "glock_shoot.mp3"))
        super().__init__(name, mag, dmg, time, start, reload, shoot)

    def start(self):
        super().start()

    def shoot(self):
        super().shoot()

    def reload(self):
        super().reload()

    def update(self):
        super().update()

class Revolver(Senjata):
    def __init__(self):
        name = 'R'
        mag = 6
        dmg = 20
        time = 300
        start = mixer.Sound(os.path.join("game_assets", "revolver_start.mp3"))
        reload = []
        for i in range(7):
            temp = mixer.Sound(os.path.join("game_assets", "revolver_reload" + str(i) + ".mp3"))
            reload.append(temp)
        shoot = mixer.Sound(os.path.join("game_assets", "revolver_shoot.mp3"))
        super().__init__(name, mag, dmg, time, start, reload, shoot)
        self.boost = 0

    def start(self):
        super().start()

    def shoot(self):
        super().shoot()

    def reload(self):
        self.time += (30 * self.boost)
        self.Sreload[self.boost].play()
        self.boost = 0
        self.ISreload = True
        self.ISshoot = False

    def update(self):
        super().update()
        print(self.boost)