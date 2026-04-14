from cmu_graphics import *
from time import sleep
import math, random

app.background = rgb(255, 255, 120)
Rect(75, 50, 250, 300, fill=rgb(235, 195, 0), border=rgb(235 / 2, 195 / 2, 0), borderWidth=5)
Rect(100, 125 - 30, 200, 150, fill=gradient('white', 'white', 'grey', 'white', 'white', start='top'))
Rect(105, 280 - 30, 190, 75, opacity=15)
co1 = Rect(100, 125 - 30, 70, 150, fill=rgb(235, 195, 0))
co2 = Rect(165, 125 - 30, 70, 150, fill=rgb(235, 195, 0))
co3 = Rect(230, 125 - 30, 70, 150, fill=rgb(235, 195, 0))
c1 = Rect(100, 125 - 30, 70, 150, fill=None, border=rgb(235 / 2, 195 / 2, 0), borderWidth=5)
c2 = Rect(165, 125 - 30, 70, 150, fill=None, border=rgb(235 / 2, 195 / 2, 0), borderWidth=5)
c3 = Rect(230, 125 - 30, 70, 150, fill=None, border=rgb(235 / 2, 195 / 2, 0), borderWidth=5)
symL1 = Label('', c1.centerX, 210, fill=rgb(255, 215, 0), bold=True, font='montserrat')
symL2 = Label('', c2.centerX, 210, fill=rgb(255, 215, 0), bold=True, font='montserrat')
symL3 = Label('', c3.centerX, 210, fill=rgb(255, 215, 0), bold=True, font='montserrat')
coinBox = Rect(c2.centerX, 315, 20, 20, opacity=20, visible=False)
coinBox.centerX = c2.centerX
coinBox.centerY = c2.centerY
rolledList = []
app.spins = 0
app.sale = None
app.saleRarity = None
app.saleCost = 0
app.cd = 0

l1 = Label('', c1.centerX, 295 - 30, fill=rgb(255 * 0.95, 255 * 0.95, 200 * 0.95), bold=True, font='montserrat')
l2 = Label('Press SPACE to spin!', c2.centerX, 295 - 30, fill=rgb(255 * 0.95, 255 * 0.95, 200 * 0.95), bold=True,
           font='montserrat')
l3 = Label('', c3.centerX, 295 - 30, fill=rgb(255 * 0.95, 255 * 0.95, 200 * 0.95), bold=True, font='montserrat')
l4 = Label('', c2.centerX, 310, fill=rgb(255 * 0.95, 255 * 0.95, 200 * 0.95), bold=True, font='montserrat')
bl = Label('', c2.centerX, 315 - 30, fill=rgb(255 * 0.9, 255 * 0.9, 200 * 0.9), bold=True, font='montserrat')
row2 = Group(l4, bl)

rolled = Group()
syms = Group()
app.group.centerY = 212.
saleLabel = Label('', 45, 30, bold=True, font='montserrat')
saleInfo = Label('', 45, 50, bold=True, font='montserrat', fill='grey')
commons = ['Coin', 'Quartz']
uncommons = ['Star', 'Dice']
rares = ['Opal', 'Prisim']
epics = ['Mythril', 'Onyx']
fableds = ['Ether Orb', 'Inferno']
mythics = ['Nebula', 'Singularity']
worth = {'Empty': 0, 'Coin': 1, 'Quartz': 5, 'Star': 10, 'Dice': 0, 'Opal': 15,
         'Prisim': 5, 'Onyx': 30, 'Mythril': 60, 'Ether Orb': 50, 'Inferno': 200,
         'Nebula': 1000, 'Singularity': 0

         }

rarities = ['common', 'uncommon', 'rare', 'epic', 'fabled', 'mythic']
common = []
uncommon = []
rare = []
epic = []
fabled = []
mythic = []
ownedRarities = [common, uncommon, rare, epic, fabled, mythic]
owned = []
syms.visible = False
app.bonus = 1
app.bonusName = None
app.coins = 0
app.c1Mult = 1
app.c2Mult = 1
app.c3Mult = 1
app.spinsF = 0
app.mythicChance = 0

