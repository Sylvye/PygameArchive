from cmu_graphics import *
from time import sleep
import math

# add a card that plays the next card twice

urls = [
    # cards
    'cmu://447627/21640089/stabCard.png',  # 0
    'cmu://447627/21640111/blockCard.png',  # 1
    'cmu://447627/21640123/restCard.png',  # 2
    'cmu://447627/22027363/criticalStrikeCard.png',  # 3
    'cmu://447627/22027289/bunkerCard.png',  # 4
    'cmu://447627/21640146/vampirismCard.png',  # 5
    'cmu://447627/21640154/fatalBlowCard.png',  # 6
    'cmu://447627/21640158/suckerPunchCard.png',  # 7
    'cmu://447627/22048452/rampageCard.png',  # 8
    'cmu://447627/21640173/smiteCard.png',  # 9
    'cmu://447627/21640181/tomeCard.png',  # 10
    'cmu://447627/21640191/inspireCard.png',  # 11
    'cmu://447627/21806950/mimicCard.png',  # 12
    'cmu://447627/21807352/ShieldBashCard.png',  # 13
    'cmu://447627/21834097/critStrike.png',  # 14
    'cmu://447627/21856143/diceCard.png',  # 15
    'cmu://447627/21856225/venomCard.png',  # 16
    'cmu://447627/21856238/brambleCard.png',  # 17
    'cmu://447627/21856251/lightningCard.png',  # 18
    'cmu://447627/21856263/exclusiveCard.png',  # 19

    # bleugh
    'cmu://447627/21636413/blankCard.png',  # 20
    'cmu://447627/21636421/flippedCard.png',  # 21

    # other
    'cmu://447627/21647630/attackButton.png',  # 22
    'cmu://447627/21647597/blockButton.png',  # 23
    'cmu://447627/21808454/placeholder.png',  # 24
    'cmu://447627/21810948/spark.png',  # 25
    'cmu://447627/21933322/spark2.png',  # 26
    'cmu://447627/21816775/critSpark.png',  # 27
    'cmu://447627/21933392/critSpark2.png',  # 28
    'cmu://447627/21938991/ghost.png',  # 29
    'cmu://447627/21939012/ghostRed.png',  # 30
    'cmu://447627/21938094/skipButton.png',  # 32

]
cards = [
    'Stab',  # 0
    'Block',  # 1
    'Rest',  # 2
    'Critical Strike',  # 3
    'Bunker',  # 4
    'Vampirism',  # 5
    'Curse',  # 6
    'Sucker Punch',  # 7
    'Rampage',  # 8
    'Ignite',  # 9
    'Demonic Tome',  # 10
    'Inspire',  # 11
    'Mimic',  # 12
    'Shield Bash',  # 13
    'Perilous Strike',  # 14
    'Dice',  # 15
    'Venomous',  # 16
    'Brambles',  # 17
    'Smite',  # 18
    'Sacrifice',  # 19
]
cardsInfo = {
    'Stab': "+1 damage.",
    'Block': "+1 block.",
    'Rest': "Heals 2 missing health points.",
    'Critical Strike': "+100% final damage multiplier.",
    'Bunker': "Heals for your block amount",
    'Vampirism': "+33% vampirism. (Vampirism - heals for x% of final damage).",
    'Curse': "+20% curse. (Curse - if your enemy's health drops below x% of its max hp on this turn, add 999 damage).",
    'Sucker Punch': "Inflicts 2 instant damage. (Affected by multipliers and persistant damage).",
    'Rampage': "+1 persisting damage. (Persistant damage - deals x damage every turn).",
    'Ignite': "+3 damage. You take 2 damage.",
    'Demonic Tome': "+200% damage multiplier. Self inflict 33% of however much damage you deal. NEGATIVE EFFECT STACKS!",
    'Inspire': "Heals 1 missing health point. Adds 1 damage.",
    'Mimic': "Will show up as any card in the game each time it appears.",
    'Shield Bash': "Adds your block amount to your attack.",
    'Perilous Strike': "75% chance to add 5 damage, otherwise it will take 5 health.",
    'Dice': "+(1-6) damage randomly. If you roll a 1: apply a -100% damage multiplier.",
    'Venomous': "+2 venom. (Venom - does x% of an enemy's health Venom is capped at x damage). VENOM IS PERSISTANT!",
    'Brambles': "+50% thorns. (Thorns - adds x% of the enemy's damage to your damage next round).",
    'Smite': "+(0-5) damage. Damage increases depending on how close an enemy is to 0 health.",
    'Sacrifice': "+(block * 2)% damage multiplier. Sets your block to 0.",
}
cardColors = {
    'Stab': rgb(255, 180, 180),
    'Block': rgb(180, 255, 180),
    'Rest': rgb(245, 245, 100),
    'Critical Strike': rgb(255, 215, 50),
    'Bunker': rgb(10, 175, 50),
    'Vampirism': rgb(225, 50, 100),
    'Curse': rgb(200, 10, 230),
    'Sucker Punch': rgb(200, 50, 10),
    'Rampage': rgb(140, 10, 70),
    'Ignite': rgb(255, 215, 0),
    'Demonic Tome': rgb(175, 10, 175),
    'Inspire': rgb(0, 255, 255),
    'Mimic': rgb(255, 0, 255),
    'Shield Bash': rgb(20, 50, 255),
    'Perilous Strike': rgb(255, 120, 0),
    'Dice': rgb(0, 120, 255),
    'Venomous': rgb(75, 200, 75),
    'Brambles': rgb(0, 150, 0),
    'Smite': rgb(255, 255, 0),
    'Sacrifice': rgb(250, 240, 150),
}
deck = [
    'Rest',
    'Rest',
    'Stab',
    'Stab',
    'Stab',
    'Stab',
    'Block',
    'Block',
    'Block',
    'Block',
    ]
