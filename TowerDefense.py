from cmu_graphics import *
from time import sleep
import math

app.background = rgb(255, 245, 245)
grid = Group(
    Line(200, 400, 200, 0, dashes=(0.5, 19.5), lineWidth=400),
    Line(400, 200, 0, 200, dashes=(0.5, 19.5), lineWidth=400),
    Line(200, 0, 200, 400, dashes=(0.5, 19.5), lineWidth=400),
    Line(0, 200, 400, 200, dashes=(0.5, 19.5), lineWidth=400)
)
danger = Group()
tiles = Group(Rect(180, 180, 40, 40, fill=gradient(rgb(255, 200, 250), rgb(255, 150, 200)), border=rgb(255, 210, 255)))
ores = Group()
stats = Group(Rect(120, 130, 120, 50, fill=rgb(240, 240, 255), opacity=75),
              Label('', 200, 150, font='monospace', bold=True, size=10),
              Label('', 200, 170, font='monospace', bold=True, size=10))
corruption = Group()
corrupted = Group()
ghost = Rect(400, 400, 20, 20, visible=False, opacity=75)
app.mx = 200
app.my = 200
app.maxGold = 500
app.gold = 200
app.rf = 1
app.core = 1
ghost.gold = 0
ghost.rf = 0
corruption.actions = 0

# spawns gold
for i in range(10):
    x = randrange(0, 401)
    y = randrange(0, 401)
    while distance(x, 200, 200, 200) < 50:
        x = randrange(0, 401)
    while distance(200, y, 200, 200) < 50:
        y = randrange(0, 401)
    while x % 20 != 0:
        x -= 1
    while y % 20 != 0:
        y -= 1
    if ores.hitTest(x + 10, y + 10) == None:
        ores.add(Rect(x, y, 20, 20, fill='gold', border=rgb(255, 245, 200)))


# spawns corruption
def spawnCorruption(amount):
    for i in range(amount):
        spawned = False
        while spawned == False:
            x = randrange(0, 401)
            y = randrange(0, 401)
            while distance(x, 200, 200, 200) < 50:
                x = randrange(0, 401)
            while distance(200, y, 200, 200) < 50:
                y = randrange(0, 401)
            while x % 20 != 0:
                x -= 1
            while y % 20 != 0:
                y -= 1
            if corruption.hitTest(x + 10, y + 10) == None and corrupted.hitTest(x + 10,
                                                                                y + 10) == None and ores.hitTest(x + 10,
                                                                                                                 y + 10) == None and tiles.hitTest(
                    x + 10, y + 10) == None:
                corruption.add(Rect(x, y, 20, 20, fill=rgb(220, 75, 25), border=rgb(175, 50, 20)))
                spawned = True


def removeAura(xo, yo, i):
    danger.remove(tiles.hitTest(i.centerX + xo, i.centerY + yo).bind)
    if tiles.hitTest(i.centerX + xo, i.centerY + yo).fill == gradient(rgb(255, 180, 200), rgb(150, 150, 255)):
        app.rf += 1
    else:
        app.rf += 3
    tiles.remove(tiles.hitTest(i.centerX + xo, i.centerY + yo))
    corrupted.add(Rect(i.left, i.top, 20, 20, fill=rgb(200, 100, 100), border=rgb(240, 100, 120)))
    i.centerX += xo
    i.centerY += yo


def defortify(xo, yo, i, level):
    if level == 1:
        tiles.hitTest(i.centerX + xo, i.centerY + yo).fill = rgb(230, 150, 255)
    else:
        tiles.hitTest(i.centerX + xo, i.centerY + yo).fill = rgb(255, 200, 200)
        tiles.hitTest(i.centerX + xo, i.centerY + yo).border = None


def removeMine(xo, yo, i, level):
    app.rf -= level
    tiles.remove(tiles.hitTest(i.centerX + xo, i.centerY + yo))
    corrupted.add(Rect(i.left, i.top, 20, 20, fill=rgb(200, 100, 100), border=rgb(240, 100, 120)))
    i.centerX += xo
    i.centerY += yo


