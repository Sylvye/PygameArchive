from cmu_graphics import *

#####
###                 TWO-PLAYER "tag" game CONTROLS:
###         BLUE                                    YELLOW
### • ASWD to move                          • Arrow keys to move
### • Q - repel Yellow player (-15 mana)     • Page up - tractor beam (-20 mana)
###     • stronger effect when used in          • useful at longer range
###       close proximity                   • Page down - super fast for a limited duration (-50 mana)
### • E - shoot projectile    (-25 mana)         • best to bounce around the
###     • projectile cannot be aimed if           arena, and not to focus on
###       the yellow player is stationary         aiming at the blue player
###                         MANA EXPLANATION
###             • Mana is the way you use your abilities,
###             it regenerates one mana each frame, capping
###             out at 100 total stored mana.
###             • The blue player relies heavily on mana,
###             as they can only win by landing a hit
###             with their projectile.
###             • yellow uses mana to assist them in
###               being able to tag the blue player
#####
app.background = 'papayaWhip'
app.ready = False

yellow = Circle(300, 200, 8, fill='yellow')  # defining stuff
yellow.dx = 0
yellow.dy = 0
yellow.energy = 0
yellow.maxV = 20
yellow.accel = 1
blue = Circle(100, 200, 8, fill='cyan')
blue.dx = 0
blue.dy = 0
blue.energy = 0
blue.maxV = 25

pulse = Circle(200, 200, 50, fill=None, border='magenta', borderWidth=10, opacity=0)
halo = Circle(0, 0, 16, fill=None, border='yellow', opacity=90)

il1 = Label('ASWD to start', blue.centerX, blue.centerY - 20)
il2 = Label('Arrow keys to start', yellow.centerX, yellow.centerY - 20)

eyesY = Group(Circle(196, 200, 3, fill=rgb(150, 150, 50)), Circle(204, 200, 3, fill=rgb(150, 150, 50)))
eyesB = Group(Circle(196, 190, 3, fill=rgb(100, 50, 200)), Circle(204, 190, 3, fill=rgb(100, 50, 200)))

yellowEbar = Rect(240, 10, 150, 20, fill='yellow')
blueEbar = Rect(10, 10, 150, 20, fill=rgb(0, 200, 250))
yellowELabel = Label(0, yellowEbar.centerX, yellowEbar.centerY, fill=rgb(127, 107, 0), bold=True)
blueELabel = Label(0, blueEbar.centerX, blueEbar.centerY, fill='darkCyan', bold=True)
yellowTrail = Line(0, 0, 0, 0, lineWidth=16)
yellowCap = Circle(200, 200, 8)
blueTrail = Line(0, 0, 0, 0, lineWidth=16)
blueCap = Circle(200, 200, 8)

tractor = Line(0, 0, 0, 0, opacity=0, lineWidth=24,
               fill=gradient(rgb(255, 115, 215), rgb(235, 115, 255), 'papayaWhip', start='right'))

orbs = Group()
orbs.opacity = 100


def gameOver(player):
    if app.ready == True:
        app.background = 'white'
        if player == 1:
            Rect(0, 0, 400, 400, fill='yellow', opacity=40)
        else:
            Rect(0, 0, 400, 400, fill='blue', opacity=40)

        halo.toFront()
        orbs.toFront()
        blue.toFront()
        yellow.toFront()
        eyesY.toFront()
        eyesB.toFront()

        if player == 1:
            Label('Yellow victory!', 200, 50, fill=rgb(100, 100, 50), size=30, bold=True)
        else:
            Label('Blue victory!', 200, 50, fill=rgb(50, 100, 50), size=30, bold=True)

        app.stop()
    else:
        if player == 1:
            yellow.dx *= -1.5
            yellow.dy *= -1.5
            yellow.centerX += yellow.dx
            yellow.centerY += yellow.dy
        if player == 2:
            blue.dx *= -1.5
            blue.dy *= -1.5
            blue.centerX += blue.dx
            blue.centerY += blue.dy