hand = []
flipping = []
app.background = rgb(150, 200, 215)
app.play = True
app.frames = 0
app.mx = 9999
app.my = 9999
app.difficulty = 1
app.maxHealth = 20
app.health = 20
app.damage = 0
app.block = 0
app.persistantDamage = 0
app.persistantBlock = 0
app.damageMult = 1
app.vampirism = 0
app.curse = 0
app.potentialCurse = 0
app.venom = 0
app.brambles = 0
app.brambleDamage = 0
app.totalDealt = 0
app.totalPain = 0
app.enemies = 0
enemy = Image(urls[29], 200, 90, align='center')
enemy.health = 5
enemy.maxHealth = 5
enemy.attacking = False
enemyCover = Image(urls[30], 200, 90, align='center', opacity=0)
healthBarBG = Rect(200, 375, 200, 14, align='center', fill=rgb(255, 50, 150))
healthBar = Rect(200, 375, 200, 15, align='center', fill=rgb(50, 255, 150))
healthLabel = Label('', 200, 390, size=13, bold=True, font='orbitron')
enemyHealthBarBG = Rect(200, 150, 100, 7, align='center', fill=rgb(255, 50, 100))
enemyHealthBar = Rect(200, 150, 100, 7.5, align='center', fill=rgb(150, 25, 100))
markers = Line(150, 150, 251, 150, lineWidth=8, dashes=(0.5, 19.5), opacity=50)
enemyHealthLabel = Label('', 200, 160, font='orbitron')
attackIndicator = Image(urls[22], 50, 350, align='center')
blockIndicator = Image(urls[23], 350, 350, align='center')
attackLabel = Label(0, 50, 310, font='montserrat', bold=True, size=15)
damageMultLabel = Label('100%', 50, 385, font='montserrat', bold=True)
blockLabel = Label(0, 350, 310, font='montserrat', bold=True, size=15)
playerCards = Group()
attackEffects = Group()
info = Group(
    Rect(0, 0, 400, 400, fill=rgb(10, 70, 100)),
    Label('How to play', 200, 50, font='montserrat', size=20, fill=rgb(225, 255, 235), bold=True),
    Label('- Click on cards in your hand to use them.', 200, 90, font='montserrat', size=15, fill=rgb(225, 255, 235),
          bold=True),
    Label('- Cards can only be used once.', 200, 120, font='montserrat', size=15, fill=rgb(225, 255, 235)),
    Label('- The indicator on the left is your damage,', 200, 150, font='montserrat', size=15, fill=rgb(225, 255, 235)),
    Label('and the one on the right is your block.', 200, 165, font='montserrat', size=15, fill=rgb(225, 255, 235)),
    Label('- Hit SPACE or click the enemy to end your turn.', 200, 195, font='montserrat', size=15,
          fill=rgb(225, 255, 235), bold=True),
    Label("- The enemy will attack you after your turn.", 200, 225, font='montserrat', size=15, fill=rgb(225, 255, 235),
          bold=True),
    Label("- After lowering an enemy's heath to 0, ", 200, 255, font='montserrat', size=15, fill=rgb(225, 255, 235)),
    Label("you may replace a card in your deck.", 200, 270, font='montserrat', size=15, fill=rgb(225, 255, 235)),
    Label("- All cards have different uses and strengths,", 200, 300, font='montserrat', size=15,
          fill=rgb(225, 255, 235)),
    Label("so try different strategies and decks!", 200, 315, font='montserrat', size=15, fill=rgb(225, 255, 235)),
    Label("Press any key to start", 200, 350, font='montserrat', size=20, fill=rgb(255, 255, 50), bold=True)
)
texts = Group()
tint = Rect(0, 0, 400, 400, fill=rgb(200, 10, 10), opacity=0)
tint.baseOpacity = 0
dim = Rect(0, 0, 400, 400, opacity=60, visible=False)
rewards = Group()
rewardsCovers = Group()
cardLabel = Label('', 200, 200, font='orbitron', bold=True)
skipButton = Image(urls[31], 350, 350, align='center')
cardInfo = Group()
fade = Group()
display = Group()
lose = Group()


