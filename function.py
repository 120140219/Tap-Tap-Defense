import math

def IScollision(mobx, moby, curx, cury, ammo):
    distance = math.sqrt((math.pow(mobx - curx, 2)) + (math.pow(moby - cury, 2)))
    if distance < 15 and ammo > 0:
        return True
    else:
        return False

def remove(list, i):
    list.remove(i)
    return list