def onStep():
    if app.ready == True:
        if blue.energy < 100:
            blue.energy += 0.5
        if yellow.energy < 100:
            yellow.energy += 0.5
    yellowTrail.x1 = yellow.centerX  # yellow movemneement n stretching n stuff
    yellowTrail.y1 = yellow.centerY
    yellow.centerX += yellow.dx
    yellow.centerY += yellow.dy
    yellow.dx *= 0.95
    yellow.dy *= 0.95
    yellowTrail.x2 = yellow.centerX
    yellowTrail.y2 = yellow.centerY
    yellowCap.centerX = yellowTrail.x1
    yellowCap.centerY = yellowTrail.y1
    yellow.toFront()
    eyesY.toFront()

    blueTrail.x1 = blue.centerX  # blue movement n stretchin
    blueTrail.y1 = blue.centerY
    blue.centerX += blue.dx
    blue.centerY += blue.dy
    blue.dx *= 0.95
    blue.dy *= 0.95
    blueTrail.x2 = blue.centerX
    blueTrail.y2 = blue.centerY
    blueCap.centerX = blueTrail.x1
    blueCap.centerY = blueTrail.y1
    blue.toFront()
    eyesB.toFront()

    # eyes centering & focusing
    eyesY.rotateAngle = angleTo(yellow.centerX, yellow.centerY, blue.centerX, blue.centerY)
    eyesY.centerX, eyesY.centerY = getPointInDir(yellow.centerX, yellow.centerY, eyesY.rotateAngle, 3)

    eyesB.rotateAngle = angleTo(blue.centerX, blue.centerY, yellow.centerX, yellow.centerY)
    eyesB.centerX, eyesB.centerY = getPointInDir(blue.centerX, blue.centerY, eyesB.rotateAngle, 3)

    if tractor.opacity > 0:  # tractor beam
        tractor.x1 = yellow.centerX
        tractor.y1 = yellow.centerY
        tractor.x2, tractor.y2 = getPointInDir(blue.centerX, blue.centerY,
                                               angleTo(yellow.centerX, yellow.centerY, blue.centerX, blue.centerY), 300)
        blue.dx -= (blue.centerX - yellow.centerX) * (0.015)
        blue.dy -= (blue.centerY - yellow.centerY) * (0.015)
        if blue.centerX > yellow.centerX and blue.centerY > yellow.centerY:
            tractor.fill = gradient(rgb(255, 115, 215), rgb(235, 115, 255), 'papayaWhip', start='left')
        elif blue.centerX < yellow.centerX and blue.centerY > yellow.centerY:
            tractor.fill = gradient(rgb(255, 115, 215), rgb(235, 115, 255), 'papayaWhip', start='right')
        elif blue.centerX > yellow.centerX and blue.centerY < yellow.centerY:
            tractor.fill = gradient(rgb(255, 115, 215), rgb(235, 115, 255), 'papayaWhip', start='left')
        else:
            tractor.fill = gradient(rgb(255, 115, 215), rgb(235, 115, 255), 'papayaWhip', start='right')

    yellow.fill = rgb(255, 255, 150)  # yellow fades out when moving slower
    yellowTrail.fill = yellow.fill
    yellowCap.fill = yellow.fill
    testOpc = ((abs(yellow.dx) + abs(yellow.dy)) * 5)
    if testOpc > 100:
        testOpc = 100
    if testOpc < 10:
        testOpc = 10
    if app.ready == True:
        yellow.opacity = testOpc
        yellowTrail.opacity = yellow.opacity
        yellowCap.opacity = yellow.opacity
        eyesY.opacity = yellow.opacity

    testColor = (abs(blue.dx) + abs(blue.dy))  # speed-based coloring of blue
    if testColor > 31.875:
        testColor = 31.875
    blue.fill = rgb(testColor * 6 + 50, 255 - testColor * 3, 255 - testColor * 2)
    blueTrail.fill = blue.fill
    blueCap.fill = blue.fill

    if yellow.right >= 400 or yellow.left <= 0:  # collision on walls, ceiling, & floor
        yellow.dx *= -1.25
        if yellow.right >= 400:
            yellow.right = 400
        else:
            yellow.left = 0
    if yellow.top <= 0:
        yellow.top = 0
        yellow.dy *= -0.5
    if yellow.bottom >= 400:
        yellow.dy *= -0.75
        yellow.bottom = 400

    if blue.right >= 400 or blue.left <= 0:
        blue.dx *= -1.25
        if blue.right >= 400:
            blue.right = 400
        else:
            blue.left = 0
    if blue.top <= 0:
        blue.top = 0
        blue.dy *= -0.5
    if blue.bottom >= 400:
        blue.dy *= -0.75
        blue.bottom = 400

    if len(orbs) != 0:
        orbs.centerX, orbs.centerY = getPointInDir(orbs.centerX, orbs.centerY, orbs.ang,
                                                   distance(blue.centerX, blue.centerY, yellow.centerX,
                                                            yellow.centerY) / 13.333)
        if orbs.hitsShape(yellow) or orbs.hitsShape(yellowTrail) or orbs.hitsShape(yellowCap):
            gameOver(2)
        if orbs.right < 0 or orbs.left > 400 or orbs.bottom < 0 or orbs.top > 400:
            orbs.clear()
    if len(orbs) > 0:
        orbs.rotateAngle += 15
    if (blue.hitsShape(yellow) or blue.hitsShape(yellowTrail) or blue.hitsShape(yellowCap)) and yellow.opacity > 10:
        gameOver(1)

    if yellow.dx > yellow.maxV:  # capping of velocity
        yellow.dx = yellow.maxV
    if yellow.dy > yellow.maxV:
        yellow.dy = yellow.maxV
    if blue.dx > blue.maxV:
        blue.dx = blue.maxV
    if blue.dy > blue.maxV:
        blue.dy = blue.maxV
    if abs(yellow.dx) + abs(yellow.dy) > 20:
        halo.centerX = yellow.centerX
        halo.centerY = yellow.centerY
        halo.visible = True
    else:
        halo.visible = False
    if tractor.opacity > 0:
        tractor.opacity -= 2
        tractor.toBack()
    if yellow.accel > 1:
        yellow.accel -= 0.04
    else:
        yellow.maxV = 25

    if pulse.opacity > 0:  # dash fade effect
        pulse.opacity -= 2
        pulse.borderWidth += 1
        pulse.radius += 16

    if app.ready == True:
        yellowEbar.opacity = rounded(yellow.energy)
        blueEbar.opacity = rounded(blue.energy)
        yellowELabel.value = rounded(yellow.energy)
        blueELabel.value = rounded(blue.energy)