### global

def loadTextures():
    # stops the program from freezing whenever a new texture appears on screen

    texts.add(Rect(0, 0, 400, 400, fill=rgb(150, 150, 150)))
    texts.add(Label('Loading textures...', 200, 200, size=30))
    sleep(0)
    loop = 0
    # loops through all urls and draws an image with it, then deletes them all
    for i in urls:
        image = Image(i, 400, 400)
        texts.add(image)
        texts.remove(image)
        loop += 1
        if loop % 4 == 0:
            label = Label(str(loop) + '/' + str(len(urls)), 200, 250)
            texts.add(label)
            sleep(0)
            texts.remove(label)
    texts.clear()


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

    chance = chance / 100
    rand = random()
    if rand <= chance:
        return True
    else:
        return False


def rescaleImage(image, scale=0.2):
    # rescales an image to be smaller (or larger), as their default size is massive

    x, y = image.centerX, image.centerY
    image.width *= scale
    image.height *= scale
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

    return segments


### card-related

def endTurn():
    # deals damage
    if (app.damage) * app.damageMult > 0:
        damage = (app.damage) * app.damageMult
        # particles
        intensity = rounded((damage / enemy.maxHealth) * 10)
        if intensity < 1:
            intensity = 1
        elif intensity > 10:
            intensity = 10
        hurt(intensity)

    # tidies enemy health & adds damage to variable
    prevHealth = enemy.health
    enemy.health -= (app.damage) * app.damageMult
    if enemy.health < 0:
        enemy.health = 0
    app.totalDealt += prevHealth - enemy.health

    # does vampirism healing / harming
    if app.vampirism != 0:
        leeched = math.ceil(damage * app.vampirism)
        if leeched > 0:
            text('+' + abrv(leeched), 200, 365, rgb(10, 150, 50))
            app.health += leeched
            if app.health > app.maxHealth:
                app.health = app.maxHealth
        elif leeched < 0:
            subtractHealth(abs(leeched), False)

    # does venom damage
    if app.venom > 0:
        prevHealth = enemy.health
        damage = math.ceil(enemy.maxHealth * app.venom)
        if damage > app.venom * 100:
            damage = app.venom * 100
        enemy.health -= damage
        text('-' + str(damage), 200, 190, rgb(100, 200, 25), 30)
        app.totalDealt += prevHealth - enemy.health

    # gets the potential curse % from cards
    app.potentialCurse = hand.count('Curse') * 0.2

    print("get: ", app.brambleDamage)
    # if enemy is defeated
    if enemy.health <= 0:
        app.enemies += 1
        enemy.opacity = 0
        pickNewCard()
        app.persistantDamage = 0
        app.persistantBlock = 0
        app.venom = 0
        app.brambles = 0
        app.brambleDamage = 0
        resetStats()
    else:
        newHand()
        enemy.attacking = True
        app.damage = app.brambleDamage
    app.brambleDamage = 0

    # updates all visuals
    updateHealthBar(enemyHealthBar, enemyHealthBarBG, enemyHealthLabel, enemy.health, enemy.maxHealth)
    updateHealthBar(healthBar, healthBarBG, healthLabel, app.health, app.maxHealth)
    updateIndicators()


def addToHand(type, scale=0.2):
    # gives the card a property that says if they are mimic
    if type == 'Mimic':
        mimic = True
    else:
        mimic = False
    # if it is a mimic, then change it's type to a random card
    while type == 'Mimic':
        type = choice(cards)
    # adds card to hand list and draws it on screen
    hand.append(type)
    angle = (len(hand) - 3) * 15
    x, y = getPointInDir(200, 450, angle, 175)
    card = Image(urls[cards.index(type)], 0, 0, align='center')
    card.type = type
    card.index = len(playerCards)
    card.width *= scale
    card.height *= scale
    card.rotateAngle = angle
    card.angle = angle
    card.nativeX, card.nativeY = y, y
    card.centerX, card.centerY = x, y
    card.mimic = mimic
    # distinguishes mimics from normal cards
    if mimic == True:
        card.opacity = 80

    playerCards.add(card)