def removeCore():
    Rect(180, 180, 40, 40, fill=rgb(230, 215, 200), border=rgb(230 * 0.9, 215 * 0.9, 200 * 0.9))
    Rect(0, 0, 400, 400, fill='red', opacity=20)
    sleep(0)
    app.stop()


spawnCorruption(3)


# abbreviates long numbers (ex. 10000 -> 10k)
def abrv(var, prefix='', suffix=''):
    if var > 100000000000000000000:
        final = var
    elif len(str(math.floor(var))) in range(5, 7):
        final = prefix + str(math.floor((var / 1000) * 10) / 10) + 'k' + suffix
    elif len(str(math.floor(var))) in range(7, 10):
        final = prefix + str(math.floor((var / 1000000) * 10) / 10) + 'm' + suffix
    elif len(str(math.floor(var))) in range(10, 13):
        final = prefix + str(math.floor((var / 1000000000) * 10) / 10) + 'b' + suffix
    elif len(str(math.floor(var))) in range(13, 16):
        final = prefix + str(math.floor((var / 1000000000000) * 10) / 10) + 't' + suffix
    elif len(str(math.floor(var))) in range(16, 19):
        final = prefix + str(math.floor((var / 1000000000000000) * 10) / 10) + 'q' + suffix
    elif len(str(math.floor(var))) in range(19, 22):
        final = prefix + str(math.floor((var / 1000000000000000000) * 10) / 10) + 'Q' + suffix
    else:
        final = prefix + str(var) + suffix
    if '.0' in str(final):
        final = final.replace('.0', '')
    return final


# draw tile func
def draw(x, y):
    if app.gold >= 10:
        while x % 20 != 0:
            x -= 1
        while y % 20 != 0:
            y -= 1
        if tiles.hitTest(x + 10, y + 10) == None and ores.hitTest(x + 10, y + 10) == None and corruption.hitTest(x + 10,
                                                                                                                 y + 10) == None and corrupted.hitTest(
                x + 10, y + 10) == None:
            if tiles.hitTest(x + 10, y - 10) != None or tiles.hitTest(x - 10, y + 10) != None or tiles.hitTest(x + 30,
                                                                                                               y + 10) != None or tiles.hitTest(
                    x + 10, y + 30) != None:
                tiles.add(Rect(x, y, 20, 20, fill=rgb(255, 200, 200)))
                i = tiles.children[len(tiles) - 1]
                if ores.hitTest(i.left + 10, i.top - 10) != None or ores.hitTest(i.left - 10,
                                                                                 i.top + 10) != None or ores.hitTest(
                        i.left + 30, i.top + 10) != None or ores.hitTest(i.left + 10, i.top + 30) != None:
                    i.fill = rgb(255, 150, 180)
                    i.border = rgb(255 * 0.9, 150 * 0.9, 180 * 0.9)
                    app.rf += 1
                app.gold -= 10


def onKeyPress(key):
    if key == '1' and ghost.fill != gradient(rgb(255, 180, 200), rgb(150, 150, 255)):
        ghost.visible = True
        ghost.fill = gradient(rgb(255, 180, 200), rgb(150, 150, 255))
        ghost.border = rgb(255, 180, 180)
        ghost.rf = -1
        ghost.gold = 50
    elif key == '2' and app.core >= 2 and ghost.fill != rgb(225, 225, 255):
        ghost.visible = True
        ghost.fill = rgb(225, 225, 255)
        ghost.border = rgb(230, 190, 90)
        ghost.rf = -1
        ghost.gold = 100
    elif key == '3' and app.core >= 3 and ghost.fill != rgb(255, 210, 100):
        ghost.visible = True
        ghost.fill = rgb(255, 210, 100)
        ghost.border = rgb(230, 190, 90)
        ghost.rf = 2
        ghost.gold = 200
    else:
        ghost.visible = False
        ghost.fill = None


