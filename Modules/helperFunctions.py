#Catalog of helper functions used in project

##
# OS Stuff
##

import os
import sys
import inspect

filename = inspect.getframeinfo(inspect.currentframe()).filename
filePath = os.path.dirname(os.path.dirname(os.path.abspath(filename))) + "\\"

##
# Importing Python Modules
##

import pygame
MUSIC_END = pygame.USEREVENT + 1
import math
import numpy
import random
import decimal
import json
import string
import copy

##
# Misc. Helper Functions
##

def readFile(path): #Taken from 15-112 website
    with open(path, "rt") as f:
        return f.read()

def intify(*args): #converts all args to int
    newArgs = []
    for arg in args:
        if isinstance(arg, float):
            newArgs.append(int(arg))
        elif isinstance(arg, tuple):
            result = intify(*arg)
            newArgs.append(tuple(result))
        elif isinstance(arg, list):
            result = intify(*arg)
            newArgs.append(result)
        else:
            newArgs.append(arg)
    return newArgs

def rectCollision(x, y, rect):
    if (x > rect[0] and x < rect[0] + rect[2] and
        y > rect[1] and y < rect[1] + rect[3]):
        return True
    return False

def incrementColor(color, incr): #Makes color brighter/darker
    red = color[0]
    green = color[1]
    blue = color[2]
    newRed = red + incr
    if newRed > 255:
        newRed = 255
    newGreen = green + incr
    if newGreen > 255:
        newGreen = 255
    newBlue = blue + incr
    if newBlue > 255:
        newBlue = 255
    return (newRed, newGreen, newBlue)

#Only for testing purposes
def uPrint1(player, data, attribute):
    if player is data.user1: print(attribute)

def uPrint2(player, data, attribute):
    if player is data.user2: print(attribute)
    
##
# Computational Helper Functions
##

def almostEqual(d1, d2, epsilon=10**-7): #Taken from 15-112 website
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

def roundHalfUp(d): #Taken from 15-112 website
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def distance(x1, y1, x2, y2): #Distance between two points
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def angle(x1, y1, x2, y2): #From x1, y1 to x2, y2
    if x2 - x1 > 0:
        return math.atan((y1 - y2) / (x2 - x1)) + math.pi
    elif x2 - x1 == 0:
        if y2 - y1 > 0:
            return math.pi / 2
        else:
            return -1 * math.pi / 2
    else:
        return math.atan((y1 - y2) / (x2 - x1))

def convertToCobMatrix(data, start, end):
    #Convers a line into a change of base matrix
    scaleDistance = distance(*start, *end) / data.length
    scaleAngle = -1 * angle(*end, *start) #Adjust for python's weird y axis
    #x, y of first change of basis vector
    basis1X = scaleDistance * math.cos(scaleAngle)
    basis1Y = scaleDistance * math.sin(scaleAngle)
    #x, y of second change of basis vector (perpendicular to first)
    if data.shootingBasket.name == "Left":
        basis2X = -1 * basis1Y
        basis2Y = basis1X
    elif data.shootingBasket.name == "Right":
        basis2X = basis1Y
        basis2Y = -1 * basis1X
    basisMatrix = [[basis1X, basis2X],
                   [basis1Y, basis2Y]]
    cobMatrix = numpy.linalg.inv(basisMatrix)
    return cobMatrix

def changeBasis(data, x, y, start, cobMatrix): #Changes vector basis
    #Adjust origin to start
    x -= start[0] 
    y -= start[1]
    vector = [[x],
              [y]]
    #Transform x and y using cobMatrix
    newVector = numpy.matmul(cobMatrix, vector)
    newX = newVector[0][0]
    newY = newVector[1][0]
    return newX, newY