def pickNewCard():
    # draws 3 flipped cards on screen with random card types

    available = cards.copy()
    for x in range(100, 301, 100):
        selected = choice(available)
        available.remove(selected)

        cover = Image(urls[21], x, 400, align='center', opacity=0)
        cover.dormant = True
        cover.type = selected
        rescaleImage(cover, 0.25)
        rewardsCovers.add(cover)

    dim.visible = True
    skipButton.visible = True
    cardLabel.value = 'Select a card'


def deal():
    # fills up your hand with new cards from your deck

    amount = 5 - len(hand)
    deckCopy = deck.copy()
    # removes cards in hand from deckCopy to prevent card duplicating
    for card in playerCards:
        if card.mimic == False:
            value = card.type
        else:
            value = 'Mimic'
        if value in deckCopy:
            deckCopy.remove(value)
    # adds random cards from your deck
    for i in range(amount):
        selected = choice(deckCopy)
        deckCopy.remove(selected)
        addToHand(selected)


def newHand():
    # removes all unused cards & deals new cards to replace them (KEEPS UNUSED CARDS)

    # clears hand & saves unused cards
    save = []
    for card in playerCards:
        if card.opacity != 25:
            if card.mimic == False:
                value = card.type
            else:
                value = 'Mimic'
            if value in deck:
                save.append(value)
    playerCards.clear()
    hand.clear()

    # deals new cards
    for i in save:
        addToHand(i)
    deal()


def playCard(card):
    # carries out the card's function

    # gets the index of the card to identify it instead of its type
    index = cards.index(card.type)
    block = 0
    # depending on their index, does certain (a) action(s)
    if index == 0:  # stab
        app.damage += 1
        text('+' + str(app.damageMult), 50, 290, rgb(200, 50, 50))
    elif index == 1:  # block
        app.block += 1
        text('+1', 350, 290, rgb(50, 100, 255))
    elif index == 2:  # rest
        app.health += 2
        text('+2', 200, 365, rgb(10, 150, 50))
        if app.health > app.maxHealth:
            app.health = app.maxHealth
    elif index == 3:  # crit
        app.damageMult += 1
        text('+100%', 50, 290, rgb(255, 200, 50), 30)
    elif index == 4:  # bunker
        app.health += app.block
        if app.health > app.maxHealth:
            app.health = app.maxHealth
    elif index == 5:  # vampirism
        app.vampirism += 1 / 3
    elif index == 6:  # Curse
        app.curse += 0.2
        value = (str(int(app.curse * 100)) + '% FATAL')
        text(value, 200, 200, rgb(225, 50, 255), 30)
    elif index == 7:  # sucker punch
        damage = (2 + app.persistantDamage) * app.damageMult
        intensity = rounded(damage / enemy.maxHealth * 10)
        if intensity < 1:
            intensity = 1
        elif intensity > 10:
            intensity = 10
        hurt(intensity, randrange(27, 29))
        if damage > 0:
            preHealth = enemy.health
            enemy.health -= damage
            text('-' + str((2 + app.persistantDamage) * app.damageMult), 200, 175, rgb(200, 50, 50), 30)
            updateHealthBar(enemyHealthBar, enemyHealthBarBG, enemyHealthLabel, enemy.health, enemy.maxHealth)
            if enemy.health <= 0:  # if enemy is defeated
                enemy.health = 0
                endTurn()
            app.totalDealt += preHealth - enemy.health
    elif index == 8:  # rampage
        app.persistantDamage += 1
        app.damage += 1
        text('=' + str(app.persistantDamage), 50, 290, rgb(225, 225, 75))
    elif index == 9:  # ignite
        app.damage += 3
        subtractHealth(2, False)
        text('+' + str(3 * app.damageMult), 50, 290, rgb(200, 50, 50))
    elif index == 10:  # tome
        app.damageMult += 2
        app.vampirism -= 1 / 3
        text('+200%', 50, 290, rgb(125, 10, 75), 30)
    elif index == 11:  # inspire
        app.health += 1
        app.damage += 1
        if app.health > app.maxHealth:
            app.health = app.maxHealth
        text('+1', 200, 365, rgb(10, 150, 50))
        text('+' + str(app.damageMult), 50, 290, rgb(200, 50, 50))
    elif index == 13:  # shield bash
        app.damage += app.block + app.persistantBlock
        text('+' + str((app.block + app.persistantBlock) * app.damageMult), 50, 290, rgb(200, 50, 50))
    elif index == 14:  # perilous strike
        if chance(75):
            app.damage += 5
            text('+' + str(5 * app.damageMult), 50, 290, rgb(200, 50, 50))
            spark = Image(urls[randrange(25, 27)], card.centerX, card.centerY, align='center')
        else:
            subtractHealth(5, False)
            spark = Image(urls[randrange(27, 29)], card.centerX, card.centerY, align='center')

        spark.rotateAngle = card.rotateAngle
        rescaleImage(spark, 0.3)
        attackEffects.add(spark)
    elif index == 15:  # dice
        num = randrange(1, 7)
        if num == 1:
            app.damageMult -= 1
            text('-100%', 50, 270, rgb(255, 200, 200), 30)
            spark = Image(urls[randrange(27, 29)], card.centerX, card.centerY, align='center')
            spark.rotateAngle = card.rotateAngle
            rescaleImage(spark, 0.3)
            attackEffects.add(spark)
        else:
            text(num, card.centerX, card.centerY, rgb(10, 50, 200), 20)
        app.damage += num
        text('+' + str(num * app.damageMult), 50, 290, rgb(200, 50, 50))
    elif index == 16:  # venom
        app.venom += 0.02
        text(str(int(app.venom * 100)) + '%', 200, 190, rgb(100, 200, 25), 30)
    elif index == 17:  # brambles
        app.brambles += 0.5
        # add a text effect & label here pls
    elif index == 18:  # smite
        damage = (5 - int((enemy.health / enemy.maxHealth) * 5))
        app.damage += damage
        text('+' + str(damage * app.damageMult), 50, 290, rgb(200, 50, 50))
    else:  # sacrifice
        mult = app.block * 2
        app.damageMult += mult
        text('+' + str(int(mult * 100)) + '%', 50, 290, rgb(255, 200, 50), 30)
        text('-' + str(app.block), 350, 290, rgb(150, 100, 255))

        app.block = 0

    # makes the card dim & unobtrusive
    card.opacity = 25
    card.toBack()

    # updates visuals
    updateHealthBar(enemyHealthBar, enemyHealthBarBG, enemyHealthLabel, enemy.health, enemy.maxHealth)
    updateHealthBar(healthBar, healthBarBG, healthLabel, app.health, app.maxHealth)
    updateIndicators()


