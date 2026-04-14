from cmu_graphics import *
import math

#####

###             TODO:
###         - balancing
###         - gaming

#####

app.background = gradient('lightGreen', rgb(20, 70, 20))
rangeDisplay = Circle(200, 200, 45, opacity=5)
turretFlair = Circle(200, 200, 12, fill='forestGreen', opacity=20)
turret = Circle(200, 200, 8, fill=rgb(50, 120, 50))
aimFlair = Line(200, 200, 200, 177, lineWidth=14, fill='forestGreen', opacity=20)
aim = Line(200, 200, 200, 180, lineWidth=7.5, fill=turret.fill)
r = Rect(200, 10, 200, 20, fill=rgb(100, 200, 100), opacity=25)
g = Rect(240, 10, 200, 20, fill=rgb(100, 200, 100), opacity=25)
HPbar = Rect(10, 12, 150, 15, fill=rgb(50, 190, 50))
XPbar = Rect(240, 12, 150, 15, fill=rgb(100 * 0.8, 255 * 0.8, 155 * 0.8))
heart = Polygon(0, 3, -10, -5, -13, -15, -5, -20, 0, -15, 5, -20, 13, -15, 10, -5, fill=rgb(115, 255, 115), opacity=75)
star = Star(315, 20, 20, 8, roundness=70, fill=rgb(100, 255, 155), opacity=75)
HPlabel = Label(20, HPbar.centerX, HPbar.centerY, fill=rgb(50, 80, 50), bold=True, font='orbitron')
XPlabel = Label('0%', XPbar.centerX, XPbar.centerY, fill=rgb(50, 80, 50), size=11, bold=True, font='orbitron')
darken = Rect(0, 0, 400, 400, opacity=40, visible=False)
msgBG = Rect(100, 50, 200, 100, fill=rgb(150, 225, 150), opacity=50, visible=False)
titleMsg = Label('', 200, 70, size=15, font='orbitron', fill=rgb(50, 80, 50), bold=True, visible=False)
msg1 = Label('', 200, 90, size=12, font='orbitron', fill=rgb(50, 80, 50))
msg2 = Label('', 200, 110, size=12, font='orbitron', fill=rgb(50, 80, 50))
msg3 = Label('', 200, 130, size=12, font='orbitron', fill=rgb(50, 80, 50))
ops = ['spd', 'hp', 'hpRgn', 'Full heal', 'rng']
try:
    coverArt = Image('https://piskel-imgstore-b.appspot.com/img/5c500dfa-7053-11ed-b972-c33d23589ca5.gif', 0, 0)
except Exception as e:
    coverArt = Rect(0, 0, 400, 400)
    print('https://piskel-imgstore-b.appspot.com/img/5c500dfa-7053-11ed-b972-c33d23589ca5.gif')
    cover = Group(coverArt, Label('Press any key to start', 200, 200, font='orbitron', size=20, fill='white'),
                  Label(e, 200, 375, size=12, fill='red', bold=True),
                  Label('Go to printed link in console to reload cover art', 200, 390, size=11, fill='gold', bold=True))
else:
    cover = Group(coverArt, Label('Press any key to start', 200, 375, font='orbitron', size=20))

enemies = Group()
bullets = Group()
player = Group(turret, turretFlair, aim, aimFlair)
bg = Group()

#####
### ADD SHOP POWERUPS/SHOOTING PATTERS/STUFF (after each levelup)
#####
app.ticks = 0
app.hp = 20  # wowza thats some definitions there
app.xp = 0
app.xpUp = 100
app.level = 1
app.hpLost = 0
app.keyPressed = False
app.shopOpen = False
app.spdBonus = 1
app.rgn = 0
app.maxHP = 20
enemies.closest = None
enemies.closestDist = 999
app.tick = 0
app.rngMult = 1
turret.atkSpd = 10
turret.bltSpd = 10
turret.damage = 1
turret.delay = 0
turret.pierce = 0
r.width = 154
r.left = 8
g.width = 154
g.right = 392
star.centerX = XPlabel.centerX
heart.height *= 1.4
heart.width *= 1.4
app.souls = 0
heart.centerX, heart.centerY = 85, 21
bullets.opacity = 100
player.vx = 0
player.vy = 0
rangeDisplay.toBack()
HPlabel.centerX = r.centerX
XPlabel.centerX = g.centerX
r.centerY += 10
g.centerY += 10
HPlabel.centerY = heart.centerY
XPlabel.centerY = star.centerY
HPbar.centerY = r.centerY
XPbar.centerY = g.centerY
XPbar.width = 0.1
cover.toFront()

