import cmu_graphics
from cmu_graphics import *
from time import sleep

app.background = rgb(25, 50, 100)
app.alphabet = 'abcdefghijklmnopqrstuvwxyz'
app.nums = '1234567890'
app.special = '!@#$%^&*'
app.length = 12
app.caps = True
app.sliding = False

border = Rect(-10, -10, 420, 420, fill=None, border=rgb(25, 50, 100), borderWidth=30)

genButton = Group(
    Rect(200, 275, 100, 40, align='center', fill=rgb(125, 255, 150)),
    Circle(150, 275, 20, fill=rgb(125, 255, 150)),
    Circle(250, 275, 20, fill=rgb(125, 255, 150))
)
genText = Label('GENERATE', 200, 275, bold=True, font='montserrat', size=20, fill=rgb(255, 255, 255))

printButton = Group(
    Rect(200, 325, 100, 40, align='center', fill=rgb(125, 255, 150)),
    Circle(150, 325, 20, fill=rgb(125, 255, 150)),
    Circle(250, 325, 20, fill=rgb(125, 255, 150))
)
printText = Label('PRINT', 200, 325, bold=True, font='montserrat', size=30, fill=rgb(255, 255, 255))

Label('Special characters', 70, 20, fill=rgb(115, 235, 255), bold=True)
switch1 = Group(
    Rect(50, 30, 40, 20, fill=rgb(125, 255, 150)),
    Circle(50, 40, 10, fill=rgb(125, 255, 150)),
    Circle(90, 40, 10, fill=rgb(125, 255, 150)),
    Circle(90, 40, 7, fill='white')
)

Label('Numbers', 200, 20, fill=rgb(115, 235, 255), bold=True)
switch2 = Group(
    Rect(180, 30, 40, 20, fill=rgb(125, 255, 150)),
    Circle(180, 40, 10, fill=rgb(125, 255, 150)),
    Circle(220, 40, 10, fill=rgb(125, 255, 150)),
    Circle(220, 40, 7, fill='white')
)

Label('Capital letters', 330, 20, fill=rgb(115, 235, 255), bold=True)
switch3 = Group(
    Rect(310, 30, 40, 20, fill=rgb(125, 255, 150)),
    Circle(310, 40, 10, fill=rgb(125, 255, 150)),
    Circle(350, 40, 10, fill=rgb(125, 255, 150)),
    Circle(350, 40, 7, fill='white')
)

slide = Group(
    Line(25, 100, 375, 100, lineWidth=10, fill=rgb(125, 255, 150)),
    Circle(25, 100, 5, fill=rgb(125, 255, 150)),
    Circle(375, 100, 5, fill=rgb(125, 255, 150))
)

slider = Group(
    Line(200, 90, 200, 110, lineWidth=8, fill=rgb(255, 255, 255)),
    Circle(200, 90, 4, fill=rgb(255, 255, 255)),
    Circle(200, 110, 4, fill=rgb(255, 255, 255)),
)
slideLabel = Label('Length: 20', 200, 75, bold=True, fill=rgb(115, 235, 255))

securityText = Label('Security Rating: ', 200, 155, fill=rgb(115, 235, 255), bold=True)
Line(125, 170, 275, 170, lineWidth=8, fill=rgb(255, 150, 175))
Circle(125, 170, 4, fill=rgb(255, 150, 175))
Circle(275, 170, 4, fill=rgb(255, 150, 175))
securitySlide = Group(
    Line(125, 170, 130, 170, lineWidth=8, fill=rgb(125, 255, 150)),
    Circle(130, 170, 4, fill=rgb(125, 255, 150)),
    Circle(125, 170, 4, fill=rgb(125, 255, 150))
)

passwordLabel = Group(
    Label('Click GENERATE to generate a password', 200, 200, font='montserrat', size=15, fill=rgb(50, 150, 255),
          bold=True))


def generate(length):
    passwordLabel.clear()
    passwordLabel.add(Label('Loading...', 200, 200, size=20, fill=rgb(255, 255, 175), bold=True, font='montserrat'))

    sleep(0)
    password = ''

    for i in range(length):
        if app.caps == True:
            letter = choice(app.alphabet + app.nums + app.special + app.alphabet.upper())
        else:
            letter = choice(app.alphabet + app.nums + app.special)

        if letter.isupper():
            color = rgb(50, 150, 255)
        elif letter.isdigit():
            color = rgb(50, 255, 215)
        elif letter.isalpha() == False:
            color = rgb(255, 50, 215)
        else:
            color = rgb(235, 255, 150)

        password += str(letter)

        character = Label(letter, passwordLabel.children[len(passwordLabel) - 1].right + 8, 150, fill=color, size=20)
        character.bottom = 210

        passwordLabel.add(character)

    passwordLabel.remove(passwordLabel.children[0])

    while passwordLabel.hitsShape(border):
        loop = 0
        for i in passwordLabel:
            i.size -= 1
            i.centerX -= loop
            loop += 1
        passwordLabel.centerX = 200

    passwordLabel.centerX = 200