### events

def onMouseMove(x, y):
    # saves the mouse coords to be used in other places
    app.mx = x
    app.my = y


def onMouseRelease(x, y):
    if len(info) == 0 and enemy.attacking == False and app.play == True:
        card = playerCards.hitTest(x, y)
        if card != None and card.opacity != 25 and dim.visible == False:  # if you click on a valid card, play it
            playCard(card)
        elif enemy.contains(x, y):  # if you click on the enemy, end your turn
            endTurn()
        elif skipButton.contains(app.mx, app.my):  # if you click the skip button, skip the card swap process
            dim.visible = False
            cardInfo.clear()
            skipButton.visible = False
            rewards.clear()
            rewardsCovers.clear()

            # resets & buffs the enemy
            enemy.maxHealth = rounded((enemy.maxHealth + 2) * 1.1)
            enemy.health = enemy.maxHealth
            updateHealthBar(enemyHealthBar, enemyHealthBarBG, enemyHealthLabel, enemy.health, enemy.maxHealth)

            texts.clear()
            attackEffects.clear()

            newHand()

        trash = display.hitTest(x, y)
        if trash != None and len(deck) > 10:  # if you click on a card to trash, delete it and continue
            deck.remove(trash.type)
            display.remove(trash)
            updateDisplay()

            # resets & buffs the enemy
            enemy.maxHealth = rounded((enemy.maxHealth + 2) * 1.1)
            enemy.health = enemy.maxHealth
            updateHealthBar(enemyHealthBar, enemyHealthBarBG, enemyHealthLabel, enemy.health, enemy.maxHealth)

            texts.clear()
            attackEffects.clear()

            newHand()  # delete card

        reward = rewards.hitTest(x, y)
        if reward != None:  # adds clicked reward card to your deck
            deck.append(reward.type)

            for i in rewards:
                fade.add(i)
            for i in rewardsCovers:
                fade.add(i)
            rewards.clear()
            rewardsCovers.clear()

            updateDisplay()
            display.visible = True
            skipButton.visible = False


def onKeyPress(key):
    if app.play == True:
        if len(info) > 0:  # clears info screen if you press anything
            info.clear()
        elif dim.visible == False and enemy.attacking == False and key == 'space' and enemy.health != 0:  # ends turn if you press space
            print("ending with: ", app.brambleDamage)
            endTurn()


