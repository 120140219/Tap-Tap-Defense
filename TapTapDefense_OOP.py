import pygame
import random
from player import player
from bombo import BomboSapiens,NormalBombo,GiantBombo
from variabels import mob,screen,rescaledBackground
from function import IScollision
from senjata import Revolver
from skills import Skill3

#initialize the pygame
pygame.init()

#settings
FPS = 60
fpsClock = pygame.time.Clock()

pygame.mouse.set_visible(False)


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
