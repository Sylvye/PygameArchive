from cmu_graphics import *

# defining variables & objects
app.background = gradient(rgb(50, 50, 100), rgb(75, 75, 125))

app.level = 1
app.totalLevels = 20

app.hardcore = False
app.impossible = True
app.start = False
app.steps = -1
app.levelSteps = -1
app.stepLimit = 200

impossibled = []
flawlessed = []

times = []

# HUD
hpBar = Rect(10, 10, 150, 15, fill=rgb(100, 255, 150))
hpbarUnderside = Rect(10, 10, 150, 15, fill=rgb(255, 205, 205))
ebarUnderside = Rect(240, 10, 150, 15, fill=rgb(225, 225, 255))
energyBar = Rect(240, 10, 150, 15, fill=rgb(215, 150, 255))
timerUnderside = Rect(170, 12.5, 60, 10, fill=rgb(185, 195, 215))
timer = Rect(170, 12.5, 60, 10, fill=rgb(155, 255, 235), opacity=100)

hazards = Group()
fadeHazards = Group()
fade = Group()

player = Group(Circle(200, 200, 8, fill='lightSteelBlue'), Circle(197, 197, 2.5), Circle(203, 197, 2.5))
player.vx = 0
player.vy = 0
player.energy = 100
player.cooldown = 0
player.hp = 5
player.speed = 0.75

bars = Group(
    hpbarUnderside,
    ebarUnderside,
    timerUnderside,
    hpBar,
    energyBar,
    timer
)

fadeBar = Group()

hardcoreLabel = Label('HARDCORE', 85, 17, fill='crimson', bold=True, visible=False, font='montserrat')
easyLabel = Label('Easy mode', 315, 17, fill='lime', size=20, bold=True, visible=False, font='montserrat')

info = Group(
    Label('Press ENTER to start', 200, 150, font='montserrat', bold=True, fill='lemonChiffon', size=20),
    Label('Press SPACE for help', 200, 250, font='montserrat', bold=True, fill='lemonChiffon', size=20)
)

# help overlay
help = Group(Rect(0, 0, 400, 400, fill=gradient(rgb(50, 50, 100), rgb(75, 75, 125))), )

for y in range(0, 401, 100):
    for x in range(0, 401, 100):
        help.add(Circle(x, y, 100, opacity=10))

help.add(
    # bars
    Rect(10, 30, 150, 15, fill=rgb(100, 255, 150)),
    Rect(240, 30, 150, 15, fill=rgb(215, 150, 255)),
    Rect(170, 32.5, 60, 10, fill=rgb(155, 255, 235)),
    # bar labels
    Label('Health bar', 80, 20, fill='lemonChiffon', font='montserrat', bold=True),
    Label('Energy bar', 320, 20, fill='lemonChiffon', font='montserrat', bold=True),
    Label('[H] toggles hardcore', 80, 55, fill='lemonChiffon', font='montserrat', bold=True),
    Label('[I] toggles easy mode', 320, 55, fill='lemonChiffon', font='montserrat', bold=True),
    Label('Timer', 200, 20, fill='lemonChiffon', font='montserrat', bold=True),
    # keybind exhibit
    Line(200, 220, 300, 220, fill=rgb(255, 200, 250), lineWidth=8, opacity=50),
    Circle(300, 220, 8, fill='lightSteelBlue'),
    Circle(303, 223, 2.5),
    Circle(303, 217, 2.5),
    Label('Arrow keys or ASWD to move', 250, 195, fill='lemonChiffon', font='montserrat', bold=True),
    Label('[SPACE] performs a dash', 250, 240, fill='lemonChiffon', font='montserrat', bold=True),
    Label('G = framerate', 250, 175, fill='lemonChiffon', font='montserrat', bold=True),
    Label('J = abandon run', 250, 155, fill='lemonChiffon', font='montserrat', bold=True),
    Label('L = skip to level', 250, 135, fill='lemonChiffon', font='montserrat', bold=True),
    Label('R = reset level', 250, 115, fill='lemonChiffon', font='montserrat', bold=True),
    # dash exhibit
    Line(50, 350, 150, 350, fill=rgb(255, 200, 250), lineWidth=8, opacity=50),
    Circle(150, 350, 8, fill='lightSteelBlue'),
    Circle(153, 353, 2.5),
    Circle(153, 297 + 50, 2.5),
    Star(100, 350, 20, 12, fill=rgb(255, 100, 150), border=rgb(255 * 0.9, 100 * 0.9, 150 * 0.9)),
    Label('Dash through the hazards!', 100, 375, fill='lemonChiffon', font='montserrat', bold=True),
    # incoming attack exhibit
    Line(310, 410, 410, 310, fill=rgb(255, 100, 150), opacity=75, lineWidth=20),
    Circle(370, 350, 8, fill='lightSteelBlue'),
    Circle(367, 353, 2.5),
    Circle(367, 297 + 50, 2.5),
    Label('Avoid incoming danger!', 320, 375, fill='lemonChiffon', font='montserrat', bold=True),
    # hazard exhibi
    Circle(75, 150, 20, fill=rgb(255, 100, 150), border=rgb(255 * 0.9, 100 * 0.9, 150 * 0.9)),
    Star(125, 150, 20, 12, fill=rgb(255, 100, 150), border=rgb(255 * 0.9, 100 * 0.9, 150 * 0.9)),
    Rect(100, 190, 30, 30, align='center', fill=rgb(255, 100, 150), border=rgb(255 * 0.9, 100 * 0.9, 150 * 0.9)),
    Label('Avoid these hazards', 100, 120, fill='lemonChiffon', font='montserrat', bold=True),
    # about game exhibit
    Label('There are a total of 15 levels, increasing in difficulty', 200, 80, fill=rgb(255, 250, 150),
          font='montserrat', bold=True, size=13),
    Label('Beat all levels on Hardcore mode for a shiny reward', 200, 95, fill=rgb(255, 250, 150), font='montserrat',
          bold=True, size=13),
    # info
    Label('Press [ENTER] to start', 200, 280, fill='paleGreen', font='montserrat', bold=True, size=15),
    Label('Press anthing else to return', 200, 300, fill='paleGreen', font='montserrat', bold=True, size=15)
)

help.visible = False


# functions for spawning objects conveiniently
def spawnCircle(x, y, radius, life=10, vx=0, vy=0, homing=0):
    r = 255
    g = 100
    b = 150

    circle = Circle(x, y, radius, fill=rgb(r, g, b), border=rgb(r * 0.9, g * 0.9, b * 0.9), borderWidth=radius / 5)

    circle.vx = vx
    circle.vy = vy
    circle.slow = 1
    circle.life = life
    circle.homing = homing

    hazards.add(circle)


