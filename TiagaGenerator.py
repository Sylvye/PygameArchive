from cmu_graphics import *
from time import sleep

# initial setup
app.background = 'lightGrey'
app.setMaxShapeCount(10000)
path = Group()
mountain = Group()
soil = Group()
checks = Group()
trees = Group()
clouds = Group()
snow = Group()
pointsX = []
pointsY = []
treePointsX = []
treePointsY = []
rough = 1
points = 0


def addCheck(amount, debug):  # draw checkmark function
    if debug == True:
        for i in range(amount):
            checks.centerX += 15
            checks.add(Line(10, 15, 15, 20, fill='limeGreen', lineWidth=3))
            checks.add(Line(14, 19, 20, 5, fill='limeGreen', lineWidth=3))
            sleep(0)


def debugRender(debug):  # adds a delay if render is in debug mode
    if debug == True:
        sleep(0)


def generate(startX, startY, debug, roughness):  # core generation script
    ### setup
    direction = randrange(-1, 2)
    checks.clear()
    mountain.clear()
    soil.clear()
    path.clear()
    trees.clear()
    clouds.clear()
    snow.clear()
    global pointsX, pointsY
    pointX = startX
    pointY = startY
    prevPointX = pointX
    prevPointY = pointY

    if debug == True:
        length = 84

    else:
        length = 84

    for i in range(length):  # drawing top snow
        differY = randrange(-5, 0) * direction

        if direction >= -2 and direction <= 2:  # adds points on floor to list for tree generation
            treePointsX.append(pointX)
            treePointsY.append(pointY)

        direction = randrange(roughness * -1, roughness + 1)
        pointX += 5
        pointY += differY

        if pointY <= 10:
            pointY = randrange(10, 15)

        path.add(Line(prevPointX, prevPointY, pointX, pointY, lineWidth=8, fill='white'))
        path.add(Circle(pointX, pointY, 4, fill='white'))
        path.add(Circle(pointX + 1, pointY + 50, 4, fill='sienna'))

        if rough >= 3:
            path.add(Line(prevPointX, prevPointY + 50, pointX, pointY + 50, lineWidth=8, fill='sienna'))

        debugRender(debug)
        pointsX.append(pointX)
        pointsY.append(pointY)
        prevPointX = pointX
        prevPointY = pointY

    addCheck(1, debug)

    while len(pointsX) > 0:  # drawing the soil
        if pointsY[0] >= 390:
            testedY = randrange(380, 390)

        else:
            testedY = pointsY[0]

        mountain.add(Rect(pointsX[0] - 4, pointsY[0], 5, 400 - testedY, fill='saddleBrown'))  # draws the lower soil
        debugRender(debug)

        if len(pointsY) > 1:  # draws soil
            soil.add(Rect(pointsX[0] + 4, pointsY[1], 5, 50, fill='sienna'))
            debugRender(debug)

        if direction >= -2 or direction <= 2:  # adding a flat tree generation location to a list
            treePointsX.append(pointsX[0])
            treePointsY.append(pointsY[0])

        pointsX.pop(0)
        pointsY.pop(0)
        debugRender(debug)

    addCheck(1, debug)
    drawX = 0

    while len(treePointsX) > 0:
        treeCooldown = 10

        if randrange(1,
                     treeCooldown + 10) == 1:  # randomness for tree gen (trees spawn more when they are further from each other)
            treeCooldown = 10  # V tree drawing
            trees.add(Line(treePointsX[0], treePointsY[0] - 3, treePointsX[0], treePointsY[0] - 20, lineWidth=5,
                           fill='saddleBrown'))
            trees.add(Polygon(treePointsX[0], treePointsY[0] - 25, treePointsX[0] - 8, treePointsY[0] - 10,
                              treePointsX[0] + 8, treePointsY[0] - 10, fill='darkGreen'))
            trees.add(Polygon(treePointsX[0], treePointsY[0] - 40, treePointsX[0] - 5, treePointsY[0] - 15,
                              treePointsX[0] + 5, treePointsY[0] - 15, fill='forestGreen'))
            trees.add(Polygon(treePointsX[0], treePointsY[0] - 30, treePointsX[0] - 7, treePointsY[0] - 18,
                              treePointsX[0] + 7, treePointsY[0] - 18, fill='white'))
            trees.add(Polygon(treePointsX[0], treePointsY[0] - 40, treePointsX[0] - 5, treePointsY[0] - 18,
                              treePointsX[0] + 5, treePointsY[0] - 18, fill='white'))

        else:  # tree fail condition
            treeCooldown -= 2

        treePointsX.pop(0)
        treePointsY.pop(0)
        debugRender(debug)

    soil.toFront()
    path.toFront()
    addCheck(1, debug)

    for i in range(15):  # cloud generation
        clouds.add(Circle(randrange(0, 400), randrange(0, 60), randrange(50, 60), fill='dimGrey', opacity=10))
        debugRender(debug)

    addCheck(1, debug)
    snowCount = 0

    for i in range(300):  # snow generation
        testX = randrange(0, 400)
        testY = randrange(0, 400)

        if path.hitTest(testX, testY) == None and mountain.hitTest(testX, testY) == None and trees.hitTest(testX,
                                                                                                           testY) == None:
            snow.add(Circle(testX, testY, 1, fill='white'))  # ^ snow collision test
            if snowCount >= 50:
                snowCount = 0
                debugRender(debug)
    addCheck(1, debug)
    clouds.toFront()


info = Label('[SPACE] Generate', 200, 190, )  # display info on startup
subInfo = Label('[D] Debug view', 200, 210)
roughnessInfoBox = Rect(140, 380, 120, 20, fill='dimGrey', opacity=75)
roughnessInfo = Label('[R] Roughness: 1', 200, 390, fill=rgb(15, 75, 7.5))
roughnessInfoBox.toFront()
roughnessInfo.toFront()


def onKeyHold(keys):  # user input
    global rough

    if 'space' in keys:  # basic mode
        info.visible = False
        subInfo.visible = False
        generate(-10, 200, False, rough)

    if 'd' in keys:  # debug mode

        info.visible = False
        subInfo.visible = False
        generate(-10, 200, True, rough)
    roughnessInfoBox.toFront()
    roughnessInfo.toFront()


def onKeyPress(key):  # handles the roughness value changing on keyPress "r"
    global rough

    if key == 'r':
        if rough < 10:
            rough += 1

        else:
            rough = 1
            roughnessInfo.bold = False

    roughnessInfo.value = '[R] Roughness: ' + str(rough)  # changes the color and text of the roughness display
    roughnessInfo.fill = rgb(rounded(rough * 8), 40, rounded(rough * 3))

    if rough == 10:  # makes roughness display bold if roughness is 10
        roughnessInfo.bold = True

cmu_graphics.run()