def onMouseDrag(x, y):
    draw(x, y)


def onMousePress(x, y):
    if ghost.visible == False or ghost.fill == rgb(255, 200, 200):
        if tiles.contains(x, y):
            # tile lvl 1 -> 2
            if tiles.hitTest(x, y).fill == rgb(255, 200, 200) and app.gold >= 10 and app.core >= 2:
                app.gold -= 10
                tiles.hitTest(x, y).fill = rgb(230, 150, 255)
                tiles.hitTest(x, y).border = rgb(230, 215, 200)

            # tile lvl 2 -> 3
            if tiles.hitTest(x, y).fill == rgb(230, 150, 255) and app.gold >= 20 and app.core >= 3:
                app.gold -= 20
                tiles.hitTest(x, y).fill = rgb(150, 200, 150)


            # aura lvl 1 -> 2
            elif tiles.hitTest(x, y).fill == gradient(rgb(255, 180, 200),
                                                      rgb(150, 150, 255)) and app.gold >= 500 and app.core >= 2:
                app.gold -= 500
                tiles.hitTest(x, y).fill = gradient(rgb(255, 200, 255), rgb(255, 100, 255))
                tiles.hitTest(x, y).border = rgb(255, 200, 70)
                tiles.hitTest(x, y).bind.top -= 20
                tiles.hitTest(x, y).bind.left -= 20
                tiles.hitTest(x, y).bind.width += 39
                tiles.hitTest(x, y).bind.height += 39
                app.rf -= 1

            # mine lvl 1 -> 2
            elif tiles.hitTest(x, y).fill == rgb(255, 150, 180) and app.gold >= 50 and app.core >= 2:
                app.gold -= 20
                app.rf += 1
                tiles.hitTest(x, y).fill = rgb(220, 170, 225)
                tiles.hitTest(x, y).border = rgb(185, 155, 195)

            # mine lvl 2 -> 3
            elif tiles.hitTest(x, y).fill == rgb(220, 170, 225) and app.gold >= 150 and app.core >= 3:
                app.gold -= 100
                app.rf += 2
                tiles.hitTest(x, y).fill = rgb(250, 255, 200)
                tiles.hitTest(x, y).border = rgb(255, 200, 70)

            # core lvl 1 -> 2
            elif tiles.hitTest(x, y).fill == gradient(rgb(255, 200, 250), rgb(255, 150, 200)) and app.gold >= 500:
                app.gold -= 500
                app.maxGold += 500
                app.core = 2
                tiles.hitTest(x, y).fill = gradient(rgb(220, 170, 225), rgb(200, 150, 255))
                tiles.hitTest(x, y).border = rgb(255 * 0.95, 255 * 0.95, 255 * 0.95)

            # core lvl 2 -> 3
            elif tiles.hitTest(x, y).fill == gradient(rgb(220, 170, 225), rgb(200, 150, 255)) and app.gold >= 1000:
                app.gold -= 1000
                app.maxGold += 4000
                app.core = 3
                tiles.hitTest(x, y).fill = gradient(rgb(250, 255, 200), rgb(200, 255, 150))
                tiles.hitTest(x, y).border = rgb(255, 200, 70)

        else:
            # draws a tile
            draw(x, y)

    # places custom tile (1, 2, 3, ...)
    elif app.rf > abs(ghost.rf) and app.gold >= ghost.gold:
        if tiles.hitTest(ghost.centerX + 20, ghost.centerY) != None or tiles.hitTest(ghost.centerX,
                                                                                     ghost.centerY + 20) != None or tiles.hitTest(
                ghost.centerX - 20, ghost.centerY) != None or tiles.hitTest(ghost.centerX, ghost.centerY - 20) != None:
            app.rf += ghost.rf
            app.gold -= ghost.gold
            tiles.add(Rect(ghost.left, ghost.top, 20, 20, fill=ghost.fill, border=ghost.border))

            # bank tile
            if ghost.fill == rgb(225, 225, 255):
                app.maxGold += 500

            # aura tile
            elif ghost.fill == gradient(rgb(255, 180, 200), rgb(150, 150, 255)):
                danger.add(Rect(ghost.left - 19, ghost.top - 19, 58, 58, fill=rgb(255, 215, 235)))
                tiles.children[len(tiles) - 1].bind = danger.children[len(danger) - 1]
            ghost.visible = False
            ghost.fill = None