def onStep():
    if len(info) == 0:  # if the info screen is down
        app.frames += 1  # updates the amount of frames (for sine waves)
        hoverCard = playerCards.hitTest(app.mx, app.my)
        hoverReward = rewards.hitTest(app.mx, app.my)

        hoverCover = rewardsCovers.hitTest(app.mx, app.my)
        if hoverCover != None and hoverCover.centerY == 150:  # if you hover over a flipped reward card, update its custom properties
            hoverCover.dormant = False
            hoverCover.nativeX = hoverCover.centerX
            hoverCover.nativeY = hoverCover.centerY

        if enemy.health > 0:  # updates the card label
            cardLabel.centerY = 200
            cardLabel.size = 18
            if hoverCard != None:
                cardLabel.value = hoverCard.type
                if hoverCard.mimic == True:
                    cardLabel.fill = cardColors['Mimic']
                else:
                    cardLabel.fill = cardColors[hoverCard.type]
            else:
                cardLabel.value = ''
        elif len(rewards) + len(rewardsCovers) > 0:  # if you are on the new card selection screen
            if hoverReward != None:
                cardLabel.fill = cardColors[hoverReward.type]
            else:
                cardLabel.fill = rgb(160, 255, 140)
            cardLabel.centerY = 60
            cardLabel.size = 20
            if hoverReward != None:
                if cardLabel.value != hoverReward.type:
                    cardInfo.clear()
                    cardLabel.value = hoverReward.type
                    infoList = split(cardsInfo[hoverReward.type])
                    y = 240
                    for line in infoList:
                        cardInfo.add(
                            Label(line, 200, y, size=15, font='montserrat', bold=True, fill=rgb(225, 225, 255)))
                        y += 20
            else:
                cardLabel.value = 'Pick a card'
                cardInfo.clear()
        elif display.visible == True:  # if you are on the trash selection screen
            if len(cardInfo) > 0:
                cardInfo.clear()
            cardLabel.fill = rgb(200, 50, 100)
            cardLabel.centerY = 90
            cardLabel.size = 20
            hoverItem = display.hitTest(app.mx, app.my)
            if hoverItem != None:
                cardLabel.value = 'Remove ' + str(hoverItem.type) + '?'
            else:
                cardLabel.value = 'Remove a card'

        if dim.visible == False:  # animates cards when hovered
            for i in playerCards:
                if i != hoverCard:
                    if i.centerY < i.nativeY:
                        i.centerY += 3
                elif i.centerY > i.nativeY - 15 and i.opacity != 25:
                    i.centerY -= 5
                    i.toFront()

                if i.type == 'Curse':
                    # (health-allDamage)/maxHealth <= potentialCurse
                    venomDamage = math.ceil(enemy.maxHealth * app.venom)
                    playerDamage = app.damage * app.damageMult
                    if i.opacity != 25 and (enemy.health - (
                            playerDamage + venomDamage)) / enemy.maxHealth <= app.potentialCurse and enemy.health > 0:
                        i.rotateAngle = (5 * dsin(20 * app.frames)) + i.angle
                    else:
                        i.rotateAngle = i.angle

        if display.visible == True:  # animates trash icons
            if len(display) == 11:  # makes the trash icons shake when they are hovered
                hover = display.hitTest(app.mx, app.my)
                for i in display:
                    i.rotateAngle = 0
                if hover != None:
                    hover.rotateAngle = (15 * dsin(40 * app.frames))
            elif enemy.opacity > 0:  # makes the trash icons fade out
                if display.opacity > 0:
                    display.opacity -= 10
                else:
                    display.opacity = 100
                    display.visible = False
                    dim.visible = False
                    cardInfo.clear()

        x = skipButton.centerX
        y = skipButton.centerY
        if skipButton.contains(app.mx, app.my):  # makes the skip button big when hovered
            skipButton.width = 90
            skipButton.height = 90
        else:
            skipButton.width = 75
            skipButton.height = 75
        skipButton.centerX = x
        skipButton.centerY = y

        # animates enemy
        enemy.centerY = 10 * dsin(4 * app.frames) + 90
        enemy.centerX = 10 * dsin(2 * app.frames) + 200
        if enemy.health > 0:
            enemy.opacity = 10 * dsin(5 * app.frames) + 90

        # animates card flip
        for i in rewardsCovers:
            if i.dormant == False:
                if i.width >= 5:
                    i.width *= 0.6
                    i.centerX = i.nativeX
                else:
                    reward = Image(urls[cards.index(i.type)], i.centerX, i.centerY, align='center')
                    rescaleImage(reward, 0.25)
                    reward.width = i.width
                    reward.type = i.type
                    reward.nativeX = i.nativeX
                    reward.nativeY = 150

                    rewards.add(reward)
                    rewardsCovers.remove(i)
            if i.opacity < 100:
                i.opacity += 10
                i.centerY -= 25
        for i in rewards:
            # makes it flip
            if i.width < 75:
                i.width *= 1.5
            else:
                i.width = 76
                i.centerY = (10 * dsin(5 * (app.frames + ((i.centerX / 100) - 2) * 10))) + 150

            i.centerX = i.nativeX

            # does hover effect
            x = i.centerX
            y = i.centerY
            if i == hoverReward:
                scale = 0.3
            else:
                scale = 0.25

            i.width = 304 * scale
            i.height = 432 * scale
            i.centerX = x
            i.centerY = y

        # attack effects & enemy attack
        if dim.visible == False:
            # animates attack effects
            if len(attackEffects) > 0:
                for i in attackEffects:
                    if i.opacity != 0:
                        i.opacity -= 10
                        if i.opacity == 0:
                            attackEffects.remove(i)
                    else:
                        if chance(20):
                            i.opacity = 100
                            enemyCover.opacity = 100
            # enemy attack
            elif enemy.attacking == True:
                if chance(50 + (app.difficulty * 10)):
                    enemyAttackDamage = randrange(1, 4 + math.floor(app.difficulty / 2))
                    # text(enemyAttackDamage, 200, 80, rgb(255, 200, 200), 30) ##### FIX ME ######
                    subtractHealth(enemyAttackDamage)
                    # does brambles
                    if app.brambles > 0:
                        app.brambleDamage = math.ceil(enemyAttackDamage * app.brambles)
                        # prevHealth = enemy.health
                        # enemy.health -= brambles
                        # app.totalDealt += prevHealth-enemy.health
                        # intensity = rounded((brambles/enemy.maxHealth)*10)
                        # if intensity < 1:
                        #     intensity = 1
                        # elif intensity > 10:
                        #     intensity = 10
                        # hurt(intensity, randrange(27, 29))
                        # text('-' + str(brambles), 200, 175, rgb(200, 100, 50), 30)
                        # if enemy.health <= 0:
                        #     enemy.health = 0
                        #     endTurn()
                        # else:
                        #     updateHealthBar(enemyHealthBar, enemyHealthBarBG, enemyHealthLabel, enemy.health, enemy.maxHealth)
                else:
                    text('MISSED', 200, 350, rgb(100, 200, 50), 20)

                enemy.attacking = False
                resetStats()

        # makes enemy red when hurt
        if enemyCover.opacity > 0:
            enemyCover.opacity -= 20
            enemyCover.centerX, enemyCover.centerY = enemy.centerX, enemy.centerY

        # makes fade group move up slowly and fade away
        for i in fade:
            if i.opacity < 10:
                fade.remove(i)
            else:
                i.opacity -= 10
            i.centerY -= 1

        # heartbeat effect when you get low on health points
        speed = 11 - app.health
        if speed > 0:
            num = 5 * dsin(speed * app.frames) + tint.baseOpacity
            if num > 0:
                tint.opacity = num
            else:
                tint.opacity = 0
        else:
            tint.opacity = 0

        # makes gameover screen fade in
        if app.play == False:
            if lose.opacity < 100:
                lose.opacity += 5

        if dim.visible == False:  # animates texts
            for i in texts:
                i.centerY -= 0.75
                i.size *= 0.95
                i.opacity -= 2
                if i.opacity <= 0:
                    texts.remove(i)


