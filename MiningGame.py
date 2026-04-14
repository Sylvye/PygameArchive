from cmu_graphics import *
from time import sleep
import math

num = app.getTextInput('Enter a seed (ESC for random)')
try:
    seed(num)
except:
    pass

app.background = rgb(225, 225, 255)
app.stoneColor = rgb(100, 100, 120)
caves = Group()
tiles = Group()
coinPiles = Group()
chests = Group()
decor = Group()

app.steps = 0
app.genDepth = 0
app.depth = 0
app.caveChance = 0
app.chestChance = 5
urls = [
    'cmu://447627/22188679/stone.png',  # 0
    'cmu://447627/22103228/aluminumOre.png',  # 1
    'cmu://447627/22103243/copperOre.png',  # 2
    'cmu://447627/22103262/ironOre.png',  # 3
    'cmu://447627/22103289/silverOre.png',  # 4
    'cmu://447627/22129528/goldOre.png',  # 5
    'cmu://447627/22103318/platinumOre.png',  # 6
    'cmu://447627/22115309/quartzChunk.png',  # 7
    'cmu://447627/22115341/amethystChunk.png.png',  # 8
    'cmu://447627/22115355/onyxChunk.png',  # 9
    'cmu://447627/22115373/sapphireChunk.png',  # 10
    'cmu://447627/22115401/emeraldChunk.png',  # 11
    'cmu://447627/22115429/rubyChunk.png',  # 12
    'cmu://447627/22115446/diamondChunk.png',  # 13
    'cmu://447627/22115462/painiteChunk.png',  # 14
    'cmu://447627/22137472/drill.png',  # 15
    'cmu://447627/22156167/drill2.png',  # 16
    'cmu://447627/22143953/coinsPile.png',  # 17
    'cmu://447627/22167779/chest.png',  # 18
    'cmu://447627/22154400/stalagmites.png',  # 19
]
ores = [
    'aluminum',
    'copper',
    'iron',
    'silver',
    'gold',
    'platinum',
]
gems = [
    'quartz',
    'amethyst',
    'onyx',
    'sapphire',
    'emerald',
    'ruby',
    'diamond',
    'painite',
]
tileDrops = {
    'stone': 0,
    'aluminum': 1,
    'copper': 2,
    'iron': 5,
    'silver': 10,
    'gold': 25,
    'platinum': 50,
    'quartz': 5,
    'amethyst': 10,
    'onyx': 20,
    'sapphire': 40,
    'emerald': 60,
    'ruby': 80,
    'diamond': 100,
    'painite': 200,
}
chestDrops = [
    'coins',
    'drill',
    'charm',
]
charms = [
    'haste',
    'reach',
    'greed',
    'spelunker',
    'looting'
]
availableOres = ['aluminum']
availableGems = ['quartz']
player = Circle(200, 50, 20, fill='purple')
player.vx = 0
player.vy = 0
player.speed = 1
player.gravity = 0
player.coins = 0
player.coinMult = 1
player.mineCD = 0.5
player.reach = 10
player.drill = 'default'
player.stepsSinceMine = 999
drill = Image(urls[15], 0, 0, visible=False)
drill.offsetX = 0
drill.offsetY = 0
shop = Rect(0, 0, 400, 400, fill=rgb(100, 150, 215), visible=False)
texts = Group()
depthLabel = Label('0 m', 380, 20, size=15, font='montserrat')
coinsLabel = Label('0 c', 20, 20, size=15, font='montserrat')


def loadTextures():
    # stops the program from freezing whenever a new texture appears on screen
    sleep(0)
    loop = 0
    # loops through all urls and draws an image with it, then deletes them all
    for i in urls:
        image = Image(i, 400, 400)
        loop += 1


