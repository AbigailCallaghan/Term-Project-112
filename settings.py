from cmu_graphics import * 
import math, random
from player import Player
from raycaster import Raycaster
from course import Course

#using this https://www.youtube.com/watch?v=E18bSJezaUE tutorial for basic raycaster 
#it's in pygame so i'm translating it to cmu graphics
# i will be rewriting most of the code, I am just getting the basics so the code right now follows the tutorial pretty closely
def onAppStart(app):
    app.potentialMaps = {0: ['straight', 9, 5, 5], 1:['curved up', 5, 9, -3]}
    # easy is more downhill and has wider areas
    #hard has increased speed
    app.difficultyLevels = {'easy': {'length range': (4, 8), 'width range': (4, 7), 'slope range': (-5, 5)},
                            'medium': {'length range': (2, 8), 'width range': (2, 5), 'slope range': (-10, 10)},
                            'hard': {'length range': (1, 8), 'width range': (1, 4), 'slope range': (-15, 15)},
                            'chaos':{'length range': (1, 8), 'width range': (1, 7), 'slope range': (-15, 15)}}
    app.playerChars = [50, .05, 100]
    app.difficultyKey = 'easy'
    app.tileSize = 50
    app.course = Course()
    app.mapKey = 0
    app.nextBottom =0
    app.player = Player(app, app.course)
    createMap(app)
    app.rows = len(app.course.map)
    app.cols = len(app.course.map[0])
    app.width = app.cols * app.tileSize
    app.height = app.rows *app.tileSize
    app.FOV = 60 * (math.pi / 180)
    app.resilution = 1
    app.rayAmount = app.width // app.resilution
    steeringWheelDimensions(app)
    app.raycaster = Raycaster(app.player, app.course)
    app.pY = app.height - 50
    app.lineLength = 30
    app.intro = False
    app.drawMap  = False
    app.manual = False
    app.loadingScreen = True
    app.mainLabelKey = 0
    app.font = 'orbitron'
    app.stepsPerSecond = 30
    app.pushZone = True

def redrawAll(app):
    if app.loadingScreen == True:
        if app.intro == True: 
            drawIntroAnimation(app)
        else: 
            drawLoadingScreen(app, app.mainLabelKey)
    else:
        drawRect(0, 0, app.width, app.height, fill = 'black')
        if app.drawMap == True:
            app.course.drawMap(app)
            app.player.drawPlayer(app)
            app.raycaster.drawAllRays(app)
        else:
            app.raycaster.drawAllRays(app)
            drawSideBar(app)
            drawSteeringWheel(app)

def steeringWheelDimensions(app):
    distanceFromSides = app.width/6
    app.steeringWheelHeight = 75
    distanceFromGround = app.height - app.steeringWheelHeight
    app.steeringWheelLeftCordinates = (distanceFromSides, distanceFromGround + 10)
    app.steeringWheelRightCordinates = (app.width - distanceFromSides, distanceFromGround + 10)

def drawSideBar(app):
    fontColor = 'chartreuse'
    labelLeft = 20
    drawRect(labelLeft -10, 10, 250, 110, fill = 'dimGray', border = fontColor)
    drawLabel('Player status', 135, 20, fill = fontColor, size = 16, font = app.font, bold = True)
    trueVelocity = app.player.velocity if app.player.velocity >=0 else 0
    velocity = roundToDeci(trueVelocity, 2)
    drawLabel(f'Velocity: {velocity} m/s', labelLeft, 40, font = app.font, fill = fontColor, align = 'left')
    sectionType = app.potentialMaps[app.mapKey][0]
    slope = app.potentialMaps[app.mapKey][3]
    nextSectionType = app.potentialMaps[app.mapKey + 1][0]
    nextSlope = app.potentialMaps[app.mapKey + 1][3]
    drawLabel(f'Current section {sectionType} with slope {slope}', labelLeft, 60, font = app.font, fill = fontColor, align = 'left')
    drawLabel(f'Next section {nextSectionType} with slope {nextSlope}', labelLeft, 80, font = app.font, fill = fontColor, align = 'left')
    drawLabel(f'Total distance: {app.player.totalDistance}m', labelLeft, 100, font = app.font, fill = fontColor, align = 'left')
    
def drawSteeringWheel(app):
    steeringWheelColor = 'darkSlateGray'
    drawRect(app.steeringWheelLeftCordinates[0], app.steeringWheelLeftCordinates[1]-10, app.width - 2* app.steeringWheelLeftCordinates[0], 20, fill = steeringWheelColor)
    drawCircle(app.steeringWheelLeftCordinates[0],  app.steeringWheelLeftCordinates[1], 10, fill = steeringWheelColor)
    drawCircle(app.width - app.steeringWheelLeftCordinates[0], app.steeringWheelLeftCordinates[1], 10, fill = steeringWheelColor)
    drawRect(app.width/2, app.steeringWheelLeftCordinates[1] + 20, 30, app.steeringWheelHeight, fill = steeringWheelColor, align = 'center')