def calculateCrossSection(data, player): #Creates cross-section from player to basket
    xi, yi = player.x, player.y
    xf, yf, = data.shootingBasket.basketX, data.shootingBasket.y
    dist = distance(xi, yi, xf, yf)
    theta = angle(xi, yi, xf, yf)
    marginL = data.court.basketDist
    fixedDist = data.length / 2
    marginR = fixedDist - dist - marginL
    end = (xi + marginR * math.cos(theta), yi - marginR * math.sin(theta))
    start = (xf - marginL * math.cos(theta), yf + marginL * math.sin(theta))
    if yi > yf and data.shootingBasket.name == "Left":
        start, end = end, start
    elif yi < yf and data.shootingBasket.name == "Right":
        start, end = end, start
    return [start, end]

def findCrossSectAngle(x1, y1, x2, y2, data):
    ang = angle(x1, y1, x2, y2)
    if data.shootingDir == 1: #Flip cross sectional angle
        ang += math.pi
    return ang

def rotateAcrossAxis(theta, axis):
    return -1 * (theta - axis) + axis

##
# Drawing Helper Functions
##

#Create Text- taken from pyGame website
def drawText(screen, font, cx, cy, writing, textColor, backgroundColor = "",
    just = 0):
    if just == 0:
        text = font.render(writing, True, textColor, backgroundColor)
        textrect = text.get_rect()
        textrect.centerx = cx
        textrect.centery = cy
        screen.blit(text, textrect)
    elif just == 1: #Left Justified
        text = font.render(writing, True, textColor, backgroundColor)
        textrect = text.get_rect()
        textrect.left = cx
        textrect.centery = cy
        screen.blit(text, textrect)
    elif just == 2: #Right Justified
        text = font.render(writing, True, textColor, backgroundColor)
        textrect = text.get_rect()
        textrect.right = cx
        textrect.centery = cy
        screen.blit(text, textrect)
    return textrect

def drawStar(screen, cx, cy, rad, fill, border): #Draws a star of a certain color
    points = []
    points2 = []
    rad2 = rad * 0.6
    for i in range(10):
        theta = math.pi / 2 + i * math.pi / 5
        if i % 2 == 0: #Outer point
            points.append((cx + rad * math.cos(theta), cy - rad * math.sin(theta)))
            points2.append((cx + rad2 * math.cos(theta), cy - rad2 * math.sin(theta)))
        else: #Inner point
            factor = 0.4
            points.append((cx + rad * factor * math.cos(theta), cy - rad * factor * math.sin(theta)))
            points2.append((cx + rad2 * factor * math.cos(theta), cy - rad2 * factor * math.sin(theta)))
    pygame.draw.polygon(screen, border, points)
    pygame.draw.polygon(screen, fill, points2)
            
def adjustZ(oldZ, data): #Adjust coordinates of points in 3D mode
    z = oldZ * data.court.width / data.height
    z = data.court.width - z
    margin = (data.width - data.court.width) / 2
    return z + margin

def reverseAdjustZ(oldZ, data):  #Converts 3D z back to 2D z
    margin = (data.width - data.court.width) / 2
    z = oldZ - margin
    z = data.court.width - z
    z *= data.height / data.court.width
    return z

def scaleZ(oldZ, scaleFactor, data): #Whenever perspective is needed
    z = adjustZ(scaleFactor * (oldZ - data.height / 2) + data.height / 2, data)
    return z

def scaleVertical(attribute, data): #Adjust lengths of drawings in 3D mode
    return attribute * data.court.width / data.height

def displayPauseText(data, text): #Toggles header text
    data.pauseText = text
    data.pauseTextOnly = True
    data.pauseTime = data.switchPosessionTime

def findMadeShotText(data, player, text = ""): #Returns text string for made shot
    if text == "" and (data.user1Shoot[0] or data.user2Shoot[0] or data.aiShoot[0]):
        text = "Jumper"
    elif text == "":
        text = "Layup"
    name = str(player.firstName) + " " + str(player.lastName)
    data.pauseText = name + " made " + text + "!"

def findPlayer1(data): #For career game
    if not data.careerGame:
        return data.user1
    else:
        if data.ball.player in data.user1Team:
            return data.ball.player

