#Class defining the baskets used in the game

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
# Basket Class
##
    
class Basket(object):
    
    #Colors
    twoDColor = (0, 0, 0)
    lineColor = (150, 150, 150)
    backboardColor = (51, 0, 102)
    netColor = (255, 255, 255)
    
##
# Init Functions
##

    #__init__ Helper
    def init2DData(self, data, name):
        self.margin = 4 * data.length / 94
        self.radius = 2 * data.length / 94
        self.height = 3.5 * data.length / 94
        self.netHeight = 1.5 * data.length / 94
        self.width = 6 * data.length / 94
        self.lineWidth = data.length / 100
        self.poleWidth = data.length / 60
        self.cx, self.cy = data.length / 2, data.width / 2
        self.lx, self.ty = self.cx - data.court.length / 2, self.cy - data.court.width / 2
        self.rx, self.by = self.cx + data.court.length / 2, self.cy + data.court.width / 2
        #Self.x and self.y represent point at which hoop meets backboard
        if name == "Left":
            self.x = self.lx + self.margin
            self.poleX = self.x - self.poleWidth / 4
            self.basketX = self.x + self.radius
        elif name == "Right":
            self.x = self.rx - self.margin
            self.poleX = self.x + self.poleWidth / 4
            self.basketX = self.x - self.radius
        self.y = self.cy
        self.z = 10 * data.length / 94
    
    #__init__ Helper
    def init3DData(self):
        #3D data
        self.poleX3D = 0
        self.poleY3D = 0
        self.poleHeight3D = 0
        self.newLX3D = 0
        self.newRX3D = 0
        self.newLY3D = 0
        self.newRY3D = 0
        self.netLX3D = 0
        self.netLY3D = 0
        self.netRX3D = 0
        self.netRY3D = 0
        self.z3D = 0
        self.height3D = 0
        self.netHeight3D = 0

    def __init__(self, data, name):
        self.name = name
        self.init2DData(data, name)
        self.init3DData()

##
# Draw Functions
##

    def draw2D(self, screen, data):
        pygame.draw.line(*intify(screen, self.twoDColor, (self.x, self.cy - self.width / 2), 
                        (self.x, self.cy + self.width / 2), self.lineWidth))
        pygame.draw.circle(*intify(screen, self.twoDColor, (self.basketX, self.cy),
                        self.radius, self.lineWidth))
    
    def draw3DCrossSection(self, screen, data):
        
        #Pole
        margin = (data.width - data.court.width) / 2
        pygame.draw.line(*intify(screen, self.lineColor, (self.poleX3D, data.width - margin), 
                        (self.poleX3D, self.poleHeight3D), self.poleWidth))
        netMargin = self.height3D / 6
        
        #Backboard
        pygame.draw.rect(*intify(screen, self.lineColor, (self.newLX3D, self.z3D - self.height3D,
                        self.newRX3D - self.newLX3D, self.height3D)))
        pygame.draw.rect(*intify(screen, self.backboardColor, (self.newLX3D + self.lineWidth / 2,
                        self.z3D - self.height3D + self.lineWidth / 2, self.newRX3D - self.newLX3D - self.lineWidth, 
                        self.height3D - self.lineWidth)))
                        
        #Net
        pygame.draw.rect(*intify(screen, self.lineColor, (self.netLX3D, self.z3D - netMargin,
                        self.netRX3D - self.netLX3D, self.netHeight3D)))
        pygame.draw.rect(*intify(screen, self.netColor, (self.netLX3D + self.lineWidth / 2,
                        self.z3D - netMargin + self.lineWidth / 2, self.netRX3D - self.netLX3D - 
                        self.lineWidth, self.netHeight3D - self.lineWidth)))
    
    def drawNet(self, screen, data): #Only draws the net
        netMargin = self.height3D / 6
        pygame.draw.rect(*intify(screen, self.lineColor, (self.netLX3D, self.z3D - netMargin,
                        self.netRX3D - self.netLX3D, self.netHeight3D)))
        pygame.draw.rect(*intify(screen, self.netColor, (self.netLX3D + self.lineWidth / 2,
                        self.z3D - netMargin + self.lineWidth / 2, self.netRX3D - self.netLX3D - 
                        self.lineWidth, self.netHeight3D - self.lineWidth)))

##
# Updating Data
##
    
    def updateCoords(self, data, start, end, cobMatrix):
        
        #Pole
        self.poleX3D, self.poleY3D = changeBasis(data, self.poleX, self.y, start, cobMatrix)
        self.poleHeight3D = adjustZ(self.z + self.height / 6, data)
        
        #Backboards
        self.newLX3D, self.newLY3D = changeBasis(data, self.x, self.cy + self.width, start, cobMatrix)
        self.newRX3D, self.newRY3D = changeBasis(data, self.x, self.cy - self.width, start, cobMatrix)
        if self.newLX3D > self.newRX3D: self.newLX3D, self.newRX3D = self.newRX3D, self.newLX3D
        
        #Net- left and right coords represented by intersection of line through center
        theta = angle(*start, *end)
        lx, ly = self.basketX + self.radius * math.cos(theta), self.y - self.radius * math.sin(theta)
        rx, ry = self.basketX - self.radius * math.cos(theta), self.y + self.radius * math.sin(theta)
        self.netLX3D, self.netLY3D = changeBasis(data, lx, ly, start, cobMatrix)
        self.netRX3D, self.netRY3D = changeBasis(data, rx, ry, start, cobMatrix)
        if self.netLX3D > self.netRX3D: self.netLX3D, self.netRX3D = self.netRX3D, self.netLX3D
        self.z3D = adjustZ(self.z, data)
        self.height3D = scaleVertical(self.height, data)
        self.netHeight3D = scaleVertical(self.netHeight, data)

##
# Importing Custom Modules
##

from helperFunctions import *
from courtClass import *
from playerClass import *
from ballClass import *
