from cmu_graphics import *
from time import sleep

### SETUP

app.background = rgb(100, 150, 255)
app.xOffset = 0
app.yOffset = 0
app.widthChange = 0
app.heightChange = 0

ocean = Rect(0, 0, 400, 400, fill=rgb(100, 150, 255))

beach = Group()
moderate = Rect(0, 0, 400, 400, fill=rgb(255, 255, 215))
cold = Group()
hot = Group()

temps = Group(moderate, cold, hot)

forests = Group()
mountains = Group()
jungle = Group()
plains = Group()

megabiome = Group(forests, mountains, jungle)

earth = Group(beach)

water = Group()
trees = Group()
rivers = Group()
rocks = Group()

landmarks = Group(rivers, water, rocks, trees)

seedValue = app.getTextInput('Enter an alphanumerical seed or leave blank')

loading = Group(
    Rect(0, 0, 400, 400, fill='white', opacity=50),
    Label('Generating seed: ', 200, 200, fill='black', bold=True, size=20),
    Label('test!', 200, 220, fill='lightGray', bold=True, size=15)
)

tempVis = Group()


### CODE

def chance(chance):
    chance = chance / 100
    rand = random()
    if rand <= chance:
        return True
    else:
        return False


def toggle(var):
    if var == False:
        var = True
    else:
        var = False
    return (var)


def scanTemp():
    tempVis.clear()
    x = 10
    y = 10
    for i in range(400):
        if hot.contains(x, y) and cold.contains(x, y):
            fill = 'lemonChiffon'
        elif hot.contains(x, y):
            fill = 'lightSalmon'
        elif cold.contains(x, y):
            fill = 'lightBlue'
        else:
            fill = 'lemonChiffon'
        tempVis.add(Rect(x, y, 20, 20, fill=fill, align='center', opacity=75))
        x += 20
        if x == 410:
            x = 10
            y += 20
    tempVis.toFront()


def drawTree(x, y):
    tree = Group()
    if (hot.contains(x, y) and cold.contains(x, y)) or (hot.contains(x, y) == False and cold.contains(x, y) == False):
        r = 75
        g = 175
        b = 75
    elif hot.contains(x, y):
        r = 25
        g = 155
        b = 25
    elif cold.contains(x, y):
        r = 115
        g = 200
        b = 115
        tree.add(Polygon(x, y - 21, x - 3, y - 11, x + 3, y - 11, fill=rgb(r, g, b)))

    tree.add(
        Line(x, y, x, y - 10, fill='sienna', lineWidth=3),
        Polygon(x, y - 15, x - 5, y - 5, x + 5, y - 5, fill=rgb(r, g, b))
    )
    tree.width += randrange(-1, 4)
    tree.height += randrange(-1, 3)
    trees.add(tree)


def drawEarth(x, y):
    if (hot.contains(x, y) and cold.contains(x, y)) or (hot.contains(x, y) == False and cold.contains(x, y) == False):
        earth.add(Circle(x, y, 100, fill=rgb(195, 255, 195)))
    elif hot.contains(x, y):
        earth.add(Circle(x, y, 100, fill=rgb(180, 255, 180)))
    elif cold.contains(x, y):
        earth.add(Circle(x, y, 100, fill=rgb(200, 255, 200)))
    if chance(80):
        drawWater(x + randrange(-50, 51), y + randrange(-50, 51))
    drawForest(x, y)


def drawForest(x, y):
    for i in range(randrange(12, 19)):
        dir = randrange(0, 360)
        ix, iy = getPointInDir(x, y, dir, randrange(5, 76))
        if landmarks.contains(ix, iy) == False and earth.contains(ix, iy):
            drawTree(ix, iy)


def drawMountain(x, y):
    rock = Group()
    rock.add(Polygon(x - randrange(3, 6), y, x, y - randrange(8, 11), x - randrange(-5, -2), y, fill='gray'))


def drawBeaches():
    for i in earth:
        i.landlocked = True
        for n in range(90):
            bx, by = getPointInDir(i.centerX, i.centerY, n * 4, 101)
            if earth.contains(bx, by) == False and earth.contains(bx, by) != 'Group()':
                beach.add(Circle(bx, by, 10, fill=rgb(255, 255, 225)))
                i.landlocked = False
    for i in beach:
        if ocean.contains(i.centerX, i.centerY) == False:
            beach.remove(i)


def drawHouse(x, y):
    house = Group()
    house.add(Rect(x, y, 10, 8, align='center', fill='peru'))
    house.add(Rect(x + 2, y + 1.5, 3, 5, align='center', fill='burlyWood'))
    house.add(Circle(x + 2.75, y + 1.25, 0.5, fill='gold'))
    roof = RegularPolygon(x, y - 4, 7, 3, fill='sienna')
    roof.width += 3
    roof.height -= 5
    house.add(roof)
    landmarks.add(house)


def drawRiver(x1, y1):
    d = randrange(0, 360)
    w = randrange(10, 21)
    river = Group()
    while earth.contains(x1, y1):
        x2, y2 = getPointInDir(x1, y1, d + randrange(-w, w + 1), 10)
        river.add(Line(x1, y1, x2, y2, fill='powderBlue', lineWidth=2))
        x1 = x2
        y1 = y2
        d += randrange(-w, w + 1)
    for i in river:
        if earth.contains(i.centerX, i.centerY) == False or water.containsShape(i):
            river.remove(i)

    rivers.add(river)