Rect(100, 92, 200, 45, fill=rgb(235, 195, 0), border=rgb(235 / 2, 195 / 2, 0), borderWidth=5)
Rect(100, 92, 200, 40, fill=rgb(235, 195, 0))

app.l1p = 0
app.l2p = 0
app.l3p = 0

Rect(0, 0, 400, 75, opacity=20)
sb = Rect(325, 40, 70, 30, opacity=20)
cb = Rect(325, 5, 70, 30, opacity=20)
ib = Rect(10, 10, 200, 55, opacity=20)
pb = Group(Rect(215, 10, 60, 55, opacity=20), Label('Spin?', 245, 27.5, font='montserrat', fill='orange', bold=True))
pb.visible = False
coinLabel = Label('Coins: 0', 0, 0, font='montserrat', fill=rgb(255, 215, 0), bold=True)
coinLabel.centerX = cb.centerX
coinLabel.centerY = cb.centerY
spinsLabel = Label('Spins: 0', 0, 0, font='montserrat', fill=rgb(255, 215, 0), bold=True)
spinsLabel.centerX = sb.centerX
spinsLabel.centerY = sb.centerY
symbol = Circle(0, 0, 1, fill=None)


def addSym(name, rarity, worth, amount, shapeType='circle', symRadius=15, symFill=rgb(255, 215, 0),
           symBorder=rgb(255 / 2, 215 / 2, 0), symPoints=None, symRotateAngle=0, symRoundness=50):
    for i in range(amount):
        if shapeType == 'circle':
            syms.add(Circle(0, 0, symRadius, fill=symFill, border=symBorder, borderWidth=3))
        elif shapeType == 'star':
            syms.add(
                Star(0, 0, symRadius, symPoints, fill=symFill, roundness=symRoundness, border=symBorder, borderWidth=3))
        elif shapeType == 'poly':
            syms.add(RegularPolygon(0, 0, symRadius, symPoints, fill=symFill, border=symBorder, borderWidth=3))
        if rarity == 'common':
            common.append(name)
        elif rarity == 'uncommon':
            uncommon.append(name)
        elif rarity == 'rare':
            rare.append(name)
        elif rarity == 'epic':
            epic.append(name)
        elif rarity == 'fabled':
            fabled.append(name)
        elif rarity == 'mythic':
            mythic.append(name)
        owned.append(name)
        syms.children[len(syms) - 1].rotateAngle = symRotateAngle
        syms.children[len(syms) - 1].rarity = rarity
        syms.children[len(syms) - 1].name = name
        syms.children[len(syms) - 1].worth = worth


def abrv(var, final=None, preffix=''):
    if final == None:
        final = var
    if len(str(math.floor(var))) in range(5, 7):
        final.value = preffix + str(math.floor((var / 1000) * 10) / 10) + 'k'
    elif len(str(math.floor(var))) in range(7, 10):
        final.value = preffix + str(math.floor((var / 1000000) * 10) / 10) + 'm'
    elif len(str(math.floor(var))) in range(10, 13):
        final.value = preffix + str(math.floor((var / 1000000000) * 10) / 10) + 'b'
    else:
        final.value = preffix + str(var)
    if '.0' in str(final.value):
        final.value = final.value.replace('.0', '')


