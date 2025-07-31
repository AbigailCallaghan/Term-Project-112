from cmu_graphics import * 
import math, random
from player import Player
from raycaster import Raycaster
from course import Course
from star import AllStars
#settings class, you run the game from here
#Used this https://www.youtube.com/watch?v=E18bSJezaUE tutorial for basic raycaster 
def onAppStart(app):
    app.potentialMaps = {0: ['straight', 9, 5, 5, True], 1:['curved up', 5, 9, -3, False]}
    # easy is more downhill and has wider areas
    #hard has increased speed, narrower areas
    app.difficultyLevels = {'easy': {'length range': (4, 8), 'width range': (3, 7), 'slope range': (-5, 5)},
                            'medium': {'length range': (4, 8), 'width range': (2, 6), 'slope range': (-10, 10)},
                            'hard': {'length range': (4, 8), 'width range': (2, 5), 'slope range': (-15, 15)},
                            'chaos':{'length range': (2, 8), 'width range': (2, 7), 'slope range': (-15, 15)}}
    app.playerChars = [50, .05, 100, 'Steering Wheel']
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
    app.intro = True
    app.drawMap  = False
    app.manual = False
    app.loadingScreen = True
    app.mainLabelKey = 0
    app.font = 'orbitron'
    app.stepsPerSecond = 30
    app.pushZone = True
    app.allStars = AllStars(app)
    app.gameOver = False
    app.coolDown = 0
    app.drawInstructions = False
    app.maxCoolDown = 250
    app.backgroundImage = 0

def redrawAll(app):
    if app.loadingScreen == True:
        if app.intro == True and app.drawInstructions == False: 
            drawIntroAnimation(app)
        elif app.intro == True and app.drawInstructions:
            instructions(app)
        else: 
            drawLoadingScreen(app, app.mainLabelKey)
    elif app.gameOver == True:
        drawDeathScreen(app)
    else:
        drawRect(0, 0, app.width, app.height, fill = 'black')
        drawBackGroundImage(app)
        if app.drawMap == True:
            app.course.drawMap(app)
            app.player.drawPlayer(app)
            app.raycaster.drawAllRays(app)
            
        else:
            if app.pushZone == True:
                drawPushingZone(app)
            app.raycaster.drawAllRays(app)
            if app.playerChars[3] == 'Steering Wheel':
                drawSteeringWheel(app)

            drawSideBar(app)
def drawBackGroundImage(app):
    potentialBackGround = ['/Users/abigailcallaghan/Documents/GitHub/Term-Project-112/GameBackGroundFiveGame.webp',
                           '/Users/abigailcallaghan/Documents/GitHub/Term-Project-112/backGroundOneGame.png',
                           '/Users/abigailcallaghan/Documents/GitHub/Term-Project-112/backGroundTwoGame.png',
                           '/Users/abigailcallaghan/Documents/GitHub/Term-Project-112/backGroundThreeGame.png',
                           '/Users/abigailcallaghan/Documents/GitHub/Term-Project-112/backGroundSix.png']
    #image credits:
    #https://www.reddit.com/r/PixelArt/comments/odvyko/deep_space/
    #https://x.com/norma_2d/status/1374371658920722441
    drawImage(potentialBackGround[app.backgroundImage], app.width/2, app.height/2, 
              width = 900, height = app.height, align = 'center')

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
    trueDistance = roundToDeci(app.player.totalDistance/ 1000, 2)
    drawLabel(f'Current section {sectionType} with slope {slope}', labelLeft, 60, 
              font = app.font, fill = fontColor, align = 'left')
    drawLabel(f'Next section {nextSectionType} with slope {nextSlope}', labelLeft, 
              80, font = app.font, fill = fontColor, align = 'left')
    drawLabel(f'Total distance: {trueDistance}km', labelLeft, 100, font = app.font, 
              fill = fontColor, align = 'left')
    
def drawSteeringWheel(app):
    steeringWheelColor = 'black'
    drawRect(app.steeringWheelLeftCordinates[0], app.steeringWheelLeftCordinates[1]-10, 
             app.width - 2* app.steeringWheelLeftCordinates[0], 20, fill = steeringWheelColor)
    drawCircle(app.steeringWheelLeftCordinates[0],  app.steeringWheelLeftCordinates[1], 
               10, fill = steeringWheelColor)
    drawCircle(app.width - app.steeringWheelLeftCordinates[0], app.steeringWheelLeftCordinates[1], 
               10, fill = steeringWheelColor)
    drawRect(app.width/2, app.steeringWheelLeftCordinates[1] + 30, 30, app.steeringWheelHeight, 
             fill = steeringWheelColor, align = 'center')

