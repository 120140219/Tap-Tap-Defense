import pygame
from pygame import mixer
import time, os, random, math
from abc import ABC, abstractmethod
from player import Player,player
from bombo import BomboSapiens,NormalBombo,GiantBombo
from variabels import mob,font,font_color,screen,rescaledBackground
from function import IScollision

#initialize the pygame
pygame.init()

#settings
FPS = 60
fpsClock = pygame.time.Clock()

pygame.mouse.set_visible(False)

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


#initiation
fast = False
weapon = Revolver()
weapon.start()
skill = Skill3()


#game loop
while player.play:
    screen.blit(rescaledBackground, (0, 0))
    player.update()
    weapon.update()
    for i in mob:
        index = i
        i.update(index)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            player.play = False
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_r]:
                weapon.reload()
            if pygame.key.get_pressed()[pygame.K_p]:
                if not fast:
                    fast = True
                    FPS = 480
                elif fast:
                    fast = False
                    FPS = 60
            if pygame.key.get_pressed()[pygame.K_o]:
                player.mana += 300
        if event.type == pygame.KEYUP:
            if pygame.key.get_pressed()[pygame.K_p]:
                FPS = 60
        if event.type == pygame.MOUSEBUTTONDOWN:
            key = pygame.mouse.get_pressed()
            if key[0]:
                weapon.shoot()
                for i in mob:
                    if IScollision(i.x, i.y, player.x, player.y, weapon.ammo):
                        i.take_damage(weapon.dmg)
                        if weapon.name == 'R':
                            weapon.boost += 1
            if key[2]:
                skill.active(mob, player.mana)

    BomboSapiens.add_mob += 1
    if BomboSapiens.add_mob == BomboSapiens.spawn_rate:
        x = random.randint(0, 1)
        if x == 0:
            mob.append(NormalBombo())
        elif x == 1:
            mob.append(GiantBombo())
        BomboSapiens.add_mob = 0

    pygame.display.update()
    fpsClock.tick(FPS)
