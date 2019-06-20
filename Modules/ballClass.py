#Class defining the ball used in the game

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
import math
import numpy
import random
import decimal
import json
import string

##
# Ball Class
##

class Ball(object):
    
    #Colors
    color = (75, 0, 130)
    lineColor = (255, 255, 255)

##
# Init Functions
##
    
    def __init__(self, data, x, y):
        #Coords and misc.
        self.x = x
        self.y = y
        self.z = 0
        self.executables = []
        self.width = data.length / 200
        self.radius = data.ballRadius
        self.radiusConst = data.ballRadius
        self.player = ""
        
        #Passing flags
        self.passResult = False
        
        #Shooting vars and flags
        self.shootingMotion = False
        self.basketSwitch = False
        self.reverseLayup = False
        self.v = 0
        self.count = 0
        self.X3Di = 0
        self.Z3Di = 0
        self.rad3D = 0
        self.theta = 0

##
# Draw Functions
##

    def draw2D(self, screen, data):
        pygame.draw.circle(*intify(screen, self.lineColor, (self.x, self.y), self.radius + self.width))
        pygame.draw.circle(*intify(screen, self.color, (self.x, self.y), self.radius))
    
    def draw3D(self, screen, data):
        pygame.draw.circle(*intify(screen, self.lineColor, (self.X3D, self.Z3D), self.rad3D + self.width))
        pygame.draw.circle(*intify(screen, self.color, (self.X3D, self.Z3D), self.rad3D))

##
# Boolean Checks
##

    def checkIfBlocked(self, player, data, randCheck = True): 
        #Checks if shot was blocked
        lx3D, rx3D = player.armLX3D, player.armRX3D
        tz3D, bz3D = player.armLZ3D, player.armRZ3D
        if lx3D > rx3D: lx3D, rx3D = rx3D, lx3D
        if bz3D > tz3D: bz3D, tz3D = tz3D, bz3D
        topLeftCoords = (player.x3D - player.bodyWidth3D / 2, player.bodyZ3D - player.bodyHeight3D / 2)
        if (self.X3D + self.rad3D >= lx3D and self.X3D - self.rad3D <= rx3D
            and self.Z3D + self.rad3D >= bz3D and self.Z3D - self.rad3D <= tz3D
            and abs(player.y3D - distance(0, 0, data.length, data.width) / 2) <= 2 * self.rad3D):
            rand = random.randint(1, 100)
            if (rand < player.block * 100 and player.canBlock) or not randCheck:
                return True
            player.canBlock = False
            return False
        elif (rectCollision(self.X3D, self.Z3D, (*topLeftCoords, player.bodyWidth3D, player.bodyHeight3D))
             and abs(player.y3D - distance(0, 0, data.length, data.width) / 2) <= 2 * self.rad3D):
            rand = random.randint(1, 100)
            if (rand < player.block * 100 and player.canBlock) or not randCheck:
                return True
            player.canBlock = False
            return False
        return False
    
    def inBounds(self, data, court): #Checks if ball is in bounds
        cx, cy = data.length / 2, data.width / 2
        if self.x < cx - court.length / 2 or self.x > cx + court.length / 2:
            return False
        elif self.y < cy - court.width / 2 or self.y > cy + court.width / 2:
            return False
        return True

##
# Updating Data
##
    
    def updateCoords(self, data):
        if isinstance(self.player, Player):
            self.x = self.player.armX
            self.y = self.player.armY
            self.z = reverseAdjustZ(self.player.armLZ3D, data)
            self.X3D = self.player.armLX3D
            self.Z3D = self.player.armLZ3D
        self.rad3D = scaleVertical(self.radiusConst, data) * data.radScale3D
    