def quickAdd(name, amount=1):
    if name == 'Empty':
        addSym('Empty', 'common', 0, amount, 'star', 20, 'red', rgb(255 / 2, 0, 0), 4, 45, 25)
    elif name == 'Coin':
        addSym('Coin', 'common', 1, amount)
    elif name == 'Quartz':
        addSym('Quartz', 'common', 5, amount, 'star', 15, rgb(230, 255, 230), rgb(200 / 2, 255 / 2, 200 / 2), 4, 0, 70)
    elif name == 'Star':
        addSym('Star', 'uncommon', 10, amount, 'star', 20, rgb(255, 215, 150), rgb(255 * 0.9, 215 * 0.9, 150 * 0.9), 4,
               0, 40)
    elif name == 'Dice':
        addSym('Dice', 'uncommon', 0, amount, 'poly', 20, rgb(255, 255, 255), rgb(255 * 0.9, 255 * 0.9, 255 * 0.9), 6,
               0)
    elif name == 'Opal':
        addSym('Opal', 'rare', 15, amount, 'circle', 20,
               gradient(rgb(255, 255, 255), rgb(255 - 50, 255, 255), rgb(255, 255 - 50, 255), rgb(255, 255, 255 - 50),
                        rgb(255, 255, 255)), rgb(255 * 0.9, 255 * 0.9, 255 * 0.9), 4, 45, 70)
    elif name == 'Prisim':
        addSym('Prisim', 'rare', 5, amount, 'poly', 20,
               gradient(rgb(255, 255 - 50, 255 - 50), rgb(255 - 50, 255, 255 - 50), rgb(255 - 50, 255 - 50, 255),
                        start='left'), rgb(255, 255, 255), 3, 45, 120)
    elif name == 'Onyx':
        addSym('Onyx', 'epic', 30, amount, 'poly', 20, gradient(rgb(50, 50, 150), rgb(50, 50, 50)), rgb(50, 50, 50), 5,
               180)
    elif name == 'Mythril':
        addSym('Mythril', 'epic', 60, amount, 'poly', 20, gradient(rgb(150, 235, 200), rgb(150, 255, 150)),
               rgb(255, 255, 255), 5, 30, 120)
    elif name == 'Ether Orb':
        addSym('Ether Orb', 'fabled', 50, amount, 'circle', 20, gradient(rgb(100, 250, 200), rgb(250, 50, 250)),
               rgb(250, 50, 250))
    elif name == 'Inferno':
        addSym('Inferno', 'fabled', 200, amount, 'star', 25, gradient(rgb(255, 215, 50), rgb(215, 255, 50)),
               rgb(255, 215, 50), 6, 30, 60)
    elif name == 'Nebula':
        addSym('Nebula', 'mythic', 1000, amount, 'star', 30,
               gradient(rgb(255, 150, 255), rgb(200, 215, 255), rgb(215, 255, 200)), None, 50, 0, 40)
    elif name == 'Singularity':
        addSym('Singularity', 'mythic', 0, amount, 'star', 20,
               gradient(rgb(255 / 4, 150 / 4, 255 / 4), rgb(200 / 4, 215 / 4, 255 / 4)), rgb(255 / 2, 215 / 2, 255 / 2),
               70, 0, 20)


quickAdd('Coin', 3)
quickAdd('Empty', 5)


###        rollin' (down in the deep)            ###

def draw(column, shapeType, symRadius, symFill, symBorder, symPoints=0, symRotateAngle=0, symRoundness=0):
    if shapeType == 'circle':
        rolled.add(Circle(0, 0, symRadius, fill=symFill, border=symBorder, borderWidth=3))
    elif shapeType == 'star':
        rolled.add(
            Star(0, 0, symRadius, symPoints, fill=symFill, roundness=symRoundness, border=symBorder, borderWidth=3))
    elif shapeType == 'poly':
        rolled.add(RegularPolygon(0, 0, symRadius, symPoints, fill=symFill, border=symBorder, borderWidth=3))
    rolled.children[len(rolled) - 1].rotateAngle = symRotateAngle
    rolled.children[len(rolled) - 1].centerX = column.centerX
    rolled.children[len(rolled) - 1].centerY = column.centerY