def drawWater(x, y):
    if y <= 100 or y >= 300:
        g = 215
    else:
        g = 235
    for i in range(randrange(1, 11)):
        x += randrange(-20, 20)
        y += randrange(-20, 20)
        water.add(Circle(x, y, randrange(18, 23), fill=rgb(200, g, 255)))
        if trees.hitsShape(water.children[len(water) - 1]) == True:
            water.remove(water.children[len(water) - 1])


def draw():
    loading.visible = True
    loading.children[2].value = 'drawing regions...'
    sleep(0)
    # DRAWS CLIMATE
    for i in range(10):
        cold.add(Circle(randrange(50, 351), randrange(50, 101), 75, fill=rgb(215, 215, 255)))
    for i in range(10):
        cold.add(Circle(randrange(50, 351), randrange(250, 401), 75, fill=rgb(215, 215, 255)))
    for i in range(12):
        hot.add(Circle(randrange(50, 351), randrange(200, 251), 75, fill=rgb(255, 215, 215)))
    loading.children[2].value = 'drawing lakes...'
    sleep(0)

    # DRAWING LAKES
    for i in range(randrange(0, 4)):
        drawWater(randrange(10, 391), randrange(10, 391))
    loading.children[2].value = 'drawing land...'
    sleep(0)

    # DRAWING land + forests
    # warm forests
    for i in hot:
        if chance(75):
            drawEarth(i.centerX + randrange(-50, 51), i.centerY + randrange(-50, 51))
    loading.children[2].value = 'drawing trees...'
    sleep(0)
    # cool forests
    for i in cold:
        if chance(25):
            drawEarth(i.centerX + randrange(-50, 51), i.centerY + randrange(-50, 51))
    loading.children[2].value = 'drawing rivers...'
    sleep(0)

    for i in water:
        # DRAWING RIVERS
        if chance(7.5):
            drawRiver(i.centerX, i.centerY)
    loading.children[2].value = 'purging inaccuracies...'
    sleep(0)
    for i in water:
        # clears lakes in the ocean
        if earth.contains(i.centerX, i.centerY) == False:
            water.remove(i)
    for i in trees:
        # clears trees touching rivers
        if rivers.hitsShape(i):
            trees.remove(i)

    loading.children[2].value = 'adjusting world border...'
    sleep(0)

    # adjusts world border to fit world
    ocean.width = earth.width + 10
    ocean.height = earth.height + 10
    ocean.centerX, ocean.centerY = earth.centerX, earth.centerY

    megabiome.visible = True
    temps.visible = False
    loading.visible = False
    loading.children[1].size = 20


def onKeyPress(key):
    if key in ['t', 'b']:
        app.group.width -= app.widthChange
        app.group.height -= app.heightChange
        app.group.centerX += app.xOffset
        app.group.centerY += app.yOffset
        app.widthChange = 0
        app.heightChange = 0
        app.xOffset = 0
        app.yOffset = 0
        if key == 't':
            if len(tempVis) == 0:
                scanTemp()
            else:
                tempVis.clear()
        if key == 'b':
            tempVis.clear()
            loading.visible = True
            loading.children[1].value = 'Generating beaches'
            loading.children[2].value = ''
            sleep(0)
            drawBeaches()
            loading.visible = False


def onKeyHold(keys):
    if 'w' in keys or 'up' in keys:
        app.group.centerY += 4
        app.yOffset -= 4
    if 's' in keys or 'down' in keys:
        app.group.centerY -= 4
        app.yOffset += 4
    if 'a' in keys or 'left' in keys:
        app.group.centerX += 4
        app.xOffset -= 4
    if 'd' in keys or 'right' in keys:
        app.group.centerX -= 4
        app.xOffset += 4
    if 'q' in keys or 'pageup' in keys:
        app.group.width -= 7.5
        app.group.height -= 7.5
        app.widthChange -= 7.5
        app.heightChange -= 7.5
    if 'e' in keys or 'pagedown' in keys:
        app.group.width += 7.5
        app.group.height += 7.5
        app.widthChange += 7.5
        app.heightChange += 7.5
    if 'i' in keys:
        app.group.centerY += 10
        temps.centerY += 10
        scanTemp()
    if 'k' in keys:
        app.group.centerY -= 10
        temps.centerY -= 10
        scanTemp()
    if 'j' in keys:
        app.group.centerX += 10
        temps.centerX += 10
        scanTemp()
    if 'l' in keys:
        app.group.centerX -= 10
        temps.centerX -= 10
        scanTemp()


def onMousePress(x, y):
    if water.contains(x, y):
        lake = water.hitTest(x, y)
        drawRiver(lake.centerX, lake.centerY)
    elif earth.contains(x, y):
        drawForest(x, y)


# allows user to change seed
if seedValue != '':
    seed(seedValue)
    loading.children[1].value += str(seedValue)
    while loading.children[1].left < 10 and loading.children[1].right > 390:
        loading.children[1].size -= 0.1
    print('World seed: ' + str(seedValue))
else:
    loading.children[1].value += 'Random seed'
draw()

cmu_graphics.run()