def spawnRect(x, y, width, life=10, vx=0, vy=0, homing=0):
    r = 255
    g = 100
    b = 150

    rect = Rect(x, y, width * 2, width * 2, fill=rgb(r, g, b), border=rgb(r * 0.9, g * 0.9, b * 0.9),
                borderWidth=width / 5, align='center')

    rect.vx = vx
    rect.vy = vy
    rect.slow = 1
    rect.life = life
    rect.homing = homing

    hazards.add(rect)


def spawnStar(x, y, radius, points, life=10, vx=0, vy=0, homing=0):
    r = 255
    g = 100
    b = 150

    star = Star(x, y, radius * 2, points, fill=rgb(r, g, b), border=rgb(r * 0.9, g * 0.9, b * 0.9),
                borderWidth=radius / 5)

    star.vx = vx
    star.vy = vy
    star.slow = 0.9
    star.life = life
    star.homing = homing

    hazards.add(star)


def spawnDrone(x, y, radius=10, speed=5, vx=0, vy=0, slow=1, life=80):
    r = 255
    g = 100
    b = 150

    drone = Circle(x, y, radius, fill=rgb(r, g, b), border=rgb(r * 0.9, g * 0.9, b * 0.9), borderWidth=radius / 5)

    drone.vx = vx
    drone.vy = vy
    drone.slow = slow
    drone.life = life
    drone.homing = speed

    hazards.add(drone)


def sweep(axis, velocity=5, width=10, life=40):
    if axis == 'y':
        rect = Rect(0 - width, 200, width, 400, align='center', fill=rgb(255, 100, 150),
                    border=rgb(255 * 0.9, 100 * 0.9, 150 * 0.9), borderWidth=width / 5)
        rect.vx = velocity
        rect.vy = 0
        rect.slow = 1
        rect.life = 160
        rect.homing = 0
        hazards.add(rect)
    elif axis == '-y':
        rect = Rect(400 + width, 200, width, 400, align='center', fill=rgb(255, 100, 150),
                    border=rgb(255 * 0.9, 100 * 0.9, 150 * 0.9), borderWidth=width / 5)
        rect.vx = velocity * -1
        rect.vy = 0
        rect.slow = 1
        rect.life = 160
        rect.homing = 0
        hazards.add(rect)
    elif axis == 'x':
        rect = Rect(200, 0 - width, 400, width, align='center', fill=rgb(255, 100, 150),
                    border=rgb(255 * 0.9, 100 * 0.9, 150 * 0.9), borderWidth=width / 5)
        rect.vx = 0
        rect.vy = velocity
        rect.slow = 1
        rect.life = 160
        rect.homing = 0
        hazards.add(rect)
    elif axis == '-x':
        rect = Rect(200, 400 + width, 400, width, align='center', fill=rgb(255, 100, 150),
                    border=rgb(255 * 0.9, 100 * 0.9, 150 * 0.9), borderWidth=width / 5)
        rect.vx = 0
        rect.vy = velocity * -1
        rect.slow = 1
        rect.life = 160
        rect.homing = 0
        hazards.add(rect)


def toss(axis, velocity=20, density=20, life=50):
    if axis == '-x':
        velocity *= -1
        for x in range(density, 401 - density, density * 2):
            spawnStar(x, 400 + x, density / 3, 10, life, 0, velocity - (x / 10))
    elif axis == 'x':
        for x in range(density, 401 - density, density * 2):
            spawnStar(x, 0 - x, density / 3, 10, life, 0, velocity + (x / 10))
    elif axis == '-y':
        velocity *= -1
        for y in range(density, 401 - density, density * 2):
            spawnStar(400 + y, y, density / 3, 10, life, velocity - (y / 10), 0)
    elif axis == 'y':
        for y in range(density, 401 - density, density * 2):
            spawnStar(0 - y, y, density / 3, 10, life, velocity + (y / 10), 0)


def sieve(axis, velocity=10, density=20, life=40):
    if axis == 'x':
        for x in range(density, 401 - density, density * 2):
            spawnRect(x, 0, density / 1.5, life, 0, velocity)
    elif axis == '-x':
        for x in range(density, 401 - density, density * 2):
            spawnRect(x, 400, density / 1.5, life, 0, -velocity)
    elif axis == 'y':
        for y in range(density, 401 - density, density * 2):
            spawnRect(0, y, density / 1.5, life, velocity, 0)
    elif axis == '-y':
        for y in range(density, 401 - density, density * 2):
            spawnRect(400, y, density / 1.5, life, -velocity, 0)


def shoot(x, y, radius=10, speed=3, life=50):
    ang = angleTo(x, y, player.centerX, player.centerY)
    destX, destY = getPointInDir(x, y, ang, speed)

    vx = destX - x
    vy = destY - y

    spawnCircle(x, y, radius, life, vx, vy)


def fire(x, y, ang, radius=10, speed=3, life=50):
    destX, destY = getPointInDir(x, y, ang, speed)

    vx = destX - x
    vy = destY - y

    spawnCircle(x, y, radius, life, vx, vy)


def smite(x, y, width=75, angle=0, delay=30, life=10):
    beam = Line(200, -400, 200, 800, fill=rgb(255, 100, 150), opacity=50, lineWidth=1)

    beam.centerX, beam.centerY = x, y
    beam.rotateAngle = angle
    beam.maxWidth = width
    beam.delay = delay
    beam.homing = 0
    beam.life = life

    fadeHazards.add(beam)


def drawLoseScreen():
    radius = 200
    points = 20
    roundness = 80
    r = 255
    g = 215
    b = 215
    while radius > 10:
        info.add(Star(200, 200, radius + 120, points, roundness=roundness, fill=rgb(r, g, b), rotateAngle=radius * 4))
        r -= 5
        g -= 15
        b -= 15
        radius *= 0.8
        points -= 1
        roundness *= 0.8


# resets level
def reset():
    player.hp = 5
    player.opacity = 51
    player.energy = 100
    player.centerX = 200
    player.centerY = 200
    player.vx = 0
    player.vy = 0
    fadeHazards.clear()
    hazards.clear()
    app.steps = 0
    app.stepLimit = 200
    if app.level == 20:
        app.stepLimit = 800
    info.clear()