def slot(name, column, columnOverlay, bias=None):
    if name == 'Empty':
        draw(column, 'star', 20, 'red', rgb(255 / 2, 0, 0), 4, 45, 25)
    elif name == 'Coin':
        draw(column, 'circle', 15, rgb(255, 215, 0), rgb(255 / 2, 215 / 2, 0 / 2))
    elif name == 'Quartz':
        draw(column, 'star', 15, rgb(230, 255, 230), rgb(200 / 2, 255 / 2, 200 / 2), 4, 0, 70)
    elif name == 'Star':
        draw(column, 'star', 20, rgb(255, 215, 150), rgb(255 * 0.9, 215 * 0.9, 150 * 0.9), 4, 0, 40)
    elif name == 'Dice':
        draw(column, 'poly', 20, rgb(255, 255, 255), rgb(255 * 0.9, 255 * 0.9, 255 * 0.9), 6, 0)
    elif name == 'Opal':
        draw(column, 'circle', 20,
             gradient(rgb(255, 255, 255), rgb(255 - 50, 255, 255), rgb(255, 255 - 50, 255), rgb(255, 255, 255 - 50),
                      rgb(255, 255, 255)), rgb(255 * 0.9, 255 * 0.9, 255 * 0.9), 4, 45, 70)
    elif name == 'Prisim':
        draw(column, 'poly', 20,
             gradient(rgb(255, 255 - 50, 255 - 50), rgb(255 - 50, 255, 255 - 50), rgb(255 - 50, 255 - 50, 255),
                      start='left'), rgb(255, 255, 255), 3, 45, 120)
    elif name == 'Onyx':
        draw(column, 'star', 20, gradient(rgb(50, 50, 150), rgb(50, 50, 50)), rgb(50, 50, 50), 5, 80, 50)
    elif name == 'Mythril':
        draw(column, 'poly', 20, gradient(rgb(150, 235, 200), rgb(150, 255, 150)), rgb(255, 255, 255), 5, 30, 120)
    elif name == 'Ether Orb':
        draw(column, 'circle', 20, gradient(rgb(100, 250, 200), rgb(250, 50, 250)), rgb(250, 50, 250))
    elif name == 'Inferno':
        draw(column, 'star', 25, gradient(rgb(255, 215, 50), rgb(215, 255, 50)), rgb(255, 215, 50), 6, 30, 60)
    elif name == 'Nebula':
        draw(column, 'star', 30, gradient(rgb(255, 150, 255), rgb(200, 215, 255), rgb(215, 255, 200)), None, 50, 0, 40)
    elif name == 'Singularity':
        draw(column, 'star', 20, gradient(rgb(255 / 4, 150 / 4, 255 / 4), rgb(200 / 4, 215 / 4, 255 / 4)),
             rgb(255 / 2, 215 / 2, 255 / 2), 70, 0, 20)
    symbol.centerX = column.centerX
    symbol.bottom = column.top - 10

    if name in commons:
        columnOverlay.opacity = 60
        columnOverlay.fill = 'grey'

    elif name in uncommons:
        columnOverlay.opacity = 60
        columnOverlay.fill = 'green'

    elif name in rares:
        columnOverlay.opacity = 40
        columnOverlay.fill = 'blue'

    elif name in epics:
        columnOverlay.opacity = 80
        columnOverlay.fill = 'mediumOrchid'

    elif name in fableds:
        columnOverlay.opacity = 70
        columnOverlay.fill = 'crimson'

    elif name in mythics:
        columnOverlay.opacity = 50
        columnOverlay.fill = 'fuchsia'

    else:
        columnOverlay.opacity = 40
        columnOverlay.fill = 'lightGrey'

    rolled.add(symbol)
    rolledList.append(name)
    syms.remove(symbol)

    if name == 'Dice':
        worth['Dice'] = randrange(1, 21)

    if column == c1:
        l1.value = worth[name]
        app.l1p = l1.value
    elif column == c2:
        l2.value = worth[name]
        app.l2p = l2.value
        if rolledList[0] == rolledList[1] and not rolledList[1] in ['Empty', 'Quartz']:
            app.bonus += 1
            app.bonusName = rolledList[1]
    else:
        l3.value = worth[name]
        app.l3p = l3.value
        if ((rolledList[0] == rolledList[2]) or (rolledList[1] == rolledList[2])) and not rolledList[2] in ['Empty',
                                                                                                            'Quartz']:
            app.bonus += 1
            app.bonusName = rolledList[2]