def onStep(app):
    if app.intro and app.loadingScreen:
        app.allStars.moveStars(app)

    else:
        app.raycaster.castAllRays(app)
        app.player.turnDirection = 0
        if app.nextBottom != 0:
            switchMaps(app)
        if app.manual == False and app.gameOver == False:
            app.player.move(app)
        if (app.player.velocity == 0 and app.pushZone == False and app.gameOver == False and 
            app.loadingScreen == False):
            app.gameOver = True
        if app.pushZone == True and app.coolDown > 0:
            app.coolDown -=25

def onKeyPress(app, key):
    if app.intro and app.loadingScreen:
        if key == 'enter':
            app.intro = False
        if key == 'i':
            app.drawInstructions = not app.drawInstructions
    if app.loadingScreen == True and app.intro == False:
        if key == 'enter' and app.mainLabelKey == 1:
            app.loadingScreen = False
            app.player = Player(app, app.course)
            app.raycaster = Raycaster(app.player, app.course)
            createMap(app)
    if app.loadingScreen == False and app.intro == False and app.gameOver == False:
        app.player.onKeyPress(app,key)
        app.raycaster.castAllRays(app)
        if key == 'm': 
            app.drawMap = not app.drawMap
    if app.gameOver:
        if key == 'r':
            app.loadingScreen = True
            app.gameOver = False
            app.potentialMaps = {0: ['straight', 9, 5, 5, True], 1:['curved up', 5, 9, -3, False]}
            app.mapKey = 0
            app.mainLabelKey = 0
            app.pushZone = True

def drawPushingZone(app):
    #inital bar
    color = 'chartreuse'
    drawRect(300, 10, 400, 40, fill = 'dimGray')
    drawCircle(300, 30, 20, fill = 'dimGray')
    if app.coolDown >0:
        progress = app.coolDown / app.maxCoolDown
        remander = 1-progress
        if remander <= ((app.maxCoolDown *.9)/app.maxCoolDown):
            drawCircle(300 + progress*400, 30, 20, fill = 'dimGray')
        drawRect(300, 10, (app.maxCoolDown - app.coolDown) % 400 + 1, 40, fill = color)
        drawCircle(300, 30, 20, fill = color)

    else:
        drawLabel("PUSH ZONE", 500, 30, fill = color, bold = True, size = 30)
    


def onMousePress(app, mouseX, mouseY):
    if app.loadingScreen == True:
        loadingScreenButtonPress(app, app.mainLabelKey, mouseX, mouseY)
    if app.manual == False and app.gameOver == False and app.playerChars[3] == 'Steering Wheel':
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
        #this is due to an off by one map error I kept getting
        #originally I solved this using reccursion but it threw another error
        #I fixed this bug after my reflection so my reflection says that there is 
        # recursion in generate partial map to fix this bug which is no longer true
        #There is still recursion in addToThirteen
        if len(app.course.map[0]) != len(app.course.map[mapOneLength + mapTwoLength]):
            print('this is called')
            print(app.course.map)
            colZero = len(app.course.map[0])
            for row in range(len(app.course.map)):
                if len(app.course.map[row]) < colZero:
                    app.course.map[row] = app.course.map[row] + [1] * abs(colZero - len(app.course.map[row]))
                    print(abs(colZero - len(app.course.map[row])))

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
    currentLength = app.potentialMaps[app.mapKey + 1][1]
    currentWidth = app.potentialMaps[app.mapKey + 1][2]
    nextLength = addToThirteen(random.randint(lengthLo, lengthHi),currentLength, lengthLo, lengthHi)
    nextWidth = addToThirteen(random.randint(widthLo, widthHi), currentWidth, widthLo, widthHi)
    slope = random.randint(slopeLo, slopeHi)
    pushingZone = True if random.randint(0, 2) == 2 else False
    if nextDirection == 'curved up':
        if nextLength + nextWidth + currentWidth > 13:
            nextWidth -= abs(13 - (nextLength + currentWidth + nextWidth))
    return [nextDirection, nextLength, nextWidth, slope, pushingZone]

def addToThirteen(val1, val2, lo, hi):
    if val1 + val2 <= 13:
        return val1
    else:
        return addToThirteen(random.randint(lo, hi),val2, lo, hi)