# handles player inputs
def onKeyHold(keys):
    if app.start == True:
        # movement
        if 'w' in keys or 'up' in keys:
            player.vy -= player.speed

        if 's' in keys or 'down' in keys:
            player.vy += player.speed

        if 'a' in keys or 'left' in keys:
            player.vx -= player.speed

        if 'd' in keys or 'right' in keys:
            player.vx += player.speed

        # dash
        if 'space' in keys and player.cooldown == 0 and app.steps <= app.stepLimit and app.steps >= 10:
            if app.impossible == True:
                if player.energy >= 20:
                    player.cooldown = 10
                    player.energy -= 20

                    # gets point
                    bx, by = getPointInDir(player.centerX, player.centerY, player.direction, 100)

                    # prevents escaping borders
                    if bx > 400:
                        bx = 400
                    if bx < 0:
                        bx = 0
                    if by > 400:
                        by = 400
                    if by < 0:
                        by = 0

                    # draws line
                    fade.add(Line(player.centerX, player.centerY, bx, by, fill=rgb(255, 200, 215), lineWidth=8))

                    # draws fade effect
                    if app.impossible == True:
                        fadeBar.add(Rect(energyBar.right - 30, 10, 30, 15, fill=rgb(215, 215, 255)))

                    # sets player's new position
                    player.centerX = bx
                    player.centerY = by
                    player.vx *= 0.2
                    player.vy *= 0.2

            elif app.impossible == False:
                player.cooldown = 10

                # gets point
                bx, by = getPointInDir(player.centerX, player.centerY, player.direction, 100)

                # limits point to be within boundries
                if bx > 400:
                    bx = 400
                if bx < 0:
                    bx = 0
                if by > 400:
                    by = 400
                if by < 0:
                    by = 0

                # draws line
                fade.add(Line(player.centerX, player.centerY, bx, by, fill=rgb(255, 200, 215), lineWidth=8))

                # sets player's new position
                player.centerX = bx
                player.centerY = by
                player.vx *= 0.2
                player.vy *= 0.2


def onKeyPress(key):
    # start game
    if app.steps == -1:
        if key == 'enter':
            if app.start == False:
                app.start = True
                info.clear()
                help.clear()
        elif key == 'space':
            if help.visible == False:
                help.visible = True
            else:
                help.visible = False
        elif key == 'l':
            # adds your time to the timer list in the mm:ss format
            seconds = app.levelSteps // 30
            minutes = seconds // 60
            if minutes > 0:
                seconds //= 60
            if len(str(minutes)) < 2:
                minutes = '0' + str(minutes)
            if len(str(seconds)) < 2:
                seconds = '0' + str(seconds)
            times.append('Level ' + str(app.level) + ': ' + str(minutes) + ':' + str(seconds))

            level = app.getTextInput('What level would you like to skip to?')
            if level != "":
                app.start = True
                info.clear()
                help.clear()
            # removes selected strings from user input
            if 'level' in level:
                level = level.replace('level', '')
            if 'lvl' in level:
                level = level.replace('lvl', '')
            if ' ' in level:
                level = level.replace(' ', '')
            if level.isdigit():
                app.level = int(level)
                reset()
                app.levelSteps = 0
            else:
                fade.add(Rect(0, 0, 400, 400, fill='red'))
    else:
        # reset level
        if key == 'r':
            reset()
        # progress to next level
        elif key in ['enter', 'f'] and app.steps >= app.stepLimit:
            if app.level == app.totalLevels + 1:
                app.level = 1
                app.steps = -1
                app.levelSteps = -1
                bars.visible = True
                player.visible = True

                easyLabel.centerX, easyLabel.centerY = 315, 17
                easyLabel.fill = 'lime'
                easyLabel.visible = False
                hardcoreLabel.visible = False

                info.add(
                    Label('Insanity', 200, 80, font='montserrat', bold=True, fill='lime', size=30),
                    Label('(doing the same thing over and over and expecting different results)', 200, 110,
                          font='montserrat', bold=True, fill='paleGreen', size=10),
                    Label('Press ENTER to start', 200, 150, font='montserrat', bold=True, fill='lemonChiffon', size=20)
                )
            else:
                # adds your time to the timer list in the mm:ss format
                seconds = app.levelSteps // 30
                minutes = seconds // 60
                if minutes > 0:
                    seconds //= 60
                if len(str(minutes)) < 2:
                    minutes = '0' + str(minutes)
                if len(str(seconds)) < 2:
                    seconds = '0' + str(seconds)
                times.append('Level ' + str(app.level) + ': ' + str(minutes) + ':' + str(seconds))

                app.level += 1
                app.levelSteps = 0

            reset()
        # framerate limit
        elif key == 'g':
            try:
                app.stepsPerSecond = int(app.getTextInput('Enter framerate'))
            except:
                pass
        # skip to step:
        elif key == 'p':
            reset()
            app.steps = int(app.getTextInput('What step would you like to skip to?'))
    # hardcore toggle
    if key == 'h':
        if app.hardcore == False:
            app.hardcore = True
            hardcoreLabel.visible = True
            hpBar.fill = rgb(255, 200, 215)
        else:
            app.hardcore = False
            hardcoreLabel.visible = False
            hpBar.fill = rgb(100, 255, 150)

    # easy mode toggle
    elif key == 'i':
        if app.steps >= app.stepLimit or app.steps == -1:
            if app.impossible == False:
                app.impossible = True
                ebarUnderside.visible = True
                energyBar.visible = True
                easyLabel.visible = False
            else:
                app.impossible = False
                ebarUnderside.visible = False
                energyBar.visible = False
                easyLabel.visible = True

    # skip to level
    elif key == 'l' and app.steps >= app.stepLimit:
        # adds your time to the timer list in the mm:ss format
        seconds = app.levelSteps // 30
        minutes = seconds // 60
        if minutes > 0:
            seconds //= 60
        if len(str(minutes)) < 2:
            minutes = '0' + str(minutes)
        if len(str(seconds)) < 2:
            seconds = '0' + str(seconds)
        times.append('Level ' + str(app.level) + ': ' + str(minutes) + ':' + str(seconds))

        level = app.getTextInput('What level would you like to skip to?')
        # removes selected strings from user input
        if 'level' in level:
            level = level.replace('level', '')
        if 'lvl' in level:
            level = level.replace('lvl', '')
        if ' ' in level:
            level = level.replace(' ', '')
        if level.isdigit():
            app.level = int(level)
            reset()
            app.levelSteps = 0
        else:
            fade.add(Rect(0, 0, 400, 400, fill='red'))

    # forfeit level
    elif key == 'j' and app.steps != -1 and app.level <= app.totalLevels and app.steps < app.stepLimit:
        drawLoseScreen()
        info.add(Rect(200, 100, 200, 50, fill=rgb(150, 25, 25), align='center'))
        info.add(Circle(100, 100, 25, fill=rgb(150, 25, 25)))
        info.add(Circle(300, 100, 25, fill=rgb(150, 25, 25)))
        info.add(Rect(200, 310, 150, 50, fill=rgb(255, 150, 150), align='center'))
        info.add(Circle(125, 310, 25, fill=rgb(255, 150, 150)))
        info.add(Circle(275, 310, 25, fill=rgb(255, 150, 150)))
        info.add(Label('Abandoned', 200, 100, size=35, fill='crimson', bold=True, font='montserrat'))
        info.add(Label('Press ENTER/F to skip', 200, 320, fill='dimGray', bold=True, font='montserrat'))
        info.add(Label('Press R to replay', 200, 300, fill='dimGray', bold=True, font='montserrat'))
        # fades out any hazards on screen
        for i in hazards:
            fade.add(i)
            hazards.remove(i)
        app.steps = 201