def spin():
    sleep(0)
    app.bonusName = None
    app.bonus = 1
    syms.visible = True
    rolled.clear()
    rolledList.clear()
    symL1.visible = False
    symL2.visible = False
    symL3.visible = False
    l1.visible = False
    l2.visible = False
    l3.visible = False
    l4.visible = False
    bl.visible = False
    coinBox.visible = False
    app.c1Mult = 1
    app.c2Mult = 1
    app.c3Mult = 1
    symL1.value = ''
    symL2.value = ''
    symL3.value = ''
    if app.spins <= 200:
        app.mythicChance = app.coins / 10000
    else:
        app.mythicChance = app.coins / 100000
    rareInt = randrange(1, 100 + rounded(app.mythicChance))
    pb.visible = False
    if rareInt <= 40:
        app.sale = commons[randrange(1, len(commons))]
        app.saleRarity = 'common'
        app.saleCost = 15
    elif rareInt <= 70 and app.spins > 10:
        app.sale = uncommons[randrange(0, len(uncommons))]
        app.saleRarity = 'uncommon'
        app.saleCost = 50
    elif rareInt <= 90 and app.spins > 25:
        app.sale = rares[randrange(0, len(rares))]
        app.saleRarity = 'rare'
        app.saleCost = 100
    elif rareInt <= 96 and app.spins > 40:
        app.sale = epics[randrange(0, len(epics))]
        app.saleRarity = 'epic'
        app.saleCost = 250
        if app.spins < 100:
            pb.visible = True
    elif rareInt <= 99 and app.spins > 50:
        app.sale = fableds[randrange(0, len(fableds))]
        app.saleRarity = 'fabled'
        app.saleCost = 1000
        pb.visible = True
    elif rareInt >= 100 and app.spins > 70:
        app.sale = mythics[randrange(0, len(mythics))]
        app.saleRarity = 'mythic'
        app.saleCost = 5000
        pb.visible = True
    else:
        app.sale = commons[randrange(0, len(uncommons))]
        app.saleRarity = 'common'
        app.saleCost = 15

    if len(rolled) != 0:
        for i in range(3):
            syms.add(rolled.children[0])
        rolled.clear()
        rolledList.clear()

    E = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    a, b, c = random.sample(owned, k=3)
    slot(a, c1, co1)
    slot(b, c2, co2)
    slot(c, c3, co3)

    if rolledList[0] == app.bonusName:
        app.l1p *= app.bonus
        l1.value *= app.bonus
        app.c1Mult *= app.bonus
    if rolledList[1] == app.bonusName:
        app.l2p *= app.bonus
        l2.value *= app.bonus
        app.c2Mult *= app.bonus
    if rolledList[2] == app.bonusName:
        app.l3p *= app.bonus
        l3.value *= app.bonus
        app.c3Mult *= app.bonus

    if app.bonus == 1:
        bl.value = ''
        l4.centerY = 330
    elif app.bonusName != None:
        bl.value = 'x' + str(app.bonus) + ' ' + str(app.bonusName + ' value')
        l4.centerY = 345
        if bl.value == 'x3 Nebula value':
            bl.value = 'CATACLYSM (x10)'
            app.l1p *= 10
            app.l2p *= 10
            app.l3p *= 10
            l1.value *= 10
            l2.value *= 10
            l3.value *= 10
            app.c1Mult *= 10
            app.c2Mult *= 10
            app.c3Mult *= 10
            l4.centerY = 345

    if rolledList[0] in ['Prisim', 'Singularity']:
        app.l2p *= 2
        l2.value *= 2
        app.c2Mult *= 2
    if rolledList[1] in ['Prisim', 'Singularity']:
        app.l1p *= 2
        app.l3p *= 2
        app.c1Mult *= 2
        app.c3Mult *= 2
        l1.value *= 2
        l3.value *= 2
    if rolledList[2] in ['Prisim', 'Singularity']:
        app.l2p *= 2
        l2.value *= 2
        app.c2Mult *= 2
    if 'Ether Orb' in rolledList:
        app.c1Mult *= 2
        app.c2Mult *= 2
        app.c3Mult *= 2
        app.l1p *= 2
        l1.value *= 2
        app.l2p *= 2
        l2.value *= 2
        app.l3p *= 2
        l3.value *= 2
    if 'Onyx' in rolledList:
        app.c1Mult *= 1.5
        app.c2Mult *= 1.5
        app.c3Mult *= 1.5
        app.l1p *= 1.5
        l1.value *= 1.5
        app.l2p *= 1.5
        l2.value *= 1.5
        app.l3p *= 1.5
        l3.value *= 1.5

    if 'Singularity' in rolledList:
        if rolledList[0] == 'Singularity':
            app.c1mod = app.l2p
        else:
            app.c1mod = 0
        if rolledList[1] == 'Singularity':
            app.c2mod = app.l1p + app.l3p
        else:
            app.c2mod = 0
        if rolledList[2] == 'Singularity':
            app.c3mod = app.l2p
        else:
            app.c3mod = 0

        app.l1p += app.c1mod
        app.l2p += app.c2mod
        app.l3p += app.c3mod
        l1.value = app.l1p
        l2.value = app.l2p
        l3.value = app.l3p

    if bl.value == 'x3 Singularity value':
        bl.value = 'APOCALPYTOPHOBIA (+90K)'
        app.l1p += 30000
        app.l2p += 30000
        app.l3p += 30000

    app.coins += rounded(app.l1p + app.l2p + app.l3p)
    l4.value = app.l1p + app.l2p + app.l3p
    l4.fill = rgb(255 * 0.95, 215 * 0.95, 0)

    coinBox.width = (len(str(l4.value)) * 7) + 12
    coinBox.centerX = l4.centerX
    coinBox.centerY = l4.centerY

    rolled.visible = True
    syms.visible = False
    app.spins += 1

    abrv(app.coins, coinLabel, 'Coins: ')
    abrv(app.spins, spinsLabel, 'Spins: ')

    abrv(l1.value, l1)
    abrv(l2.value, l2)
    abrv(l3.value, l3)
    abrv(l4.value, l4)

    l4.value = '+' + l4.value

    cb.width = len(coinLabel.value) * 8
    sb.width = len(spinsLabel.value) * 8
    cb.right = 395
    sb.right = 395
    coinLabel.centerX = cb.centerX
    spinsLabel.centerX = sb.centerX

    if app.c1Mult > 1:
        symL1.value = 'x' + str(app.c1Mult)
        if '.0' in str(symL1.value):
            symL1.value = symL1.value.replace('.0', '')
    if app.c2Mult > 1:
        symL2.value = 'x' + str(app.c2Mult)
        if '.0' in str(symL1.value):
            symL1.value = symL1.value.replace('.0', '')
    if app.c3Mult > 1:
        symL3.value = 'x' + str(app.c3Mult)
        if '.0' in str(symL1.value):
            symL1.value = symL1.value.replace('.0', '')

    saleLabel.value = 'For sale: ' + str(app.sale) + ' - $' + str(app.saleCost)
    saleLabel.left = 20
    saleInfo.value = ''
    saleInfo.left = saleLabel.left

    if app.saleRarity == 'common':
        saleLabel.fill = 'grey'
    elif app.saleRarity == 'uncommon':
        saleLabel.fill = 'green'
    elif app.saleRarity == 'rare':
        saleLabel.fill = 'cornFlowerBlue'
    elif app.saleRarity == 'epic':
        saleLabel.fill = 'violet'
    elif app.saleRarity == 'fabled':
        saleLabel.fill = 'red'
    elif app.saleRarity == 'mythic':
        saleLabel.fill = 'deepPink'

    symL1.visible = True
    symL2.visible = True
    symL3.visible = True
    l1.visible = True
    l2.visible = True
    l3.visible = True
    l4.visible = True
    bl.visible = True
    coinBox.visible = True