### xtra

def text(value, x, y, color='black', size=25):
    # makes writing little bit of info easier
    texts.add(Label(value, x, y, bold=True, font='orbitron', fill=color, size=size))


def updateHealthBar(bar, barBG, label, health, maxHealth):
    # updates a health bar by using the variables provided

    if health < 0:
        health = 0
    newPercent = (health / maxHealth) * barBG.width
    if newPercent <= 0:
        newPercent = 0.01
    elif newPercent > barBG.width:
        newPercent = barBG.width
    bar.width = newPercent

    label.value = ((str(health) + '/' + str(maxHealth)).replace('.0', '')) + ' (' + str(
        rounded((health / maxHealth) * 100)) + '%)'


def updateIndicators():
    # updates the attack, attack multiplier, & block indicators

    # updates damage & block labels
    if enemy.health > 0:
        venomDamage = math.ceil(enemy.maxHealth * app.venom)
        playerDamage = (app.damage * app.damageMult)
        if app.curse > 0 and (enemy.health - (playerDamage + venomDamage)) / enemy.maxHealth <= app.curse:
            app.damage = 999
            app.damageMult = 1
        attackLabel.value = str(app.damage * app.damageMult).replace('.0', '')
        blockLabel.value = str(app.block).replace('.0', '')
    else:
        attackLabel.value = '-'
        blockLabel.value = '-'

    # updates attack multiplier label
    damageMultLabel.value = str(app.damageMult * 100) + '%'

    # colors attack label depending on if you can defeat the enemy
    if app.damage * app.damageMult >= enemy.health:
        attackLabel.fill = rgb(200, 50, 50)
    else:
        attackLabel.fill = rgb(0, 0, 0)


