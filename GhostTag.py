from cmu_graphics import *
from time import sleep

#####                                 INFO
# You will spawn on the right, the enemy (ghost) will chase you with using a
# set of rules on how it will behave.
# you use W, A, S, & D to move your character
# You can make the ghost have a grey aura in the code
# TWO PLAYER MODE IS HERE!
#   - control the ghost with arrow keys
#   - the ai will take control if arrow keys are not being pressed
# 2 NEW DIFFICULTIES!
#   - easy: you are faster, ghost does not hide
#   - hard: you are slower, ghost summons more illusions (some illusions have illusions! >:) )
# The ghost will:
#   - teleport halfway to you if you are too far away
#   - move slowly towards you and obey physics if you are not in it's FOV
#   - move at a medium pace if it can see you, but is not close
#   - sprint when you come close and reveal it's presence
#   - the longer the game goes on, the shorter the distance required to
# teleport
#   - the ghost moves slightly faster the longer you have evaded the ghost for
#   - later in the game, the ghost will move faster after time has passed
# without seeing you
#   - the orb in the center glows redder when the ghost is nearer to you
#                                  PHASE 2
#   - illusory specters will appear to discombobulate you, but do not fear! They cannot harm you
#   - blinding flash will happen when the clock strikes midnight
#   - the ghost will be harder to distinguish
#####                            IDEAS FOR LATER
#       - difficulty selector screen
#       - invisible-unless-you're-nearby barriers - ?
#       - dynamic backgroud
#       - improve illusions
#       - game restarts on death
#       - glitchy numerals
#       - reduce lag on phase too
#       - maybe add map selector?? / random map generation with infinite scrolling
#####                                 CODE
import math

app.background = 'lavender'
p1 = Circle(100, 200, 10, fill='peachPuff', opacity=75)
p2 = Circle(300, 200, 10, fill='lightSalmon')
difficulty = 4
p2.timer = 0
p2.roaming = False
p1.hunting = False
cast = Line(-10, -10, -10, -10, lineWidth=6, fill='salmon')
los = Line(0, 0, 0, 0, visible=False, lineWidth=0.1)
sensing = Circle(0, 0, 90, visible=False, opacity=10)
clone = Circle(100, 200, 10, fill='lightSalmon', visible=False)
orbitor = Line(0, 0, 0, 120, visible=False)
orbitor2 = Line(0, 0, 0, 120, visible=False)
orbitor3 = Line(0, 0, 0, 120, visible=False)
illusion = Circle(100, 200, 10, fill='lightSalmon', visible=False)
illusion2 = Circle(100, 200, 10, fill='lightSalmon', visible=False)
illusion3 = Circle(100, 200, 10, fill='lightSalmon', visible=False)
title = Label('', 200, 20, size=35, fill='white', font='monospace', bold=True)

maze = Group(
    Circle(200, 200, 20, fill='lightSteelBlue'),
    Line(200, 100, 200, 300, lineWidth=10, fill='lightSteelBlue'),
    Circle(200, 100, 5, fill='lightSteelBlue'),
    Circle(200, 300, 5, fill='lightSteelBlue'),
    Rect(125, 350, 150, 10, fill='lightSteelBlue'),
    Rect(125, 50, 150, 10, fill='lightSteelBlue'),
    Rect(300, 150, 95, 10, fill='lightSteelBlue'),
    Rect(5, 250, 95, 10, fill='lightSteelBlue'),
    Circle(300, 155, 5, fill='lightSteelBlue'),
    Circle(395, 155, 5, fill='lightSteelBlue'),
    Circle(100, 255, 5, fill='lightSteelBlue'),
    Circle(5, 255, 5, fill='lightSteelBlue'),
    Circle(125, 355, 5, fill='lightSteelBlue'),
    Circle(275, 355, 5, fill='lightSteelBlue'),
    Circle(125, 55, 5, fill='lightSteelBlue'),
    Circle(275, 55, 5, fill='lightSteelBlue'),
    Rect(-10, 0, 5, 405),
    Rect(0, -10, 405, 5),
    Rect(0, 405, 400, 5),
    Rect(405, 0, 5, 400)
)