def onStep(app):
    #app.player.move()
    app.raycaster.castAllRays(app)
    app.player.turnDirection = 0
    if app.nextBottom != 0:
        switchMaps(app)
    if app.manual == False:
        app.player.move(app)

def angleInUnitCircle(angle):
    angle = angle % (2 * math.pi)
    if angle < 0:
        angle = (2 * math.pi) + angle
    return angle

def onKeyPress(app, key):
    if app.loadingScreen == True:
        if key == 'enter' and app.mainLabelKey == 1:
            app.loadingScreen = False
            app.player = Player(app, app.course)
            app.raycaster = Raycaster(app.player, app.course)
            createMap(app)

    app.player.onKeyPress(app,key)
    app.raycaster.castAllRays(app)
    if key == 'm': 
        app.drawMap = not app.drawMap


def onMousePress(app, mouseX, mouseY):
    if app.loadingScreen == True:
        loadingScreenButtonPress(app, app.mainLabelKey, mouseX, mouseY)
    if app.manual == False:
        app.player.onMousePress(app, mouseX, mouseY)

def createMap(app):
    nextPartial = generatePartialMap(app)
    app.potentialMaps[app.mapKey + 2] = nextPartial
    
    if app.mapKey + 1 < len(app.potentialMaps):
        mapOneDirection = app.potentialMaps[app.mapKey][0]
        mapTwoDirection = app.potentialMaps[app.mapKey + 1][0]
        mapOneLength = app.potentialMaps[app.mapKey][1]
        mapTwoLength = app.potentialMaps[app.mapKey + 1][1]
        mapOneWidth = app.potentialMaps[app.mapKey][2]
        mapTwoWidth = app.potentialMaps[app.mapKey + 1][2]
        app.nextBottom = mapOneLength +1
        app.course.combineMaps(app, mapOneDirection, mapOneLength, mapOneWidth, mapTwoDirection, mapTwoLength, mapTwoWidth)
        #need to reset player position for y, x is fine
        placeHolderX = app.player.x
        print(app.course.map)
        app.player.y, app.player.x = app.course.findClosestWhiteSpace(app, 'down')
        if app.course.map[int(app.player.y//app.tileSize)][int(placeHolderX//app.tileSize)] == 0:
            app.player.x = placeHolderX
        

def generatePartialMap(app):
    nextDirection = 'curved up' if app.mapKey % 2 == 1 else 'straight'
    difficultyLevels = app.difficultyLevels[app.difficultyKey]
    lengthRange = difficultyLevels['length range']
    widthRange = difficultyLevels['width range']
    slopeRange = difficultyLevels['slope range']
    lengthLo, lengthHi = lengthRange[0], lengthRange[1]
    widthLo, widthHi = widthRange[0], widthRange[1]
    slopeLo, slopeHi = slopeRange[0], slopeRange[1]
    currentLength = app.potentialMaps[app.mapKey][1]
    currentWidth = app.potentialMaps[app.mapKey][2]
    nextLength = addToFourteen(random.randint(lengthLo, lengthHi),currentLength, lengthLo, lengthHi)
    nextWidth = addToFourteen(random.randint(widthLo, widthHi), currentWidth, widthLo, widthHi)
    slope = random.randint(slopeLo, slopeHi)
    print([nextDirection, nextLength, nextWidth, slope])
    return [nextDirection, nextLength, nextWidth, slope]

def addToFourteen(val1, val2, lo, hi):
    if val1 + val2 <= 13:
        return val1
    else:
        return addToFourteen(random.randint(lo, hi),val2, lo, hi)

def switchMaps(app):
    trueYCoord = int(app.player.y//app.tileSize)
    if trueYCoord < (15 - (app.nextBottom)):
        app.mapKey +=1
        createMap(app)
        app.raycaster.castAllRays(app)

def drawIntroAnimation(app):
    pass

def drawLoadingScreen(app, mainLabelKey):
    #gradient = gradient('black', rgb(0, 0, 25), 'midnightBlue', 'darkSlateGray', 'dimGray', start='top')
    drawRect(0, 0, app.width, app.height, 
             fill =  gradient('black', rgb(0, 0, 25), 'midnightBlue', 'darkSlateGray', 'dimGray', start='top'))
    drawLabel('Loading Screen', app.width/2, 75, size = 50, bold = True, fill = 'white')
    mainLabel = {0: 'Choose your difficulty', 1: 'Choose your characteristics'}
    drawLabel(mainLabel[mainLabelKey], app.width/2, 150, size = 25, bold = True, fill = 'white')
    drawLoadingScreenOption(app, app.mainLabelKey)

def drawLoadingScreenOption(app, mainLabelKey):
    backGroundColor =  rgb(0, 0, 25)
    if mainLabelKey == 0:
        section = (app.width - 60)//4
        potentialLabels = ['Easy', 'Medium', 'Hard', 'Chaos']
        potentialUrls=['https://streak.club/img/Mix1c2VyX2NvbnRlbnQvdXBsb2Fkcy9pbWFnZS8zMjYxOC5wbmc=/original/cMTlu6.png']
        #black hole image: https://streak.club/p/29287/black-hole-by-mentalpop
        #voyager image: https://www.reddit.com/r/PixelArt/comments/c83okd/voyager/
        #planet image: https://www.reddit.com/r/PixelArt/comments/16zw3mh/pixel_art_of_saturn_orginal_picture_from_nasa_on/
        #star image: https://rare-gallery.com/uploads/posts/1102198-illustration-video-games-pixel-art-planet-space-Earth-pixels-circle-atmosphere-universe-indie-games-quasars-Steredenn-screenshot-computer-wallpaper-atmosphere-of-earth-.png
        for i in range(4):
            labelText = potentialLabels[i]
            drawRect(i*section + 30, 200, section - 10, app.height - 500, fill = backGroundColor, border = 'lightGrey')
            drawLabel(f'{labelText}', i*section + 30 + section/2, 250, size = 25, bold = True, fill = 'white')
            drawImage(potentialUrls[0], i*section + 40, 300, width = (section -30), height = (section -30))
    if mainLabelKey == 1:
        potentialLabels = ['Mass', 'Friction Coeffishent', 'Push Strength']
        backLabels = ['kg', '', 'N']
        for i in range(3):
            heightLevel = i*100
            drawRect(100, heightLevel + 300, app.width - 200, 80, fill = backGroundColor, border = 'lightGrey')
            
            drawLabel(f'{potentialLabels[i]}: {app.playerChars[i]} {backLabels[i]}', 
                      app.width/2, heightLevel + 340, bold = True, fill = 'white', size = 25)
            drawCircle(150, heightLevel + 340, 20, fill = 'red')
            drawCircle(150 + app.width-300, heightLevel + 340, 20, fill = 'green')
        drawLabel('Press the green button to increase value',
                  app.width/2, 200, size = 20, bold = True, fill = 'white')
        drawLabel('Press the red button to decrease value', app.width/2, 225, size = 20, bold = True, fill = 'white')
        drawLabel('Press enter to start the game', app.width/2, 250, size = 20, bold = True, fill = 'white')

def loadingScreenButtonPress(app, mainLabelKey, mouseX, mouseY):
    if mainLabelKey == 0:
        section = (app.width - 60)//4
        trueX = int((mouseX)// section)
        difficulties = ['easy', 'medium', 'hard', 'chaos']
        if mouseX > 30 and mouseX < (app.width - 30) and mouseY > 200 and mouseY < (app.height - 500) + 200:
            app.difficultyKey = difficulties[trueX]
            app.mainLabelKey +=1
    if mainLabelKey == 1:
        trueY = (mouseY-300)//(100)
        if distance(mouseX, mouseY, 150, (trueY *100) + 340) <= 20:
            if trueY == 0 and app.playerChars[0] >= 20 and app.playerChars[0] <= 100:
                app.playerChars[0] -= 1
            elif trueY == 1 and app.playerChars[1] >= .01 and app.playerChars[1] <= .5:
                app.playerChars[1] -= .01
                app.playerChars[1] = roundToDeci(app.playerChars[1], 3)
            elif trueY == 2 and app.playerChars[2] >= 10 and app.playerChars[2] <= 250:
                app.playerChars[2] -= 10
        if distance(mouseX, mouseY, app.width-150, (trueY *100) + 340) <= 20:
            if trueY == 0 and app.playerChars[0] >= 20 and app.playerChars[0] <= 100:
                app.playerChars[0] += 1
            elif trueY == 1 and app.playerChars[1] >= .01 and app.playerChars[1] <= .5:
                app.playerChars[1] += .01
                app.playerChars[1] = roundToDeci(app.playerChars[1], 3)
            elif trueY == 2 and app.playerChars[2] >= 10 and app.playerChars[2] <= 250:
                app.playerChars[2] += 50

def roundToDeci(value, amount):
    stringVal = str(value)
    indexOfDeci = stringVal.find('.')
    if indexOfDeci == -1: 
        return float(stringVal + '.00')
    return float(stringVal[:indexOfDeci + amount + 1])
        
def distance(x0, y0, x1, y1):
    return ((x0-x1)**2 + (y0 -y1)**2) **.5


def main():
    runApp()

main()