def updateDisplay():
    # updates and draws the display group on screen (for selecting a card to trash)

    display.clear()
    deckCopy = deck.copy()

    deckCopy.sort()

    # draws
    loop = 0
    for y in range(150, math.ceil(len(deckCopy) / 5) * 75 + 76, 75):
        for x in range(75, 326, 60):
            if len(deckCopy) - 1 >= loop:
                url = urls[cards.index(deckCopy[loop])]
                item = Image(url, x, y, align='center')
                rescaleImage(item, 0.15)
                item.type = deckCopy[loop]
                display.add(item)

                loop += 1


def subtractHealth(amount, kill=True):
    preHealth = app.health
    amount -= app.block
    if amount > 0:
        app.health -= amount
        value = '-' + abrv(amount)
        if enemy.attacking == False:
            url = randrange(27, 29)
            angle = randrange(0, 360, 90)
        else:
            url = 30
            angle = 0
        spark = Image(urls[url], 200 + randrange(-25, 26), 360, align='center', opacity=100)
        percent = amount / app.maxHealth
        rescaleImage(spark, percent * 0.3 + 0.2)
        spark.rotateAngle = angle
        attackEffects.add(spark)
        text(value, 200, 350, rgb(200, 50, 50), 20)
    else:
        text('BLOCKED', 200, 350, rgb(100, 200, 50), 20)
    if kill == False:
        if app.health < 1:
            app.health = 1
    else:
        if app.health < 0:
            app.health = 0

    dealt = preHealth - app.health
    app.totalPain += dealt

    if app.health <= 0:
        app.play = False
        lose.add(Rect(0, 0, 400, 400, fill=rgb(10, 50, 100)))
        lose.add(Label('Game Over', 200, 100, bold=True, size=30, font='montserrat', fill=rgb(215, 50, 50)))
        lose.add(Label('You beat ' + str(abrv(app.enemies)) + ' foes!', 200, 150, bold=True, size=20, font='montserrat',
                       fill=rgb(215, 100, 100)))
        lose.add(
            Label('You dealt ' + str(abrv(app.totalDealt)) + ' damage', 200, 175, bold=True, size=20, font='montserrat',
                  fill=rgb(215, 100, 100)))
        lose.add(Label('You received ' + str(abrv(app.totalPain)) + ' damage', 200, 200, bold=True, size=20,
                       font='montserrat', fill=rgb(215, 100, 100)))

        lose.opacity = 0

    updateHealthBar(healthBar, healthBarBG, healthLabel, app.health, app.maxHealth)

    num = 11 - ((app.health / app.maxHealth) * 20)
    if num < 0:
        num = 0

    tint.baseOpacity = num


def hurt(intensity=1, url=-1):
    if url == -1:
        url = randrange(25, 27)
    for i in range(intensity):
        spark = Image(urls[url], enemy.centerX + randrange(-25, 26), enemy.centerY + randrange(-50, 51), align='center',
                      opacity=0)
        rescaleImage(spark, (randrange(5, 10) + intensity) / 50)
        spark.rotateAngle = randrange(0, 360, 90)
        attackEffects.add(spark)


def resetStats():
    app.damage = app.persistantDamage
    app.block = app.persistantBlock
    app.damageMult = 1
    app.vampirism = 0
    app.curse = 0
    damageMultLabel.value = '100%'
    updateIndicators()


### setup

skipButton.visible = False
display.visible = False

loadTextures()
answer = app.getTextInput('Enter the difficulty level (1-5)')
while not (answer.isdigit() and int(answer) <= 5 and int(answer) >= 1):  # forces user to answer with an integer 1-5
    answer = app.getTextInput('Enter the difficulty level (1 is the easiest & 5 is the hardest)')
app.difficulty = int(answer)
rescaleImage(skipButton, 0.2)
rescaleImage(attackIndicator, 0.2)
rescaleImage(blockIndicator, 0.2)
rescaleImage(enemy, 0.35)
rescaleImage(enemyCover, 0.35)
updateHealthBar(enemyHealthBar, enemyHealthBarBG, enemyHealthLabel, enemy.health, enemy.maxHealth)
updateHealthBar(healthBar, healthBarBG, healthLabel, app.health, app.maxHealth)
deal()
updateDisplay()

cmu_graphics.run()