mazeCover = Group(
    Rect(190, 95, 20, 210, fill=rgb(200, 220, 255)),
    Circle(200, 200, 25, fill=rgb(200, 220, 255)),
    Circle(200, 97, 10, fill=rgb(200, 220, 255)),
    Circle(200, 303, 10, fill=rgb(200, 220, 255)),
    Rect(120, 345, 160, 20, fill=rgb(200, 220, 255)),
    Rect(120, 45, 160, 20, fill=rgb(200, 220, 255)),
    Rect(295, 145, 105, 20, fill=rgb(200, 220, 255)),
    Rect(0, 245, 105, 20, fill=rgb(200, 220, 255)),
    Circle(122, 55, 10, fill=rgb(200, 220, 255)),
    Circle(278, 55, 10, fill=rgb(200, 220, 255)),
    Circle(297, 155, 10, fill=rgb(200, 220, 255)),
    Circle(103, 255, 10, fill=rgb(200, 220, 255)),
    Circle(122, 355, 10, fill=rgb(200, 220, 255)),
    Circle(278, 355, 10, fill=rgb(200, 220, 255)),
)

maze.toFront()
orb = Circle(200, 200, 15, fill=None, opacity=5)
start = False
clock = 0
runes = Group()
flash = Rect(0, 0, 400, 400, opacity=0)
runes.toBack()


