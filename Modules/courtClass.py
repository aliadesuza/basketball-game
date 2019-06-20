#Class defining the court used in the game

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
# Court Class
##

class Court(object):
    
    #Colors
    lineColor = (255, 255, 255)
    
##
# Init Functions
##
    
    def __init__(self, length, color, paintColor):
        self.color = color
        self.paintColor = paintColor
        self.length = length
        self.width = 50 * length / 94
        self.lineWidth = length / 100
        self.centerRad = 6 * length / 94
        self.restrictedRad = 4 * length / 94
        self.threePointRad = 23.75 * length / 94
        self.threePointDist = 14 * length / 94
        self.keyWidth = 16 * length / 94
        self.basketDist = 4 * length / 94
        self.freeThrowDist = 19 * length / 94
        self.margin = 4 * length / 94

##
# Draw Functions
##
    
    def drawCourt(self, screen, data):
        cx, cy = data.length / 2, data.width / 2
        lx, ty = cx - self.length / 2, cy - self.width / 2
        rx, by = cx + self.length / 2, cy + self.width / 2
        
        #Court
        courtRect = intify(lx, ty, self.length, self.width)
        screen.blit(data.courtImg, courtRect)

        #Center Line and Circle
        pygame.draw.circle(*intify(screen, self.lineColor, (cx, cy), self.centerRad))
        pygame.draw.circle(*intify(screen, self.color, (cx, cy), self.centerRad - self.lineWidth))
        pygame.draw.line(*intify(screen, self.lineColor, (cx, ty), (cx, by), self.lineWidth))
        
        #Three Point Arcs
        rect = (lx + self.basketDist - self.threePointRad, cy - self.threePointRad, 2 * self.threePointRad,
                2 * self.threePointRad)
        pygame.draw.arc(screen, self.lineColor, rect, -1.15, 1.15, int(self.lineWidth))
        pygame.draw.line(*intify(screen, self.lineColor, (lx, ty + self.margin), 
                        (lx + self.threePointDist, ty + self.margin), self.lineWidth))
        pygame.draw.line(*intify(screen, self.lineColor, (lx, by - self.margin), 
                        (lx + self.threePointDist, by - self.margin), self.lineWidth))
        rect = (rx - self.basketDist - self.threePointRad, cy - self.threePointRad, 2 * self.threePointRad,
                2 * self.threePointRad)
        pygame.draw.arc(screen, self.lineColor, rect, math.pi - 1.12, math.pi + 1.15, int(self.lineWidth))
        pygame.draw.line(*intify(screen, self.lineColor, (rx - self.threePointDist, ty + self.margin), 
                        (rx, ty + self.margin), self.lineWidth))
        pygame.draw.line(*intify(screen, self.lineColor, (rx - self.threePointDist, by - self.margin), 
                        (rx, by - self.margin), self.lineWidth))
                        
        #Paint
        pygame.draw.circle(*intify(screen, self.lineColor, (rx - self.freeThrowDist, cy), self.keyWidth / 2))
        pygame.draw.circle(*intify(screen, self.color, (rx - self.freeThrowDist, cy), self.keyWidth / 2 - self.lineWidth))
        pygame.draw.rect(*intify(screen, self.paintColor, (rx - self.freeThrowDist, cy - 
                        self.keyWidth / 2, self.freeThrowDist, self.keyWidth)))
        pygame.draw.rect(*intify(screen, self.lineColor, (rx - self.freeThrowDist, cy - 
                        self.keyWidth / 2, self.freeThrowDist, self.keyWidth), self.lineWidth))
        pygame.draw.circle(*intify(screen, self.lineColor, (lx + self.freeThrowDist, cy), self.keyWidth / 2))
        pygame.draw.circle(*intify(screen, self.color, (lx + self.freeThrowDist, cy), self.keyWidth / 2 - self.lineWidth))
        pygame.draw.rect(*intify(screen, self.paintColor, (lx, cy - self.keyWidth / 2, 
                        self.freeThrowDist, self.keyWidth)))
        pygame.draw.rect(*intify(screen, self.lineColor, (lx, cy - self.keyWidth / 2, 
                        self.freeThrowDist, self.keyWidth), self.lineWidth))

##
# Importing Custom Modules
##

from helperFunctions import *
from basketClass import *
from playerClass import *
from ballClass import *