def findPlayer2(data): #For drawing bottom stats, finds player 2 if its AI
    if data.numPlayers == 2:
        player2 = data.user2
    else:
        if data.user1 in data.offensiveTeam:
            player2 = data.user1.guardedBy #Person guarding player 1
        else:
            player2 = data.ball.player #Offensive player with ball
        if player2 == "" or player2 not in data.user2Team:
            player2 = data.prevPlayer2
        else:
            data.prevPlayer2 = player2
    return player2

def findPlayer2Dup(data): #For helper functions, finds player 2 if its AI
    if data.numPlayers == 2:
        player2 = data.user2
    else:
        if data.user1 in data.offensiveTeam:
            player2 = data.user1.guardedBy #Person guarding player 1
        else:
            player2 = data.ball.player #Offensive player with ball
        if player2 == "" or player2 not in data.user2Team:
            player2 = data.prevPlayer2Dup
        else:
            data.prevPlayer2Dup = player2
    return player2

##
# Gameplay Data Checks Helper Functions
##

def checkBallPlayer(data): #Checks if ball has switched hands
    result = False
    if data.ball.player != data.prevBallHandler:
        result = True
    data.prevBallHandler = data.ball.player
    return result

def checkIfBallInBounds(data): #Causes turnover if ball is out of bounds
    if not data.ball.inBounds(data, data.court):
        data.pauseText = "Out of Bounds!"
        if data.ball.player is data.user1:
            #Career Grades- Turnover on User1
            data.user1Turnovers += 1
        switchPosession(data)

def checkShotClock(data): #Causes turnoer if shot clock runs out
    if data.mode == "2D":
        data.shotClockCounter += 1
        if data.shotClockCounter % data.timerDelay == 0:
            data.shotClock -= 1
        if data.shotClock == 0:
            data.pauseText = "Shot Clock Violation!"
            if data.ball.player is data.user1:
                #Career Grades- Turnover on User1
                data.user1Turnovers += 1
            switchPosession(data)
            
def checkBackcourt(data): #Causes turnover if back court violation or eight second violation
    player2 = findPlayer2(data)
    player1 = findPlayer1(data)
    if data.mode == "3D":
        return
    if player1 in data.offensiveTeam:
        if not data.user1Backcourt:
            if ((player1.x > data.length / 2 and data.shootingBasket.name == "Right")
                or (player1.x < data.length / 2 and data.shootingBasket.name == "Left")):
                data.user1Backcourt = True
            elif data.shotClock <= 16 and data.ball.player == player1:
                data.pauseText = "Eight Second Violation!"
                if player1 is data.user1:
                    #Career Grades- Turnover on User1
                    data.user1Turnovers += 1
                switchPosession(data)
        else:
            if (((player1.x < data.length / 2 and data.shootingBasket.name == "Right")
                or (player1.x > data.length / 2 and data.shootingBasket.name == "Left"))
                and data.ball.player == player1):
                data.pauseText = "Backcourt Violation!"
                if player1 is data.user1:
                    #Career Grades- Turnover on User1
                    data.user1Turnovers += 1
                switchPosession(data)
    elif player2 in data.offensiveTeam:
        if not data.user2Backcourt:
            if ((player2.x > data.length / 2 and data.shootingBasket.name == "Right")
                or (player2.x < data.length / 2 and data.shootingBasket.name == "Left")):
                data.user2Backcourt = True
            elif data.shotClock <= 16 and data.ball.player == player2:
                data.pauseText = "Eight Second Violation!"
                switchPosession(data)
        else:
            if (((player2.x < data.length / 2 and data.shootingBasket.name == "Right")
                or (player2.x > data.length / 2 and data.shootingBasket.name == "Left"))
                and data.ball.player == player2):
                data.pauseText = "Backcourt Violation!"
                switchPosession(data)

##
# Updating Gameplay Data Helper Functions
##

def switchUser(data, player, L, player2): #Switches a user to another player
    if player2 == None:
        userI = 0
        for i in range(len(L)):
            if L[i] is player:
                userI = i
        userI += 1
    else:
        userI = L.index(player2)
    if userI == len(L): userI = 0
    if isinstance(player, Player):
       player.headColor = player.defaultColor
    if data.ball.player is player:
        data.ball.player = L[userI]
    L[userI].headColor = L[userI].userColor
    return L[userI]