def abrv(var):
    # abreviates large numbers to have a -k, -m, or -b at the end

    mod = rounded(var)
    if len(str(math.floor(mod))) in range(5, 7):
        abrvd = str(math.floor((mod / 1000) * 10) / 10) + 'k'
    elif len(str(math.floor(mod))) in range(7, 10):
        abrvd = str(math.floor((mod / 1000000) * 10) / 10) + 'm'
    elif len(str(math.floor(mod))) in range(10, 13):
        abrvd = str(math.floor((mod / 1000000000) * 10) / 10) + 'b'
    else:
        abrvd = str(mod)
    if '.0' in str(abrvd):
        abrvd = abrvd.replace('.0', '')

    return str(abrvd)


def chance(chance):
    # makes it easier to do chance-based actions
    if chance < 100:
        chance = chance / 100
        rand = random()
        if rand < chance:
            return True
        else:
            return False
    else:
        return True


def rescale(image, scale=0.2, width=None, height=None):
    # rescales an image to be smaller (or larger), as their default size is massive

    x, y = image.centerX, image.centerY
    if width == None and height == None:
        image.width *= scale
        image.height *= scale
    else:
        image.width = width
        image.height = height
    image.centerX, image.centerY = x, y


def split(input, characterLimit=40, splitOnPunc=True):
    # takes a string and returns a list of smaller segments that are limited to a certain amount of characters

    words = input.split()
    segments = []
    line = ''
    for word in words:
        # if the word fits in the current line, adds it
        if len(line + word) <= characterLimit:
            line += word + ' '
        # otherwise, start a new line with the word on it
        else:
            segments.append(line)
            line = word + ' '
        # adds a blank line after periods and starts a new line after commas and colons
        if splitOnPunc == True:
            index = words.index(word)
            if index != len(words) - 1:
                lastCharacter = word[len(word) - 1]
                if lastCharacter == ',' or lastCharacter == ':':
                    segments.append(line)
                    line = ''
                elif lastCharacter == '.':
                    segments.append(line)
                    segments.append('')
                    line = ''
    # adds remainder to segments
    if len(line) > 0:
        segments.append(line)

    return segments  # maybe


def kill(message):
    Rect(0, 0, 400, 400, fill=rgb(255, 150, 100), opacity=50)
    loop = 0
    message += ' You explored to a depth of ' + str(app.genDepth) + '. You obtained ' + str(player.coins) + ' coins.'
    for segment in split(message):
        if segment != '':
            label = Label(segment, 200, 150 + loop * 20, size=15)
            if loop == 0:
                label.size += 5
                label.bold = True
        loop += 1
    app.stop()


def text(value, x, y, color='gold'):
    texts.add(Label(value, x, y, bold=True, size=15, fill=color, font='montserrat'))


def shift(amount):
    tiles.centerY += amount
    player.centerY += amount
    caves.centerY += amount
    coinPiles.centerY += amount
    decor.centerY += amount
    texts.centerY += amount
    chests.centerY += amount