def onMouseMove(x, y):
    app.mx = x
    app.my = y

    if tiles.hitTest(x, y) in tiles:
        stats.visible = True
    elif corrupted.hitTest(x, y) in corrupted.children:
        stats.centerX, stats.centerY = corrupted.hitTest(x, y).centerX, corrupted.hitTest(x, y).centerY - 40
        stats.children[1].value = 'Stagnant corruption'
        stats.children[2].value = 'Lifeless matter'
        stats.visible = True
    elif corruption.hitTest(x, y) in corruption.children:
        stats.centerX, stats.centerY = corruption.hitTest(x, y).centerX, corruption.hitTest(x, y).centerY - 40
        stats.children[1].value = 'Live Corruption'
        stats.children[2].value = 'Infectious!'
        stats.visible = True
    elif ores.hitTest(x, y) in ores:
        stats.centerX, stats.centerY = ores.hitTest(x, y).centerX, ores.hitTest(x, y).centerY - 40
        stats.children[1].value = 'Gold deposit!'
        stats.children[2].value = 'Place tiles nearby '
        stats.visible = True
    else:
        stats.visible = False
    if stats.top < 0:
        stats.centerY += 80
    if stats.left < 0:
        stats.left = 0
    if stats.right > 400:
        stats.right = 400


def onStep():
    danger.toBack()
    grid.toFront()
    corrupted.toFront()
    corruption.toFront()
    ores.toFront()
    tiles.toFront()
    stats.toFront()

    stats.children[1].centerX = stats.children[0].centerX
    stats.children[2].centerX = stats.children[0].centerX
    stats.children[1].centerY = stats.children[0].centerY - 9
    stats.children[2].centerY = stats.children[0].centerY + 9

    if ghost.visible == True:
        if tiles.contains(app.mx, app.my) == False and corruption.contains(app.mx,
                                                                           app.my) == False and corrupted.contains(
                app.mx, app.my) == False and ores.contains(app.mx, app.my) == False:
            x = app.mx
            y = app.my
            while x % 20 != 0:
                x -= 1
            while y % 20 != 0:
                y -= 1
            ghost.left = x
            ghost.top = y
        else:
            ghost.left = 999
            ghost.top = 999

    # all corruption AI
    for i in corruption:
        try:
            if i.spawned == False:
                pass
        except:
            i.spawned = False

        if i.spawned == True:
            i.fill = rgb(200, 100, 100)
        if i.spawned == False and i.opacity >= 50:
            if tiles.hitsShape(i):
                ### tries to spread to all adjacent player-placed tiles
                # tile to right
                if randrange(1, 51) <= app.core and tiles.hitTest(i.centerX + 20, i.centerY) != None:
                    if tiles.hitTest(i.centerX + 20, i.centerY).fill in [
                        gradient(rgb(255, 180, 200), rgb(150, 150, 255)),
                        gradient(rgb(255, 200, 255), rgb(255, 100, 255))]:
                        removeAura(20, 0, i)

                    elif tiles.hitTest(i.centerX + 20, i.centerY).fill == rgb(150, 200, 150):
                        defortify(20, 0, i, 1)
                    elif tiles.hitTest(i.centerX + 20, i.centerY).fill == rgb(230, 150, 255):
                        defortify(20, 0, i, 2)

                    elif tiles.hitTest(i.centerX + 20, i.centerY).fill == rgb(255, 150, 180):
                        removeMine(20, 0, i, 1)
                    elif tiles.hitTest(i.centerX + 20, i.centerY).fill == rgb(220, 170, 225):
                        removeMine(20, 0, i, 2)
                    elif tiles.hitTest(i.centerX + 20, i.centerY).fill == rgb(250, 255, 200):
                        removeMine(20, 0, i, 3)

                    elif tiles.hitTest(i.centerX + 20, i.centerY) == tiles.children[0]:
                        removeCore()

                    else:
                        tiles.remove(tiles.hitTest(i.centerX + 20, i.centerY))
                        corrupted.add(Rect(i.left, i.top, 20, 20, fill=rgb(200, 100, 100), border=rgb(240, 100, 120)))
                        i.centerX += 20

                # tile below
                elif randrange(1, 51) <= app.core and tiles.hitTest(i.centerX, i.centerY + 20) != None:
                    if tiles.hitTest(i.centerX, i.centerY + 20).fill in [
                        gradient(rgb(255, 180, 200), rgb(150, 150, 255)),
                        gradient(rgb(255, 200, 255), rgb(255, 100, 255))]:
                        removeAura(0, 20, i)

                    elif tiles.hitTest(i.centerX, i.centerY + 20).fill == rgb(150, 200, 150):
                        defortify(0, 20, i, 1)
                    elif tiles.hitTest(i.centerX, i.centerY + 20).fill == rgb(230, 150, 255):
                        defortify(0, 20, i, 2)

                    elif tiles.hitTest(i.centerX, i.centerY + 20).fill == rgb(255, 150, 180):
                        removeMine(0, 20, i, 1)
                    elif tiles.hitTest(i.centerX, i.centerY + 20).fill == rgb(220, 170, 225):
                        removeMine(0, 20, i, 2)
                    elif tiles.hitTest(i.centerX, i.centerY + 20).fill == rgb(250, 255, 200):
                        removeMine(0, 20, i, 3)

                    elif tiles.hitTest(i.centerX, i.centerY + 20) == tiles.children[0]:
                        removeCore()

                    else:
                        tiles.remove(tiles.hitTest(i.centerX, i.centerY + 20))
                        corrupted.add(Rect(i.left, i.top, 20, 20, fill=rgb(200, 100, 100), border=rgb(240, 100, 120)))
                        i.centerY += 20

                # tile to left
                elif randrange(1, 51) <= app.core and tiles.hitTest(i.centerX - 20, i.centerY) != None:
                    if tiles.hitTest(i.centerX - 20, i.centerY).fill in [
                        gradient(rgb(255, 180, 200), rgb(150, 150, 255)),
                        gradient(rgb(255, 200, 255), rgb(255, 100, 255))]:
                        removeAura(-20, 0, i)

                    elif tiles.hitTest(i.centerX - 20, i.centerY).fill == rgb(150, 200, 150):
                        defortify(-20, 0, i, 1)
                    elif tiles.hitTest(i.centerX - 20, i.centerY).fill == rgb(230, 150, 255):
                        defortify(-20, 0, i, 2)

                    elif tiles.hitTest(i.centerX - 20, i.centerY).fill == rgb(255, 150, 180):
                        removeMine(-20, 0, i, 1)
                    elif tiles.hitTest(i.centerX - 20, i.centerY).fill == rgb(220, 170, 225):
                        removeMine(-20, 0, i, 2)
                    elif tiles.hitTest(i.centerX - 20, i.centerY).fill == rgb(250, 255, 200):
                        removeMine(-20, 0, i, 3)

                    elif tiles.hitTest(i.centerX - 20, i.centerY) == tiles.children[0]:
                        removeCore()

                    else:
                        tiles.remove(tiles.hitTest(i.centerX - 20, i.centerY))
                        corrupted.add(Rect(i.left, i.top, 20, 20, fill=rgb(200, 100, 100), border=rgb(240, 100, 120)))
                        i.centerX -= 20

                # tile above
                elif randrange(1, 51) <= app.core and tiles.hitTest(i.centerX, i.centerY - 20) != None:
                    if tiles.hitTest(i.centerX, i.centerY - 20).fill in [
                        gradient(rgb(255, 180, 200), rgb(150, 150, 255)),
                        gradient(rgb(255, 200, 255), rgb(255, 100, 255))]:
                        removeAura(0, -20, i)

                    elif tiles.hitTest(i.centerX, i.centerY - 20).fill == rgb(150, 200, 150):
                        defortify(0, -20, i, 1)
                    elif tiles.hitTest(i.centerX, i.centerY - 20).fill == rgb(230, 150, 255):
                        defortify(0, -20, i, 2)

                    elif tiles.hitTest(i.centerX, i.centerY - 20).fill == rgb(255, 150, 180):
                        removeMine(0, -20, i, 1)
                    elif tiles.hitTest(i.centerX, i.centerY - 20).fill == rgb(220, 170, 225):
                        removeMine(0, -20, i, 2)
                    elif tiles.hitTest(i.centerX, i.centerY - 20).fill == rgb(250, 255, 200):
                        removeMine(0, -20, i, 3)

                    elif tiles.hitTest(i.centerX, i.centerY - 20) == tiles.children[0]:
                        removeCore()

                    else:
                        tiles.remove(tiles.hitTest(i.centerX, i.centerY - 20))
                        corrupted.add(Rect(i.left, i.top, 20, 20, fill=rgb(200, 100, 100), border=rgb(240, 100, 120)))
                        i.centerY -= 20


            ### tries to expand (if possible)
            else:
                if randrange(1, 201) <= app.core * 5 - 4:
                    if tiles.hitTest(i.centerX + 20, i.centerY) == None and ores.hitTest(i.centerX + 20,
                                                                                         i.centerY) == None and corruption.hitTest(
                            i.centerX + 20, i.centerY) == None and corrupted.hitTest(i.centerX + 20,
                                                                                     i.centerY) == None and i.centerX + 20 < 400:
                        corrupted.add(Rect(i.left, i.top, 20, 20, fill=rgb(200, 100, 100), border=rgb(240, 100, 120)))
                        i.centerX += 20

                if randrange(1, 201) <= app.core * 5 - 4:
                    if tiles.hitTest(i.centerX, i.centerY + 20) == None and ores.hitTest(i.centerX,
                                                                                         i.centerY + 20) == None and corruption.hitTest(
                            i.centerX, i.centerY + 20) == None and corrupted.hitTest(i.centerX,
                                                                                     i.centerY + 20) == None and i.centerY + 20 < 400:
                        corrupted.add(Rect(i.left, i.top, 20, 20, fill=rgb(200, 100, 100), border=rgb(240, 100, 120)))
                        i.centerY += 20

                if randrange(1, 201) <= app.core * 5 - 4:
                    if tiles.hitTest(i.centerX - 20, i.centerY) == None and ores.hitTest(i.centerX - 20,
                                                                                         i.centerY) == None and corruption.hitTest(
                            i.centerX - 20, i.centerY) == None and corrupted.hitTest(i.centerX - 20,
                                                                                     i.centerY) == None and i.centerX - 20 > 0:
                        corrupted.add(Rect(i.left, i.top, 20, 20, fill=rgb(200, 100, 100), border=rgb(240, 100, 120)))
                        i.centerX -= 20

                if randrange(1, 201) <= app.core * 5 - 4:
                    if tiles.hitTest(i.centerX, i.centerY - 20) == None and ores.hitTest(i.centerX,
                                                                                         i.centerY - 20) == None and corruption.hitTest(
                            i.centerX, i.centerY - 20) == None and corrupted.hitTest(i.centerX,
                                                                                     i.centerY - 20) == None and i.centerY - 20 > 0:
                        corrupted.add(Rect(i.left, i.top, 20, 20, fill=rgb(200, 100, 100), border=rgb(240, 100, 120)))
                        i.centerY -= 20

    if danger.hitsShape(corruption):
        for i in corruption:
            if danger.contains(i.centerX, i.centerY):
                # i.opacity -= 5
                # if i.opacity <= 20:
                spawnCorruption(1)
                corrupted.add(Rect(i.left, i.top, 20, 20, fill=rgb(200, 100, 100), border=rgb(240, 100, 120)))
                corruption.remove(i)
    if danger.hitsShape(corrupted):
        for i in corrupted:
            if danger.contains(i.centerX, i.centerY):
                # i.opacity -= 5
                # if i.opacity <= 20:
                corrupted.remove(i)

    # gives info on hovering
    if tiles.hitTest(app.mx, app.my) in tiles.children:
        stats.centerX, stats.centerY = tiles.hitTest(app.mx, app.my).centerX, tiles.hitTest(app.mx, app.my).centerY - 40
        stats.visible = True

        if stats.top < 0:
            stats.centerY += 80
        if stats.left < 0:
            stats.left = 0
        if stats.right > 400:
            stats.right = 400

        if tiles.hitTest(app.mx, app.my).fill == rgb(255, 200, 200):
            stats.children[1].value = 'Default tile'
            if app.core == 2:
                stats.children[2].value = 'T1=(10G)'
            elif app.core == 3:
                stats.children[2].value = 'T2=(30G)'
            else:
                stats.children[2].value = '- - -'
        elif tiles.hitTest(app.mx, app.my).fill == rgb(230, 150, 255):
            stats.children[1].value = 'T1 Fortified tile'
            if app.core >= 3:
                stats.children[2].value = 'T2=(20G)'
            else:
                stats.children[2].value = '- - -'
        elif tiles.hitTest(app.mx, app.my).fill == rgb(150, 200, 150):
            stats.children[1].value = 'T2 Fortified tile'
            stats.children[2].value = 'MAX'
        elif tiles.hitTest(app.mx, app.my).fill == gradient(rgb(255, 180, 200), rgb(150, 150, 255)):
            stats.children[1].value = 'Tier 1 Aura'
            if app.core >= 2:
                stats.children[2].value = '-1 RF : T2=(50G)'
            else:
                stats.children[2].value = '- - -'
        elif tiles.hitTest(app.mx, app.my).fill == gradient(rgb(255, 200, 255), rgb(255, 100, 255)):
            stats.children[1].value = 'Tier 2 Aura'
            stats.children[2].value = '-2 RF : MAX'
        elif tiles.hitTest(app.mx, app.my).fill == rgb(225, 225, 255):
            stats.children[1].value = 'Gold Vault'
            stats.children[2].value = 'Stores 500G : 100G'
        elif tiles.hitTest(app.mx, app.my).fill == rgb(255, 150, 180):
            stats.children[1].value = 'Tier 1 mine'
            if app.core >= 2:
                stats.children[2].value = '1 RF : T2=(10G)'
            else:
                stats.children[2].value = '- - -'
        elif tiles.hitTest(app.mx, app.my).fill == rgb(220, 170, 225):
            stats.children[1].value = 'Tier 2 mine'
            if app.core >= 3:
                stats.children[2].value = '2 RF : T3=(50G)'
            else:
                stats.children[2].value = '- - -'
        elif tiles.hitTest(app.mx, app.my).fill == rgb(250, 255, 200):
            stats.children[1].value = 'Tier 3 mine'
            stats.children[2].value = '3 RF : MAX'
        elif tiles.hitTest(app.mx, app.my).fill == rgb(255, 210, 100):
            stats.children[1].value = 'Gold drill'
            stats.children[2].value = '2 RF'
        else:
            stats.children[1].value = str(abrv(math.floor(app.gold))) + '/' + str(abrv(app.maxGold)) + ' G'
            stats.children[2].value = str(abrv(app.rf)) + ' RF'

    app.gold += app.rf / 30
    if app.maxGold < app.gold:
        app.gold = app.maxGold

cmu_graphics.run()