def onStep():
    if app.cd > 0:
        app.cd -= 1


def onKeyHold(keys):
    if 'space' in keys and not app.saleRarity in ['fabled', 'mythic']:
        if app.spins > 100 or app.saleRarity in ['common', 'uncommon', 'rare', None]:
            if l2.visible == True and app.cd == 0:
                spin()
                app.cd = 10
    elif 'space' in keys:
        saleInfo.value = '(Press skip to reroll)'
        saleInfo.left = saleLabel.left

        ##### FIX BELOW CODE SO NO CRASH WHEN YOU DELETE TOO MANY THINGS AT ONCE (owned = [10 coin, 2 empty], -10 coin = 2 owned symbols left, causing a crash)
    elif 'backspace' in keys:
        if len(owned) > 8:
            response1 = app.getTextInput('Which symbol do you want to remove?')
            if response1 in owned:
                response2 = app.getTextInput('How many? (1-' + str(owned.count(response1)) + ')')
                ### USE .casefold() to flip all uppercases to lowercases
                try:
                    if int(response2) <= owned.count(response1):
                        for i in range(int(response2)):
                            owned.remove(response1)
                        print(
                            '[SUCCESS] You now have ' + str(owned.count(response1)) + ' [' + str(response1) + '] left')
                    else:
                        print("[ERROR] You don't have that many [" + str(response1) + ']')
                except:
                    print('[ERROR] Please enter an integer (1, 2, 3, etc.)')
            else:
                print('[ERROR] Please enter an owned symbol (for example, ' + str(
                    random.choice(owned)) + ')\n(Caps matter)')
    elif 'tab' in keys:
        if app.coins >= app.saleCost and app.sale != None:
            if app.sale == 'Coin':
                quickAdd('Coin')

            elif app.sale == 'Quartz':
                quickAdd('Quartz')

            elif app.sale == 'Star':
                quickAdd('Star')

            elif app.sale == 'Dice':
                quickAdd('Dice')

            elif app.sale == 'Opal':
                quickAdd('Opal')

            elif app.sale == 'Prisim':
                quickAdd('Prisim')

            elif app.sale == 'Onyx':
                quickAdd('Onyx')

            elif app.sale == 'Mythril':
                quickAdd('Mythril')

            elif app.sale == 'Ether Orb':
                quickAdd('Ether Orb')

            elif app.sale == 'Inferno':
                quickAdd('Inferno')

            elif app.sale == 'Nebula':
                quickAdd('Nebula')

            elif app.sale == 'Singularity':
                quickAdd('Singularity')
            saleLabel.value = 'Sold! (+1 ' + str(app.sale) + ')'
            saleLabel.left = 20
            app.sale = None
            app.saleRarity = None
            app.coins -= app.saleCost
            abrv(app.coins, coinLabel, 'Coins: ')
        elif 'For' in saleLabel.value:
            saleInfo.value = 'Insufficient Funds!'
            saleInfo.left = 20