# handles game running
def onStep():
    # run game when app.start == True
    if app.start == True:
        app.steps += 1
        app.levelSteps += 1

    # spawns hazards for designated (chunks of) levels
    if app.steps <= app.stepLimit:
        # levels divisioned into groups to reduce lag
        if app.level <= 5:
            if app.level == 1:
                if app.steps == 30:
                    sweep('-x', 5, 25)
                elif app.steps == 40:
                    sweep('x', 5, 25)
                elif app.steps == 60:
                    if app.impossible == True:
                        sweep('-x', 5, 25)
                elif app.steps == 120:
                    sweep('y', 8, 20)
                    sweep('-y', 8, 20)

            elif app.level == 2:
                if app.steps == 30:
                    toss('x', 20, 20, 40)
                elif app.steps == 40:
                    if app.impossible == True:
                        toss('-y', 20, 20, 40)
                elif app.steps == 50:
                    toss('-x', 20, 20, 40)
                elif app.steps == 60:
                    if app.impossible == True:
                        toss('y', 20, 20, 40)
                elif app.steps == 100:
                    sweep('-x', 5, 20, 80)
                    sweep('x', 5, 20, 80)

            elif app.level == 3:
                if app.steps == 30:
                    sweep('y', 2.5, 20)
                elif app.steps == 35:
                    shoot(200, 0, 5, 8, 100)
                    shoot(0, 200, 5, 8, 100)
                    shoot(400, 200, 5, 8, 100)
                    shoot(200, 400, 5, 8, 100)
                elif app.steps == 40:
                    if app.impossible == True:
                        shoot(0, 0, 5, 8, 100)
                        shoot(0, 400, 5, 8, 100)
                        shoot(400, 0, 5, 8, 100)
                        shoot(400, 400, 5, 8, 100)
                elif app.steps == 45:
                    shoot(200, 0, 5, 8, 100)
                    shoot(0, 200, 5, 8, 100)
                    shoot(400, 200, 5, 8, 100)
                    shoot(200, 400, 5, 8, 100)
                elif app.steps == 50:
                    if app.impossible == True:
                        shoot(0, 0, 5, 8, 100)
                        shoot(0, 400, 5, 8, 100)
                        shoot(400, 0, 5, 8, 100)
                        shoot(400, 400, 5, 8, 100)
                elif app.steps == 120:
                    if app.impossible == True:
                        sweep('y', 8, 20, 50)
                        sweep('-y', 8, 20, 50)
                    else:
                        sweep('y', 5, 20, 80)
                        sweep('-y', 5, 20, 80)

            elif app.level == 4:
                if app.impossible == True:
                    if app.steps == 30:
                        sweep('y', 4, 40)
                    elif app.steps == 50:
                        sweep('x', 4, 40)
                    elif app.steps == 70:
                        sweep('-y', 4, 40)
                    elif app.steps == 90:
                        sweep('-x', 4, 40)
                    elif app.steps == 110:
                        sweep('y', 4, 40)
                    elif app.steps == 130:
                        sweep('x', 4, 40)
                    elif app.steps == 150:
                        sweep('-y', 4, 40)
                else:
                    if app.steps == 30:
                        sieve('y', 4, 40, 150)
                    elif app.steps == 50:
                        sieve('x', 4, 40, 150)
                    elif app.steps == 70:
                        sieve('-y', 4, 40, 130)
                    elif app.steps == 90:
                        sieve('-x', 4, 40, 110)

            elif app.level == 5:
                if app.steps == 30:
                    spawnRect(200, -200, 100, 100, 0, 12)
                elif app.steps == 40:
                    circle = Circle(600, 600, 200, fill=None, border=rgb(255, 100, 150), borderWidth=5)
                    circle.vx = -5
                    circle.vy = -5
                    circle.slow = 1
                    circle.life = 150
                    circle.homing = 0
                    hazards.add(circle)
                elif app.steps == 50:
                    circle = Circle(-200, 600, 200, fill=None, border=rgb(255, 100, 150), borderWidth=5)
                    circle.vx = 5
                    circle.vy = -5
                    circle.slow = 1
                    circle.life = 150
                    circle.homing = 0
                    hazards.add(circle)
                elif app.steps == 75:
                    if app.impossible == True:
                        sweep('-y', 5, 20, 80)

        elif app.level <= 10:
            if app.level == 6:
                if app.steps == 30:
                    spawnStar(100, -100, 50, 8, 170, 0, 50)
                elif app.steps == 50:
                    if app.impossible == True:
                        spawnStar(300, 500, 50, 8, 150, 0, -50)
                elif app.steps == 70:
                    if app.impossible == True:
                        spawnStar(500, 100, 50, 8, 130, -50, 0)
                elif app.steps == 90:
                    if app.impossible == True:
                        spawnStar(-100, 300, 50, 8, 110, 50)
                    else:
                        spawnStar(300, 500, 50, 8, 110, 0, -50)
                elif app.steps == 120:
                    sweep('y', 10, 25)
                elif app.steps == 150:
                    sweep('-y', 10, 25)

            elif app.level == 7:
                if app.steps == 10:
                    if app.impossible == True:
                        toss('y', 5, 40, 190)
                        toss('-y', 5, 40, 190)
                    else:
                        toss('y', 5, 15, 190)
                        toss('-y', 5, 15, 190)
                elif app.steps == 40:
                    spawnStar(200, 600, 90, 12, 50, 0, -90)
                elif app.steps == 100:
                    spawnStar(200, -200, 90, 12, 50, 0, 90)
                elif app.steps == 130:
                    if app.impossible == True:
                        sweep('x', 10, 20, 40)
                elif app.steps == 150:
                    sweep('y', 10, 18, 50)
                    sweep('-y', 10, 18, 50)

            elif app.level == 8:
                if app.steps >= 30 and app.steps < 200 and app.steps % 10 == 0 and app.impossible == True:
                    shoot(200, 150, 5, 8, 50)
                    shoot(150, 250, 5, 8, 50)
                    shoot(250, 250, 5, 8, 50)
                if app.steps == 1 and app.impossible == True:
                    spawnCircle(200, 150, 10, 200)
                    spawnCircle(145, 250, 10, 200)
                    spawnCircle(255, 250, 10, 200)
                elif app.steps == 30:
                    circle = Circle(200, 600, 200, fill=None, border=rgb(255, 100, 150), borderWidth=10)
                    circle.vx = 0
                    circle.vy = -10
                    circle.slow = 1
                    circle.life = 75
                    circle.homing = 0
                    hazards.add(circle)
                elif app.steps == 80:
                    circle = Circle(200, -200, 200, fill=None, border=rgb(255, 100, 150), borderWidth=10)
                    circle.vx = 0
                    circle.vy = 10
                    circle.slow = 1
                    circle.life = 75
                    circle.homing = 0
                    hazards.add(circle)
                elif app.steps == 120:
                    circle = Circle(200, 600, 200, fill=None, border=rgb(255, 100, 150), borderWidth=10)
                    circle.vx = 0
                    circle.vy = -10
                    circle.slow = 1
                    circle.life = 75
                    circle.homing = 0
                    hazards.add(circle)

            elif app.level == 9:
                if app.steps == 1:
                    if app.impossible == True:
                        circle = Circle(200, 200, 100, fill=None, border=rgb(255, 100, 150), borderWidth=50)
                        circle.vx = 0
                        circle.vy = 0
                        circle.slow = 1
                        circle.life = 199
                        circle.homing = 0
                        hazards.add(circle)

                    circle = Circle(200, 200, 300, fill=None, border=rgb(255, 100, 150), borderWidth=100)
                    circle.vx = 0
                    circle.vy = 0
                    circle.slow = 1
                    circle.life = 199
                    circle.homing = 0
                    hazards.add(circle)
                elif app.steps == 20:
                    if app.impossible == True:
                        toss('y', 4, 50, 180)
                        toss('-y', 4, 50, 180)
                elif app.steps == 30:
                    circle = Circle(200, -150, 150, fill=None, border=rgb(255, 100, 150), borderWidth=5)
                    circle.vx = 0
                    circle.vy = 10
                    circle.slow = 1
                    circle.life = 100
                    circle.homing = 0
                    hazards.add(circle)
                elif app.steps == 100:
                    if app.impossible == True:
                        toss('x', 4, 50, 100)
                        toss('-x', 4, 50, 100)
                elif app.steps == 120:
                    sweep('y', 10, 20)
                elif app.steps == 140:
                    sweep('-y', 10, 20)

            elif app.level == 10:
                if app.impossible == True:
                    if app.steps >= 10 and app.steps < 200:
                        if app.steps % 20 == 0:
                            spawnRect(app.steps * 2, -40, 30, 60, 0, 8)
                        if app.steps % 20 == 0:
                            spawnRect(400 - app.steps * 2, 440, 30, 60, 0, -8)
                        if app.steps % 40 == 0:
                            sweep('y', 10, 20)
                else:
                    if app.steps >= 10 and app.steps < 200:
                        if app.steps % 30 == 0:
                            spawnRect(app.steps * 2, -40, 30, 60, 0, 8)
                        if app.steps % 30 == 0:
                            spawnRect(400 - app.steps * 2, 440, 30, 60, 0, -8)
                        if app.steps % 50 == 0:
                            sweep('y', 10, 20)

        elif app.level <= 15:
            if app.level == 11:
                if app.steps == 20:
                    sweep('y', 5, 20)
                elif app.steps == 40:
                    smite(player.centerX, 200, 75, 0, 10)
                elif app.steps == 60:
                    smite(player.centerX, 200, 75, 0, 10)
                    if app.impossible == True:
                        sweep('-y', 5, 20)
                elif app.steps == 80:
                    smite(player.centerX - 75, 200, 100, 0, 15)
                    smite(player.centerX + 75, 200, 100, 0, 15)
                elif app.steps == 100:
                    fire(50, -50, 180, 40, 8, 60)
                    fire(150, 450, 0, 40, 8, 60)
                    fire(250, -50, 180, 40, 8, 60)
                    fire(350, 450, 0, 40, 8, 60)
                elif app.steps == 140:
                    toss('-y', 15, 20, 60)
                    toss('y', 15, 20, 60)

            elif app.level == 12:
                if app.steps == 20:
                    smite(200, 200, 30, 45)
                    smite(100, 300, 30, 125)
                    smite(300, 150, 30, 225)
                    smite(400, 100, 30, 90)
                    smite(375, 325, 30, 110)
                elif app.steps == 30:
                    if app.impossible == True:
                        smite(100, 400, 30, 315)
                        smite(150, 250, 30, 90)
                        smite(200, 150, 30, 225)
                        smite(300, 100, 30, 315)
                        smite(50, 125, 30, 315)
                elif app.steps == 40:
                    smite(350, 150, 30, 240)
                    smite(200, 400, 30, 225)
                    smite(150, 250, 30, 80)
                    smite(250, 150, 30, 120)
                    smite(30, 150, 30, 70)
                    smite(360, 300, 30, 345)
                elif app.steps == 50:
                    if app.impossible == True:
                        smite(100, 100, 30, 135)
                        smite(150, 300, 30, 120)
                        smite(50, 300, 30, 50)
                        smite(200, 150, 30, 220)
                        smite(40, 175, 30, 20)
                        smite(340, 330, 30, 45)
                elif app.steps == 60:
                    smite(200, 200, 200, 0)
                elif app.steps == 100:
                    fire(200, 700, 0, 150, 10, 100)
                    circle = Circle(200, 700, 240, fill=None, border=rgb(255, 100, 150), borderWidth=10)
                    circle.vx = 0
                    circle.vy = -10
                    circle.slow = 1
                    circle.life = 100
                    circle.homing = 0
                    hazards.add(circle)

            elif app.level == 13:
                if app.steps <= 50:
                    if app.impossible == True:
                        if app.steps >= 20 and app.steps <= 40 and app.steps % 2 == 0:
                            smite((app.steps - 20) * 20, 200, 10, 0, 51 - app.steps)
                        if app.steps >= 30 and app.steps <= 50 and app.steps % 2 == 0:
                            smite(200, (app.steps - 30) * 20, 10, 90, 71 - app.steps)
                    else:
                        if app.steps >= 20 and app.steps <= 40 and app.steps % 4 == 0:
                            smite((app.steps - 20) * 20, 200, 10, 0, 51 - app.steps)
                        if app.steps >= 30 and app.steps <= 50 and app.steps % 4 == 0:
                            smite(200, (app.steps - 30) * 20, 20, 90, 71 - app.steps)
                elif app.steps == 80:
                    spawnStar(-100, -100, 50, 10, 120, 12, 12)
                    spawnStar(500, 500, 50, 10, 120, -12, -12)
                elif app.steps >= 80:
                    if app.impossible == True:
                        if app.steps % 40 == 0:
                            spawnDrone(20, 20, 10, 7, 0, 15, 0.8, 200 - app.steps + 1)
                            spawnDrone(380, 380, 10, 7, 0, 15, 0.8, 200 - app.steps + 1)
                    else:
                        if app.steps % 40 == 0:
                            spawnDrone(20, 20, 10, 6, 0, 15, 0.8, 200 - app.steps + 1)
                            spawnDrone(380, 380, 10, 6, 0, 15, 0.8, 200 - app.steps + 1)

            elif app.level == 14:
                if app.steps >= 30 and app.steps <= 50 and app.steps % 2 == 0:
                    if app.impossible == True:
                        smite((app.steps - 30) * 20, 200, 10, 0, 71 - app.steps)
                    else:
                        smite((app.steps - 30) * 20, 200, 10, 0, 81 - app.steps)
                if app.steps == 20:
                    if app.impossible == True:
                        for i in range(13):
                            fire(600 - (i * 32), 225 + (i * 32), 315, 20, 5, 130)
                    else:
                        for i in range(10):
                            fire(600 - (i * 64), 225 + (i * 64), 315, 20, 5, 130)
                elif app.steps == 80:
                    circle = Circle(300, -400, 200, fill=None, border=rgb(255, 100, 150), borderWidth=20)
                    circle.vx = -2
                    circle.vy = 10
                    circle.slow = 1
                    circle.life = 120
                    circle.homing = 0
                    hazards.add(circle)

                    if app.impossible == True:
                        sweep('-y', 10, 20)
                        sweep('y', 10, 20)

            elif app.level == 15:
                if app.steps >= 30 and app.steps <= 50 and app.steps % 4 == 0:
                    smite(200, (app.steps - 30) * 20, 40, 90, 71 - app.steps)
                if app.steps == 20:
                    if app.impossible == True:
                        spawnCircle(200, 550, 150, 180, 0, 0, 4)
                    else:
                        spawnCircle(200, 550, 140, 180, 0, 0, 3)
                elif app.steps == 100:
                    sweep('-x', 5, 20)

        elif app.level <= 20:
            if app.level == 16:
                interval = 5
                if not app.impossible:
                    interval = 8
                if app.steps % interval == 0:
                    if app.steps <= 50:
                        smite(200, (app.steps * 8), 10, 90, 40)
                    elif app.steps <= 100:
                        smite(200, (app.steps * -8) + 800, 10, 90, 40)
                    smite(player.centerX, player.centerY, 20, app.steps * (20 / 18), 20)

            elif app.level == 17:
                if app.steps == 1:
                    if app.impossible:
                        smite(100, 200, 70, 0, 40, 160)
                        smite(300, 200, 70, 0, 40, 160)
                    else:
                        smite(100, 200, 60, 0, 40, 160)
                        smite(300, 200, 60, 0, 40, 160)
                if app.steps == 50:
                    sweep('y', 10, 10, 40)
                if app.steps == 100:
                    if app.impossible:
                        circle = Circle(200, 600, 200, fill=None, border=rgb(255, 100, 150), borderWidth=70)
                    else:
                        circle = Circle(200, 600, 200, fill=None, border=rgb(255, 100, 150), borderWidth=50)
                    circle.vx = 0
                    circle.vy = -10
                    circle.slow = 1
                    circle.life = 150
                    circle.homing = 0
                    hazards.add(circle)

            elif app.level == 18:
                w = 15
                d = 25
                l = 20
                s = 1
                if (not app.impossible):
                    s = 1.5
                    l = 15
                if app.steps % (s * 10) == 0:
                    num = (app.steps * 400 / 360 / s) % 90
                    smite(0, 0, w, num - 90, d, l);
                    if app.steps >= 40:
                        smite(400, 0, w, num + 180, d, l);
                        if app.steps >= 80:
                            smite(0, 400, w, num, d, l);
                            if app.steps >= 120:
                                smite(400, 400, w, num + 90, d, l);

            # IN PROGRESS
            elif app.level == 19:
                if app.steps == 20:
                    smite(300, 100, 25, 0, 20, 100)
                    smite(300, 100, 25, 90, 20, 100)
                if app.steps == 25:
                    smite(200, 200, 25, 0, 20, 155)
                    smite(200, 200, 25, 90, 20, 155)
                if app.steps == 30:
                    smite(100, 300, 25, 0, 20, 90)
                    smite(100, 300, 25, 90, 20, 90)

                s = 0.7
                if not app.impossible:
                    s = 0.6
                if app.steps == 50:
                    sweep("y", 10 * s, 10, 40)
                if app.steps == 70:
                    sweep("-x", 10 * s, 10, 40)
                    if app.impossible:
                        smite(150, 150, 25, 0, 50, 80)
                        smite(150, 150, 25, 90, 50, 80)
                if app.steps == 90:
                    sweep("-y", 10 * s, 10, 40)
                if app.steps == 110:
                    sweep("x", 10 * s, 10, 40)
                    if app.impossible:
                        smite(250, 250, 25, 0, 50, 40)
                        smite(250, 250, 25, 90, 50, 40)
                if not app.impossible and app.steps >= 150 and app.steps % 10 == 0:
                    smite(player.centerX, 200, 20, 0, 20, 10)

            # final level, uses a step limit of 800, not 200
            elif app.level == 20:
                if app.impossible:
                    if app.steps < 200:
                        if app.steps == 1:
                            smite(300, 200, 200, 0, 50, 50)
                        if app.steps == 20:
                            spawnRect(50, 0, 60, 40, 0, 15)
                        if app.steps == 40:
                            spawnRect(150, 0, 60, 40, 0, 15)
                        if app.steps == 60:
                            spawnRect(50, 0, 60, 40, 0, 15)
                        if app.steps == 80:
                            spawnRect(150, 0, 60, 40, 0, 15)
                        if app.steps == 100:
                            spawnRect(250, 0, 60, 40, 0, 15)
                            smite(100, 200, 200, 0, 50, 50)
                        if app.steps == 120:
                            spawnRect(350, 0, 60, 40, 0, 15)
                        if app.steps == 140:
                            spawnRect(250, 0, 60, 40, 0, 15)
                        if app.steps == 160:
                            spawnRect(350, 0, 60, 40, 0, 15)
                    elif app.steps < 400:
                        if app.steps % 5 == 0 and app.steps >= 200 and app.steps <= 280:
                            smite(200, (app.steps - 200) * 8, 20, 90, 20, 5)
                        if app.steps % 20 == 0 and app.steps >= 300:
                            smite(player.centerX, 200, 50, 00, 10, 10)
                        if app.steps == 250:
                            smite(200, 350, 200, 90, 50, 100)
                            smite(200, 50, 200, 90, 50, 100)
                        if app.steps == 300:
                            sweep('y', 5, 10, 20)
                            sweep('-y', 5, 10, 20)
                    elif app.steps < 600:
                        if app.steps % 2 == 0 and app.steps > 420:
                            smite(player.centerX, player.centerY, 10, (app.steps - 400) * 200 / 45, 5, 5)
                    else:
                        if app.steps % 5 == 0:
                            smite(200, ((app.steps - 600) * 4) % 205, 20, 90, 30, 15)
                            smite(200, -1 * ((app.steps - 600) * 4 % 205) + 400, 20, 90, 30, 19)
                else:
                    if app.steps < 200:
                        if app.steps == 1:
                            smite(300, 200, 200, 0, 50, 50)
                        if app.steps == 20:
                            spawnRect(50, 0, 50, 40, 0, 15)
                        if app.steps == 40:
                            spawnRect(150, 0, 50, 40, 0, 15)
                        if app.steps == 60:
                            spawnRect(50, 0, 50, 40, 0, 15)
                        if app.steps == 80:
                            spawnRect(150, 0, 50, 40, 0, 15)
                        if app.steps == 100:
                            spawnRect(250, 0, 50, 40, 0, 15)
                            smite(100, 200, 200, 0, 50, 50)
                        if app.steps == 120:
                            spawnRect(350, 0, 50, 40, 0, 15)
                        if app.steps == 140:
                            spawnRect(250, 0, 50, 40, 0, 15)
                        if app.steps == 160:
                            spawnRect(350, 0, 50, 40, 0, 15)
                    elif app.steps < 400:
                        if app.steps % 5 == 0 and app.steps >= 200 and app.steps <= 280:
                            smite(200, (app.steps - 200) * 8, 20, 90, 20, 5)
                        if app.steps % 30 == 0 and app.steps >= 300:
                            smite(player.centerX, 200, 50, 00, 15, 10)
                        if app.steps == 250:
                            smite(200, 350, 200, 90, 50, 100)
                            smite(200, 50, 200, 90, 50, 100)
                        if app.steps == 300:
                            sweep('y', 5, 10, 20)
                            sweep('-y', 5, 10, 20)
                    elif app.steps < 600:
                        if app.steps % 5 == 0 and app.steps > 440:
                            smite(player.centerX, player.centerY, 10, (app.steps - 400) * 200 / 45, 10, 5)
                    else:
                        if app.steps % 10 == 0:
                            smite(200, ((app.steps - 600) * 4) % 205, 20, 90, 30, 15)
                            smite(200, -1 * ((app.steps - 600) * 4 % 205) + 400, 20, 90, 30, 19)
        # end screen
        elif app.level > app.totalLevels:
            info.clear()
            app.start = False
            app.steps = 200
            bars.visible = False
            player.visible = False
            info.add(Label("You've reached the end!", 200, 100, fill='lime', size=30, bold=True, font='montserrat'))
            x = 100
            y = 200
            for i in times:
                info.add(Label(i, x, y, font='montserrat', bold=True, fill=rgb(255, 255, 215)))
                y += 20
                if y >= 300:
                    y = 200
                    x += 100
            info.add(Label('Press ENTER/F to play again', 200, 350, fill='dimGray', bold=True, font='montserrat'))
            if [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] == flawlessed:
                # shiny title
                info.add(Rect(100, 150, 200, 40, fill=rgb(255, 255, 215)))
                info.add(Circle(100, 170, 20, fill=rgb(255, 255, 215)))
                info.add(Circle(300, 170, 20, fill=rgb(255, 255, 215)))
                info.add(Label('IMPECCABLE', 200, 169, fill='gold', bold=True, size=25, font='montserrat', italic=True))
                # gold stars
                info.add(Star(160, 70, 20, 5, fill='gold', border='goldenRod'))
                info.add(Star(240, 70, 20, 5, fill='gold', border='goldenRod'))
                info.add(Star(200, 60, 30, 5, fill='gold', border='goldenRod'))
            if [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] != impossibled:
                easyLabel.centerX, easyLabel.centerY = 200, 130
                easyLabel.visible = True
                easyLabel.fill = 'paleGreen'
                easyLabel.value = 'Easy mode / skipped'
            hardcoreLabel.visible = False
        # win/lose screen
        if app.steps == app.stepLimit and app.level <= app.totalLevels:
            # lose
            if player.hp > 0:
                info.add(Rect(200, 120, 320, 50, fill=rgb(200, 255, 150), align='center'))
                info.add(Circle(40, 120, 25, fill=rgb(200, 255, 150)))
                info.add(Circle(360, 120, 25, fill=rgb(200, 255, 150)))
                info.add(Rect(200, 310, 150, 50, fill=rgb(200, 255, 150), align='center'))
                info.add(Circle(125, 310, 25, fill=rgb(200, 255, 150)))
                info.add(Circle(275, 310, 25, fill=rgb(200, 255, 150)))
                info.add(Label('Level ' + str(app.level) + ' completed', 200, 120, fill='limeGreen', size=35, bold=True,
                               font='montserrat'))
                info.add(Label('Press ENTER/F to advance', 200, 320, fill='dimGray', bold=True, font='montserrat'))
            else:
                drawLoseScreen()
                info.add(Rect(200, 100, 100, 50, fill=rgb(150, 25, 25), align='center'))
                info.add(Circle(150, 100, 25, fill=rgb(150, 25, 25)))
                info.add(Circle(250, 100, 25, fill=rgb(150, 25, 25)))
                info.add(Rect(200, 310, 150, 50, fill=rgb(255, 150, 150), align='center'))
                info.add(Circle(125, 310, 25, fill=rgb(255, 150, 150)))
                info.add(Circle(275, 310, 25, fill=rgb(255, 150, 150)))
                info.add(Label('Fail...', 200, 100, fill='crimson', size=40, bold=True, font='montserrat'))
                info.add(Label('Press ENTER/F to skip', 200, 320, fill='dimGray', bold=True, font='montserrat'))
            info.add(Label('Press R to replay', 200, 300, fill='dimGray', bold=True, font='montserrat'))

            # win
            if player.hp == 5:
                info.add(Rect(200, 150, 100, 20, fill=rgb(255, 255, 180), align='center'))
                info.add(Circle(150, 150, 10, fill=rgb(255, 255, 180)))
                info.add(Circle(250, 150, 10, fill=rgb(255, 255, 180)))
                info.add(Label('FLAWLESS', 200, 150, fill='gold', bold=True, size=15, font='montserrat', italic=True))
                # gold stars
                info.add(Star(160, 75, 20, 5, fill='gold', border='goldenRod'))
                info.add(Star(240, 75, 20, 5, fill='gold', border='goldenRod'))
                info.add(Star(200, 65, 30, 5, fill='gold', border='goldenRod'))
                # adds level to the list of flawlessed levels
                if not app.level in flawlessed:
                    flawlessed.append(app.level)
            # silver stars
            elif player.hp == 4:
                info.add(Star(180, 80, 20, 5, fill='gainsBoro', border='silver'))
                info.add(Star(220, 80, 20, 5, fill='gainsBoro', border='silver'))
            # bronze star
            elif player.hp > 0:
                info.add(Star(200, 90, 20, 5, fill=rgb(205 * 1.15, 133 * 1.15, 63 * 1.15), border='peru'))
            # adds level to the list of levels beaten on impossible mode
            if app.impossible == True and not app.level in impossibled:
                impossibled.append(app.level)

    # regenerates energy
    if player.energy < 100 and app.steps <= app.stepLimit:
        player.energy += 0.2
    # dash cooldown
    if player.cooldown > 0:
        player.cooldown -= 1

    # update player location and applied forces
    player.direction = angleTo(player.centerX, player.centerY, player.centerX + player.vx, player.centerY + player.vy)
    player.rotateAngle = player.direction
    player.centerX += player.vx
    player.centerY += player.vy

    # friction
    player.vx *= 0.9
    player.vy *= 0.9

    # immunity frames
    if player.children[0].fill == rgb(255, 200, 200):
        player.children[0].fill = rgb(255, 225, 225)
    elif player.children[0].fill == rgb(255, 225, 225):
        player.children[0].fill = 'lightSteelBlue'

    # update energy bar
    if app.impossible == True:
        newWidth = player.energy * 1.5
        if newWidth <= 0:
            newWidth = 0.1
        energyBar.width = newWidth

    # update hp bar
    newWidth = player.hp * 30
    if newWidth <= 0:
        newWidth = 0.1
    hpBar.width = newWidth

    # update timer
    if app.steps <= app.stepLimit:
        newWidth = app.steps / app.stepLimit * 60
        if newWidth <= 0:
            newWidth = 0.1
        timer.width = newWidth

    # bounce on walls
    if player.left < 0:
        player.vx *= -1
        player.left = 0
    if player.right > 400:
        player.vx *= -1
        player.right = 400
    if player.top < 0:
        player.vy *= -1
        player.top = 0
    if player.bottom > 400:
        player.vy *= -1
        player.bottom = 400

    # fade in effect for player
    if player.opacity > 50 and player.opacity != 100:
        if player.opacity == 99:
            player.opacity += 1
        else:
            player.opacity += 3

    # fade effect for fade group
    for i in fade:
        i.opacity -= 10
        if i.opacity == 0:
            fade.remove(i)

    # fade effect for hp/energy bars
    for i in fadeBar:
        i.opacity -= 10
        if i.opacity == 0:
            fadeBar.remove(i)

    # fade effect for smite attack
    for i in fadeHazards:
        i.lineWidth += i.maxWidth / i.delay
        # detonates
        if i.lineWidth >= i.maxWidth:
            i.vx = 0
            i.vy = 0
            i.slow = 0
            i.opacity = 100
            hazards.add(i)
            fadeHazards.remove(i)

    # updates hazards
    for i in hazards:
        # guides homing hazards
        if i.homing != 0:
            ang = angleTo(i.centerX, i.centerY, player.centerX, player.centerY)
            i.centerX, i.centerY = getPointInDir(i.centerX, i.centerY, ang, i.homing)
        # other hazard movement
        i.centerX += i.vx
        i.centerY += i.vy
        i.vx *= i.slow
        i.vy *= i.slow
        i.life -= 1

        # removes timed out hazards
        if i.life == 0:
            hazards.remove(i)

    # handles player collision with hazards
    if player.hitsShape(hazards) and player.children[0].fill == 'lightSteelBlue' and app.steps < app.stepLimit:
        player.hp -= 1
        player.children[0].fill = rgb(255, 200, 200)

        # resets game and fades the shape that hit you
        if app.hardcore == True:
            for i in hazards:
                if i.hitsShape(player):
                    fade.add(i)
            # makes a fake player that fades out when you die
            fade.add(Circle(player.children[0].centerX, player.children[0].centerY, 8, fill='lightSteelBlue'))
            fade.add(Circle(player.children[1].centerX, player.children[1].centerY, 2.5))
            fade.add(Circle(player.children[2].centerX, player.children[2].centerY, 2.5))
            reset()
        # draws fade effect
        else:
            if player.hp >= 0:
                fadeBar.add(Rect(hpBar.right - 30, 10, 30, 15, fill=rgb(255, 100, 150)))

        # if you run out of hp, you turn transparent
        if player.hp <= 0:
            player.opacity = 50


cmu_graphics.run()