def switchUser1(data, playerToSwitchTo = None): #Switch user1
    if not data.careerGame:
        data.user1 = switchUser(data, data.user1, 
                    data.user1Team, playerToSwitchTo)

def switchUser2(data, playerToSwitchTo = None): #Switch user2
    #Set to dummy if one player game
    if data.numPlayers < 2:
        data.user2 = data.dummyPlayer
        switchUser(data, data.prevPlayer2Dup, data.user2Team, findPlayer2Dup(data))
        return
    data.user2 = switchUser(data, data.user2, data.user2Team, playerToSwitchTo)

def changePlayerOrder(data): #Changes order in which players are drawn
    newPlayerList = []
    coordList = []
    coordDict = {}
    for player in data.players:
        x, y = changeBasis(data, player.x, player.y, data.crossSection[0], data.cobMatrix)
        depthSpan = (data.length ** 2 + data.width ** 2) ** 0.5
        if data.shootingBasket.name == "Right": y = depthSpan - y
        if y in coordDict:
            return
        coordDict[y] = player
        coordList.append(y)
    coordList.sort()
    for coord in coordList:
        newPlayerList.append(coordDict[coord])
    data.players = newPlayerList[:]

def calculateShootingDir(data): #Calculates basket shooting direction
    dir = -1
    if distance(data.shootingBasket.x, data.shootingBasket.y, *data.crossSection[0]) < distance(
                data.shootingBasket.x, data.shootingBasket.y, *data.crossSection[1]): 
        dir = 1
    data.shootingDir = dir

def updatePauseData(data): #If animations are paused, increments pause count
    data.pauseCount += 1
    if data.pauseCount > data.pauseTime * data.timerDelay:
        data.pause, data.pauseNoDraw, data.pausePlayer = False, False, ""
        data.pauseTextOnly = False
        data.pauseText = ""
        data.pauseCount = 0

def updateFlags(data): #Updates shooting flags
    if data.mode == "2D":
        data.user1Shoot = (False, 0, 0, 0)
        data.user2Shoot = (False, 0, 0, 0)
        data.aiShoot = (False, 0, 0, 0)
    
#updateTeams Helper
def switchBasket(data):
    for basket in data.baskets:
        if not basket is data.shootingBasket:
            data.shotClock = 24
            data.shotClockCounter = 0
            data.shootingBasket = basket
            return

def updateTeams(data): #Checks if posession was changed and changes teams accoridngly
    if data.ball.player in data.user1Team:
        if not data.offensiveTeam is data.user1Team: #Switch teams and basket
            switchBasket(data)
            data.user1Backcourt, data.user2Backcourt = False, False
            data.passTarget = ""
            forceUpdateAI(data, data.user1Team, data.user2Team)
            for player in data.players:
                player.displayArm = False
        data.offensiveTeam = data.user1Team
        data.defensiveTeam = data.user2Team
        data.rebounding = False
    elif data.ball.player in data.user2Team:
        if not data.offensiveTeam is data.user2Team: #Switch teams and basket
            switchBasket(data)
            data.user1Backcourt, data.user2Backcourt = False, False
            data.passTarget = ""
            forceUpdateAI(data, data.user2Team, data.user1Team)
            for player in data.players:
                player.displayArm = False
        data.offensiveTeam = data.user2Team
        data.defensiveTeam = data.user1Team
        data.rebounding = False

def updateUser(data): #Updates user if ball was passed
    if data.ball.player in data.user1Team and not data.ball.player is data.user1:
        switchUser1(data, data.ball.player)
    elif data.ball.player in data.user2Team and not data.ball.player is data.user2:
        switchUser2(data, data.ball.player)