def onKeyHold(keys):
    global clock
    if difficulty != 1:
        testOpacity = rounded(math.sqrt(((p2.centerX - p1.centerX) ** 2) + ((p2.centerY - p1.centerY) ** 2)))
        if testOpacity > 100:
            testOpacity = 100
        p2.opacity = 100 - testOpacity

        if clock > 360:
            testOpacity = rounded(
                math.sqrt(((illusion.centerX - p1.centerX) ** 2) + ((illusion.centerY - p1.centerY) ** 2)))
            if testOpacity > 100:
                testOpacity = 100
            illusion.opacity = testOpacity

            testOpacity = rounded(math.sqrt(((clone.centerX - p1.centerX) ** 2) + ((clone.centerY - p1.centerY) ** 2)))
            if testOpacity > 100:
                testOpacity = 100
            clone.opacity = testOpacity

            if difficulty == 3:
                testOpacity = rounded(
                    math.sqrt(((illusion2.centerX - p1.centerX) ** 2) + ((illusion2.centerY - p1.centerY) ** 2)))
                if testOpacity > 100:
                    testOpacity = 100
                illusion2.opacity = 100 - testOpacity

                testOpacity = rounded(
                    math.sqrt(((illusion3.centerX - p1.centerX) ** 2) + ((illusion3.centerY - p1.centerY) ** 2)))
                if testOpacity > 100:
                    testOpacity = 100
                illusion3.opacity = 100 - testOpacity

    los.x1 = p2.centerX
    los.y1 = p2.centerY
    los.x2 = p1.centerX
    los.y2 = p1.centerY
    sensing.centerX = p2.centerX
    sensing.centerY = p2.centerY

    if 'up' in keys or 'down' in keys or 'left' in keys or 'right' in keys or 'space' in keys:
        p2.facing = keys
        p2.opacity = 10
        if 'up' in keys:
            p2.centerY -= 5
            if maze.contains(p2.centerX, p2.top):
                p2.centerY += 4

        if 'down' in keys:
            p2.centerY += 5
            if maze.contains(p2.centerX, p2.bottom):
                p2.centerY -= 4

        if 'left' in keys:
            p2.centerX -= 5
            if maze.contains(p2.left, p2.centerY):
                p2.centerX += 4

        if 'right' in keys:
            p2.centerX += 5
            if maze.contains(p2.right, p2.centerY):
                p2.centerX -= 4

        if 'space' in keys and rounded(
                math.sqrt(((p2.centerX - p1.centerX) ** 2) + ((p2.centerY - p1.centerY) ** 2))) >= 405 - clock / 2:
            p2.timer = clock / 2
            cast.x1 = p2.centerX
            cast.y1 = p2.centerY
            cast.x2 = p1.centerX
            cast.y2 = p1.centerY
            p2.centerX = cast.centerX
            p2.centerY = cast.centerY
            cast.x2 = p2.centerX
            cast.y2 = p2.centerY
            cast.opacity = 76

    else:
        if difficulty != 1:
            testOpacity = rounded(math.sqrt(((p2.centerX - p1.centerX) ** 2) + ((p2.centerY - p1.centerY) ** 2)))
            if testOpacity > 100:
                testOpacity = 100
            p2.opacity = 100 - testOpacity
            illusion.opacity = p2.opacity
            clone.opacity = p2.opacity

        if difficulty == 1:
            illusion.visible == p2.visible
            clone.visible == p2.visible

        los.x1 = p2.centerX
        los.y1 = p2.centerY
        los.x2 = p1.centerX
        los.y2 = p1.centerY
        sensing.centerX = p2.centerX
        sensing.centerY = p2.centerY

        if not maze.hitsShape(los) and sensing.hitsShape(p1):  # if ghost is in range and can see the player
            p2.visible = True
            if p1.centerX < p2.centerX:
                p2.centerX -= 3 + (clock / 760)
                if maze.contains(p2.left, p2.centerY):
                    p2.centerX += 3 + (clock / 760)

            elif p1.centerX > p2.centerX:
                p2.centerX += 3 + (clock / 760)
                if maze.contains(p2.right, p2.centerY):
                    p2.centerX -= 3 + (clock / 760)

            if p1.centerY < p2.centerY:
                p2.centerY -= 3 + (clock / 760)
                if maze.contains(p2.centerX, p2.top):
                    p2.centerY += 3 + (clock / 760)

            elif p1.centerY > p2.centerY:
                p2.centerY += 3 + (clock / 760)
                if maze.contains(p2.centerX, p2.bottom):
                    p2.centerY -= 3 + (clock / 760)

            p2.timer = 0

        elif not maze.hitsShape(los):  # if ghost can see player
            p2.visible = True

            if p1.centerX < p2.centerX:
                p2.centerX -= 2 + (clock / 760)
                if maze.contains(p2.left, p2.centerY):
                    p2.centerX += 2 + (clock / 760)

            elif p1.centerX > p2.centerX:
                p2.centerX += 2 + (clock / 760)
                if maze.contains(p2.right, p2.centerY):
                    p2.centerX -= 2 + (clock / 760)

            if p1.centerY < p2.centerY:
                p2.centerY -= 2 + (clock / 760)
                if maze.contains(p2.centerX, p2.top):
                    p2.centerY += 2 + (clock / 760)

            elif p1.centerY > p2.centerY:
                p2.centerY += 2 + (clock / 760)
                if maze.contains(p2.centerX, p2.bottom):
                    p2.centerY -= 2 + (clock / 760)

            p2.timer = 0

        elif sensing.hitsShape(p1):  # if the ghost senses the player through a wall
            p2.timer += 1
            p2.visible = False

            if p1.centerX < p2.centerX:
                p2.centerX -= 1 + (clock / 760)
            elif p1.centerX > p2.centerX:
                p2.centerX += 1 + (clock / 760)
            if p1.centerY < p2.centerY:
                p2.centerY -= 1 + (clock / 760)
            elif p1.centerY > p2.centerY:
                p2.centerY += 1 + (clock / 760)

        elif p2.roaming == True:  # if the ghost starts to roam
            p2.visible = False
            p2.timer += 2

            if p1.centerX < p2.centerX:
                p2.centerX -= 1 + (clock / 760)
            elif p1.centerX > p2.centerX:
                p2.centerX += 1 + (clock / 760)
            if p1.centerY < p2.centerY:
                p2.centerY -= 1 + (clock / 760)
            elif p1.centerY > p2.centerY:
                p2.centerY += 1 + (clock / 760)

        else:
            p2.timer += 1
            p2.visible = False

            if p2.timer >= 50:
                p2.roaming = True

        if rounded(math.sqrt(((p2.centerX - p1.centerX) ** 2) + ((p2.centerY - p1.centerY) ** 2))) >= 395 - clock / 2:
            p2.timer = clock / 2
            cast.x1 = p2.centerX
            cast.y1 = p2.centerY
            cast.x2 = p1.centerX
            cast.y2 = p1.centerY
            p2.centerX = cast.centerX
            p2.centerY = cast.centerY
            cast.x2 = p2.centerX
            cast.y2 = p2.centerY
            cast.opacity = 76

    if clone.visible == True:
        if clone.hitsShape(p1) or clone.hitsShape(p2):
            clone.visible = False
        if p1.centerX < clone.centerX:
            clone.centerX -= 4
        elif p1.centerX > clone.centerX:
            clone.centerX += 4
        if p1.centerY < clone.centerY:
            clone.centerY -= 4
        elif p1.centerY > clone.centerY:
            clone.centerY += 4

    if clock >= 360 and clone.visible == False:
        destX = p1.centerX
        destY = p1.centerY

        if 'w' in keys:
            destY -= 100
        if 's' in keys:
            destY += 100
        if 'a' in keys:
            destX -= 100
        if 'd' in keys:
            destX += 100

        clone.centerX = destX + randrange(-10, 11)
        clone.centerY = destY + randrange(-10, 11)
        clone.visible = True

    if clock > 360:
        orbitor.centerX = p1.centerX
        orbitor.centerY = p1.centerY
        orbitor.rotateAngle += 6
        illusion.centerX = orbitor.x2
        illusion.centerY = orbitor.y2
        illusion.visible = True

        if difficulty == 3:
            orbitor2.centerX = p2.centerX
            orbitor2.centerY = p2.centerY
            orbitor2.rotateAngle -= 6
            illusion2.centerX = orbitor2.x2
            illusion2.centerY = orbitor2.y2
            illusion2.visible = True

            orbitor3.centerX = clone.centerX
            orbitor3.centerY = clone.centerY
            orbitor3.rotateAngle -= 6
            illusion3.centerX = orbitor3.x2
            illusion3.centerY = orbitor3.y2
            illusion3.visible = True

    if cast.opacity >= 3:
        cast.opacity -= 3

    if difficulty != 3:
        if 'w' in keys:
            p1.centerY -= 5
        if maze.contains(p1.centerX, p1.top):
            p1.centerY += 5

        if 's' in keys:
            p1.centerY += 5
        if maze.contains(p1.centerX, p1.bottom):
            p1.centerY -= 5

        if 'a' in keys:
            p1.centerX -= 5
        if maze.contains(p1.left, p1.centerY):
            p1.centerX += 5

        if 'd' in keys:
            p1.centerX += 5
        if maze.contains(p1.right, p1.centerY):
            p1.centerX -= 5

    elif difficulty == 2:
        if 'w' in keys:
            p1.centerY -= 4.5
        if maze.contains(p1.centerX, p1.top):
            p1.centerY += 4.5

        if 's' in keys:
            p1.centerY += 4.5
        if maze.contains(p1.centerX, p1.bottom):
            p1.centerY -= 4.5

        if 'a' in keys:
            p1.centerX -= 4.5
        if maze.contains(p1.left, p1.centerY):
            p1.centerX += 4.5

        if 'd' in keys:
            p1.centerX += 4.5
        if maze.contains(p1.right, p1.centerY):
            p1.centerX -= 4.5

    else:
        if 'w' in keys:
            p1.centerY -= 5.5
        if maze.contains(p1.centerX, p1.top):
            p1.centerY += 5.5

        if 's' in keys:
            p1.centerY += 5.5
        if maze.contains(p1.centerX, p1.bottom):
            p1.centerY -= 5.5

        if 'a' in keys:
            p1.centerX -= 5.5
        if maze.contains(p1.left, p1.centerY):
            p1.centerX += 5.5

        if 'd' in keys:
            p1.centerX += 5.5
        if maze.contains(p1.right, p1.centerY):
            p1.centerX -= 5.5

    color = rounded(math.sqrt(((p2.centerX - p1.centerX) ** 2) + ((p2.centerY - p1.centerY) ** 2))) / 2

    if color > 255:
        color = 255

    orb.fill = rgb(rounded(255 - color), 50, 50)
    orb.opacity = (255 - color) / 4

    if flash.opacity > 0:
        flash.opacity -= 2

    clock += 0.5

    maze.children[1].rotateAngle = clock
    maze.children[2].centerX = maze.children[1].x1
    maze.children[2].centerY = maze.children[1].y1
    maze.children[3].centerX = maze.children[1].x2
    maze.children[3].centerY = maze.children[1].y2
    mazeCover.children[2].centerX = maze.children[1].x1
    mazeCover.children[2].centerY = maze.children[1].y1
    mazeCover.children[3].centerX = maze.children[1].x2
    mazeCover.children[3].centerY = maze.children[1].y2
    mazeCover.children[0].rotateAngle = clock

    if clock == 30:
        runes.add(
            Label('I', maze.children[1].x1, maze.children[1].y1, font='orbitron', size=20, fill='grey', bold=True))
    elif clock == 60:
        runes.add(
            Label('II', maze.children[1].x1, maze.children[1].y1, font='orbitron', size=20, fill='grey', bold=True))
    elif clock == 90:
        runes.add(
            Label('III', maze.children[1].x1, maze.children[1].y1, font='orbitron', size=20, fill='grey', bold=True))
    elif clock == 120:
        runes.add(
            Label('IV', maze.children[1].x1, maze.children[1].y1, font='orbitron', size=20, fill='grey', bold=True))
    elif clock == 150:
        runes.add(
            Label('V', maze.children[1].x1, maze.children[1].y1, font='orbitron', size=20, fill='grey', bold=True))
    elif clock == 180:
        runes.add(
            Label('VI', maze.children[1].x1, maze.children[1].y1, font='orbitron', size=20, fill='grey', bold=True))
    elif clock == 210:
        runes.add(
            Label('VII', maze.children[1].x1, maze.children[1].y1, font='orbitron', size=20, fill='grey', bold=True))
    elif clock == 240:
        runes.add(
            Label('VIII', maze.children[1].x1, maze.children[1].y1, font='orbitron', size=20, fill='grey', bold=True))
    elif clock == 270:
        runes.add(
            Label('IX', maze.children[1].x1, maze.children[1].y1, font='orbitron', size=20, fill='grey', bold=True))
    elif clock == 300:
        runes.add(
            Label('X', maze.children[1].x1, maze.children[1].y1, font='orbitron', size=20, fill='grey', bold=True))
    elif clock == 330:
        runes.add(
            Label('XI', maze.children[1].x1, maze.children[1].y1, font='orbitron', size=20, fill='grey', bold=True))
    elif clock == 360:
        runes.add(
            Label('XII', maze.children[1].x1, maze.children[1].y1, font='orbitron', size=20, fill='grey', bold=True))
        runes.fill = 'crimson'
        flash.opacity = 100
        app.background = 'thistle'
        maze.fill = 'violet'
        mazeCover.fill = 'plum'
    elif clock == 390:
        runes.children[0].bold = False
        runes.children[0].border = 'lightCyan'
    elif clock == 420:
        runes.children[1].bold = False
        runes.children[1].border = 'lightCyan'
    elif clock == 450:
        runes.children[2].bold = False
        runes.children[2].border = 'lightCyan'
    elif clock == 480:
        runes.children[3].bold = False
        runes.children[3].border = 'lightCyan'
    elif clock == 510:
        runes.children[4].bold = False
        runes.children[4].border = 'lightCyan'
    elif clock == 540:
        runes.children[5].bold = False
        runes.children[5].border = 'lightCyan'
    elif clock == 570:
        runes.children[6].bold = False
        runes.children[6].border = 'lightCyan'
    elif clock == 600:
        runes.children[7].bold = False
        runes.children[7].border = 'lightCyan'
    elif clock == 630:
        runes.children[8].bold = False
        runes.children[8].border = 'lightCyan'
    elif clock == 660:
        runes.children[9].bold = False
        runes.children[9].border = 'lightCyan'
    elif clock == 690:
        runes.children[10].bold = False
        runes.children[10].border = 'lightCyan'
    elif clock == 720:
        runes.children[11].bold = False
        runes.children[11].border = 'lightCyan'
        title.value = 'You win!'
        title.fill = 'paleGreen'
        Label('Ghost', p2.centerX, p2.centerY, size=15, fill='lightSalmon')
        Label('You', p1.centerX, p1.centerY, size=15, fill='paleGreen')
        illusion.visible = False
        clone.visible = False
        p2.opacity = 100

        while p2.opacity > 0:
            p2.opacity -= 10
            p2.radius += 10
            sleep(0)
        app.stop()

    if p2.hitsShape(p1) and title.value != 'You win!':
        illusion.visible = False
        clone.visible = False
        title.value = 'You were caught...'
        title.fill = 'lightSalmon'
        runes.fill = 'lightSalmon'
        p1.opacity = 100

        while p1.opacity > 0:
            p1.opacity -= 10
            p1.radius += 10
            sleep(0)
        app.stop()

    if clock >= 360:
        for i in range(len(runes)):
            if runes.children[i].bold == True:
                runes.children[i].border = rgb(randrange(175, 255), 100, 100)
                runes.children[i].fill = rgb(randrange(175, 255), 100, 100)

cmu_graphics.run()