def onMousePress(x, y):
    if genButton.contains(x, y):
        generate(app.length)
    elif printButton.contains(x, y):
        password = ''
        for i in passwordLabel:
            password += i.value
        print(password)

    elif switch1.contains(x, y):
        if switch1.children[0].fill == rgb(125, 255, 150):
            switch1.children[0].fill = rgb(255, 125, 150)
            switch1.children[1].fill = rgb(255, 125, 150)
            switch1.children[2].fill = rgb(255, 125, 150)
            switch1.children[3].centerX = 50
            app.special = ''
        else:
            switch1.children[0].fill = rgb(125, 255, 150)
            switch1.children[1].fill = rgb(125, 255, 150)
            switch1.children[2].fill = rgb(125, 255, 150)
            switch1.children[3].centerX = 90
            app.special = '!@#$%^&*'

    elif switch2.contains(x, y):
        if switch2.children[0].fill == rgb(125, 255, 150):
            switch2.children[0].fill = rgb(255, 125, 150)
            switch2.children[1].fill = rgb(255, 125, 150)
            switch2.children[2].fill = rgb(255, 125, 150)
            switch2.children[3].centerX = 180
            app.nums = ''
        else:
            switch2.children[0].fill = rgb(125, 255, 150)
            switch2.children[1].fill = rgb(125, 255, 150)
            switch2.children[2].fill = rgb(125, 255, 150)
            switch2.children[3].centerX = 220
            app.nums = '1234567890'

    elif switch3.contains(x, y):
        if switch3.children[0].fill == rgb(125, 255, 150):
            switch3.children[0].fill = rgb(255, 125, 150)
            switch3.children[1].fill = rgb(255, 125, 150)
            switch3.children[2].fill = rgb(255, 125, 150)
            switch3.children[3].centerX = 310
            app.caps = False
        else:
            switch3.children[0].fill = rgb(125, 255, 150)
            switch3.children[1].fill = rgb(125, 255, 150)
            switch3.children[2].fill = rgb(125, 255, 150)
            switch3.children[3].centerX = 350
            app.caps = True

    elif slide.contains(x, y) or slider.contains(x, y):
        app.sliding = True
        slider.fill = rgb(255, 255, 175)
    else:
        slider.fill = rgb(255, 255, 255)


def onMouseRelease(x, y):
    app.sliding = False


def onMouseMove(x, y):
    if genButton.contains(x, y):
        genText.fill = rgb(255, 255, 175)
        genButton.width = 145
        genButton.height = 45
        genButton.centerX = 200
        genButton.centerY = 275
    else:
        genText.fill = rgb(255, 255, 255)
        genButton.width = 140
        genButton.height = 40
        genButton.centerX = 200
        genButton.centerY = 275

    if printButton.contains(x, y):
        printText.fill = rgb(255, 255, 175)
        printButton.width = 145
        printButton.height = 45
        printButton.centerX = 200
        printButton.centerY = 325
    else:
        printText.fill = rgb(255, 255, 255)
        printButton.width = 140
        printButton.height = 40
        printButton.centerX = 200
        printButton.centerY = 325

    if switch1.contains(x, y):
        switch1.children[3].fill = rgb(255, 255, 175)
    else:
        switch1.children[3].fill = rgb(255, 255, 255)

    if switch2.contains(x, y):
        switch2.children[3].fill = rgb(255, 255, 175)
    else:
        switch2.children[3].fill = rgb(255, 255, 255)

    if switch3.contains(x, y):
        switch3.children[3].fill = rgb(255, 255, 175)
    else:
        switch3.children[3].fill = rgb(255, 255, 255)

    if slide.contains(x, y) or slider.contains(x, y):
        slider.fill = rgb(255, 255, 175)
    else:
        slider.fill = rgb(255, 255, 255)


def onMouseDrag(x, y):
    if app.sliding == True:
        if x < 50:
            x = 50
        elif x > 350:
            x = 350
        slider.centerX = x
        slideLabel.value = 'Length: ' + str(x // 10)
        app.length = x // 10


def onStep():
    security = (app.length * 2)

    if app.caps == True:
        security += 15
    if app.nums != '':
        security += 5
    if app.special != '':
        security += 10

    security -= 10 - (security / 10)

    securitySlide.children[0].x2 = (security * 1.5) + 125
    securitySlide.children[1].centerX = (security * 1.5) + 125

    securitySlide.fill = rgb(255 - security * 1.30, (security * 1.05) + 150, security * 1.5)

cmu_graphics.run()