def updateScoreboardData(data): #Updates scoreboards
    data.scoreboardData = "User 1: %d, User 2: %d" % (data.user1Score, data.user2Score)
    data.scoreboard1Text = data.user1Score
    data.scoreboard2Text = data.user2Score
    if data.mode == "2D":
        if data.user1Score >= data.maxScore:
            data.winner = data.user1TeamName
            data.mode = "Post Game"
        elif data.user2Score >= data.maxScore:
            data.winner = data.user2TeamName
            data.mode = "Post Game"

def updateArmTheta3D(data): #Updates player arm coords
    for player in data.players:
        if not player is data.shooter:
            player.armTheta = angle(*data.crossSection[0], *data.crossSection[1])
            if data.shootingDir > 0: player.armTheta += math.pi

def updatePlayerFlags(data): #Updates player flags
    for player in data.players:
        if player.crossoverDelay > 0:
            player.crossover = False
        player.crossoverDelay += 1

def initPositions(data): #Resets player positions on a turnover
    for player in data.players:
        if isinstance(player, Guard): #Point guard starts with ball
            if player in data.offensiveTeam:
                data.ball.player = player
            player.x = 4 * data.length / 5
            player.y = data.width / 2
        elif isinstance(player, Forward):
            player.x = 3 * data.length / 4
            player.y = 2 * data.width / 3
        elif isinstance(player, Center):
            player.x = 3 * data.length / 4
            player.y = data.width / 3
        if ((data.shootingBasket.name == "Left" and player in data.defensiveTeam)
            or (data.shootingBasket.name == "Right" and player in data.offensiveTeam)):
            player.x = data.length - player.x

def switchPosession(data): #Switches ball posession on turnover
    data.aiShoot = (False, 0, 0, 0)
    for player in data.players:
        if isinstance(player, Guard): #Point guard starts with ball
            if player in data.defensiveTeam:
                data.ball.player = player
            player.x = 4 * data.length / 5
            player.y = data.width / 2
        elif isinstance(player, Forward):
            player.x = 3 * data.length / 4
            player.y = 2 * data.width / 3
        elif isinstance(player, Center):
            player.x = 3 * data.length / 4
            player.y = data.width / 3
        if ((data.shootingBasket.name == "Left" and player in data.defensiveTeam)
            or (data.shootingBasket.name == "Right" and player in data.offensiveTeam)):
            player.x = data.length - player.x
    data.ball.player.startDribbling(data)
    data.pauseNoDraw = True
    data.pauseTime = data.switchPosessionTime

def forceUpdateAI(data, oTeam, dTeam): #Gives AI players proper AI
    for player in oTeam:
        AI = False
        for executable in player.executables:
            if executable[0].__name__ == "aiOffensive":
                AI = True
        if not AI:
            player.aiOffensive(player, data, True)
    for player in dTeam:
        AI = False
        for executable in player.executables:
            if executable[0].__name__ == "aiDefensive":
                AI = True
        if not AI:
            player.aiDefensive(player, data, True)

def updateAI(data): #Gives AI players proper AI
    for player in data.players:
        if player in data.defensiveTeam:
            AI = False
            for executable in player.executables:
                if executable[0].__name__ == "aiDefensive":
                    AI = True
            for executable in player.tempExecutables:
                if executable[1][0].__name__ == "aiDefensive":
                    AI = True
            if not AI:
                player.aiDefensive(player, data, True)
        elif player in data.offensiveTeam:
            AI = False
            for executable in player.executables:
                if executable[0].__name__ == "aiOffensive":
                    AI = True
            for executable in player.tempExecutables:
                if executable[1][0].__name__ == "aiOffensive":
                    AI = True
            if not AI:
                player.aiOffensive(player, data, True)