for i in range(10):
    bg.add(Circle(randrange(-50, 451), randrange(-50, 451), 50, fill=rgb(50, 90, 50), opacity=5))


def popUp(result, extra1='', extra2='', extra3=''):
    darken.visible = True
    darken.toFront()
    msgBG.visible = True
    titleMsg.visible = True
    titleMsg.toFront()
    msg1.toFront()
    msg2.toFront()
    msg3.toFront()
    msg1.visible = True
    msg2.visible = True
    msg3.visible = True
    if result == 'lose':  # lose screen
        HPbar.visible = False
        HPlabel.value = 0
        titleMsg.value = 'You were overcome...'
        msg1.value = 'Kills: ' + str(app.souls)
        msg2.value = 'Level: ' + str(app.level)
        msg3.value = 'Damage taken: ' + str(app.hpLost)
        app.stop()
    else:  # fbfbfb
        titleMsg.value = result
        msg1.value = extra1
        msg2.value = extra2
        msg3.value = extra3


def onStep():
    app.ticks += 1
    if cover.opacity == 0 and app.shopOpen == False:
        app.hp += app.rgn / app.maxHP

        bg.toBack()

        if turret.fill == rgb(200, 255, 200):  # updates immunity frame
            turret.fill = rgb(50, 120, 50)

        if app.hp < 0:  # corrects underflow and overflow health
            app.hp = 0
        elif app.hp > app.maxHP:
            app.hp = app.maxHP

        if turret.delay > 0:  # ticks the delay between shots
            turret.delay -= 1

        HPbar.left = 10  # updating bars
        HPbar.width = ((app.hp / app.maxHP) * 150) + 0.1
        XPbar.width = (((app.xp / app.xpUp) * 100) * 1.5) + 0.1
        XPbar.right = 390
        HPlabel.value = math.floor(app.hp)
        XPlabel.value = str(math.floor((app.xp / app.xpUp) * 100)) + '%'

        if app.xp >= app.xpUp:  # what to do when levelling up
            app.xp -= app.xpUp
            app.xpUp *= 1.1
            app.level += 1
            app.shopOpen = True
            up1 = ops[randrange(0, len(ops))]
            ops.remove(up1)
            up2 = ops[randrange(0, len(ops))]
            ops.remove(up2)
            up3 = ops[randrange(0, len(ops))]
            ops.remove(up3)

            upg1 = None
            upg2 = None
            upg3 = None

            # UPGRADES ⬇                   ||    BROKEN /!\   ||
            for i in range(3):

                if i == 1:
                    slot = up1
                if i == 2:
                    slot = up2
                if i == 3:
                    slot = up3

                if 'Full heal' in [up1, up2, up3]:
                    app.HP = app.maxHP
                if 'spd' in [up1, up2, up3]:
                    randint = randrange(5, 11)
                    app.spdBonus += randint / 100
                    if i == 1:
                        up1 = '+' + str(randint) + '% Speed'
                        upg1 = 'spd'
                    if i == 2:
                        up2 = '+' + str(randint) + '% Speed'
                        upg2 = 'spd'
                    if i == 3:
                        up3 = '+' + str(randint) + '% Speed'
                        upg3 = 'spd'
                if 'hp' in [up1, up2, up3]:
                    randint = randrange(2, 5)
                    app.hp += randint
                    app.maxHP += randint
                    if i == 1:
                        up1 = '+' + str(randint) + ' Max health'
                        upg1 = 'hp'
                    if i == 2:
                        up2 = '+' + str(randint) + ' Max health'
                        upg2 = 'hp'
                    if i == 3:
                        up3 = '+' + str(randint) + ' Max health'
                        upg3 = 'hp'
                if 'hpRgn' in [up1, up2, up3]:
                    randint = randrange(rounded(app.maxHP / 20), (rounded(app.maxHP / 15)) + 1)
                    app.rgn += pythonRound(randint / app.maxHP, 2)
                    if i == 1:
                        up1 = '+' + str(randint) + ' Regeneration'
                        upg1 = 'hpRgn'
                    if i == 2:
                        up2 = '+' + str(randint) + ' Regeneration'
                        upg2 = 'hpRgn'
                    if i == 3:
                        up3 = '+' + str(randint) + ' Regeneration'
                        upg3 = 'hpRgn'
                if 'rng' in [up1, up2, up3]:
                    randint = randrange(4, 11)
                    app.rngMult += randint / 100
                    if i == 1:
                        up1 = '+' + str(randint) + '% Range'
                        upg1 = 'rng'
                    if i == 2:
                        up2 = '+' + str(randint) + '% Range'
                        upg2 = 'rng'
                    if i == 3:
                        up3 = '+' + str(randint) + '% Range'
                        upg3 = 'rng'

            ops.append(upg1)
            ops.append(upg2)
            ops.append(upg3)

            popUp('Level ' + str(app.level - 1) + ' -> ' + str(app.level), up1, up2, up3)
            XPbar.width = 150
            XPbar.right = 390

        rangeDisplay.radius = (50 * (app.rngMult)) - 5

        bullets.centerX += player.vx  # moving scene based on velocity
        enemies.centerX += player.vx
        bullets.centerY += player.vy
        enemies.centerY += player.vy
        bg.centerX += player.vx
        bg.centerY += player.vy

        player.vx *= 0.7  # slows movement down (friction)
        player.vy *= 0.7

        for i in range(10):
            if bg.children[i].left > 390:
                bg.children[i].right = 10
                bg.children[i].centerY = randrange(10, 391)
            elif bg.children[i].right < 10:
                bg.children[i].left = 390
                bg.children[i].centerY = randrange(10, 391)
            if bg.children[i].top > 390:
                bg.children[i].bottom = 10
                bg.children[i].centerX = randrange(10, 391)
            elif bg.children[i].bottom < 10:
                bg.children[i].top = 390
                bg.children[i].centerX = randrange(10, 391)

        for i in range(len(bullets)):  # bullet script
            bullets.children[i].centerX, bullets.children[i].centerY = getPointInDir(bullets.children[i].centerX,
                                                                                     bullets.children[i].centerY,
                                                                                     bullets.children[i].ang,
                                                                                     turret.bltSpd)
            if 100 - (distance(bullets.children[i].centerX, bullets.children[i].centerY, 200, 200) / 2) < 0:
                bullets.children[i].opacity = 0
            elif 100 - (distance(bullets.children[i].centerX, bullets.children[i].centerY, 200, 200) / 2) > 100:
                bullets.children[i].opacity = 100
            else:
                bullets.children[i].opacity = 100 - (
                            distance(bullets.children[i].centerX, bullets.children[i].centerY, 200, 200) / 2)

        for i in range(len(bullets)):  # deleting bullets
            if bullets.children[i].left > 400 or bullets.children[i].right < 0 or bullets.children[i].top > 400 or \
                    bullets.children[i].bottom < 0 or bullets.children[i].opacity == 0:
                bullets.remove(bullets.children[i])
                break

        bullets.toBack()

        if enemies.closest != None and distance(enemies.closest.centerX, enemies.closest.centerY, turret.centerX,
                                                turret.centerY) < (50 * (app.rngMult)) + 3 and turret.delay == 0:
            turret.delay = turret.atkSpd  # shoots at closest enemy
            if len(bullets) < 20:
                ang = angleTo(200, 200, enemies.closest.centerX, enemies.closest.centerY)
                x, y, = getPointInDir(200, 200, ang, 20)
                aim.x2, aim.y2 = x, y
                bullets.add(Line(200, 200, x, y, fill=rgb(200, 255, 200), lineWidth=5))
                bullets.children[len(bullets) - 1].ang = ang
                bullets.children[len(bullets) - 1].pierce = 0
                x, y, = getPointInDir(200, 200, ang, 23)
                aimFlair.x2, aimFlair.y2 = x, y

        app.tick += 1  # ticks between enemy spawns
        if len(enemies) < 5 and app.tick >= 3:  # spawns enemies
            app.tick = 0
            wall = randrange(1, 5)
            if wall == 1:
                enemies.add(Circle(-5, randrange(0, 401), 5, fill=rgb(80, 150, 80)))
            elif wall == 2:
                enemies.add(Circle(405, randrange(0, 401), 5, fill=rgb(80, 150, 80)))
            elif wall == 3:
                enemies.add(Circle(randrange(0, 401), -5, 5, fill=rgb(80, 150, 80)))
            elif wall == 4:
                enemies.add(Circle(randrange(0, 401), 405, 5, fill=rgb(80, 150, 80)))
            enemies.children[len(enemies) - 1].health = app.level * 2
            enemies.children[len(enemies) - 1].speed = 3 + app.level / 5

        for i in range(len(enemies)):
            # resets targeted enemy when previous is killed ⬇
            if not enemies.closest in enemies:
                enemies.closestDist = 999
                enemies.closest = None

                # resets each enemy's invincibility frame ⬇
            if enemies.children[i].fill == rgb(200, 255, 200):
                enemies.children[i].fill = rgb(80, 150, 80)

                # enemy AI ⬇
            enemies.children[i].ang = angleTo(enemies.children[i].centerX, enemies.children[i].centerY, 200, 200)
            enemies.children[i].centerX, enemies.children[i].centerY = getPointInDir(enemies.children[i].centerX,
                                                                                     enemies.children[i].centerY,
                                                                                     enemies.children[i].ang,
                                                                                     enemies.children[i].speed)

            # stores closest enemy & it's distance ⬇
            if distance(enemies.children[i].centerX, enemies.children[i].centerY, 200, 200) < enemies.closestDist:
                enemies.closest = enemies.children[i]
                enemies.closestDist = distance(enemies.children[i].centerX, enemies.children[i].centerY, 200, 200)

                # collision damage with turret ⬇
            if enemies.children[i].hitsShape(turret) and turret.fill != rgb(200, 255, 200):
                app.hp -= 1
                app.hpLost += 1
                turret.fill = rgb(200, 255, 200)

                # fancy opacity shenanigans based off of distance to turret ⬇
            if 100 - (distance(enemies.children[i].centerX, enemies.children[i].centerY, 200, 200) / 2) < 0:
                enemies.children[i].opacity = 0
            else:
                enemies.children[i].opacity = 100 - (
                            distance(enemies.children[i].centerX, enemies.children[i].centerY, 200, 200) / 2)

            # controls deletion of enemies ⬇⬇⬇
        for i in range(len(enemies)):
            if enemies.children[i].hitsShape(bullets) and enemies.children[i].fill != rgb(200, 255, 200):
                enemies.children[i].health -= turret.damage  # takes hp away from enemy [i]
                if enemies.children[i].health <= 0:
                    enemies.remove(enemies.children[i])  # deletes enemy [i]
                    app.xp += randrange(1, 6)
                    app.souls += 1
                    # ⬇ IndexError: list index out of range 💀
                    break  # inefficient but functional method for avoiding a crash when deleting children
                enemies.children[i].fill = rgb(200, 255, 200)
            elif enemies.children[i].hitsShape(turret) or distance(enemies.children[i].centerX,
                                                                   enemies.children[i].centerY, 200, 200) > 240:
                enemies.remove(enemies.children[i])
                break  # IndexError: list index out of range 💀
            aim.fill = turret.fill  # updates color of turret's barrel

        if rounded(app.hp) <= 0:  # checks if youre dead
            popUp('lose')
    elif app.keyPressed == True:
        if cover.opacity > 0:
            cover.opacity -= 2

    if HPbar.width > 150:
        HPbar.width = 150


def onKeyHold(keys):
    if cover.opacity == 0 and app.shopOpen == False:
        if 'w' in keys or 'up' in keys:
            player.vy += app.spdBonus
        if 's' in keys or 'down' in keys:
            player.vy -= app.spdBonus
        if 'a' in keys or 'left' in keys:
            player.vx += app.spdBonus
        if 'd' in keys or 'right' in keys:
            player.vx -= app.spdBonus


def onKeyPress(key):
    app.keyPressed = True
    if app.shopOpen == True and not key in ['a', 's', 'w', 'd', 'up', 'down', 'left', 'right']:
        app.shopOpen = False
        titleMsg.visible = False
        msg1.visible = False
        msg2.visible = False
        msg3.visible = False
        msgBG.visible = False
        darken.visible = False
    if key == 'X':
        app.xp += 40 + (app.xpUp / 10)
    if key == 'Z':
        app.hp -= 5
    if key == 'C':
        popUp('Forced termination', 'if this was an accident,', 'dont press shift+c idiot', '>:)')

cmu_graphics.run()