def newLayer():
    shift(-50)
    app.genDepth += 1
    if app.genDepth in [10, 25, 50, 100, 150, 200, 300, 400, 500]:
        if app.genDepth == 10:
            app.caveChance += 1
            app.background = rgb(160, 180, 200)
        elif app.genDepth == 25:
            app.caveChance += 1
            availableOres.append('copper')
            app.background = rgb(150, 170, 190)
        elif app.genDepth == 50:
            app.caveChance += 3
            app.background = rgb(140, 160, 180)
            availableOres.append('iron')
            availableGems.append('amethyst')
        elif app.genDepth == 100:
            app.caveChance += 3
            app.background = rgb(130, 150, 170)
            availableGems.append('onyx')
            availableOres.remove('aluminum')
            availableGems.remove('quartz')
        elif app.genDepth == 150:
            app.caveChance += 2
            app.background = rgb(120, 140, 160)
            availableOres.append('silver')
            availableGems.append('sapphire')
        elif app.genDepth == 200:
            app.caveChance += 2
            app.background = rgb(110, 130, 150)
            availableOres.remove('copper')
            availableGems.remove('amethyst')
        elif app.genDepth == 300:
            app.caveChance += 3
            app.background = rgb(100, 120, 140)
            availableOres.append('gold')
            availableGems.append('emerald')
            availableGems.append('sapphire')
            availableOres.remove('iron')
            availableGems.remove('onyx')
        elif app.genDepth == 400:
            app.caveChance += 5
            app.background = rgb(90, 110, 130)
            availableGems.append('ruby')
            availableGems.append('diamond')
            availableOres.append('platinum')
            availableOres.remove('silver')
            availableGems.remove('sapphire')
        elif app.genDepth == 500:
            app.caveChance += 5
            app.background = rgb(80, 100, 120)
            availableGems.append('painite')
            availableGems.remove('emerald')
            availableGems.remove('ruby')
    if chance(app.caveChance):
        x = randrange(0, 401, 25)
        width = randrange(150, 451, 50)
        height = randrange(150, 451, 50)
        angle = randrange(0, 360)
        cave = Oval(x, 999, width, height, rotateAngle=angle, fill=None)
        cave.top = 375
        caves.add(cave)
    for x in range(25, 400, 50):
        if not caves.contains(x, 375):
            left = tiles.hitTest(x - 50, 375)
            right = tiles.hitTest(x + 50, 375)
            top = tiles.hitTest(x, 325)
            oreChance = 5
            ore = choice(availableOres)

            if left != None and left.opacity == 100 and left.type in ores:
                oreChance += 30
                ore = left.type
            if right != None and right.opacity == 100 and right.type in ores:
                oreChance += 30
                ore = right.type
            if top != None and top.opacity == 100 and top.type in ores:
                oreChance += 30
                ore = top.type

            if chance(2):
                type = choice(availableGems)
                url = gems.index(type) + 7
            elif chance(oreChance):
                type = ore
                url = ores.index(type) + 1
            else:
                type = 'stone'
                url = 0

            tile = Image(urls[url], x, 375, align='center', rotateAngle=randrange(0, 360, 90))
            rescale(tile, None, 50, 50)
            tile.drop = tileDrops[type]
            tile.type = type

            if tile.hitsShape(caves) and (top == None or top.opacity != 100):
                # spawns chests
                if chance(app.chestChance):
                    chest = Image(urls[18], tile.centerX, tile.centerY - 50, align='center')
                    rescale(chest, None, 50, 50)
                    chest.item = choice(chestDrops)

                    chests.add(chest)

                # spawns coin piles
                elif chance(25):
                    coinPile = Image(urls[17], tile.centerX, tile.centerY - 50, align='center')
                    rescale(coinPile, None, 50, 50)
                    coinPiles.add(coinPile)

                # spawns stalagmites
                elif chance(25):
                    stalagmite = Image(urls[19], tile.centerX, tile.centerY - 50, align='center')
                    rescale(stalagmite, None, 50, 50)
                    decor.add(stalagmite)

            tiles.add(tile)

    depthLabel.value = abrv(app.depth) + ' m'
    depthLabel.right = 390


def destroy(tile):
    if player.stepsSinceMine / 30 >= player.mineCD:
        if tile.drop != 0:
            updateCoinLabel(tile.drop)
        decoration = decor.hitTest(tile.centerX, tile.centerY - 50)
        if decoration != None:
            decoration.opacity = 33
        tile.opacity = 33
        player.stepsSinceMine = 0


def shear():
    if tiles.top < 0:
        for i in tiles:
            if i.centerY < 0:
                tiles.remove(i)
    if len(caves):
        for i in caves:
            if i.bottom < 400:
                caves.remove(i)
    if coinPiles.top < 0:
        for i in coinPiles:
            if i.centerY < 0:
                coinPiles.remove(i)
            elif i.centerY > 400:
                coinPiles.remove(i)
    if chests.top < 0:
        for i in chests:
            if i.centerY < 0:
                chests.remove(i)
            elif i.centerY > 400:
                chests.remove(i)
    if decor.top < 0:
        for i in decor:
            if i.centerY < 0:
                decor.remove(i)