def updateCareerGrade(data): #Gives letter grade for career game
    points = data.user1.points
    assists = data.user1.assists
    rebounds = data.user1.rebounds
    steals = data.user1.steals
    blocks = data.user1.blocks
    fgm = data.user1.fgm
    fga = data.user1.fga
    turnovers = data.user1Turnovers
    for player in data.user2Team:
        if type(player) == type(data.user1):
            opp = player
    Ofgm = opp.fgm
    Ofga = opp.fga
    Opoints = opp.points
    score = 0
    score += points + 2 * assists + rebounds + 2 * blocks + steals + fgm + Ofga
    score -= (2 * turnovers + fga + Opoints + Ofgm)
    if -1 * data.maxScore // 4 <= score < data.maxScore // 4:
        data.grade = "C"
    elif data.maxScore // 4 <= score < 3 * data.maxScore // 4:
        data.grade = "B"
    elif score >= 3 * data.maxScore // 4:
        data.grade = "A"
    elif -3 * data.maxScore // 4 <= score < -1 * data.maxScore // 4:
        data.grade = "D"
    else:
        data.grade = "F"
        
def adjustFontSize(data): #Changing career name font size
    statsL = data.length / 16
    statsR = statsL + 4 * data.length / 7
    margin = (data.width - data.court.width) / 2 - data.court.lineWidth
    barWidth = margin / 20
    data.nameFontSize = int(barWidth * 2.5)
    font = pygame.font.SysFont("verdana", data.nameFontSize, bold = True)
    text = font.render(data.myName, True, (0, 0, 0), (0, 0, 0))
    textRect = text.get_rect()
    while textRect[2] >= ((statsR - statsL) / 2) * 0.95: #Text is too big
        decrement = int(barWidth * 0.2)
        if decrement < 1:
            decrement = 1
        data.nameFontSize -= int(barWidth * 0.2)
        font = pygame.font.SysFont("verdana", data.nameFontSize, bold = True)
        text = font.render(data.myName, True, (0, 0, 0), (0, 0, 0))
        textRect = text.get_rect()

def updateAchievementCompletion(data, player, achievement): #Career mode ach.
    if data.grade == "D" or data.grade == "F":
        return False
    result = True
    for quantityList in achievement:
        stack = []
        if not isinstance(quantityList, tuple):
            qL = [quantityList]
        else:
            qL = quantityList
        for item in qL:
            if item == "grade":
                stack.append(data.grade)
                break
            elif item == "turnovers":
                stack.append(data.user1Turnovers)
                break
            elif item not in ["+", "-", "*", "/"]:
                stack.append(getattr(player, item, 0))
            else:
                arg1 = stack.pop()
                arg2 = stack.pop()
                if item == "+":
                    stack.append(arg2 + arg1)
                elif item == "-":
                    stack.append(arg2 - arg1)
                elif item == "*":
                    stack.append(arg2 * arg1)
                elif item == "/":
                    if arg1 == 0:
                        stack.append(0)
                    else:
                        stack.append(arg2 / arg1)
        comparison = achievement[quantityList][0]
        valueList = achievement[quantityList][1]
        result = False
        for value in valueList:
            if comparison == "<=":
                result = stack[0] <= value
            elif comparison == ">=":
                result = stack[0] >= value
            elif comparison == "<":
                result = stack[0] < value
            elif comparison == ">":
                result = stack[0] > value
            elif comparison == "==":
                result = stack[0] == value
            elif comparison == "!=":
                result = stack[0] != value
            if result:
                break
        if not result:
            return False
    return True

##
# Careers Helper Functions
##

def retreiveDict(path): #Loads dictionary from text file
    dict = readFile(path)
    dict = dict.replace("'", '"')
    dict = json.loads(dict)
    return dict

def writeFile(path, contents): #Writing helper functions
    try:
        with open(path, "wt") as f:
            f.write(contents)
    except:
        pass

def saveUserStats(path, data, reset = False): #Save career stats from my career
    dictRound(data.myCareer)
    if not data.changeName and not reset:
        spaceIndex = data.myName.find(" ")
        if spaceIndex == -1:
            data.myCareer["firstName"] = data.myName
            data.myCareer["lastName"] = ""
        else:
            data.myCareer["firstName"] = data.myName[:spaceIndex]
            data.myCareer["lastName"] = data.myName[spaceIndex + 1:]
    writeFile(path + "MyCareer.txt", str(data.myCareer))
    data.saved = True

def dictRound(dict): #Rounds stats to two decimal places
    for element in dict:
        if isinstance(dict[element], float):
            dict[element] = float("{0:.2f}".format(dict[element]))