##
# Animations
##

    #Generic animation helper
    def trackPosition(self, data, power, coords): #Moves ball to specifed pos
        dstep = data.d * power * 2
        theta = angle(*coords, self.x, self.y)
        dx = dstep * math.cos(theta)
        dy = dstep * math.sin(theta)
        self.x += dx
        self.y -= dy
        if distance(self.x, self.y, *coords) <= 0.5 * dstep:
            self.x = coords[0]
            self.y = coords[1]
            return True
        return False
    
    @staticmethod
    def movePassedBall(self, data, power, coords, firstPass = False):
        #Moves the ball to designating passing location
        if firstPass:
            self.player = ""
            self.executables.append([Ball.movePassedBall, data, power, coords])
        else:
            if not self.passResult:
                result = self.trackPosition(data, power, coords)
                if result:
                    self.passResult = True
            if self.player != "":
                data.passer = ""
                self.passResult = False
                self.executables.remove([Ball.movePassedBall, data, power, coords])
    
    @staticmethod
    def ricochet(self, data, player, theta, dist, firstPass = False): 
        #Rebound the ball off of a missed shot
        if firstPass:
            self.executables.append([Ball.ricochet, data, player, theta, dist])
            for player2 in data.players:
                if not player2 is data.user1 and not player2 is data.user2:
                    player2.aiReboundBall(player2, player, data, theta, dist, True)
                
        else:
            d = data.length / 400
            xDir = -1 * d * data.shootingDir
            yDir = d * data.shootingDir
            if not data.pause or not data.pauseNoDraw:
                self.x += xDir * math.cos(theta)
                self.y -= yDir * math.sin(theta)
                self.z = data.shootingBasket.z - self.count
                inc = 0.2 * (data.length / dist) + (1 - player.strength) * d
                self.count += inc
                if self.z < 0:
                    self.z = 0
                    self.count = 0
                    self.executables.remove([Ball.ricochet, data, player, theta, dist])
    
    #moveInArc Helper:
    def resetShotMotion(self, data, player, endPos, shotMade, dist, blocked = False):
        self.count = 0
        self.v = 0
        data.mode = "2D"
        data.firstPass2D = True
        self.shootingMotion = False
        self.basketSwitch = False
        scaleDistance = distance(*data.crossSection[0], *data.crossSection[1]) / data.length
        theta = angle(*data.crossSection[0], *data.crossSection[1])
        if data.shootingBasket.name == "Right":
            self.x = data.shootingBasket.x - self.radius
        elif data.shootingBasket.name == "Left":
            self.x = data.shootingBasket.x + self.radius
        self.y = data.shootingBasket.cy
        theta = angle(*data.crossSection[0], *data.crossSection[1])
        if self.reverseLayup: #Reverse Layup
            theta *= -1
        if shotMade:
            findMadeShotText(data, player)
            switchPosession(data)
        else:
            self.ricochet(self, data, player, theta, dist, True)
        player.checkIfAssisted(shotMade)
        player.updateStats()
        self.executables.remove([Ball.moveInArc, data, player, endPos, shotMade, dist])
    
    #moveInArc Helper:
    def resetBlockedShot(self, data, player, endPos, shotMade, dist, blocker):
        if shotMade:
            if player in data.user1Team:
                data.user1Score -= player.prevValue
            elif player in data.user2Team:
                data.user2Score -= player.prevValue
            player.points -= player.prevValue
            player.fgm -= 1
            if player.prevValue == 3:
                player.fgm3 -= 1
        self.count = 0
        self.v = 0
        data.mode = "2D"
        data.blocked = True
        data.firstPass2D = True
        self.shootingMotion = False
        self.basketSwitch = False
        scaleDistance = distance(*data.crossSection[0], *data.crossSection[1]) / data.length
        theta = angle(*data.crossSection[0], *data.crossSection[1])
        theta = rotateAcrossAxis(theta, math.pi / 2)
        self.x = blocker.x + data.shootingDir * (self.radius + blocker.radius) * 1.1 * math.cos(theta)
        self.y = blocker.y + data.shootingDir * (self.radius + blocker.radius) * 1.1 * math.sin(theta)
        self.ricochet(self, data, player, theta + math.pi, dist, True)
        displayPauseText(data, "Blocked By %s %s!" % (blocker.firstName, blocker.lastName))
        blocker.blocks += 1
        blocker.updateStats()
        player.updateStats()
        self.executables.remove([Ball.moveInArc, data, player, endPos, shotMade, dist])
        
    #moveInArcHelper:
    def updateBallCoords(self, player, endPos):
        x = abs(self.X3Di - endPos[0])
        sign = numpy.sign(endPos[0] - self.X3Di)
        tFin = x / (self.v * math.cos(self.theta))
        self.count += 0.04 + player.strength * 0.04
        self.X3D = self.X3Di + sign * self.v * math.cos(self.theta) * self.count
        self.Z3D = self.Z3Di - (self.v * math.sin(self.theta) * self.count - 4.9 * self.count ** 2)
        return tFin
    
    #calculateKinematics Helper
    def calculateEndAngle(self, data):
        x = (data.shootingBasket.netLX3D + data.shootingBasket.netRX3D) / 2
        dir = self.X3D - x
        self.reverseLayup = dir * data.shootingDir < 0
        netMargin = data.shootingBasket.height / 6
        if data.shootingDir < 0:
            endAngle = angle(self.X3D, self.Z3D, x, data.shootingBasket.z3D - netMargin * 2) - math.pi
        else:
            endAngle = -1 * angle(self.X3D, self.Z3D, x, data.shootingBasket.z3D - netMargin * 2)
        if self.reverseLayup: #Reverse layup
            endAngle = rotateAcrossAxis(endAngle, math.pi / 2)
            if endAngle > math.pi * 2:
                endAngle -= math.pi * 2
        return math.pi / 2 - ((math.pi / 2 - endAngle) / 2)
    
    #moveInArc Helper
    def calculateKinematics(self, data, player, endPos):
        #Finds initial velocity and angle of shot ball
        self.X3Di, self.Z3Di = self.X3D, self.Z3D
        x = abs(self.X3Di - endPos[0])
        if data.user1Shoot[0]: #Jump Shot
            self.theta = player.armPhi
        else: #Layup
            self.theta = self.calculateEndAngle(data)
        z = self.Z3Di - endPos[1]
        self.v = (4.9 / (x * math.tan(self.theta) - z)) ** 0.5 * x / math.cos(self.theta)
        count = 0
        while math.isnan(self.v) and count < 100:
            count += 1
            self.theta -= math.pi / 18
            self.v = (4.9 / (x * math.tan(self.theta) - z)) ** 0.5 * x / math.cos(self.theta)
        if count >= 100:
            self.v = 3
    
    #moveInArc Helper
    def madeShot(self, data, player, endPos, shotMade, dist): #Animates a made shot
        if data.sound and player.firstPassSound: 
            playSound(player.commentary)
        zFin = data.shootingBasket.z3D + 0.4 * self.rad3D
        self.Z3D += 1
        player.firstPassSound = False
        if self.Z3D > zFin:
            player.firstPassSound = True
            self.Z3D = zFin
            self.resetShotMotion(data, player, endPos, shotMade, dist)
            data.pauseNoDraw = True
            data.pauseCount = data.switchPosessionTime
    
    #moveInArc Helper
    def moveBallInAir(self, data, player, endPos, shotMade, dist):
        #Move ball through the air parabolically
        tFin = self.updateBallCoords(player, endPos)
        blocked = False
        for p in data.players:
            if not p is player: 
                if self.checkIfBlocked(p, data):
                    self.resetBlockedShot(data, player, endPos, shotMade, dist, p)
                    return
        if self.count > tFin:
            self.X3D, self.Z3D = endPos[0], endPos[1]
            if not shotMade:
                self.resetShotMotion(data, player, endPos, shotMade, dist)
            else:
                self.basketSwitch = True
    
    @staticmethod
    def moveInArc(self, data, player, endPos, shotMade, dist, firstPass = False): 
        #Making the ball follow the path of the shot
        if firstPass:
            self.executables.append([Ball.moveInArc, data, player, endPos, shotMade, dist])
            self.shootingMotion = True
        else:
            if player.shotReachedPeak() and self.v == 0:
                self.player = ""
                self.calculateKinematics(data, player, endPos)
            elif player.shotReachedPeak():
                if self.basketSwitch: #If shot is made and ball is right above basket
                    self.madeShot(data, player, endPos, shotMade, dist)
                else:
                    self.moveBallInAir(data, player, endPos, shotMade, dist)
    
    #dunkBall Helper
    def resetDunkedBall(self, data, player, shotMade):
        self.count = 0
        self.v = 0
        data.mode = "2D"
        data.firstPass2D = True
        self.shootingMotion = False
        self.basketSwitch = False
        scaleDistance = distance(*data.crossSection[0], *data.crossSection[1]) / data.length
        theta = angle(*data.crossSection[0], *data.crossSection[1])
        if data.shootingBasket.name == "Right":
            self.x = data.shootingBasket.x - self.radius
        elif data.shootingBasket.name == "Left":
            self.x = data.shootingBasket.x + self.radius
        self.y = data.shootingBasket.cy
        theta = angle(*data.crossSection[0], *data.crossSection[1])
        if self.reverseLayup: #Reverse Layup
            theta *= -1
        if shotMade:
            findMadeShotText(data, player, "Dunk")
            switchPosession(data)
        else:
            self.ricochet(self, data, player, theta, dist, True)
        player.checkIfAssisted(shotMade)
        player.updateStats()
        self.executables.remove([Ball.dunkBall, data, player, shotMade])
        
    @staticmethod
    def dunkBall(self, data, player, shotMade, firstPass = False): 
        #Dunking the ball
        if firstPass:
            if data.sound: playSound(player.commentary)
            self.player = ""
            self.executables.append([Ball.dunkBall, data, player, shotMade])
            self.shootingMotion = True
        else:
            self.basketSwitch = True
            zFin = data.shootingBasket.z3D + 0.4 * self.rad3D
            self.Z3D += 1
            if self.Z3D > zFin:
                self.Z3D = zFin
                self.resetDunkedBall(data, player, shotMade)
                data.pauseNoDraw = True
                data.pauseTime = data.switchPosessionTime
    
    def checkBlockedDunk(self, data, shooter, blocker, override = False):
        strO = shooter.strength
        strD = blocker.strength
        strDif = ((strD - strO) + 0.5)
        rand = random.randint(1, 100)
        if rand < strDif * 100 or override:
            self.count = 0
            self.v = 0
            data.mode = "2D"
            data.blocked = True
            data.firstPass2D = True
            self.shootingMotion = False
            self.basketSwitch = False
            scaleDistance = distance(*data.crossSection[0], *data.crossSection[1]) / data.length
            theta = angle(*data.crossSection[0], *data.crossSection[1])
            theta = rotateAcrossAxis(theta, math.pi / 2)
            if not override: #Missed not blocked dunk
                shooter.fga += 1
                shooter.updateStats()
                self.x = blocker.x + data.shootingDir * (self.radius + blocker.radius) * 1.1 * math.cos(theta)
                self.y = blocker.y + data.shootingDir * (self.radius + blocker.radius) * 1.1 * math.sin(theta)
                data.ball.player = ""
                displayPauseText(data, "Blocked By %s %s!" % (blocker.firstName, blocker.lastName))
                blocker.blocks += 1
                blocker.updateStats()
            else:
                data.ball.player = ""
            dist = data.court.length / 3
            self.ricochet(self, data, shooter, theta + math.pi, dist, True)
            return True
        else:
            return False

##
# Importing Custom Modules
##

from helperFunctions import *
from courtClass import *
from basketClass import *
from playerClass import *