#Class defining the buttons on screen that you press

##
# OS Stuff / Initialization
##

import os
import sys
import inspect

filename = inspect.getframeinfo(inspect.currentframe()).filename
filePath = os.path.dirname(os.path.dirname(os.path.abspath(filename))) + "\\"

##
# Importing Modules
##

#Python modules
import pygame
import math
import numpy
import random
import decimal
import json
import string

#Custom modules
from helperFunctions import *

##
# Button Class
##

class button(object):
    
##
# Init Functions
##
    
    def __init__(self, data, x, y, width, height, fill, border, textColor, text, fontScale = 1, 
                fontScale2 = 1, color2 = None):
                    
        #Button draw data
        self.rect = (x, y, width, height)
        lineWidth = data.length / 100
        self.rect2 = (x + lineWidth, y + lineWidth, width - 2 * lineWidth, height - 2 * lineWidth)
        self.fill = fill
        self.borderColor = border
        self.text = text
        self.textColor = textColor
        if color2 == None:
            self.textColor2 = textColor
        else:
            self.textColor2 = color2
        self.font = pygame.font.SysFont("verdana", int(height / 2 * fontScale), bold = True)
        self.font2 = pygame.font.SysFont("verdana", int(height / 2 * fontScale2), bold = True)
        
        #Draw placeholder data
        self.tempFill = (0, 0, 0)
        self.tempBorder = (0, 0, 0)
        self.tempText = (0, 0, 0)
        self.tempText2 = (0, 0, 0)
        self.colorChanged = False
    
##
# Draw Functions
##

    def draw(self, screen, data, text = None):
        pygame.draw.rect(*intify(screen, self.borderColor, self.rect))
        pygame.draw.rect(*intify(screen, self.fill, self.rect2))
        cx = self.rect[2] / 2 + self.rect[0]
        cy = self.rect[3] / 2 + self.rect[1]
        if text == None:
            if isinstance(self.text, list): #Multiple text lines
                cy = self.rect[3] / (1.5 * len(self.text)) + self.rect[1]
                for i in range(len(self.text)):
                    if i == 0:
                        drawText(*intify(screen, self.font, cx, cy, self.text[i], self.textColor))
                    else:
                        drawText(*intify(screen, self.font2, cx, cy, self.text[i], self.textColor2))
                    cy += self.rect[3] / (1.5 * len(self.text))
            else:
                drawText(*intify(screen, self.font, cx, cy, self.text, self.textColor))
        else:
            drawText(*intify(screen, self.font, cx, cy, text, self.textColor))
        if self.colorChanged: #Change button color to something elsw
            self.fill = self.tempFill
            self.borderColor = self.tempBorder
            self.textColor = self.tempText
            self.textColor2 = self.tempText2
            self.colorChanged = False

##
# Boolean Checks
##

    def checkIfPressed(self, pos):
        if (pos[0] >= self.rect[0] and pos[0] <= self.rect[0] + self.rect[2] and
            pos[1] >= self.rect[1] and pos[1] <= self.rect[1] + self.rect[3]):
            return True
        return False

##
# Updating Data
##

    def changeColors(self, newFill, newBorder, newText, newText2): #Change color of button
        self.tempFill, self.tempBorder = self.fill, self.borderColor
        self.tempText, self.tempText2 = self.textColor, self.textColor2
        self.fill, self.borderColor = newFill, newBorder
        self.textColor, self.textColor2 = newText, newText2
        self.colorChanged = True
    
    def changeBorderSize(self, lineWidth):
        lineWidth = int(lineWidth)
        if lineWidth <= 0:
            lineWidth = 1
        self.rect2 = (self.rect[0] + lineWidth, self.rect[1] + lineWidth, 
                    self.rect[2] - 2 * lineWidth, self.rect[3] - 2 * lineWidth)
    
    def updateUIText(self, data): #If UI mode is changed
        self.text = "UI: " + data.ui
    
    def updateSoundText(self, data): #If sound is toggled
        text = "On"
        if data.sound:
            text = "Off"
        self.text = "Sounds: " + text
    
    def updateMusicText(self, data): #If music is toggled
        text = "On"
        if not data.musicPlay:
            text = "Off"
        self.text = "Music: " + text
        