def dictAverage(dict): #Calculating overall
    sum = 0
    count = 0
    for element in dict:
        if isinstance(dict[element], float):
            sum += dict[element]
            count += 1
    return sum / count

def multiDictAverage(dict1, dict2, dict3):
    return (dictAverage(dict1) + dictAverage(dict2) + dictAverage(dict3)) / 3

def overallIncrease(dict, incr): #Increases all stats by set increment
    list = ["guard", "center", "forward"]
    newDict = copy.deepcopy(dict)
    for position in list:
        positionDict = newDict[position]
        for attribute in positionDict:
            value = positionDict[attribute]
            if isinstance(value, float):
                value += incr
                if value > 0.99:
                    value = 0.99
                elif value < 0.5:
                    value = 0.5
                positionDict[attribute] = value
    return newDict

def createNewCareer(path, data, difficulty): #Creates and saves new myCareer
    rand = random.randint(1, 3)
    guardGood = ["speed", "passing", "ballHandling", "steal"]
    forwardGood = ["shotForm", "accuracyShort", "accuracyMid", "accuracyLong"]
    centerGood = ["strength", "block", "rebounding", "jump"]
    guardBad = centerGood + forwardGood
    forwardBad = guardGood + centerGood
    centerBad = guardGood + forwardGood
    allStats = guardGood + forwardGood + centerGood
    if rand == 1:
        position = "guard"
        height = [5, 3]
        weight = 175
        good = guardGood
        bad = guardBad
    elif rand == 2:
        position = "forward"
        height = [5, 7]
        weight = 190
        good = forwardGood
        bad = forwardBad
    else:
        position = "center"
        height = [6, 0]
        weight = 215
        good = centerGood
        bad = centerBad
    goodStats = [0, 1, 2, 3]
    badStats = [0, 1, 2, 3, 4, 5, 6, 7]
    random.shuffle(goodStats)
    random.shuffle(badStats)
    playerDict = {}
    for stat in allStats:
        if stat == good[goodStats[0]] or stat == good[goodStats[1]]:
            playerDict[stat] = 0.7
        elif (stat == bad[badStats[0]] or stat == bad[badStats[1]] or 
              stat == bad[badStats[2]]):
            playerDict[stat] = 0.5
        else:
            playerDict[stat] = 0.6
    playerDict["height"] = height
    playerDict["weight"] = weight
    playerDict["position"] = position
    rand = random.randint(1, 5)
    if rand == 1:
        firstName, lastName = "Krispy", "Kreeme"
    elif rand == 2:
        firstName, lastName = "Sauce", "Castillo"
    elif rand == 3:
        firstName, lastName = "Gnarls", "Barkley"
    elif rand == 4:
        firstName, lastName = "Cash", "Considerations"
    elif rand == 5:
        firstName, lastName = "Nets", "Pick"
    playerDict["firstName"] = firstName
    playerDict["lastName"] = lastName
    playerDict["team"] = random.randint(1, 4)
    playerDict["VC"] = 0
    playerDict["difficulty"] = difficulty
    playerDict["achievements"] = ["No", "No", "No", "No", "No", "No", "No",
                                  "No", "No", "No", "No", "No"]
    #["No", "Confirm", "Yes", "No", "No", "No", "Yes", "Confirm", "No", "No", "No", "Yes"]
    oppList = [1, 2, 3, 4]
    random.shuffle(oppList)
    playerDict["oppList"] = [oppList, 0]
    data.myCareer = playerDict
    saveUserStats(path, data, True)

def addMyPlayer(dict, player): #Adds my career dict to team
    playerDict = copy.deepcopy(player)
    position = playerDict["position"]
    playerDict.pop("team")
    playerDict.pop("position")
    playerDict.pop("oppList")
    playerDict.pop("VC")
    playerDict.pop("difficulty")
    playerDict.pop("achievements")
    playerDict["height"]
    playerDict["height"]
    dict[position] = playerDict
    return dict

