#Class defining the players used in the game

##
# OS Stuff / Initialization
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
import math
import numpy
import random
import decimal
import json
import string

##
# Player Class
##

class Player(object):
    
    #Colors
    bodyColor = (150, 150, 150)
    borderColor = (255, 255, 255)
    fontColor = (255, 255, 255)
    backgroundColor = (0, 0, 0)
    
    def __repr__(self):
        string = self.firstName + " " + self.lastName
        if len(string) > 14:
            string = self.firstName[0].upper() + ". " + self.lastName[0:14]
        return string
        
##
# Init Functions
##

    #__init__ Helper
    def initDimensions(self, data):
        #Dimensions when drawing players
        self.x = 0
        self.y = 0
        self.armX = self.x
        self.armY = self.y
        self.radius = data.length / 60
        self.bodyWidth = data.length / 12
        self.width = data.length / 200
        self.armJoint = 1/2 #From middle of head
        self.armPhi = 0
        self.armTheta = 0
        self.armLengthConst = 4 * data.length / 94
        self.armLength = 4 * data.length / 94
        self.armWidth = 2 * data.length / 94

    #__init__ Helper
    def initMiscData(self, data, userColor, defaultColor):
        #Coords and flags
        self.userColor = userColor
        self.defaultColor = defaultColor
        self.basket = "Left" #Basket you're shooting at
        self.headColor = self.defaultColor
        self.executables = [] #Methods currently partaking in
        self.tempExecutables = [] #Methods which have been paused
        self.dir = -1
        self.mode = ""
    
    #__init__ Helper
    def initGameplayData(self): #Flags and gameplay multipliers
        
        #Dribbling
        self.dribbleDir = -1
        self.dribblingHand = "Right"
        self.dribbleAxis = 0
        
        #Shooting
        self.shootCount = 0
        self.endLen = 1.5 * self.armLengthConst
        self.endAngle = 0
        self.commentary = ""
        self.firstPassSound = True
        
        #Jumping
        self.jumpCount = 0
        
        #Layups:
        self.finishing = 0
        
        #AI Movement:
        self.moveTheta = None
        
        #Blocking:
        self.blocking = False
        self.canBlock = True
        self.prevValue = 0
        
        #Assist Counting:
        self.assistCount = 0
        self.assistTime = 2
        self.assistCheck = False
        self.isAssisted = False
        self.assiter = ""
        
        #Stealing:
        self.stealCount = 0
        self.immobile = False
        self.immobile3D = False
        self.crossover = False
        self.crossoverDelay = 20
        self.stealing = False
        self.displayArm = False
        self.stealCountMax = 0
        self.stealCrossCount = 0
        
        #AI Offense / Defense:
        self.crossoverCooldown = 1001
        self.pickUpCount = 0
        self.rhythm = 100
        self.key = ""
        self.dxList = []
        self.dyList = [] 
        self.currZone = (0, 0)
        self.guardedBy = ""
        self.waitCount = 0
        self.prevPos = []
    
    #__init__ Helper
    def initPlayerStats(self, data, dict):
        #Stats and Name
        for attribute in dict:
            if attribute == "height":
                heightList = dict[attribute]
                height = heightList[0] * data.length / 94
                height += heightList[1] * (data.length / 94) / 12
                dict[attribute] = height
                self.z = height
            setattr(self, attribute, dict[attribute])
        self.release = self.shotForm
        self.arc = self.shotForm
        self.accuracy = (self.accuracyShort + self.accuracyMid + self.accuracyLong) / 3
    
    #__init__ Helper
    def initCountingStats(self):
        #Stats for the player during the game
        self.points = 0
        self.assists = 0
        self.rebounds = 0
        self.steals = 0
        self.blocks = 0
        self.fgm = 0
        self.fga = 0
        self.fgm3 = 0
        self.fga3 = 0
        self.hasTripleDouble = False
        self.hasQuadrupleDouble = False
        self.displayStats = {"FGM":self.fgm, "FGA":self.fga, "POINTS":self.points, 
                             "ASSISTS":self.assists, "REBOUNDS":self.rebounds, 
                             "STEALS":self.steals, "BLOCKS":self.blocks}
    
    #__init__ Helper
    def init3DData(self):
        #3D placeholder coordinates
        self.x3D  = 0
        self.y3D = 0
        self.scaleFactor = 0
        self.z3D = 0 #Head Z in 3D
        self.bodyZ3D = 0
        self.bodyHeight3D = 0
        self.bodyWidth3D = 0
        self.rad3D = 0
        self.armLX3D = 0
        self.armRX3D = 0
        self.armLZ3D = 0
        self.armRZ3D = 0
        self.armLY3D = 0
        self.armRY3D = 0
        self.armWidth3D = 0
        self.crossSectAng = 0
    
    def __init__(self, data, dict, userColor, defaultColor):
        self.initDimensions(data)
        self.initMiscData(data, userColor, defaultColor)
        self.initGameplayData()
        self.initPlayerStats(data, dict)
        self.initCountingStats()
        self.init3DData()