def updateCoinLabel(add=0):
    player.coins += math.ceil(add * player.coinMult)
    coinsLabel.value = abrv(player.coins) + ' c'
    coinsLabel.left = 10


def onKeyPress(key):
    if key == 'f':
        if not shop.visible:
            shop.visible = True
            texts.clear()
        else:
            shop.visible = False
            texts.clear()
    elif key == 'w':
        if player.vy < 0:
            bottom = tiles.hitTest(player.centerX, player.bottom)
            if bottom == None or bottom.opacity != 100:
                left = tiles.hitTest(player.left - 6, player.centerY)
                right = tiles.hitTest(player.right + 6, player.centerY)
                if left != None and left.opacity == 100:
                    player.vy = -15
                    player.gravity = 0
                    player.vx = -18
                elif right != None and right.opacity == 100:
                    player.vy = -15
                    player.gravity = 0
                    player.vx = 18
    elif key == 'e' and player.hitsShape(chests):
        chest = chests.hitTest(player.centerX, player.centerY)
        if chest != None:
            gold = False
            if chest.item == 'coins':
                gold = True
            elif chest.item == 'drill':
                if player.drill == 'default':
                    player.drill = 'platinum'
                    text('+platinum drill', chest.centerX, chest.centerY, rgb(255, 0, 100))
                else:
                    gold = True
            elif chest.item == 'charm':
                charm = choice(charms)
                if charm == 'haste':
                    if player.mineCD > 0:
                        player.mineCD -= 0.05
                    else:
                        gold = True
                elif charm == 'reach':
                    if player.reach < 10:
                        player.reach += 0.25
                    else:
                        gold = True
                elif charm == 'greed':
                    player.coinMult += 0.05
                elif charm == 'spelunker':
                    if app.caveChance < 50:
                        app.caveChance += 0.5
                    else:
                        gold = True
                elif charm == 'looting':
                    if app.chestChance < 10:
                        app.chestChance += 0.2
                    else:
                        gold = True

                if gold == False:
                    text('+' + str(charm) + ' charm', chest.centerX, chest.centerY, rgb(255, 150, 50))
            if gold == True:
                bestGem = availableGems[len(availableGems) - 1]
                amount = math.ceil(tileDrops[bestGem] * randrange(10, 16) * player.coinMult)
                updateCoinLabel(amount)
                text("+" + str(amount) + ' c', chest.centerX, chest.centerY)
                chests.remove(chest)
            chests.remove(chest)


def onKeyHold(keys):
    destroyed = False
    if 'down' in keys and player.bottom >= 150:
        app.depth += 1
        if app.genDepth == app.depth:
            newLayer()
        shear()
    if 'w' in keys:
        bottom = tiles.hitTest(player.centerX, player.bottom)
        if bottom != None and bottom.opacity == 100:
            player.vy -= 12
        left = tiles.hitTest(player.left - 5, player.centerY)
        if 'a' in keys and left != None and left.opacity == 100:
            player.vx = -5
        right = tiles.hitTest(player.right + 5, player.centerY)
        if 'd' in keys and right != None and right.opacity == 100:
            player.vx = 5
        if 'space' in keys and not destroyed:
            drill.visible = True
            drill.offsetX = 0
            drill.offsetY = -20
            drill.rotateAngle = 270
            tile = tiles.hitTest(player.centerX, player.top - player.reach)
            if tile != None and tile.opacity == 100:
                destroy(tile)
                destroyed = True
    if 'a' in keys:
        bottom = tiles.hitTest(player.centerX, player.bottom)
        if bottom != None and bottom.opacity == 100:
            player.vx -= player.speed
        if 'space' in keys and not destroyed:
            drill.visible = True
            drill.offsetX = -20
            drill.offsetY = 0
            drill.rotateAngle = 180
            tile = tiles.hitTest(player.left - player.reach, player.centerY)
            if tile != None and tile.opacity == 100:
                destroy(tile)
                destroyed = True
    if 's' in keys and 'space' in keys and not destroyed:
        drill.visible = True
        drill.offsetX = 0
        drill.offsetY = 20
        drill.rotateAngle = 90
        tile = tiles.hitTest(player.centerX, player.bottom + player.reach)
        if tile != None and tile.opacity == 100:
            destroy(tile)
            destroyed = True
    if 'd' in keys:
        bottom = tiles.hitTest(player.centerX, player.bottom)
        if bottom != None and bottom.opacity == 100:
            player.vx += player.speed
        if 'space' in keys and not destroyed:
            drill.visible = True
            drill.offsetX = 20
            drill.offsetY = 0
            drill.rotateAngle = 0
            tile = tiles.hitTest(player.right + player.reach, player.centerY)
            if tile != None and tile.opacity == 100:
                destroy(tile)
                destroyed = True