def statsComplete(playerDict): #Whether player's stats are completed
    statMax = 0.799
    if playerDict["difficulty"] == "Normal":
        statMax = 0.989
    for attribute in playerDict:
        stat = playerDict[attribute]
        if isinstance(stat, float) and stat < statMax:
            return False
    return True

def achievementsComplete(playerDict): #Whether player achievements are complete
    aList = playerDict["achievements"]
    for achievement in aList:
        if achievement != "Yes":
            return False
    return True

##
# Music Helper Functions
##

def playMusic(data): #playMusic on startup
    if not pygame.mixer.music.get_busy():
        data.music = [(filePath + "Music/Heartless.ogg", 11),
                        (filePath + "Music/JohnWall.ogg", 1.5),
                        (filePath + "Music/NoChurchInTheWild.ogg", 17),
                        (filePath + "Music/WrittenInTheStars.ogg", 6),
                        (filePath + "Music/ET.ogg", 0),
                        (filePath + "Music/Disturbia.ogg", 2.2),
                        (filePath + "Music/MyTime.ogg", 0),
                        (filePath + "Music/Here.ogg", 14),
                        (filePath + "Music/DeadAndGone.ogg", 0),
                        (filePath + "Music/RememberTheName.ogg", 0),
                        (filePath + "Music/MaadCity.ogg", 16),
                        (filePath + "Music/LetItRock.ogg", 0),
                        (filePath + "Music/LoseYourself.ogg", 31)]
        random.shuffle(data.music)
        data.musicIndex = 0
        pygame.mixer.music.set_endevent(MUSIC_END)
        updateMusic(data)

def updateMusic(data): #updateMusic if previous song stops
    pygame.mixer.music.load(data.music[data.musicIndex][0])
    pygame.mixer.music.play(start = data.music[data.musicIndex][1])
    data.musicIndex += 1
    data.musicIndex %= len(data.music)
    data.fadeInCount = 0
    pygame.mixer.music.set_volume(0)

def fadeInMusic(data): #fadeIn new song
    maxFadeCount = 2 * data.timerDelay
    if data.fadeInCount <= maxFadeCount:
        data.fadeInCount += 1
        volume = data.fadeInCount / maxFadeCount
        pygame.mixer.music.set_volume(volume)

def playSound(file): #Play wave file
    sound = pygame.mixer.Sound(file)
    sound.set_volume(0.5)
    sound.play()

# def playTitleMusic(data):
#     if pygame.mixer.music.get_busy():
#         pygame.mixer.music.fadeout(500)
#         pygame.mixer.music.set_endevent(MUSIC_END)
#     else:
#         data.fadeInCount = 0
#         updateTitleMusic(data)
# 
# def playInGameMusic(data):
#     data.music = [(filePath + "Music/Heartless.mp3", 11), 
#                 (filePath + "Music/NoChurchInTheWild.mp3", 17),
#                 (filePath + "Music/WrittenInTheStars.mp3", 6),
#                 (filePath + "Music/ET.mp3", 0),
#                 (filePath + "Music/Disturbia.mp3", 2.2)]
#     random.shuffle(data.music)
#     data.musicIndex = 0
#     # pygame.mixer.music.fadeout(2000)
#     # pygame.mixer.music.set_endevent(MUSIC_END)
# 
# def updateTitleMusic(data):
#     pygame.mixer.music.load(filePath + "Music/JohnWall.mp3")
#     pygame.mixer.music.play(start = 1.5)
#     data.fadeInCount = 0
#     pygame.mixer.music.set_volume(0)
# 
# def updateInGameMusic(data):
#     pygame.mixer.music.load(data.music[data.musicIndex][0])
#     pygame.mixer.music.play(start = data.music[data.musicIndex][1])
#     data.musicIndex += 1
#     data.musicIndex %= len(data.music)
#     data.fadeInCount = 0
#     pygame.mixer.music.set_volume(0)
    
##
# Importing Custom Modules
##

from buttonClass import *
from courtClass import *
from basketClass import *
from playerClass import *
from ballClass import *