def switchMaps(app):
    trueYCoord = int(app.player.y//app.tileSize)
    if trueYCoord < (15 - (app.nextBottom)):
        app.mapKey +=1
        createMap(app)
        app.raycaster.castAllRays(app)
        app.pushZone = app.potentialMaps[app.mapKey][4]
        app.maxCoolDown = 250
        app.backgroundImage = random.randint(0,4)

def drawIntroAnimation(app):
    drawRect(0, 0, app.width, app.height, fill = rgb(0, 0, 30))
    app.allStars.drawAllStars()
    drawLabel('Press i for instructions', app.width/2, app.height/2 + 200, 
              fill = 'white', bold = True, size = 25)
    drawLabel('Press enter to move to the loading screen', app.width/2, app.height/2 + 150, 
              fill = 'white', bold = True, size = 25)

    url = '/Users/abigailcallaghan/Documents/GitHub/Term-Project-112/SpaceRacingTitle.jpeg'
    #source: https://perchance.org/ai-pixel-art-generator
    drawImage(url, app.width/2, 250, width = 400, height = 500, align = 'center')

def instructions(app):
    drawRect(0, 0, app.width, app.height)
    drawLabel('Adjust difficulty and vehicle characteristics in loading screen', app.width/2-350, 
              app.height - 600, fill = 'white', bold = True, size = 16, align = 'left')
    drawLabel('If the steering wheel is toggled steer cart by clicking on the sides of the steering wheel', 
               app.width/2-350, app.height - 575, fill = 'white', bold = True, size = 16, align = 'left')
    drawLabel('(located at the bottom of the screen)', app.width/2-350, app.height - 550, fill = 'white', 
              bold = True, size = 16, align = 'left')
    drawLabel("If keys are toggled, steer cart by pressing 'a' to turn left and 'b' to turn right", 
               app.width/2 - 350, app.height - 525, fill = 'white', bold = True, size = 16, align = 'left')
    drawLabel("Press 'm' to switch between first person view and grid view",  
              app.width/2 - 350, app.height - 500, fill = 'white', bold = True, size = 16, align = 'left')
    drawLabel("At the top left is your status bar",  app.width/2 -350, 
              app.height - 475, fill = 'white', bold = True, size = 16, align = 'left')
    drawLabel("It displays current velocity, slope, distance traveled, ", app.width/2 - 350, 
              app.height - 450, fill = 'white', bold = True, size = 16, align = 'left')
    drawLabel("type and characteristics of your current zone and next zone",  app.width/2 - 350, 
              app.height - 425, fill = 'white', bold = True, size = 16, align = 'left')
    drawLabel("Move by pressing the space bar when you are in a push zone",  app.width/2 - 350, 
              app.height - 400, fill = 'white', bold = True, size = 16, align = 'left')
    drawLabel("After you push, pushing will be on a cool down, ",app.width/2 - 350, app.height - 375, 
              fill = 'white', bold = True, size = 16, align = 'left')
    drawLabel("The time until your next push is displayed by the green bar",  app.width/2 - 350, 
              app.height - 350, fill = 'white', bold = True, size = 16, align = 'left')
    drawLabel('The game ends when you cannot move (velocity is zero) and you are not in a push zone',  
              app.width/2 - 350, app.height - 325, fill = 'white', bold = True, size = 16, align = 'left')
    drawLabel("Press i to return to main menu: ", 
              app.width/2 - 350, app.height - 300, fill = 'white', bold = True, size = 16, align = 'left')

def drawDeathScreen(app):
    drawRect(0, 0, app.width, app.height, opacity=50)
    url = '/Users/abigailcallaghan/Documents/GitHub/Term-Project-112/gameOverArt.png'
    #source: https://rare-gallery.com/uploads/posts/1102195-illustration-video-games-pixel-art-space-nebula-pixels-indie-games-biology-Steredenn-ART-computer-wallpaper.png
    drawImage(url, app.width/2, app.height/2, align = 'center')
    drawLabel('GAME OVER', app.width/2, app.height/2 - 50, bold = True, fill = 'white', size = 50)
    trueDistance = roundToDeci(app.player.totalDistance/ 1000, 2)
    drawLabel(f'Total distance: {trueDistance}', app.width/2, app.height/2, 
              bold = True, fill = 'white', size = 25)
    totalSections = len(app.potentialMaps) -1
    drawLabel(f'Total sections cleared: {totalSections}', app.width/2, app.height/2 + 50, 
              bold = True, fill = 'white', size = 25)
    drawLabel('Press r to reset', app.width/2, app.height/2 + 100, bold = True, fill = 'white', size = 25)
    
    

def drawLoadingScreen(app, mainLabelKey):
    url = '/Users/abigailcallaghan/Documents/GitHub/Term-Project-112/Screenshot 2025-07-31 at 1.57.51 PM.png'
    #sorce: https://www.reddit.com/r/PixelArt/comments/zvtl9r/a_nebula_background_for_a_game_im_working_on/
    drawImage(url, app.width/2, app.height/2, align = 'center')
    drawLabel('Loading Screen', app.width/2, 50, size = 50, bold = True, fill = 'white')
    mainLabel = {0: 'Choose your difficulty', 1: 'Choose your characteristics'}
    drawLabel(mainLabel[mainLabelKey], app.width/2, 125, size = 25, bold = True, fill = 'white')
    drawLoadingScreenOption(app, app.mainLabelKey)

def drawLoadingScreenOption(app, mainLabelKey):
    backGroundColor =  rgb(0, 0, 25)
    if mainLabelKey == 0:
        section = (app.width - 60)//4
        potentialLabels = ['Easy', 'Medium', 'Hard', 'Chaos']
        potentialUrls=['/Users/abigailcallaghan/Documents/GitHub/Term-Project-112/VoyagerImageGame.png', 
                       '/Users/abigailcallaghan/Documents/GitHub/Term-Project-112/SaturnGameImage.webp',
                       '/Users/abigailcallaghan/Documents/GitHub/Term-Project-112/starImageGame.png',
                       'https://streak.club/img/Mix1c2VyX2NvbnRlbnQvdXBsb2Fkcy9pbWFnZS8zMjYxOC5wbmc=/original/cMTlu6.png']
        #black hole image: https://streak.club/p/29287/black-hole-by-mentalpop
        #voyager image: https://www.reddit.com/r/PixelArt/comments/c83okd/voyager/
        #planet image: https://www.reddit.com/r/PixelArt/comments/16zw3mh/pixel_art_of_saturn_orginal_picture_from_nasa_on/
        #star image: https://rare-gallery.com/uploads/posts/1102198-illustration-video-games-pixel-art-planet-space-Earth-pixels-circle-atmosphere-universe-indie-games-quasars-Steredenn-screenshot-computer-wallpaper-atmosphere-of-earth-.png
        for i in range(4):
            labelText = potentialLabels[i]
            drawRect(i*section + 30, 200, section - 10, app.height - 500, 
                     fill = backGroundColor, border = 'lightGrey')
            drawLabel(f'{labelText}', i*section + 30 + section/2, 250, size = 25, bold = True, fill = 'white')
            drawImage(potentialUrls[i], i*section + 40, 300, width = (section -30), height = (section -30))
    if mainLabelKey == 1:
        potentialLabels = ['Mass: ', 'Friction Coeffishent: ', 'Push Strength: ', '']
        backLabels = ['kg', '', 'N', '']
        for i in range(4):
            heightLevel = i*100
            drawRect(100, heightLevel + 300, app.width - 200, 80, fill = backGroundColor, border = 'lightGrey')
            
            drawLabel(f'{potentialLabels[i]}{app.playerChars[i]} {backLabels[i]}', 
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
            if trueY == 0 and app.playerChars[0] >= 20:
                app.playerChars[0] -= 1
            elif trueY == 1 and app.playerChars[1] >= .01:
                app.playerChars[1] -= .01
                app.playerChars[1] = roundToDeci(app.playerChars[1], 3)
            elif trueY == 2 and app.playerChars[2] >= 50:
                app.playerChars[2] -= 50
            elif trueY == 3:
                if app.playerChars[3] == 'Steering Wheel':
                    app.playerChars[3] = 'Keys'
        if distance(mouseX, mouseY, app.width-150, (trueY *100) + 340) <= 20:
            if trueY == 0 and app.playerChars[0] <= 100:
                app.playerChars[0] += 1
            elif trueY == 1 and  app.playerChars[1] <= .5:
                app.playerChars[1] += .01
                app.playerChars[1] = roundToDeci(app.playerChars[1], 3)
            elif trueY == 2 and app.playerChars[2] <= 500:
                app.playerChars[2] += 50
            elif trueY == 3:
                if app.playerChars[3] == 'Keys':
                    app.playerChars[3] = 'Steering Wheel'

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