##
# Draw Functions
##

    def draw2D(self, screen, data):
        #Steal Lasso
        if self.displayArm:
            pygame.draw.line(*intify(screen, self.borderColor, (self.x, self.y),
                            (data.ball.x, data.ball.y), data.length / 100))
            pygame.draw.circle(*intify(screen, self.headColor, (data.ball.x, data.ball.y),
                                data.ball.radiusConst * 2, data.length / 100))
                                
        #Head
        pygame.draw.circle(*intify(screen, self.borderColor, (self.x, self.y), self.radius + self.width))
        pygame.draw.circle(*intify(screen, self.headColor, (self.x, self.y), self.radius))
        
        #X if Immobile
        if self.immobile and self in data.defensiveTeam:
            pygame.draw.line(*intify(screen, self.borderColor, (self.x - self.radius,
            self.y - self.radius), (self.x + self.radius, self.y + self.radius),
            data.length / 100 + self.width))
            pygame.draw.line(*intify(screen, self.borderColor, (self.x - self.radius,
            self.y + self.radius), (self.x + self.radius, self.y - self.radius),
            data.length / 100 + self.width))
            pygame.draw.line(*intify(screen, self.headColor, (self.x - self.radius,
            self.y - self.radius), (self.x + self.radius, self.y + self.radius),
            data.length / 100))
            pygame.draw.line(*intify(screen, self.headColor, (self.x - self.radius,
            self.y + self.radius), (self.x + self.radius, self.y - self.radius),
            data.length / 100))
    
    def displayName(self, screen, data): #Draws name if player is pass target
        firstI = self.firstName[0]
        lastName = self.lastName
        name = "%s. %s" % (firstI, lastName)
        font = pygame.font.SysFont("verdana", data.length // 50, bold = True)
        drawText(screen, font, self.x, self.y - 2 * self.radius, name, self.fontColor, self.backgroundColor)
        
    def draw3DCrossSection(self, screen, data):
        #Calculating data
        if self.armLX3D > self.armRX3D: 
            armLX3D, armRX3D, armLZ3D, armRZ3D = \
                self.armRX3D, self.armLX3D, self.armRZ3D, self.armLZ3D
        else:
            armRX3D, armLX3D, armRZ3D, armLZ3D = \
                self.armRX3D, self.armLX3D, self.armRZ3D, self.armLZ3D
        topLeftCoords = (self.x3D - self.bodyWidth3D / 2, self.bodyZ3D - self.bodyHeight3D / 2)
        topLeftCoords2 = (self.x3D - self.bodyWidth3D / 2 - self.width, self.bodyZ3D - self.bodyHeight3D / 2 - self.width)
    
        if self.y3D - (data.length ** 2 + data.width ** 2) ** 0.5 / 2 < data.maxYDraw:
            if self.armLY3D <= 0: #Arms should be drawn before body
            
                #Draw Arm
                pygame.draw.line(*intify(screen, self.borderColor, (armLX3D - self.width, armLZ3D), 
                                (armRX3D + self.width, armRZ3D), self.armWidth3D + self.width * 2))
                pygame.draw.line(*intify(screen, self.headColor, (armLX3D, armLZ3D), 
                                (armRX3D, armRZ3D), self.armWidth3D))
                                
            #Draw Body
            pygame.draw.ellipse(*intify(screen, self.borderColor, (*topLeftCoords2, 
                                self.bodyWidth3D + 2 * self.width, self.bodyHeight3D + 2 * self.width)))
            pygame.draw.ellipse(*intify(screen, self.bodyColor, (*topLeftCoords, self.bodyWidth3D, self.bodyHeight3D)))
            
            #Draw Head
            pygame.draw.circle(*intify(screen, self.borderColor, (self.x3D, self.z3D), self.rad3D + self.width))
            pygame.draw.circle(*intify(screen, self.headColor, (self.x3D, self.z3D), self.rad3D))
            
            if self.armLY3D > 0: #Arms should be drawn after body
                #Draw Arms
                pygame.draw.line(*intify(screen, self.borderColor, (armLX3D - self.width, armLZ3D), 
                                (armRX3D + self.width, armRZ3D), self.armWidth3D + self.width * 2))
                pygame.draw.line(*intify(screen, self.headColor, (armLX3D, armLZ3D), 
                                (armRX3D, armRZ3D), self.armWidth3D))
    
##
# Boolean Checks
##
    
    def inBounds(self, data, court): #Checks if player is in bounds
        cx, cy = data.length / 2, data.width / 2
        if self.x < cx - court.length / 2 or self.x > cx + court.length / 2:
            return False
        elif self.y < cy - court.width / 2 or self.y > cy + court.width / 2:
            return False
        return True
        
    def outsideThreePointArc(self, data, court): #Checks if player shot a three or two
        cx, cy = data.length / 2, data.width / 2
        lx, ty = cx - court.length / 2, cy - court.width / 2
        rx, by = cx + court.length / 2, cy + court.width / 2
        if self.y < ty + court.margin or self.y > by - court.margin:
            return True
        elif self.x > lx + court.threePointDist or self.x < rx - court.threePointDist:
            if (distance(self.x, self.y, lx + court.basketDist, cy) > court.threePointRad and
                data.shootingBasket.name == "Left"):
                return True
            elif (distance(self.x, self.y, rx - court.basketDist, cy) > court.threePointRad and
                data.shootingBasket.name == "Right"):
                return True
        return False
    
    def withinPaint(self, data, court): #Checks if player is within paint
        if (self.x > data.length / 2 + court.length / 2 - court.freeThrowDist and 
            self.x < data.length / 2 + court.length / 2 and
            self.y > data.width / 2 - court.keyWidth / 2 and
            self.y < data.width / 2 + court.keyWidth / 2 and
            data.shootingBasket.name == "Right"):
            return True
        elif (self.x < data.length / 2 - court.length / 2 + court.freeThrowDist and 
              self.x > data.length / 2 - court.length / 2 and
              self.y > data.width / 2 - court.keyWidth / 2 and
              self.y < data.width / 2 + court.keyWidth / 2 and
              data.shootingBasket.name == "Left"):
            return True
        return False
    
    def hasCollided(self, other): #2D Collision
        if distance(self.x, self.y, other.x, other.y) <= (self.radius + other.radius):
            return True
        return False
    
    def hasCollided3D(self, other): #3D Collision
        if distance(self.x3D, self.y3D, other.x3D, other.y3D) <= (self.rad3D + other.rad3D):
            return True
        return False
    
    def checkIfAssisted(self, shotMade): #Checks if player's shot was assisted
        if self.isAssisted and shotMade:
            self.assister.assists += 1
            self.assister.updateStats()
        self.isAssisted = False
        self.assister = ""

##
# Updating Player Data and Flags
##
    
    def updateData(self, data, start, end, cobMatrix):
        #Updates the 3D data for drawing
        self.mode = data.mode
        self.crossSectAng = findCrossSectAngle(*start, *end, data)
        self.armX = self.x + self.armLength * math.cos(self.armPhi) * math.cos(self.armTheta)
        self.armY = self.y - self.armLength * math.cos(self.armPhi) * math.sin(self.armTheta)
        #Following code transforms x-y coordinates based on lin alg change of basis
        self.x3D, self.y3D = changeBasis(data, self.x, self.y, start, cobMatrix)
        depthSpan = (data.length ** 2 + data.width ** 2) ** 0.5
        self.y3D += depthSpan / 2
        if data.shootingBasket.name == "Right": self.y3D = depthSpan - self.y3D
        if self.y3D < 0: self.y3D = 0
        self.scaleFactor = (self.y3D / (depthSpan / 2))
        self.rad3D = self.scaleFactor * scaleVertical(self.radius, data) * data.radScale3D
        self.z3D = scaleZ(self.z, self.scaleFactor, data)
        self.bodyHeight3D = self.height * self.scaleFactor
        self.bodyHeight3D = scaleVertical(self.bodyHeight3D, data)
        self.bodyHeight3D -= self.rad3D
        self.bodyWidth3D = self.bodyWidth * self.scaleFactor
        self.bodyZ3D = self.z3D + self.rad3D + 0.5 * self.bodyHeight3D
        self.armLX3D, self.armLY3D = changeBasis(data, self.armX, self.armY, start, cobMatrix)
        self.armLY3D = round(self.armLY3D, 4)
        self.armRX3D, junk = changeBasis(data, self.x, self.y, start, cobMatrix)
        self.armLX3D = (self.armLX3D - self.armRX3D) * self.scaleFactor + self.armRX3D
        self.armRZ3D = self.z3D + 0.5 * (self.rad3D + self.bodyHeight3D)
        self.armLZ3D = -1 * (abs(self.armLX3D - self.armRX3D) / math.cos(self.armPhi) * 
                        math.sin(self.armPhi)) + self.armRZ3D
        self.armWidth3D = self.armWidth * self.scaleFactor
        #Adjust right arm start point based on theta rotation
        beta = self.armTheta - self.crossSectAng
        self.armRX3D = self.armRX3D + data.shootingDir * self.bodyWidth3D / 2 * math.cos(beta)
    
    def updateStats(self): #Updates player's counting stats
        self.displayStats = {"FGM":self.fgm, "FGA":self.fga, "POINTS":self.points, 
                             "ASSISTS":self.assists, "REBOUNDS":self.rebounds, 
                             "STEALS":self.steals, "BLOCKS":self.blocks}
        self.hasTripleDouble = True
        self.hasQuadrupleDouble = True
        lessCount = 0
        for stat in [self.points, self.assists, self.rebounds, 
                                                    self.steals, self.blocks]:
            if stat < 10:
                lessCount += 1
        if lessCount > 2:
            self.hasTripleDouble = False
        if lessCount > 1:
            self.hasQuadrupleDouble = False
        
    def updateAssistCount(self, data): #Determines whether player has been assisted
        if self.assistCheck:
            if data.mode == "3D" and self is data.shooter:
                self.isAssisted = True
                self.assistCheck = False
                self.assistCount = 0
            elif self.assistCount > self.assistTime * data.timerDelay:
                self.assistCheck = False
                self.assistCount = 0
            else:
                self.assistCount += 1
    
    def resetTo2D(self): #Resets arm length and angle
        self.armPhi = 0
        self.armLength = self.armLengthConst
        self.z = self.height
        self.canBlock = True
        self.immobile3D = False
    
    def overrideAIMethods(self, method):
        newExecutables = []
        for executable in self.executables:
            if executable[0].__name__[0:2] == "ai":
                self.tempExecutables.append((method, executable))
            else:
                newExecutables.append(executable)
        self.executables = newExecutables
    
    def returnAIMethods(self, method):
        for tuple in self.tempExecutables:
            if tuple[0] is method and tuple[1] not in self.executables:
                self.executables.append(tuple[1])
    
    def removeAIMethods(self):
        newExecutables = []
        for executable in self.executables:
            if not executable[0].__name__[0:2] == "ai":
                newExecutables.append(executable)
        self.executables = newExecutables
        self.tempExecutables = []

##
# Non-Animation User Controls
##
    
    def setDribbleStraight(self, data, dx, dy): 
        #Sets dribble ang if moving straight
        if dx > 0:
            self.dribbleAxis = 0
            self.armTheta = -1 * data.dribbleAngle
        elif dx < 0:
            self.dribbleAxis = 0
            self.armTheta = -1 * (math.pi + data.dribbleAngle)
        elif dy > 0:
            self.dribbleAxis = math.pi / 2
            self.armTheta = math.pi + (math.pi / 2 - data.dribbleAngle)
        elif dy < 0:
            self.dribbleAxis = math.pi / 2
            self.armTheta = math.pi / 2 - data.dribbleAngle
        if self.dribblingHand == "Left":
            self.armTheta = rotateAcrossAxis(self.armTheta, self.dribbleAxis)
            
    def setDribbleDiag(self, data, dx, dy, possKeys, keys): 
        #Sets dribble ang if moving diag
        if possKeys[3] in keys and possKeys[0] in keys:
            self.dribbleAxis = math.pi / 4
            self.armTheta = -1 * (math.pi / 2 - data.dribbleAngle)
        elif possKeys[2] in keys and possKeys[1] in keys:
            self.dribbleAxis = math.pi / 4
            self.armTheta = -1 * (math.pi / 2 - data.dribbleAngle) + math.pi
        elif possKeys[0] in keys and possKeys[1] in keys:
            self.dribbleAxis = 3 * math.pi / 4
            self.armTheta = data.dribbleAngle
        elif possKeys[2] in keys and possKeys[3] in keys:
            self.dribbleAxis = 3 * math.pi / 4
            self.armTheta = data.dribbleAngle + math.pi
        if self.dribblingHand == "Left":
            self.armTheta = rotateAcrossAxis(self.armTheta, self.dribbleAxis)
    
    def move(self, data, possKeys, dx, dy): #2D Movement
        multiplier = self.speed
        if data.subMode == "Career" and data.rebounding: #Rebounding has effect
            multiplier = multiplier + ((self.rebounding - 0.75) * 0.5)
        keys = set(possKeys) & data.currKeys
        if len(keys) % 2 == 0:
            multiplier *= 2 ** 0.5 / 2
        self.x += dx * multiplier
        self.y += dy * multiplier
        coll = False
        for player in data.players:
            if not player is self and self.hasCollided(player):
                coll = True
        if self.inBounds(data, data.court) and not coll:
            if len(keys) % 2 != 0:
                self.setDribbleStraight(data, dx, dy)
            else: #Move in two directions at once
                self.setDribbleDiag(data, dx, dy, possKeys, keys)
        elif not self.inBounds(data, data.court) or coll:
            self.x -= dx * multiplier
            self.y -= dy * multiplier
    
    def move3D(self, data, possKeys, dx): #3D Movement
        thetaC = theta = angle(*data.crossSection[0], *data.crossSection[1])
        dStep = data.layupSpeed
        if data.user1Shoot[0] or data.user2Shoot[0]:
            dStep = data.shootSpeed
        scaleDistance = distance(*data.crossSection[0], *data.crossSection[1]) / data.length
        d = dStep * data.d * self.speed * data.defenderSpeedInc
        keys = set(possKeys) & data.currKeys
        if dx > 0:
            theta += 0
        elif dx < 0:
            theta += math.pi
        self.armTheta = rotateAcrossAxis(theta,  thetaC + math.pi / 2)
        self.x -= d * math.cos(theta)
        self.y += d * math.sin(theta)
        coll = False
        for player in data.players:
            if not player is self and self.hasCollided3D(player):
                coll = True
            elif not player is self and self.hasCollided(player):
                coll = True
        if not self.inBounds(data, data.court) or coll:
            self.x += d * math.cos(theta)
            self.y -= d * math.sin(theta)
    
    def switchHand(self, data): #Crossover dribble
        #pygame.mixer.Sound(data.sounds[0])
        rand = random.randint(0, 100)
        if rand < 100 * ((1 - self.ballHandling) * data.crossoverFailChance): #Failed crossover
            theta = (self.dribbleAxis - self.armTheta) % (2 * math.pi)
            if theta > math.pi:
                launchTheta = self.dribbleAxis - math.pi / 2
            else:
                launchTheta = self.dribbleAxis + math.pi / 2
            launchDist = random.randint(data.length // 10, data.length // 5)
            coords = (data.ball.x + launchDist * math.cos(launchTheta),
                      data.ball.y + launchDist * math.sin(launchTheta))
            passStrength = (self.passing + self.strength) / 2 * data.passStrengthAdj
            data.ball.movePassedBall(data.ball, data, passStrength, coords, True)
            data.passer = self
            return False
        self.crossover = True
        self.crossoverDelay = 0
        if self.dribblingHand == "Right":
            self.dribblingHand = "Left"
            self.armTheta = rotateAcrossAxis(self.armTheta, self.dribbleAxis)
        else:
            self.dribblingHand = "Right"
            self.armTheta = rotateAcrossAxis(self.armTheta, self.dribbleAxis)
    
    #passBall Helper
    def calculatePassError(self, data, finCoords):
        errorAdj = 1
        error = errorAdj * (1 - self.passing)
        dist = distance(self.x, self.y, *finCoords)
        rand = random.randint(0, int(error * 100))
        theta = random.randint(0, 359)
        theta *= math.pi / 180
        posX = finCoords[0] + (rand / 100) * dist * math.cos(theta)
        posY = finCoords[1] - (rand / 100) * dist * math.sin(theta)
        rand2 = random.randint(0, 100)
        if rand2 < (self.passing + 0.5 * (1 - self.passing)) * 100:
            tempX = self.x
            self.x = posX 
            while not self.inBounds(data, data.court): #Make sure pass is in bounds
                dirX = numpy.sign(data.length / 2 - self.x)
                self.x += dirX
            tempY = self.y
            self.y = posY
            while not self.inBounds(data, data.court):
                dirY = numpy.sign(data.width / 2 - self.y)
                self.y += dirY
            posX, posY = self.x, self.y
            self.x, self.y = tempX, tempY
        return(posX, posY)
    
    def passBall(self, data, savePrevTarget = False): #Initiate pass
        if isinstance(data.passTarget, Player):
            if savePrevTarget:
                data.prevPassTarget = data.passTarget
            if data.passTarget.moveTheta == None:
                passFinCoords = (data.passTarget.x, data.passTarget.y)
            else:
                coords = [data.passTarget.x, data.passTarget.y]
                while True:
                    step = data.length / 800
                    coords[0] += step * math.cos(data.passTarget.moveTheta)
                    coords[1] -= step * math.sin(data.passTarget.moveTheta)
                    passStrength = (self.strength + self.passing) / 2 * data.passStrengthAdj
                    t1 = distance(data.passTarget.x, data.passTarget.y, coords[0], coords[1]) /  (data.d * data.passTarget.speed)
                    t2 = distance(data.ball.x, data.ball.y, coords[0], coords[1]) / (data.d * passStrength * 2)
                    if almostEqual(t1, t2, 1):
                        break
                passFinCoords = tuple(coords)
            passFinCoords = self.calculatePassError(data, passFinCoords)
            data.passFinCoords = passFinCoords
            data.passTarget.aiReceivePass(data.passTarget, data, passFinCoords, True)
            passStrength = (self.strength + self.passing) / 2 * data.passStrengthAdj
            data.ball.movePassedBall(data.ball, data, passStrength, passFinCoords, True)
            data.passTarget = ""
            data.passer = self
    
    def startDribbling(self, data):
        self.dribble(self, data, True)
    
    def stopDribbling(self, data):
        self.dribble(self, data, False, True)
    
    def Block(self, data): #Blocking
        jumpHeight = data.minJump + self.jump * (data.maxJump - data.minJump)
        if data.user1Shoot[0] or data.user2Shoot[0]:
            jumpHeight = data.minShootJump + self.jump * (data.maxShootJump - data.minShootJump)
        self.endAngle = data.blockAngle
        endLen = 1.5 * self.armLengthConst
        self.extendArm(self, endLen, True, 1.7)
        self.rotateArm(self, self.endAngle, 1, self.block, True)
        self.Jump(self, data, jumpHeight + self.height, True)
        self.blocking = True

##
# Non-Animation AI Functions
##
    
    # def trackPosition(self, data, coords, speedMultiplier = 1): #AI Tracking
    #     dstep = data.d * self.speed * speedMultiplier
    #     theta = angle(*coords, self.x, self.y)
    #     dx = dstep * math.cos(theta)
    #     dy = dstep * math.sin(theta)
    #     self.x += dx
    #     self.y -= dy
    #     coll = False
    #     for player in data.players:
    #         if not player is self and self.hasCollided(player):
    #             coll = True
    #     if coll:
    #         self.x -= dx
    #         self.y += dy
    #     self.moveTheta = theta % (2 * math.pi)
    #     if distance(self.x, self.y, *coords) <= 0.5 * dstep:
    #         self.x = coords[0]
    #         self.y = coords[1]
    #         self.moveTheta = None
    #         return (True, coll)
    #     return (False, coll)
    
    def trackPosition(self, data, coords, speedMultiplier = 1): #AI Tracking
        dstep = data.d * self.speed * speedMultiplier
        theta = angle(*coords, self.x, self.y)
        dx = dstep * math.cos(theta)
        dy = dstep * math.sin(theta)
        self.x += dx
        self.y -= dy
        coll = False
        oppTeam = data.user2Team
        if self in data.user2Team:
            oppTeam = data.user1Team
        for player in data.players:
            if not player is self and self.hasCollided(player):
                rand = random.randint(1, 100)
                stDif = self.strength - player.strength + 0.5
                if (rand < stDif * 100 and not player.immobile and player in
                    oppTeam): 
                    #AI muscles through
                    player.x += dx
                    player.y -= dy
                    coll = False
                    for pl in data.players:
                        if (not pl is self and not pl is player and
                            player.hasCollided(pl)):
                            coll = True
                    if coll:
                        player.x -= dx
                        player.y += dy
                        self.x -= dx
                        self.y += dy
                else:
                    self.x -= dx
                    self.y += dy
                    coll = True
        self.moveTheta = theta % (2 * math.pi)
        if distance(self.x, self.y, *coords) <= 0.5 * dstep:
            self.x = coords[0]
            self.y = coords[1]
            self.moveTheta = None
            return (True, coll)
        return (False, coll)
    
    def pickUpBall(self, data): #AI Picking Up Loose Balls
        for other in data.players:
            if (abs(distance(other.x, other.y, data.ball.x, data.ball.y)) <= self.radius + data.ball.radius
                and not other is data.passer and other.strength > self.strength):
                return
        if (abs(distance(self.x, self.y, data.ball.x, data.ball.y)) <= self.radius + data.ball.radius
            and (not self is data.passer or data.ball.passResult)):
            data.ball.player = self
            if self in data.user1Team:
                switchUser1(data, self)
            elif self in data.user2Team:
                switchUser2(data, self)
            if data.rebounding:
                displayPauseText(data, "Rebound %s %s!" % (self.firstName, self.lastName))
                self.rebounds += 1
                data.rebounding = False
                self.updateStats()
            elif not self in data.offensiveTeam:
                if data.passer is data.user1 or data.prevPassTarget is data.user1:
                    #Career Grades- Turnover on User1
                    data.user1Turnovers += 1
                displayPauseText(data, "Stolen By %s %s!" % (self.firstName, self.lastName))
                self.steals += 1
                self.updateStats()
            else:
                self.assistCheck = True
                self.assister = data.passer
            self.pickUpCount = 0
            data.prevPassTarget = ""
            self.startDribbling(data)
    
##
# User-Controlled Animations
##
    
    #This one's just for debugging
    @staticmethod
    def rotateTheta(self, endAngle, direction, firstPass = False): #Rotates theta
        if firstPass:
            self.executables.append([Player.rotateTheta, endAngle, direction])
        else:
            increment = self.release * math.pi / 50
            self.armTheta += direction * increment
            if self.armTheta > endAngle and direction > 0:
                self.armTheta = endAngle
                self.executables.remove([Player.rotateTheta, endAngle, direction])
            elif self.armTheta < endAngle and direction < 0:
                self.armTheta = endAngle
                self.executables.remove([Player.rotateTheta, endAngle, direction])
    
    #Again just for debugging
    @staticmethod
    def aiDebugMove(self, data, firstPass = False):
        if firstPass:
            self.executables.append([Player.aiDebugMove, data])
        else:
            coords = (0, data.width)
            result = self.trackPosition(data, coords)[0]
            if result:
                self.executables.remove([Player.aiDebugMove, data])
    
    #Steal Helper
    def resetStealIfSuccessful(self, data):
        displayPauseText(data, "Stolen By %s %s!" % (self.firstName, self.lastName))
        self.steals += 1
        self.updateStats()
        if data.ball.player is data.user1:
            #Career Grades- Turnover on User1
            data.user1Turnovers += 1
        data.ball.player = self
        self.executables.remove([Player.Steal, data])
        self.stealing = False
        self.stealCount = 0
    
    #Steal Helper
    def resetStealIfNotSuccessful(self, data):
        self.stealCount = 0
        self.immobile = False
        self.stealing = False
        self.displayArm = False
        if data.mode == "3D":
            self.immobile3D = True
        self.executables.remove([Player.Steal, data])
                
    @staticmethod
    def Steal(self, data, firstPass = False): #Initiate stealing the ball
        self.stealCountMax = (data.stealImmobileCount + (1 - (self.steal - 0.5) * 2) 
                              * (data.stealCountMax - data.stealImmobileCount))
        self.stealCrossCount = int(data.stealCrossoverCount + (1 - (self.steal - 0.5) * 2) 
                              * (data.stealCrossCountMax - data.stealCrossoverCount))
        if firstPass:
            self.stealing = True
            self.executables.append([Player.Steal, data])
            self.armTheta = angle(data.ball.x, data.ball.y, self.x, self.y)
            self.displayArm = True
        else:
            self.stealCount += 1
            if (isinstance(data.ball.player, Player) and
                data.ball.player.crossover) and self.stealCount < self.stealCrossCount:
                self.immobile = True
                self.displayArm = False
            if not self.immobile and self.stealCount == self.stealCrossCount and data.mode == "2D":
                self.displayArm = False
                if isinstance(data.ball.player, Player):
                    diff = self.steal - data.ball.player.ballHandling
                else:
                    diff = 0.5
                diff += 0.5
                rand = random.randint(0, 100)
                if rand < diff * data.stealChance * 100:
                    self.resetStealIfSuccessful(data)
            if self.immobile and self.stealCount == data.stealImmobileCount:
                self.immobile = False
            if self.stealCount > self.stealCountMax or data.mode == "3D":
                self.resetStealIfNotSuccessful(data)
            
    
    @staticmethod
    def dribble(self, data, firstPass = False, stopDribbling = False): #Dribbles the ball
        if firstPass:
            self.executables.append([Player.dribble, data])
        else:
            data.ball.radius += self.dribbleDir * data.length / 3000
            if data.ball.radius <= data.length / 200 or data.ball.radius > data.ballRadius:
                self.dribbleDir *= -1
            if stopDribbling or data.mode != "2D" or data.ball.player == "":
                data.ball.radius = data.ballRadius
                self.executables.remove([Player.dribble, data])

    #Used for shooting and blocking
    @staticmethod
    def rotateArm(self, endAngle, direction, multiplier, firstPass = False): #Rotates arm to final angle
        if firstPass:
            self.executables.append([Player.rotateArm, endAngle, direction, multiplier])
        else:
            increment = math.pi / (40 + (1 - multiplier) * 60)
            self.armPhi += direction * increment * multiplier
            if self.armPhi > endAngle and direction > 0:
                self.armPhi = endAngle
                self.executables.remove([Player.rotateArm, endAngle, direction, multiplier])
            elif self.armPhi < endAngle and direction < 0:
                self.armPhi = endAngle
                self.executables.remove([Player.rotateArm, endAngle, direction, multiplier])
            elif self.mode == "2D":
                self.executables.remove([Player.rotateArm, endAngle, direction, multiplier])
    
    #Used for shooting and blocking
    @staticmethod
    def extendArm(self, endLen, firstPass = False, multiplier = 1): #Extends arm to final length
        if firstPass:
            self.executables.append([Player.extendArm, endLen, False])
        else:
            direction = numpy.sign(endLen - self.armLengthConst)
            increment = self.armLengthConst / 40 * multiplier
            self.armLength += direction * increment * self.release
            if self.armLength > endLen and direction > 0:
                self.armLength = endLen
                self.executables.remove([Player.extendArm, endLen, False])
            elif self.armLength < endLen and direction < 0:
                self.armLength = endLen
                self.executables.remove([Player.extendArm, endLen, False])
            elif self.mode == "2D":
                self.executables.remove([Player.extendArm, endLen, False])
    
    #Used for shooting and blocking
    @staticmethod
    def layupMove(self, data, dx, dy, firstPass = False): #Movement while shooting
        if firstPass:
            self.executables.append([Player.layupMove, data, dx, dy])
        else:
            dX = dx * self.speed
            dY = dy * self.speed
            self.x += dX
            self.y += dY
            coll = False
            for player in data.players:
                if not player is self and self.hasCollided3D(player):
                    coll = True
                elif not player is self and self.hasCollided(player):
                    coll = True
            if not self.inBounds(data, data.court) or coll:
                self.x -= dX
                self.y -= dY
            elif self.x + self.radius > data.shootingBasket.x and data.shootingBasket.name == "Right":
                self.x -= dX
                self.y -= dY
            elif self.x - self.radius < data.shootingBasket.x and data.shootingBasket.name == "Left":
                self.x -= dX
                self.y -= dY
            if self.z == self.height:
                self.executables.remove([Player.layupMove, data, dx, dy])
    
    #Used for shooting and blocking
    @staticmethod
    def Jump(self, data, jumpHeight = None, firstPass = False):
        if firstPass:
            if jumpHeight == None:
                jumpHeight = data.minJump + self.jump * (data.maxJump - data.minJump) + self.height
            self.executables.append([Player.Jump, data, jumpHeight])
        vInit = (19.6 * (jumpHeight - self.height)) ** 0.5
        self.jumpCount += data.jumpInterval
        self.z = self.height + vInit * self.jumpCount - 4.9 * self.jumpCount ** 2
        if self.z < self.height or data.mode == "2D":
            self.z = self.height
            self.jumpCount = 0
            self.blocking = False
            self.executables.remove([Player.Jump, data, jumpHeight])
    
    #Shoot Helper
    def determineMadeShot(self, data, dist, value): #Binary value if shot made or missed
        if self.shootCount == 0:
            error = (1 - (self.endAngle - self.armPhi) / self.endAngle)
            if error < 0: error = 0
        else:
            error = (1 - (self.shootCount * data.shotErrorWeight) * 0.01)
            if error < 0: error = 0
        if dist >= 32 * data.length / 94:
            acc = self.accuracyLong * 0.2
        elif dist >= 23.75 * data.length / 94:
            acc = self.accuracyLong
        elif dist >= 10 * data.length / 94:
            acc = self.accuracyMid
        else:
            acc = self.accuracyShort
        rand = random.randint(1, 100)
        self.fga += 1
        if value == 3:
            self.fga3 += 1
        if rand < acc * error * 100:
            #print("Made shot!", error)
            if self in data.user1Team:
                data.user1Score += value
            elif self in data.user2Team:
                data.user2Score += value
            self.points += value
            self.prevValue = value
            self.fgm += 1
            if value == 3:
                self.fgm3 += 1
            return (True, error)
        else:
            #print("Missed shot...", error)
            return (False, error)
    
    #Shoot Helper
    def determineEndPosition(self, shotMade, error, data, dev = None):
        x = (data.shootingBasket.netRX3D + data.shootingBasket.netLX3D) / 2
        netMargin = data.shootingBasket.height3D / 6
        y = data.shootingBasket.z3D - 2 * netMargin
        if not shotMade:
            maxDev = abs(data.shootingBasket.newRX3D - data.shootingBasket.newLX3D) / 2
            if dev == None:
                dev = (1 - error) * maxDev
            rand = random.randint(0, 1)
            if rand == 0:
                x -= dev
            else:
                x += dev
            if data.shootingBasket.newLX3D > data.shootingBasket.newRX3D:
                lx3D = data.shootingBasket.newRX3D
                rx3D = data.shootingBasket.newLX3D
            else:
                lx3D = data.shootingBasket.newLX3D
                rx3D = data.shootingBasket.newRX3D
            if x + data.ball.rad3D * 1.2  < lx3D:
                x = lx3D - data.ball.rad3D * 1.2
            elif x - data.ball.rad3D * 1.2 > rx3D:
                x = rx3D + data.ball.rad3D * 1.2
        return (x, y)
    
    #Shoot Helper
    def calculateEndAngle(self, data, finZ):
        x = (data.shootingBasket.netLX3D + data.shootingBasket.netRX3D) / 2
        netMargin = data.shootingBasket.height / 6
        if data.shootingDir < 0:
            endAngle = angle(self.x3D, finZ, x, data.shootingBasket.z3D - netMargin * 2) - math.pi
        else:
            endAngle = -1 * angle(self.x3D, finZ, x, data.shootingBasket.z3D - netMargin * 2)
        arcAdj = 1 - self.arc / 2
        self.endAngle = math.pi / 2 - (arcAdj * (math.pi / 2 - endAngle))
    
    #Shoot Helper:
    def shotReachedPeak(self):
        rotate = False
        extend = False
        for executable in self.executables:
            if executable[0] is Player.rotateArm:
                rotate = True
            elif executable[0] is Player.extendArm:
                extend = True
        return not rotate and not extend

    @staticmethod
    def shoot(self, data, shootKey, dx, dy, value, firstPass = False): #Shoots the ball
        if firstPass:
            jumpHeight = data.minShootJump + self.jump * (data.maxShootJump - data.minShootJump)
            finZ = self.armRZ3D + jumpHeight
            self.calculateEndAngle(data, finZ)
            self.Jump(self, data, jumpHeight + self.height, True)
            self.layupMove(self, data, dx, dy, True)
            self.extendArm(self, self.endLen, True)
            self.rotateArm(self, self.endAngle, 1, self.release, True)
            self.executables.append([Player.shoot, data, shootKey, dx, dy, value])
        else:
            if self.shotReachedPeak():
                if shootKey == "!" and "!" in data.currKeys: #AI Good Shot
                    data.currKeys.remove(shootKey)
                    self.shootCount = -1
                elif shootKey == "@" and self.shootCount == 10 and "@" in data.currKeys: #AI Bad Shot
                    data.currKeys.remove(shootKey)
                self.shootCount += 1
            if shootKey not in data.currKeys or almostEqual(self.z, self.height, 0.5):
                dist = distance(self.x, self.y, data.shootingBasket.x, data.shootingBasket.y)
                shotMade, error = self.determineMadeShot(data, dist, value)
                self.commentary = random.choice(data.shootSounds)
                endPos = self.determineEndPosition(shotMade, error, data)
                self.shootCount = 0
                self.executables.remove([Player.shoot, data, shootKey, dx, dy, value])
                data.ball.moveInArc(data.ball, data, self, endPos, shotMade, dist, True)
    
    #Layup Helper
    def determineMissedDunk(self, data): #Binary value if shot made or missed
        error = 1
        acc = self.accuracyShort
        rand = random.randint(1, 100)
        self.fga += 1
        if rand < acc * error * 100:
            return False
        else:
            self.updateStats()
            return True
    
    #Layup Helper:
    def determineMadeShotDunk(self, data, value):
        if self in data.user1Team:
            data.user1Score += value
        elif self in data.user2Team:
            data.user2Score += value
        self.points += value
        self.prevValue = value
        self.fgm += 1
        return True
    
    #Layup Helper
    def dunkBall(self, data, value, shootKey, dx, dy, jumpHeight):
        self.z -= data.length / 400
        shotMade = self.determineMadeShotDunk(data, value)
        self.commentary = random.choice(data.layupSounds)
        data.ball.dunkBall(data.ball, data, self, shotMade, True)
        self.executables.remove([Player.layup, data, shootKey, dx, dy, value])
        if [Player.extendArm, self.endLen] in self.executables:
            self.executables.remove([Player.extendArm, self.endLen])
        if [Player.rotateArm, self.endAngle, 1] in self.executables:
            self.executables.remove([Player.rotateArm, self.endAngle, 1])
        if [Player.layupMove, data, dx, dy] in self.executables:
            self.executables.remove([Player.layupMove, data, dx, dy])
        for executable in self.executables:
            if (executable[0] == Player.extendArm or
                executable[0] == Player.rotateArm or
                executable[0] == Player.layupMove):
                self.executables.remove(executable)
        self.executables.remove([Player.Jump, data, jumpHeight])
        self.jumpCount = 0
        try:
            self.executables.pop()
        except:
            pass
    
    #Layup Helper
    def layupBall(self, data, value, shootKey, dx, dy):
        dist = distance(self.x, self.y, data.shootingBasket.x, data.shootingBasket.y)
        shotMade, error = self.determineMadeShot(data, dist, value)
        self.commentary = random.choice(data.layupSounds)
        endPos = self.determineEndPosition(shotMade, error, data, 0)
        self.shootCount = 0
        data.ball.moveInArc(data.ball, data, self, endPos, shotMade, dist, True)
        self.executables.remove([Player.layup, data, shootKey, dx, dy, value])

    @staticmethod
    def layup(self, data, shootKey, dx, dy, value, firstPass = False):
        jumpHeight = data.minJump + self.jump * (data.maxJump - data.minJump) + self.height
        if firstPass:
            self.calculateEndAngle(data, jumpHeight)
            self.Jump(self, data, jumpHeight, True)
            self.layupMove(self, data, dx, dy, True)
            self.executables.append([Player.layup, data, shootKey, dx, dy, value])
        else:
            vInit = (19.6 * (jumpHeight - self.height)) ** 0.5
            countPeak = vInit / 19.6
            if abs(self.jumpCount - countPeak) <= data.jumpInterval / 2:
                self.endAngle = math.pi / 3
                self.extendArm(self, self.endLen, True)
                self.rotateArm(self, self.endAngle, 1, self.release, True)
            elif self.jumpCount > countPeak:
                if self.shotReachedPeak():
                    self.shootCount += 1
                if (almostEqual(data.ball.Z3D + data.ball.rad3D, data.shootingBasket.z3D - data.shootingBasket.height / 6, 2)
                    and data.ball.X3D - data.ball.rad3D > data.shootingBasket.netLX3D
                    and data.ball.X3D + data.ball.rad3D < data.shootingBasket.netRX3D
                    and isinstance(self, Center)): #Dunk
                    for player in data.defensiveTeam:
                        result = data.ball.checkIfBlocked(player, data, False)
                        if result:
                            result = data.ball.checkBlockedDunk(data, self, player)
                            if result:
                                self.executables.remove([Player.layup, data, shootKey, dx, dy, value])
                                break
                    if not result:
                        result = self.determineMissedDunk(data)
                        if result: #Missed Dunk
                            result = data.ball.checkBlockedDunk(data, self, self, True)
                            self.executables.remove([Player.layup, data, shootKey, dx, dy, value])
                    if not result:
                        self.dunkBall(data, value, shootKey, dx, dy, jumpHeight)
                elif shootKey not in data.currKeys or almostEqual(self.z, self.height, 5):
                    self.layupBall(data, value, shootKey, dx, dy)

##
# AI-Controlled Animations
##
    
    @staticmethod
    def aiReceivePass(self, data, coords, firstPass = False): #Track pass if ai is target
        if firstPass:
            self.overrideAIMethods(Player.aiReceivePass)
            self.executables.append([Player.aiReceivePass, data, coords])
        else:
            result = self.trackPosition(data, coords)[0]
            if data.ball.player != "":
                self.moveTheta = None
                self.returnAIMethods(Player.aiReceivePass)
                self.executables.remove([Player.aiReceivePass, data, coords])
    
    #aiReboundBall Helper
    def findReboundCoords(self, data, theta, dist, player):
        coords = [data.ball.x, data.ball.y]
        count = 0
        while True:
            multiplier = (self.rebounding - 0.75) * 3 + 1
            step = data.length / 800
            d = data.length / 400
            xDir = -1 * data.shootingDir
            yDir = data.shootingDir
            coords[0] += xDir * step * math.cos(theta)
            coords[1] -= yDir * step * math.sin(theta)
            inc = 0.2 * (data.length / dist) + (1 - player.strength) * d
            countFin = data.shootingBasket.z / inc * d / step
            t1 = distance(self.x, self.y, coords[0], coords[1]) /  (data.d * self.speed * multiplier)
            t2 = distance(data.ball.x, data.ball.y, coords[0], coords[1]) / d
            if count > countFin:
                break
            elif almostEqual(t1, t2, 1):
                break
            count += 1
        coords = tuple(coords)
        return coords
    
    @staticmethod
    def aiReboundBall(self, player, data, theta, dist, firstPass = False, coords = (0, 0)):
        #Rebound ball after missed or blocked shot
        if firstPass:
            coords = self.findReboundCoords(data, theta, dist, player)
            self.overrideAIMethods(Player.aiReboundBall)
            self.executables.append([Player.aiReboundBall, player, data, theta, dist, False, coords])
        else:
            multiplier = (self.rebounding - 0.75) * 3 + 1
            result = self.trackPosition(data, coords, multiplier)[0]
            if result or data.ball.player != "":
                self.moveTheta = None
                self.returnAIMethods(Player.aiReboundBall)
                self.executables.remove([Player.aiReboundBall, player, data, theta, dist, False, coords])
    
    #aiDefensive Helper
    def findMan(self, data):
        typ = type(self)
        for opponent in data.offensiveTeam:
            if isinstance(opponent, typ):
                return opponent
    
    #aiDefensive Helper
    def aiDefensive2D(self, data, guarding):
        #Guard shooter giving space proportional to distance to basket
        if data.ball.player == "": #Pick up loose balls
            self.trackPosition(data, (data.ball.x, data.ball.y))
            self.pickUpBall(data)
            return
        rand = random.randint(1, 1000)
        if (not self.stealing and isinstance(data.ball.player, Player) and 
            distance(self.x, self.y, data.ball.x, data.ball.y) <=
            data.ball.radius + self.armLength * 1.5 and rand < 
            self.steal * 0.015 * 1000): #Steal the ball
            self.Steal(self, data, True)
        if not self.immobile:
            minSpace = data.length / 20
            maxSpace = data.length / 5
            space = (distance(guarding.x, guarding.y, data.shootingBasket.x, data.shootingBasket.y)
                    / data.length) * (maxSpace - minSpace) + minSpace
            theta = angle(guarding.x, guarding.y, data.shootingBasket.x, data.shootingBasket.y)
            pos = (guarding.x - space * math.cos(theta), guarding.y + space * math.sin(theta))
            result, coll = self.trackPosition(data, pos)
            space = 2 * self.radius
            #Collision check
            while coll:
                space += 4
                pos = (guarding.x - space * math.cos(theta), guarding.y + space * math.sin(theta))
                result, coll = self.trackPosition(data, pos)
                if space > data.length:
                    break
            #If shooter is close to the basket, prevent dunks
            if (almostEqual(self.x, data.shootingBasket.basketX, 5) and
                almostEqual(self.y, data.shootingBasket.y, 5) and
                distance(self.x, self.y, guarding.x, guarding.y) <
                4 * self.radius):
                self.x = data.shootingBasket.basketX
                self.y = data.shootingBasket.y
    
    #aiDefensive Helper
    def aiDefensive3D(self, data, guarding):
        if ((guarding is data.user1 or guarding is data.user2 or 
            (data.numPlayers < 2 and guarding is data.ball.player)) and not
            self.immobile3D and not self.immobile):
            #Get closer to user
            space = data.length / 15
            theta = angle(guarding.x, guarding.y, data.shootingBasket.x, data.shootingBasket.y)
            pos = (guarding.x - space * math.cos(theta), guarding.y + space * math.sin(theta))
            mult = data.layupSpeed
            if data.user1Shoot[0] or data.user2Shoot[0]:
                mult = data.shootSpeed
            result = self.trackPosition(data, pos, mult)[0]
            #Block shot
            blocking = False
            for executable in self.executables:
                if executable[0].__name__ == "Jump":
                    blocking = True
            if not blocking:
                self.Block(data)
    
    @staticmethod
    def aiDefensive(self, data, firstPass = False): #Defensive AI
        if firstPass:
            self.executables.append([Player.aiDefensive, data])
        elif self in data.offensiveTeam:
            self.executables.remove([Player.aiDefensive, data])
        if self is data.user1 or self is data.user2:
            return
        elif not firstPass:
            guarding = self.findMan(data)
            guarding.guardedBy = self
            if data.mode == "2D" and not data.rebounding:
               self.aiDefensive2D(data, guarding)
            elif data.mode == "3D":
                self.aiDefensive3D(data, guarding)
    
    #AI Helper
    def findZoneI(self, data): #Initially, goes for a random zone
        newZones = []
        team = data.user2Team
        if self in data.user1Team:
            team = data.user1Team
        for zone in self.zones:
            if data.shootingBasket.name == "Left":
                zone = (data.length - zone[0], zone[1])
            for player in team: #Make sure players start at opposite sides of court
                if (numpy.sign(zone[1] - data.width / 2) !=
                    numpy.sign(player.currZone[1] - data.width / 2)
                    and not player is data.user1 and not player is
                    data.user2):
                    newZones.append(zone)
        rand = random.randint(0, len(newZones) - 1)
        return newZones[rand]
    
    #aiOffensive Helper
    def findZone(self, data): #Finds best offensive zone to go to
        averageMaxDist = 0
        bestZone = (0, 0)
        for rawZone in self.zones:
            zone = rawZone
            if data.shootingBasket.name == "Left":
                zone = (data.length - rawZone[0], rawZone[1])
            if zone != (self.x, self.y):
                sum = 0
                count = 0
                dTeam = data.user2Team
                oTeam = data.user1Team
                if self in data.user2Team:
                    dTeam = data.user1Team
                    oTeam = data.user2Team
                for player in dTeam:
                    dist = distance(player.x, player.y, *zone)
                    sum += dist
                    count += 1
                for player in oTeam:
                    if player.currZone != (0, 0):
                        dist = distance(*zone, *player.currZone)
                        sum += dist
                        count += 1
                if sum / count > averageMaxDist:
                    averageMaxDist = sum / count
                    bestZone = zone
        #Cuts to basket if closer to basket than defender
        if isinstance(self.guardedBy, Player):
            if (distance(self.x, self.y, data.shootingBasket.basketX, data.shootingBasket.y) <
                distance(self.guardedBy.x, self.guardedBy.y, data.shootingBasket.basketX, 
                data.shootingBasket.y)):
                bestZone = (data.shootingBasket.basketX, data.shootingBasket.y)
        return bestZone

    def aiOffensive2D(self, data):    
        if self.currZone != (0, 0):
            #Go to current zone
            result, coll = self.trackPosition(data, self.currZone)
            #Collision check
            if coll:
                for i in range(len(self.zones)):
                    self.currZone =  self.zones[i]
                    if data.shootingBasket.name == "Left":
                        self.currZone = (data.length - self.currZone[0], self.currZone[1])
                    result, coll = self.trackPosition(data, self.currZone)
                    if not coll:
                        return
            #Change zones if there is collision
            if result:
                if self.currZone == (data.shootingBasket.basketX, data.shootingBasket.y):
                    self.currZone =  self.findZone(data)
                else:
                    self.currZone = (0, 0)
        #If reached zone, find new zone
        else:
            self.waitCount += 1
            if self.waitCount > data.aiWaitTime * data.timerDelay:
                self.waitCount = 0
                self.currZone =  self.findZone(data)
    
    def aiDribble(self, data, dx, dy): #AI Move Helper, sets dribble angle
        self.dxList.append(dx)
        self.dyList.append(dy)
        if len(self.dxList) > 10:
            self.dxList.pop(0)
        if len(self.dyList) > 10:
            self.dyList.pop(0)
        dx = sum(self.dxList) / len(self.dxList)
        dy = sum(self.dyList) / len(self.dyList)
        alpha = 0.5
        if dx < alpha and dy > alpha:
            if dx == 0:
                return
            self.setDribbleStraight(data, abs(dx) // dx, 0)
        elif dx > alpha and dy < alpha:
            if dy == 0:
                return
            self.setDribbleStraight(data, 0, abs(dy) // dy)
        else:
            if dx > 0 and dy > 0:
                keys = [3, 4]
            elif dx < 0 and dy > 0:
                keys = [2, 3]
            elif dx > 0 and dy < 0:
                keys = [1, 4]
            elif dx < 0 and dy < 0:
                keys = [1, 2]
            else:
                return
            possKeys = [1, 2, 3, 4]
            self.setDribbleDiag(data, dx, dy, possKeys, keys)
    
    def aiMove(self, data, override = False, guarder = None): #Moves the AI Player
        if override: #Dribble around immobile
            dx = 0
            dy = 1
            if self.y - guarder.y < 0:
                dy = -1
            if abs(self.y - guarder.y) < self.radius * 2:
                dx = -1
                if data.shootingBasket.name == "Left":
                    dx = 1
            overrideDX, overrideDY = True, True
        dy = 0
        overrideDX = False #Flags for OOB / Backcourt
        overrideDY = False
        if data.shootingBasket.name == "Left":
            dx = -1
            if self.x > 9 * data.court.length / 20:
                overrideDX = True
        else:
            dx = 1
            if self.x < 11 * data.court.length / 20:
                overrideDX = True
        if self.x < data.court.length / 8:
            dx = 1
            overrideDX = True
        elif self.x > 7 * data.court.length / 8:
            dx = -1
            overrideDX = True
        if self.y < data.width / 2 - 7 * data.court.width / 16:
            dy = 1
            overrideDY = True
        elif self.y > data.width / 2 + 7 * data.court.width / 16:
            dy = -1
            overrideDY = True
        averageDist = 0
        count = 0
        for player in data.defensiveTeam:
             if not player.immobile:
                count += 1
                averageDist += distance(self.x, self.y, data.shootingBasket.x, data.shootingBasket.y)
        if count != 0:
            averageDist = averageDist / count
        else:
            averageDist = data.court.length
        if averageDist < 15 * data.court.length / 94:
            dx *= -1
        if not overrideDY: #Goes up or down depending which is freer
            topDist = 0
            botDist = 0
            for player in data.defensiveTeam:
                if (self.x != player.x and 
                    int(abs(self.x - player.x) / (self.x - player.x) != dx)):
                    if self.y > player.y:
                        topDist += distance(self.x, self.y, player.x, player.y)
                    else:
                        botDist += distance(self.x, self.y, player.x, player.y)
            if botDist < topDist:
                dy = -1
            else:
                dy = 1
        multiplier = self.speed * 1.2
        self.x += dx * multiplier
        self.y += dy * multiplier
        coll = False
        collPlayer = None
        for player in data.players:
            if not player is self and self.hasCollided(player):
                coll = True
                collPlayer = player
        if coll: #Handle collision
            if override:
                self.x -= dx * multiplier
                coll = False
                for player in data.players:
                    if not player is self and self.hasCollided(player):
                        coll = True
                if coll:
                    self.y -= dy * multiplier
            elif collPlayer is guarder:
                rand = random.randint(1, 100)
                stDif = self.strength - guarder.strength + 0.5
                if rand < stDif * 100: #AI muscles through
                    guarder.x += dx * multiplier
                    guarder.y += dy * multiplier
                    coll = False
                    for player in data.players:
                        if (not player is self and not player is guarder and
                            guarder.hasCollided(player)):
                            coll = True
                    if coll:
                        guarder.x -= dx * multiplier
                        guarder.y -= dy * multiplier
                        self.x -= dx * multiplier
                        self.y -= dy * multiplier
                else:
                    self.x -= dx * multiplier
                    self.y -= dy * multiplier
            else:
                self.x -= dx * multiplier
                self.y -= dy * multiplier
        else:
            self.aiDribble(data, dx, dy)
    
    def aiPass(self, data, rand): #AI decides to pass the ball
        defensiveThetaList = []
        for player in data.defensiveTeam:
            defensiveThetaList.append(angle(self.x, self.y, player.x, player.y))
        maxDist = 0
        maxPlayer = None
        for player in data.offensiveTeam:
            if player is self:
                continue
            theta = angle(self.x, self.y, player.x, player.y)
            safePass = True
            for theta2 in defensiveThetaList: #Check if no nearby defenders
                if almostEqual(theta, theta2, math.pi / 8):
                    safePass = False
            if (player.x < 53 * data.court.length / 100 and data.shootingBasket.name
                == "Right") or (player.x > 47 * data.court.length / 100 
                and data.shootingBasket.name == "Left"): #No backcourt
                safePass = False
            if safePass:
                dist = 0
                for player2 in data.defensiveTeam:
                    dist += distance(player.x, player.y, player2.x, player2.y)
                if dist > maxDist:
                    maxDist = dist
                    maxPlayer = player
        if maxDist > data.court.length: #Open player must pass
            data.passTarget = maxPlayer
            self.passBall(data)
            return True
        elif (maxPlayer != None and data.properCount % self.rhythm == 0 
            and rand < self.passing * 100):
            data.passTarget = maxPlayer
            self.passBall(data)
            return True
        elif data.careerGame and data.callForPass: #Call for pass in career game
            data.passTarget = data.user1
            self.passBall(data, True)
            data.callForPass = False
        return False
    
    def aiShoot(self, data, shotProb): #AI Shoots the ball
        if self.y >= data.width / 2:
            self.armTheta = 3 * math.pi / 4 + angle(self.x, self.y, data.shootingBasket.x, data.shootingBasket.y)
        else:
            self.armTheta = 5 * math.pi / 4 + angle(self.x, self.y, data.shootingBasket.x, data.shootingBasket.y)
        rand = random.randint(1, 100)
        if rand < shotProb * 100:
            self.key = "!"
        else:
            self.key = "@"
        data.currKeys.add(self.key)
        data.crossSection = calculateCrossSection(data, self)
        data.cobMatrix = convertToCobMatrix(data, *data.crossSection)
        if self.outsideThreePointArc(data, data.court):
            shotValue = 3
        else:
            shotValue = 2
        data.mode = "3D"
        data.firstPass3D = True
        data.shooter = self
        data.aiShoot = (True, 0, 0, shotValue)
    
    def determineShootingStats(self, data):
        dist = distance(self.x, self.y, data.shootingBasket.x, data.shootingBasket.y)
        biased = False #Determines whether this is a high percentage shot
        plsDontShoot = False
        if self.withinPaint(data, data.court): #Short shooting
            if (self.accuracyShort >= self.accuracyMid and
                self.accuracyShort >= self.accuracyLong):
                biased = True
            shotChance = self.accuracyShort
        elif self.outsideThreePointArc(data, data.court): #Long shooting
            if (self.accuracyLong >= self.accuracyMid and
                self.accuracyLong >= self.accuracyShort):
                biased = True
            shotChance = self.accuracyLong
        else: #Mid shooting
            if (self.accuracyMid >= self.accuracyShort and
                self.accuracyMid >= self.accuracyLong):
                biased = True
            shotChance = self.accuracyShort
        #shootingSpace = (1 - self.release) * dist * 1.2
        shootingSpace = 2 * dist / 3
        canShoot = True
        mustShoot = biased
        if dist > 26 * data.court.length / 94: #Don't want to chuck shots
            plsDontShoot = True
        minDist = data.court.length
        minPlayer = ""
        for player in data.defensiveTeam: #Check how close other players are
            dx = 1
            if data.shootingBasket.name == "Left":
                dx = -1
            if (self.x != player.x and 
                int(abs(self.x - player.x) / (self.x - player.x) != dx)):
                d = distance(self.x, self.y, player.x, player.y)
                if d < minDist:
                    minDist = d
                    minPlayer = player
                if d < shootingSpace:
                    canShoot = False
                if d < 6 * data.court.length / 94:
                    mustShoot = False
        if isinstance(minPlayer, Player) and minPlayer.immobile:
            mustShoot = True
        return canShoot, mustShoot, shotChance, minPlayer, plsDontShoot
                    
    def aiOffensive2DBH(self, data): #Player is ball handler
        override = False
        canShoot, mustShoot, shotChance, guarder, plsDontShoot = self.determineShootingStats(data)
        self.crossoverCooldown += 1
        if data.ball.player == "": #Pickup loose balls
            self.trackPosition(data, (data.ball.x, data.ball.y))
            self.pickUpBall(data)
            return
        if guarder != "" and guarder.displayArm: #Check whether to cross up
            rand = random.randint(1, 1000)
            crossoverChance = self.ballHandling
            if rand < crossoverChance * 1000 and self.crossoverCooldown > 200:
                self.switchHand(data)
            self.crossoverCooldown = 0
        if guarder != "" and guarder.immobile: #Go around a crossed player
            override = True
        #Can shoot- has green light. must shoot- should shoot
        rand = random.randint(1, 100)
        if data.shotClock == 1:
            mustShoot = True
            plsDontShoot = False
        result = True
        if (((data.properCount % 2 * self.rhythm == 0  and canShoot and rand < shotChance * 100)
            or mustShoot) and not plsDontShoot and self.pickUpCount > 20): 
            #Shoot the ball
            self.aiShoot(data, shotChance)
        else: #Try to pass the ball
            result = self.aiPass(data, rand)
        if not result: #Move around
            self.aiMove(data, override, guarder)
        
    @staticmethod
    def aiOffensive(self, data, firstPass = False): #Offensive AI
        if firstPass:
            self.crossoverCooldown = 1001
            self.rhythm = random.randint(50, 150)
            self.currZone = self.findZoneI(data)
            self.executables.append([Player.aiOffensive, data])
        elif self in data.defensiveTeam:
            self.executables.remove([Player.aiOffensive, data])
        if self is data.user1 or self is data.user2:
            return
        elif not firstPass:
            self.pickUpCount += 1
            if data.mode == "2D" and not data.ball.player is self:
                self.aiOffensive2D(data)
            elif data.mode == "2D" and data.ball.player is self: #AI is primary ball handler
                self.aiOffensive2DBH(data)

##
# Guard Class
##

class Guard(Player):
    
    def __init__(self, data, dict, userColor, defaultColor):
        super().__init__(data, dict, userColor, defaultColor)
        
        self.zones = [(data.length / 1.08, data.length / 3.33), (data.length / 1.08, data.length / 1.43),
             (data.length / 1.43, data.length / 1.50), (data.length / 1.43, data.length / 3.25),
             (data.length / 1.65, data.length / 1.48), (data.length / 1.65, data.length / 3.08),
             (data.length / 1.64, data.length / 2)]

##
# Forward Class
##
    
class Forward(Player):
    
    def __init__(self, data, dict, userColor, defaultColor):
        super().__init__(data, dict, userColor, defaultColor)
        
        self.zones = [(data.length / 1.21, data.length / 3.08), (data.length / 1.21, data.length / 1.48),
             (data.length / 1.43, data.length / 1.50), (data.length / 1.43, data.length / 3.25),
             (data.length / 1.47, data.length / 2.72), (data.length / 1.47, data.length / 1.58),
             (data.length / 1.36, data.length / 2)]

##
# Center Class
##
            
class Center(Player):
    
    def __init__(self, data, dict, userColor, defaultColor):
        super().__init__(data, dict, userColor, defaultColor)
        
        self.zones = [(data.length / 1.10, data.length / 1.70), (data.length / 1.10, data.length / 2.42),
             (data.length / 1.23, data.length / 1.67), (data.length / 1.23, data.length / 2.50),
             (data.length / 1.18, data.length / 3.33), (data.length / 1.18, data.length / 1.43),
             (data.length / 1.31, data.length / 2)]

##
# Importing Custom Modules
##

from helperFunctions import *
from courtClass import *
from basketClass import *
from ballClass import *