def onKeyHold(keys):
    if 'up' in keys:  # yellow's movement from key inputs
        il2.visible = False
        yellow.dy -= yellow.accel
    if 'left' in keys:
        il2.visible = False
        yellow.dx -= yellow.accel
    if 'right' in keys:
        il2.visible = False
        yellow.dx += yellow.accel
    if 'down' in keys:
        il2.visible = False
        yellow.dy += yellow.accel

    if 'w' in keys:  # players's movement from key inputs
        il1.visible = False
        blue.dy -= 0.8
    if 'a' in keys:
        il1.visible = False
        blue.dx -= 0.8
    if 'd' in keys:
        il1.visible = False
        blue.dx += 0.8
    if 's' in keys:
        il1.visible = False
        blue.dy += 0.8

    if il1.visible == False and il2.visible == False:
        app.ready = True

    # abilities (q+e, pgup+pgdwn)
    if app.ready == True:
        if 'e' in keys and blue.energy >= 25:
            if len(orbs) <= 5 and yellow.opacity > 15:
                blue.energy -= 25
                px = None
                py = None
                for i in range(3):
                    x, y = getPointInDir(blue.centerX, blue.centerY, i * 120, 20)
                    if px != None:
                        orbs.add(Line(px, py, x, y, fill='magenta', lineWidth=6))
                        orbs.children[len(orbs) - 1].toBack()
                    else:
                        ppx = x
                        ppy = y
                    orbs.add(Circle(x, y, 6, fill='hotPink', opacity=80))

                    orbs.opacity = 100
                    px = x
                    py = y
                    if len(orbs) == 5:
                        orbs.add(Line(ppx, ppy, x, y, fill='magenta', lineWidth=6))
                        orbs.children[len(orbs) - 1].toBack()
                ang = angleTo(orbs.centerX, orbs.centerY, yellow.centerX - yellow.dx, yellow.centerY - yellow.dy)
                x, y = getPointInDir(orbs.centerX, orbs.centerY, ang, 10)
                orbs.ang = angleTo(orbs.centerX, orbs.centerY, yellow.centerX + yellow.dx * 15,
                                   yellow.centerY + yellow.dy * 15)
        if 'q' in keys and blue.energy >= 15 and pulse.opacity == 0:
            blue.energy -= 15
            pulse.opacity = 40
            pulse.radius = 1
            pulse.borderWidth = 1
            pulse.centerX = pulse.centerX
            pulse.centerY = pulse.centerY
            pulse.centerX, pulse.centerY = blue.centerX, blue.centerY

            ang = angleTo(yellow.centerX, yellow.centerY, pulse.centerX, pulse.centerY)
            nx, ny = getPointInDir(yellow.centerX, yellow.centerY, ang + 180,
                                   20 - distance(pulse.centerX, pulse.centerY, yellow.centerX, yellow.centerY) / 25)
            yellow.dx, yellow.dy = nx - yellow.centerX, ny - yellow.centerY

        if '.' in keys and yellow.energy >= 20 and tractor.opacity == 0:
            yellow.energy -= 20
            tractor.opacity = 50
        if '/' in keys and yellow.energy >= 50:
            yellow.energy -= 50
            yellow.accel = 5
            yellow.maxV = 50

cmu_graphics.run()