def onKeyRelease(key):
    if key == 'space':
        drill.visible = False


def onStep():
    if not shop.visible:
        app.steps += 1
        player.stepsSinceMine += 1
        player.centerX += player.vx
        player.centerY += player.vy
        bottom = tiles.hitTest(player.centerX, player.bottom)
        if bottom != None and bottom.opacity == 100:
            player.vx *= 0.9
        player.vy *= 0.9

        # prevents walking away from playfield
        if player.left < 0:
            player.left = 0
            player.vx = 0
        elif player.right > 400:
            player.right = 400
            player.vx = 0
        elif player.top < -50:
            player.top = -50
            player.vy = 0

        # collisions
        left = tiles.hitTest(player.left, player.centerY)
        if left != None and left.opacity == 100:
            player.left = left.right
            player.vx *= -0.33
        right = tiles.hitTest(player.right, player.centerY)
        if right != None and right.opacity == 100:
            player.right = right.left
            player.vx *= -0.33
        top = tiles.hitTest(player.centerX, player.top)
        if top != None and top.opacity == 100:
            player.top = top.bottom
            player.vy *= -0.1
        bottom = tiles.hitTest(player.centerX, player.bottom)
        if bottom != None and bottom.opacity == 100:
            player.bottom = bottom.top
            player.vy *= -0.1
            player.gravity = 0
        else:
            # gravity
            if player.vy > 0:
                player.gravity += 0.4
            else:
                player.vy += 0.3
            if player.gravity > 2:
                player.gravity = 2
            player.vy += player.gravity

        if player.hitsShape(decor) and player.vy > 15:
            stalag = decor.hitTest(player.centerX, player.centerY)
            if stalag != None and stalag.opacity == 100:
                kill('You were impaled by a stalagmite.')

        for i in coinPiles:
            bottom = tiles.hitTest(i.centerX, i.bottom)
            if bottom == None or bottom.opacity != 100:
                i.centerY += 10

        for i in chests:
            bottom = tiles.hitTest(i.centerX, i.bottom)
            if bottom == None or bottom.opacity != 100:
                i.centerY += 10

        for i in texts:
            i.opacity -= 2.5
            i.size -= 0.1
            i.centerY -= 0.5
            if i.opacity == 0:
                texts.remove(i)

        coinPile = coinPiles.hitTest(player.centerX, player.centerY)
        if coinPile != None:
            bestOre = availableOres[len(availableOres) - 1]
            amount = math.ceil(tileDrops[bestOre] * randrange(5, 11) * player.coinMult)
            updateCoinLabel(amount)
            text("+" + str(amount) + ' c', coinPile.centerX, coinPile.centerY)
            coinPiles.remove(coinPile)

        if player.bottom > 300:
            player.bottom = 300
            newLayer()
            shear()
            app.depth += 1

        x = player.centerX + drill.offsetX
        y = player.centerY + drill.offsetY
        drill.centerX = dsin(110 * app.steps) + x
        drill.centerY = dsin(90 * app.steps) + y


loadTextures()
rescale(drill, 0.2)
newLayer()
newLayer()

cmu_graphics.run()