def onMouseRelease(x, y):
    if ib.contains(x, y):
        if app.coins >= app.saleCost and app.sale != None:
            if app.sale == 'Coin':
                quickAdd('Coin')

            elif app.sale == 'Quartz':
                quickAdd('Quartz')

            elif app.sale == 'Star':
                quickAdd('Star')

            elif app.sale == 'Dice':
                quickAdd('Dice')

            elif app.sale == 'Opal':
                quickAdd('Opal')

            elif app.sale == 'Prisim':
                quickAdd('Prisim')

            elif app.sale == 'Onyx':
                quickAdd('Onyx')

            elif app.sale == 'Mythril':
                quickAdd('Mythril')

            elif app.sale == 'Ether Orb':
                quickAdd('Ether Orb')

            elif app.sale == 'Inferno':
                quickAdd('Inferno')

            elif app.sale == 'Nebula':
                quickAdd('Nebula')

            elif app.sale == 'Singularity':
                quickAdd('Singularity')
            saleLabel.value = 'Sold! (+1 ' + str(app.sale) + ')'
            saleLabel.left = 20
            app.sale = None
            app.saleRarity = None
            app.coins -= app.saleCost
            abrv(app.coins, coinLabel, 'Coins: ')
        elif 'For' in saleLabel.value:
            saleInfo.value = 'Insufficient Funds!'
            saleInfo.left = 20

    if pb.contains(x, y) and pb.visible == True:
        spin()

cmu_graphics.run()