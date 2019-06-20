#Main program- tackles all the user input, drawing, data init etc.

##
# OS Stuff
##

import os
import sys
import inspect

filename = inspect.getframeinfo(inspect.currentframe()).filename
filePath = os.path.dirname(os.path.abspath(filename)) + "\\"
sys.path.append(os.path.abspath(filePath + "/Modules"))

##
# Importing Modules
##

#Python modules
import pygame
MUSIC_END = pygame.USEREVENT + 1
import math
import numpy
import random
import decimal
import json
import string
import traceback
import copy

#Custom modules
from helperFunctions import *
from buttonClass import *
from courtClass import *
from basketClass import *
from playerClass import *
from ballClass import *

##
# Model Functions
##

#initMainMenu Helper
def initMainMenuBasicData(data): #Modes and other misc. basic stuff
    data.mode = "Main Menu"
    data.subMode = "None"
    data.screenColor = (0, 0, 0)
    data.court = Court(data.length, (0, 0, 0), (204, 51, 255))

#initMainMenu Helper
def initMainMenuPictures(data): #Background pictures
    data.mainMenu = pygame.image.load(filePath + "Images/homeScreen.jpg")
    data.mainMenu = pygame.transform.scale(*intify(data.mainMenu, 
                    (data.length, data.width)))
    data.mainMenu2 = pygame.image.load(filePath + "Images/teamsScreen.png")
    data.mainMenu2 = pygame.transform.scale(*intify(data.mainMenu2, 
                    (data.length, data.width)))
    data.mainMenuText = pygame.image.load(filePath + "Images/homeScreenText.png")
    data.mainMenuText = pygame.transform.scale(*intify(data.mainMenuText, 
                        (data.length / 6 * 4.08, data.width / 6)))
    data.mainMenuText = pygame.transform.rotate(data.mainMenuText, 335)
    rect = data.mainMenuText.get_rect()
    data.mainMenuTextRect = (rect[0] + data.length / 3, rect[1] - data.width / 20, rect[2], rect[3])
    data.teamsText = pygame.image.load(filePath + "Images/teamsText.png")
    data.teamsText = pygame.transform.scale(*intify(data.teamsText, 
                        (data.length / 6 * 3.5, data.width / 6)))
    data.teamsRect = (data.length / 5, data.width / 12.5, data.length / 7 * 3.5, data.width / 7)
    data.careerText = pygame.image.load(filePath + "Images/careerText.png")
    data.careerText = pygame.transform.scale(*intify(data.careerText, 
                        (data.length / 5 * 4, data.width / 6)))
    data.careerRect = (data.length / 10, data.width / 12.5, data.length, data.width / 7)

#initMainMenu Helper
def initMainMenuTeams(data): #Loads the team dicts
    data.dragons = retreiveDict(filePath + "TeamFiles/Team1.txt")
    data.supernova = retreiveDict(filePath + "TeamFiles/Team2.txt")
    data.tide = retreiveDict(filePath + "TeamFiles/Team3.txt")
    data.copperheads = retreiveDict(filePath + "TeamFiles/Team4.txt")
    data.teamDicts = [data.dragons, data.supernova, data.tide, data.copperheads]

#initMainMenu Helper
def initMainMenuButtons(data): #Buttons that you press
    # Home Screen
    data.playButton =  button(data, 4 * data.length / 7, data.width / 2, 5 * data.length / 14, data.width / 8,
                        data.screenColor, data.court.lineColor, data.court.paintColor, "Play")
    data.careerButton =  button(data, 4 * data.length / 7, 2 * data.width / 3, 5 * data.length / 14, data.width / 8,
                        data.screenColor, data.court.lineColor, data.court.paintColor, "Career")
    data.controlsButton =  button(data, 5 * data.length / 7, 9 * data.width / 10, data.length / 4, data.width / 15,
                        data.screenColor, data.court.lineColor, data.court.paintColor, "Controls")
    #Career Screen
    data.careerPlayButton = button(data, 5 * data.length / 7, 3 * data.width / 10, data.length / 4, 4 * data.width / 15,
                        data.screenColor, data.court.lineColor, data.court.paintColor, "")
    data.helpButton = button(data, 5 * data.length / 7, 7 * data.width / 10, data.length / 4, data.width / 15,
                        data.screenColor, data.court.lineColor, data.court.paintColor, "Help")
    data.resetButton = button(data, 5 * data.length / 7, 8 * data.width / 10, data.length / 4, data.width / 15,
                        data.screenColor, data.court.lineColor, data.court.paintColor, "Reset")
    data.saveExitButton =  button(data, 5 * data.length / 7, 9 * data.width / 10, data.length / 4, data.width / 15,
                        data.screenColor, data.court.lineColor, data.court.paintColor, "Exit")
    data.upgradeButtons = {}
    statsT = data.width / 3.4
    statsL = data.length / 16
    statsR = statsL + 4 * data.length / 7
    margin = (data.width - data.court.width) / 2 - data.court.lineWidth
    barWidth = margin / 20
    data.nameButton = button(data, (statsL + statsR) / 2, statsT + 3.5 * barWidth,
                     (statsL + statsR) / 2, 3 * barWidth, data.screenColor, 
                     data.court.lineColor, data.court.paintColor, "")
    data.statsButton = button(data, (statsL + statsR) / 2 - margin / 10 - data.length / 4.5, 
                            11 * data.width / 12, data.length / 4.5, 
                            data.width / 21, data.screenColor,
                            data.court.lineColor, data.court.lineColor, "Stats")
    data.statsButton.changeBorderSize(data.width / 200)
    data.achievementsButton = button(data, (statsL + statsR) / 2 + margin / 10, 
                            11 * data.width / 12, data.length / 4.5, 
                            data.width / 21, data.screenColor,
                            data.court.lineColor, data.court.lineColor, "Achievements")
    data.achievementsButton.changeBorderSize(data.width / 200)
    #Play Screens
    data.backButton = button(data, 6 * data.length / 7, 9 * data.width / 10, data.length / 8, data.width / 15,
                        data.screenColor, data.court.lineColor, data.court.paintColor, "Back")
    data.teamButtons = []
    teamList = [["Dakota Dragons", "Style: Aggressive"], ["Hawaii Supernova", "Style: Defensive"],
                ["Jersey Tide", "Style: Ball Movement"], ["Vegas Copperheads", "Style: Floor Spacing"]]
    width, height = 13 * data.length / 32, data.width / 6
    cx1, cx2, cy = data.length / 16, 17 * data.length / 32, 31 * data.width / 64
    teamColors = [tuple(data.dragons["dColor"]), tuple(data.supernova["dColor"]),
                  tuple(data.tide["dColor"]), tuple(data.copperheads["dColor"])]
    for i in range(2):
        data.teamButtons.append(button(data, cx1, cy, width, height, data.screenColor, 
                        data.court.lineColor, teamColors[2 * i], teamList[2 * i], 0.4, 0.3,  data.court.lineColor))
        data.teamButtons.append(button(data, cx2, cy, width, height, data.screenColor, 
                        data.court.lineColor, teamColors[2 * i + 1], teamList[2 * i  + 1], 0.4, 0.3, data.court.lineColor))
        cy += height + data.width / 32

#initMainMenu Helper
def initMainMenuPlaceholders(data): #Attributes that will be modified later
    data.user1TeamDict = {}
    data.user2TeamDict = {}
    data.maxScore = 0
    data.careerGame = False
    
def initMainMenu(data):
    playMusic(data)
    #playTitleMusic(data)
    initMainMenuBasicData(data)
    initMainMenuPictures(data)
    initMainMenuTeams(data)
    initMainMenuButtons(data)
    initMainMenuPlaceholders(data)

#initCareers Helper
def initCareerFlags(data): #Initializes flags and colors for career screen
    data.reset = False
    data.help = False
    data.changeName = False
    data.saved = True
    data.confirm = False
    data.achieveFlag = False
    data.lightPurple = (255, 140, 255) #Used in prompt text
    data.achieveColor = incrementColor(data.myDict["dColor"], 150)
    if data.myDict["name"] == "VEG":
        data.achieveColor = incrementColor(data.myDict["dColor"], 75)

#initCareersHelper
def initMyCareer(data): #Reads the career file
    string = readFile(filePath + "TeamFiles/MyCareer.txt")
    if string == "":
        createNewCareer(filePath + "TeamFiles/", data)
    else:
        data.myCareer = retreiveDict(filePath + "TeamFiles/MyCareer.txt")
    data.myName = data.myCareer["firstName"] + " " + data.myCareer["lastName"]
    data.myAchievements = data.myCareer["achievements"]
    adjustFontSize(data)

#initCareersHelper
def initCareerTeams(data): #Initializes my team and opposing team
    #Modify Opponents
    myOvr = dictAverage(data.myCareer)
    if data.myCareer["difficulty"] == "Normal":
        overallAdj = myOvr - 0.7
    elif data.myCareer["difficulty"] == "Hard":
        overallAdj = (myOvr - 0.5) * 2 + 0.58 - 0.7
    data.dragonsOpp = overallIncrease(data.dragons, overallAdj)
    data.copperheadsOpp = overallIncrease(data.copperheads, overallAdj)
    data.tideOpp = overallIncrease(data.tide, overallAdj)
    data.supernovaOpp = overallIncrease(data.supernova, overallAdj)
    #Parse Team
    team = data.myCareer["team"]
    oppTeam = data.myCareer["oppList"][0][data.myCareer["oppList"][1]]
    while team == oppTeam:
        data.myCareer["oppList"][1] = (data.myCareer["oppList"][1] + 1) % 4
        oppTeam = data.myCareer["oppList"][0][data.myCareer["oppList"][1]]
    if team == 1:
        data.myTeam = "Dakota Dragons"
        myImage = "dragons.png"
        data.myDict = data.dragonsOpp
    elif team == 2:
        data.myTeam = "Hawaii Supernova"
        myImage = "supernova.png"
        data.myDict = data.supernovaOpp
    elif team == 3:
        data.myTeam = "Jersey Tide"
        myImage = "tide.png"
        data.myDict = data.tideOpp
    elif team == 4:
        data.myTeam = "Vegas Copperheads"
        myImage = "copperheads.png"
        data.myDict = data.copperheads
    #Parse Opponents
    if oppTeam == 1:
        data.opponents = data.dragonsOpp
        oppImage = "dragons.png"
    elif oppTeam == 2:
        data.opponents = data.supernovaOpp
        oppImage = "supernova.png"
    elif oppTeam == 3:
        data.opponents = data.tideOpp
        oppImage = "tide.png"
    elif oppTeam == 4:
        data.opponents = data.copperheadsOpp
        oppImage = "copperheads.png"
    #Team Images
    statsT = data.width / 3.4
    margin = data.width / 20
    statsL = data.length / 16
    statsR = statsL + 4 * data.length / 7
    average = (statsL + statsR) / 2
    data.myImage = pygame.image.load(filePath + "Images/" + myImage)
    data.myImage = pygame.transform.scale(*intify(data.myImage, 
                        (average * 0.6, average * 0.5)))
    data.myImageRect = (statsL + margin, statsT + margin, average * 0.75, average * 0.75)
    5 * data.length / 7, 3 * data.width / 10, data.length / 4, 4 * data.width / 15
    data.oppImage = pygame.image.load(filePath + "Images/" + oppImage)
    data.oppImage = pygame.transform.scale(*intify(data.oppImage, 
                        (3 * data.width / 15, 2.5 * data.width / 15)))
    data.oppImageRect = (5.2 * data.length / 7, 3 * data.width / 10 + 0.8 * data.width / 30,
                        data.width, data.width)

#initCareers Helper
def initCareerAchievements(data):
    a1 = [{("grade"):["==", ["B", "A"]]}, "6th Man", "Achieve a B or higher", 50]
    a2 = [{("grade"):["==", ["A"]]}, "All Star", "Achieve an A", 100]
    a3 = [{("hasTripleDouble"):["==", [True]]}, "Russell Westbrook", 
            "Have a triple double", 150]
    a4 = [{("hasQuadrupleDouble"):["==", [True]]}, "Hakeem Olajuwon", 
            "Have a quadruple double", 300]
    a5 = [{("points"):[">=", [20]]}, "Kobe Bryant", "Score all the team's points", 100]
    a6 = [{("points"):[">=", [5]], ("assists"):[">=", [5]], ("rebounds"):[">=", [5]],
            ("steals"):[">=", [5]], ("blocks"):[">=", [5]]}, 
            "Draymond Green", "Have a 5 x 5 game", 300]
    a7 = [{("points"):["<=", [0]], ("grade"):["==", ["B", "A"]]}, 
            "Reggie Evans", "B or higher w/o points", 150]
    a8 = [{("points"):["<=", [0]], ("grade"):["==", ["A"]]}, 
            "Dennis Rodman", "Get an A w/o points", 200]
    a9 = [{("assists"):[">=", [10]]}, "John Stockton", "10+ assists in a game", 300]
    a10 = [{("points"):[">=", [10]], ("assists"):[">=", [5]],
            ("turnovers"):["<=", [0]]}, "Chris Paul", "10+ pts, 5+ assists, no TO", 400]
    a11 = [{("fgm", "fga", "/"):[">=", [0.85]], ("points"):[">=", [15]]}, 
            "LeBron James", "15+ points shooting 85+%", 150]
    a12 = [{("fgm3", "fga3", "/"):[">=", [0.8]], ("fgm3"):[">=", [6]]}, 
            "Steph Curry", "Score 6 3's on 80+% 3P%", 300]
    data.achievements = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12]
    
def initCareers(data): #Initializes career screen
    initMyCareer(data)
    initCareerTeams(data)
    initCareerFlags(data)
    initCareerAchievements(data)

#initGameplay Helper
def initGameplayModes(data):
    data.mode = "2D"
    data.subMode = "None"

#initGameplay Helper
def initGameplayModifiers(data):
    #Modifiers that are used in player methods to adjust gameplay
    
    #Drawing
    data.maxYDraw = 100
    data.radScale3D = 0.6
    
    #Movement
    data.d = data.length / 333.33
    
    #Dribbling
    data.dribbleAngle = math.pi / 3
    
    #Shooting
    data.defenderSpeedInc = 1.2
    data.shootSpeed = 0.4
    data.layupSpeed = 0.4
    data.shotErrorWeight = 4 #IMPORTANT! Affects how easy it is to make shots
    
    #Jumping
    data.maxJump = 7 * data.length / 94
    data.minJump = 2 * data.length / 94
    data.minShootJump = data.length / 94
    data.maxShootJump = 3 * data.length / 94
    data.jumpInterval = 0.06
    
    #Blocking
    data.blockAngle = 38 * math.pi / 100
    data.blockCount = 0
    data.blockCountMax = 200
    
    #Stealing
    data.stealChance = 0.5
    data.stealCountMax = 500
    data.stealCrossoverCount = 10 #Minimum time for crossover- edit later
    data.stealCrossCountMax = 60 #Maximum time for crossover- edit later
    data.stealImmobileCount = 100
    
    #Crossovers
    data.crossoverFailChance = 0.5
    
    #Passing
    data.passStrengthAdj = 1.2
    
    #AI
    data.aiWaitTime = 0.2

#initGameplay Helper
def initGameplayUserTeams(data):
    #Set up user teams based on user dicts
    data.user1Colors = {"uColor":tuple(data.user1TeamDict["uColor"]), "dColor":tuple(data.user1TeamDict["dColor"])}
    data.user1TeamName = data.user1TeamDict["name"]
    data.user2Colors = {"uColor":tuple(data.user2TeamDict["uColor"]), "dColor":tuple(data.user2TeamDict["dColor"])}
    data.user2TeamName = data.user2TeamDict["name"]
    #Dummy for one player games
    dummyDict = copy.deepcopy(data.user2TeamDict)
    data.dummyPlayer = Forward(data, dummyDict["forward"], data.user2Colors["uColor"], data.user2Colors["dColor"])
    data.user1Team = [Center(data, data.user1TeamDict["center"], data.user1Colors["uColor"], data.user1Colors["dColor"]),
                      Guard(data, data.user1TeamDict["guard"], data.user1Colors["uColor"], data.user1Colors["dColor"]),
                      Forward(data, data.user1TeamDict["forward"], data.user1Colors["uColor"], data.user1Colors["dColor"])]
    data.user2Team = [Center(data, data.user2TeamDict["center"], data.user2Colors["uColor"], data.user2Colors["dColor"]),
                      Guard(data, data.user2TeamDict["guard"], data.user2Colors["uColor"], data.user2Colors["dColor"]),
                      Forward(data, data.user2TeamDict["forward"], data.user2Colors["uColor"], data.user2Colors["dColor"])]
    data.prevPlayer2 = data.user2Team[0] #AI Drawing Purposes
    data.prevPlayer2Dup = data.user2Team[0]
    data.offensiveTeam = data.user1Team
    data.defensiveTeam = data.user2Team
    data.players = data.user1Team + data.user2Team

#initGameplay Helper
def initGameplayObjects(data): #Court, baskets, ball
    data.court = Court(data.length, (0, 0, 0), (204, 51, 255))
    data.baskets = [Basket(data, "Left"), Basket(data, "Right")]
    data.shootingBasket = data.baskets[1]
    data.ballRadius = data.length / 100
    data.ball = Ball(data, 0, 0)
    initPositions(data) #Place players in the right positions

#initGameplay Helper
def initGameplayFlags(data): #Flags, counts and placeholder values for gameplay
    
    #Drawing
    data.crossSection = [(0, 0), (data.width, data.height)]
    data.cobMatrix = [[0, 0], [0, 0]]
    data.screenColor = (0, 0, 0)
    data.ui = "Full"
    
    #Animation
    data.count = 0
    data.animationCount = 100
    data.shootingDir = 1
    data.firstPass2D = True
    data.firstPass3D = False 
    
    #Pausing Animation
    data.pause = False
    data.pausePlayer = ""
    data.pauseNoDraw = False
    data.pauseCount = 0
    data.pauseTime = 0
    data.pauseTextOnly = False
    data.switchPosessionTime = 1.5
    data.pauseText = ""
    
    #Scoreboard/Shotclock
    data.user1Score = 0
    data.user2Score = 0
    data.scoreboardData = "User 1: %d, User 2: %d" % (data.user1Score, data.user2Score)
    data.scoreboard1Text = 0
    data.scoreboard2Text = 0
    data.shotClock = 24
    data.shotClockCounter = 0
    
    #Gameplay
    data.user1 = ""
    if data.careerGame: #User1 is my player if my career game
        user1Position = data.myCareer["position"]
        if user1Position == "center":
            index = 0
        elif user1Position == "guard":
            index = 1
        else:
            index = 2
        data.user1 = data.user1Team[index]
        data.user1.headColor = data.user1TeamDict["uColor"]
    data.user2 = ""
    data.user1Shoot = (False, 0, 0, 0)
    data.user2Shoot = (False, 0, 0, 0)
    data.aiShoot = (False, 0, 0, 0)
    data.shooter = ""
    data.passTarget = ""
    data.prevPassTarget = ""
    data.passer = ""
    data.prevBallHandler = ""
    data.winner = ""
    switchUser1(data) #Initiate user1 and user2
    switchUser2(data)
    data.rebounding = False
    data.blocked = False
    data.user1Backcourt = False
    data.user2Backcourt = False
    data.callForPass = False
    data.user1Turnovers = 0
    
    #Sound
    data.sound = True
    data.musicPlay = True

#initGameplay Helper
def initGameplayPictures(data): #Images used in background
    data.background = pygame.image.load(filePath + "Images/shootingScreen.jpg")
    data.background = pygame.transform.scale(*intify(data.background,
                    (data.court.length, data.court.width))) 
    data.courtImg = pygame.image.load(filePath + "Images/court.png")
    data.courtImg = pygame.transform.scale(*intify(data.courtImg, 
                    (data.court.length, data.court.width)))
    data.pauseImg = pygame.image.load(filePath + "Images/pauseScreen.png")
    data.pauseImg = pygame.transform.scale(*intify(data.pauseImg, 
                    (data.length, data.width)))
    data.pausedText = pygame.image.load(filePath + "Images/pausedText.png")
    data.pausedText = pygame.transform.scale(*intify(data.pausedText, 
                    (data.length / 5.5 * 3.375, data.length / 5.5)))
    data.pausedText = pygame.transform.rotate(data.pausedText, 40)
    rect = data.pausedText.get_rect()
    data.pausedTextRect = (rect[0] - data.length / 30, rect[1] - data.length / 13, rect[2], rect[3])

#initGameplay Helper
def initGameplayButtons(data): #Buttons in pause screen

    #Pause Buttons
    stats = button(data, 3 * data.length / 7, data.width / 4, data.length / 2, data.width / 8,
                        data.screenColor, data.court.lineColor, data.court.paintColor, "Player Stats")
    controls = button(data, data.length / 5, 3 * data.width / 7, data.length / 2, data.width / 8,
                        data.screenColor, data.court.lineColor, data.court.paintColor, "Controls")
    options = button(data, 3 * data.length / 7, 17 * data.width / 28, data.length / 2, data.width / 8,
                        data.screenColor, data.court.lineColor, data.court.paintColor, "Options")
    exitText = "Main Menu"
    if data.careerGame: #Exiting is forfeiting
        exitText = "Forfeit"
    exit = button(data, data.length / 5, 11 * data.width / 14, data.length / 2, data.width / 8,
                        data.screenColor, data.court.lineColor, data.court.paintColor, exitText)
    data.pauseButtons = {"stats":stats, "controls":controls, "exit":exit, "options":options}
    
    #Options Buttons
    toggleSounds = button(data, 3 * data.length / 7, data.width / 4, data.length / 2, data.width / 8,
                        data.screenColor, data.court.lineColor, data.court.paintColor, "Sounds: On")
    toggleMusic = button(data, data.length / 5, 3 * data.width / 7, data.length / 2, data.width / 8,
                        data.screenColor, data.court.lineColor, data.court.paintColor, "Music: On")
    cycleMusic = button(data, 3 * data.length / 7, 17 * data.width / 28, data.length / 2, data.width / 8,
                        data.screenColor, data.court.lineColor, data.court.paintColor, "Cycle Music")
    uiText = "UI: " + data.ui
    uiShift = button(data, data.length / 5, 11 * data.width / 14, data.length / 2, data.width / 8,
                        data.screenColor, data.court.lineColor, data.court.paintColor, uiText)
    data.optionsButtons = {"toggleM":toggleMusic, "toggleS":toggleSounds, "cycle":cycleMusic, "ui":uiShift}

#initGameplay Helper
def initGameplayControls(data): #Player controls
    data.user1moveKeys = ["w", "a", "s", "d"]
    data.user2moveKeys = ["đ", "Ĕ", "Ē", "ē"] #Arrow keys
    data.user1shootKey = " "
    data.user2shootKey = "'"
    data.user1passKey = "İ" #Left shift
    data.user2passKey = "l"
    data.user1crossoverKey = "f"
    data.user2crossoverKey = "k"

#initGameplay Helper
def initSounds(data):
    data.shootSounds = [filePath + "Sounds/UnosDosTres.wav", filePath + "Sounds/HumanLife.wav",
                        filePath + "Sounds/Gravity.wav"]
    data.layupSounds = [filePath + "Sounds/ManFly.wav", filePath + "Sounds/Flight9.wav",
                        filePath + "Sounds/Birdman.wav", filePath + "Sounds/UpHighDownHard.wav"]

def initGameplay(data):
    #playInGameMusic(data)
    
    initGameplayModes(data)
    initGameplayModifiers(data)
    initGameplayUserTeams(data)
    initGameplayObjects(data)
    initGameplayFlags(data)
    initGameplayPictures(data)
    initGameplayButtons(data)
    initGameplayControls(data)
    initSounds(data)

def initPostGame(data): #Only for career mode, adjust rewards
    #Rewards system, can tweak later
    if data.careerGame:
        #Update Achievements
        for i in range(len(data.achievements)):
            if (updateAchievementCompletion(data, data.user1, data.achievements[i][0])
                and data.myAchievements[i] == "No"):
                data.myAchievements[i] = "Confirm"
        #Go to next team
        data.myCareer["oppList"][1] = (data.myCareer["oppList"][1] + 1) % 4
        stats =  ["speed", "passing", "ballHandling", "steal", "shotForm", 
        "accuracyShort", "accuracyMid", "accuracyLong", "strength", "block", 
        "rebounding", "jump"]
        abbrevs = {"speed": "SPD", "passing": "PAS", "ballHandling": "BLH",
                "steal": "STL", "shotForm": "SHT", "accuracyShort": "ACCS",
                "accuracyMid": "ACCM", "accuracyLong": "ACCL", 
                "strength": "STR", "block": "BLK", "rebounding": "RBD",
                "jump": "JMP"}
        random.shuffle(stats)
        winReward = 75
        lossPenalty = 0
        aReward = 150
        bReward = 75
        cReward = 0
        if data.myCareer["difficulty"] == "Normal":
            dec = -0.05
        elif data.myCareer["difficulty"] == "Hard":
            dec = -0.02
        forfeitPenalty = [dec, dec]
        dPenalty = [dec]
        fPenalty = [dec]
        if data.winner == "": #Forfeit
            lost = []
            for i in range(len(forfeitPenalty)):
                j = 0
                while (j < len(stats) and (data.myCareer[stats[j]] < 0.5 - 
                        forfeitPenalty[i] or abbrevs[stats[j]] in lost)):
                    j += 1
                if j == len(stats):
                    continue
                else:
                    data.myCareer[stats[j]] += forfeitPenalty[i]
                    if data.myCareer[stats[j]] < 0.5:
                        data.myCareer[stats[j]] = 0.5
                    lost.append(abbrevs[stats[j]])
            lostText = ""
            for i in range(len(lost)):
                lostText += " " + str(forfeitPenalty[i]) + " " + lost[i]
            data.gradeText = "Forfeit Penalty:" + lostText
            if lostText == "":
                data.gradeText = "No Forfeit Penalty"
            data.winText = "Better Luck Next Time"
            saveUserStats(filePath + "TeamFiles/", data)
            return
        elif data.winner == data.user1TeamDict["name"]:
            data.winText = "Win Reward: " + str(winReward) + " VC"
            data.myCareer["VC"] += winReward
        else:
            data.winText = "Loss Penalty: " + str(lossPenalty) + " VC"
            data.myCareer["VC"] -= lossPenalty
        if data.grade == "A":
            data.gradeText = "Grade Reward: " + str(aReward) + " VC"
            data.myCareer["VC"] += aReward
        elif data.grade == "B":
            data.gradeText = "Grade Reward: " + str(bReward) + " VC"
            data.myCareer["VC"] += bReward
        elif data.grade == "C":
            data.gradeText = "Grade Reward: " + str(cReward) + " VC"
            data.myCareer["VC"] += cReward
        elif data.grade == "D": #D and F result in loss of stats
            lost = []
            for i in range(len(dPenalty)):
                j = 0
                while (j < len(stats) and (data.myCareer[stats[j]] < 0.5 - 
                        dPenalty[i] or abbrevs[stats[j]] in lost)):
                    j += 1
                if j == len(stats):
                    continue
                else:
                    data.myCareer[stats[j]] += dPenalty[i]
                    if data.myCareer[stats[j]] < 0.5:
                        data.myCareer[stats[j]] = 0.5
                    lost.append(abbrevs[stats[j]])
            lostText = ""
            for i in range(len(lost)):
                lostText += " " + str(dPenalty[i]) + " " + lost[i]
            data.gradeText = "Grade Penalty:" + lostText
            if lostText == "":
                data.gradeText = "No Grade Penalty"
        elif data.grade == "F":
            lost = []
            for i in range(len(fPenalty)):
                j = 0
                while (j < len(stats) and (data.myCareer[stats[j]] < 0.5 - 
                        fPenalty[i] or abbrevs[stats[j]] in lost)):
                    j += 1
                if j == len(stats):
                    continue
                else:
                    data.myCareer[stats[j]] += fPenalty[i]
                    if data.myCareer[stats[j]] < 0.5:
                        data.myCareer[stats[j]] = 0.5
                    lost.append(abbrevs[stats[j]])
            lostText = ""
            for i in range(len(lost)):
                lostText += " " + str(fPenalty[i]) + " " + lost[i]
            data.gradeText = "Grade Penalty:" + lostText
            if lostText == "":
                data.gradeText = "No Grade Penalty"
        saveUserStats(filePath + "TeamFiles/", data)

##
# Controller Functions
##

#keyPressed Helper
def calculateShotData(data, player, moveKeys, possKeys, dStep):
    data.crossSection = calculateCrossSection(data, player)
    data.cobMatrix = convertToCobMatrix(data, *data.crossSection)
    if player.outsideThreePointArc(data, data.court):
        shotValue = 3
    else:
        shotValue = 2
    d = data.length / 333.33
    dx = 0
    dy = 0
    if possKeys[0] in moveKeys:
        dy -= dStep * d
    if possKeys[2] in moveKeys:
        dy += dStep * d
    if possKeys[1] in moveKeys:
        dx -= dStep * d
    if possKeys[3] in moveKeys:
        dx += dStep * d
    if dx != 0 and dy != 0:
        dx *= 2 ** 0.5 / 2
        dy *= 2 ** 0.5 / 2
    data.mode = "3D"
    data.firstPass3D = True
    data.shooter = player
    return dx, dy, shotValue

#keyPressed Heloer
def layupTrigger(data, player, shootKey, moveKeys, possKeys):
    dx, dy, shotValue = calculateShotData(data, player, moveKeys, possKeys, data.layupSpeed)
    player.layup(player, data, shootKey, dx, dy, shotValue, True)

#keypressed Helper
def shotTrigger(data, player, moveKeys, possKeys): #Initiate shot
    dx, dy, shotValue = calculateShotData(data, player, moveKeys, possKeys, data.shootSpeed)
    if player is data.user1:
        data.user1Shoot = (True, dx, dy, shotValue)
    elif player is data.user2:
        data.user2Shoot = (True, dx, dy, shotValue)

#keyPressed Helper
def cyclePassTarget(data, user): #Switch pass target
    if user is data.user1:
        L = data.user1Team
    elif user is data.user2:
        L = data.user2Team
    for player in L:
        if not player is user and not player is data.passTarget:
            data.passTarget = player
            return

#keyPressed Helper
def mainMenuKeyPressed(event, data):
    if data.subMode == "Career" and data.changeName:
        #Enter name
        if event.key == pygame.K_BACKSPACE:
            data.myName = data.myName[:-1]
            adjustFontSize(data)
        elif event.key == pygame.K_RETURN:
            data.changeName = False
        elif chr(event.key) in string.ascii_letters + " " and len(data.myName) < 20:
            letter = chr(event.key)
            if len(data.myName) == 0 or data.myName[-1] == " ":
                letter = letter.upper()
            data.myName = data.myName + letter
            adjustFontSize(data)
    elif data.subMode == "Pick Score":
        #Enter max score
        if chr(event.key) in string.digits:
            data.maxScore = data.maxScore * 10 + int(chr(event.key))
            if data.maxScore > 99:
                data.maxScore //= 10
        elif event.key == pygame.K_BACKSPACE:
            data.maxScore //= 10
        elif event.key == pygame.K_RETURN and data.maxScore != 0:
            initGameplay(data)

#keyPressed Helper
def pauseScreenKeyPressed(event, data):
    #Unpause
    if chr(event.key) == "p":
        data.mode = "2D"
        data.prevMode = ""
        data.subMode = "None"

#gameplayKeyPressed Helper
def user1Controls(event, data):
    moveKeys1 = set(data.user1moveKeys) & data.currKeys

    #User1 Cycle Pass Target
    if (chr(event.key) == data.user1shootKey and data.mode == "2D"
        and data.ball.player is data.user1 and data.user1 in data.offensiveTeam
        and data.user1passKey in data.currKeys):
        cyclePassTarget(data, data.user1)
        
    #User1 Layup or Dunk
    elif (chr(event.key) == data.user1shootKey and len(moveKeys1) != 0 and 
        data.user1.withinPaint(data, data.court) and not data.pause 
        and not data.pauseNoDraw and data.ball.player is data.user1 and data.mode == "2D"):
        layupTrigger(data, data.user1, data.user1shootKey, moveKeys1, data.user1moveKeys)
        
    #User1 Jump Shot
    elif (chr(event.key) == data.user1shootKey and not data.pause and 
        not data.pauseNoDraw and data.ball.player is data.user1
        and data.mode == "2D"):
        shotTrigger(data, data.user1, moveKeys1, data.user1moveKeys)
        
    #User1 Call for Pass
    elif (chr(event.key) == data.user1shootKey and not data.pause and 
        not data.pauseNoDraw and not data.ball.player is data.user1
        and data.mode == "2D" and data.user1 in data.offensiveTeam and
        data.careerGame):
        data.callForPass = True
    
    #User1 Block
    elif (chr(event.key) == data.user1shootKey and not data.pause and
        not data.pauseNoDraw and data.user1 in data.defensiveTeam and
        data.mode == "3D" and not data.user1.blocking):
        data.user1.Block(data)
    
    #User1 Steal
    elif (chr(event.key) == data.user1shootKey and not data.pause and
        not data.pauseNoDraw and data.user1 in data.defensiveTeam and
        data.mode == "2D" and not data.user1.stealing and isinstance(data.ball.player, Player)
        and distance(data.user1.x, data.user1.y, data.ball.x, data.ball.y) <=
        data.ball.radius + data.user1.armLength * 1.5):
        data.user1.Steal(data.user1, data, True)
    
    #User1 Pass Initiate
    elif (chr(event.key) == data.user1passKey and data.mode == "2D"
        and data.ball.player is data.user1):
        cyclePassTarget(data, data.user1)
    
    #User1 Switch Player
    elif (chr(event.key) == data.user1passKey and data.mode == "2D"
        and not data.ball.player in data.user1Team and (not data.user1Team is
        data.offensiveTeam or data.rebounding and not data.user1.immobile)):
        switchUser1(data)
    
    #User1 Crossover
    elif (chr(event.key) == data.user1crossoverKey and data.mode == "2D"
        and data.ball.player is data.user1):
        data.user1.switchHand(data)

#gameplayKeyPressed Helper
def user2Controls(event, data):
    moveKeys2 = set(data.user2moveKeys) & data.currKeys
    
    #User2 Cycle Pass Target
    if (chr(event.key) == data.user2shootKey and data.mode == "2D"
        and data.ball.player is data.user2 and data.user2 in data.offensiveTeam
        and data.user2passKey in data.currKeys):
        cyclePassTarget(data, data.user2)
    
    #User2 Layup or Dunk
    elif (chr(event.key) == data.user2shootKey and len(moveKeys2) != 0 and 
        data.user2.withinPaint(data, data.court) and not data.pause 
        and not data.pauseNoDraw and data.ball.player is data.user2 and data.mode == "2D"):
        layupTrigger(data, data.user2, data.user2shootKey, moveKeys2, data.user2moveKeys)
        
    #User2 Jump Shot
    elif (chr(event.key) == data.user2shootKey and not data.pause and 
        not data.pauseNoDraw and data.ball.player is data.user2
        and data.mode == "2D"):
        shotTrigger(data, data.user2, moveKeys2, data.user2moveKeys)
    
    #User2 Block
    elif (chr(event.key) == data.user2shootKey and not data.pause and
        not data.pauseNoDraw and data.user2 in data.defensiveTeam and
        data.mode == "3D" and not data.user2.blocking):
        data.user2.Block(data)
    
    #User2 Steal
    elif (chr(event.key) == data.user2shootKey and not data.pause and
        not data.pauseNoDraw and data.user2 in data.defensiveTeam and
        data.mode == "2D" and not data.user2.stealing and isinstance(data.ball.player, Player)
        and distance(data.user2.x, data.user2.y, data.ball.x, data.ball.y) <=
        data.ball.radius + data.user2.armLength * 1.5):
        data.user2.Steal(data.user2, data, True)
    
    #User2 Pass Initiate
    elif (chr(event.key) == data.user2passKey and data.mode == "2D"
        and data.ball.player is data.user2):
        cyclePassTarget(data, data.user2)
    
    #User2 Switch Player
    elif (chr(event.key) == data.user2passKey and data.mode == "2D"
        and not data.ball.player in data.user2Team and (not data.user2Team is
        data.offensiveTeam or data.rebounding and not data.user2.immobile)):
        switchUser2(data)
    
    #User2 Crossover
    elif (chr(event.key) == data.user2crossoverKey and data.mode == "2D"
        and data.ball.player is data.user2):
        data.user2.switchHand(data)

#keyPressed Helper
def gameplayKeyPressed(event, data):
    #Pause
    if chr(event.key) == "p" and data.mode == "2D" and not data.pauseNoDraw:
        data.mode = "Pause"
    #User Controls
    if not data.pause and not data.pauseNoDraw:
        user1Controls(event, data)
        if data.numPlayers == 2:
            user2Controls(event, data)


def keyPressed(event, data):
    if data.mode == "Main Menu":
        mainMenuKeyPressed(event, data)
    elif data.mode == "Pause":
        pauseScreenKeyPressed(event, data)
    elif data.mode == "2D" or data.mode == "3D":
        gameplayKeyPressed(event, data)

#keyHeld Helper
def movement2D(data, key):
    if not data.user1.immobile or data.user1 in data.offensiveTeam:
        #User1 Movement
        if key == data.user1moveKeys[0]:
            data.user1.move(data, data.user1moveKeys, 0, -1 * data.d)
        elif key == data.user1moveKeys[2]:
            data.user1.move(data, data.user1moveKeys, 0, data.d)
        elif key == data.user1moveKeys[1]:
            data.user1.move(data, data.user1moveKeys, -1 * data.d, 0)
        elif key == data.user1moveKeys[3]:
            data.user1.move(data, data.user1moveKeys, data.d, 0)
        
    if not data.user2.immobile or data.user2 in data.offensiveTeam:
        #User2 Movement
        if key == data.user2moveKeys[0]:
            data.user2.move(data, data.user2moveKeys, 0, -1 * data.d)
        elif key == data.user2moveKeys[2]:
            data.user2.move(data, data.user2moveKeys, 0, data.d)
        elif key == data.user2moveKeys[1]:
            data.user2.move(data, data.user2moveKeys, -1 * data.d, 0)
        elif key == data.user2moveKeys[3]:
            data.user2.move(data, data.user2moveKeys, data.d, 0)

#keyHeld Helper
def movement3D(data, key):
    if not data.user1 is data.shooter:
        #User1 Movement 3D
        if key == data.user1moveKeys[1]:
            data.user1.move3D(data, data.user1moveKeys, -1)
        elif key == data.user1moveKeys[3]:
            data.user1.move3D(data, data.user1moveKeys, 1)
    
    elif not data.user2 is data.shooter:
        #User2 Movement 3D
        if key == data.user2moveKeys[1]:
            data.user2.move3D(data, data.user2moveKeys, -1)
        elif key == data.user2moveKeys[3]:
            data.user2.move3D(data, data.user2moveKeys, 1)

def keyHeld(data, key): 
    if data.mode == "2D" and not data.pause and not data.pauseNoDraw:
        movement2D(data, key)
    elif data.mode == "3D" and not data.pauseNoDraw:
        movement3D(data, key)

def keyReleased(event, data):
    # chr(event.key) gives the character
    #Doesn't work for backspace, up etc. you have to use regular event.key
    #Ex. if event.key == pygame.K_BACKSPACE
    if data.mode == "2D" or data.mode == "3D":

        #User1 Pass Ball:
        if (chr(event.key) == data.user1passKey and data.mode == "2D"
            and data.ball.player is data.user1 and data.user1 in data.offensiveTeam):
            data.user1.passBall(data)
        
        #User2 Pass Ball:
        elif (chr(event.key) == data.user2passKey and data.mode == "2D"
            and data.ball.player is data.user2 and data.user2 in data.offensiveTeam):
            data.user2.passBall(data)

#mainMenuMousePressed Helper
def player1TeamSelection(event, data):
    for i in range(len(data.teamButtons)):
        if data.teamButtons[i].checkIfPressed(event.pos):
            #Dakota Dragons
            if i == 0:
                data.user1TeamDict = data.dragons
            #Hawaii Supernova
            elif i == 1:
                data.user1TeamDict = data.supernova
            #Jersey Tide
            elif i == 2:
                data.user1TeamDict = data.tide
            #Vegas Copperheads
            elif i == 3:
                data.user1TeamDict = data.copperheads
            data.subMode = "Player 2 Team Selection"
    if data.backButton.checkIfPressed(event.pos):
        data.user1TeamDict = {}
        data.subMode = "None"

#mainMenuMousePressed Helper
def player2TeamSelection(event, data):
    for i in range(len(data.teamButtons)):
        if data.teamButtons[i].checkIfPressed(event.pos):
            #Dakota Dragons
            if i == 0 and data.user1TeamDict != data.dragons:
                data.user2TeamDict = data.dragons
                data.subMode = "Pick Score"
            #Hawaii Supernova
            elif i == 1 and data.user1TeamDict != data.supernova:
                data.user2TeamDict = data.supernova
                data.subMode = "Pick Score"
            #Jersey Tide
            elif i == 2 and data.user1TeamDict != data.tide:
                data.user2TeamDict = data.tide
                data.subMode = "Pick Score"
            #Vegas Copperheads
            elif i == 3 and data.user1TeamDict != data.copperheads:
                data.user2TeamDict = data.copperheads
                data.subMode = "Pick Score"
        if event.button == 3: #AI Game
            data.numPlayers = 1
        else:
            data.numPlayers = 2
    if data.backButton.checkIfPressed(event.pos):
        data.user1TeamDict = {}
        data.user2TeamDict = {}
        data.subMode = "Player 1 Team Selection"

#careerScreenMousePressedHelper
def incrementAttribute(data, attribute): #Increases attribute by 5
    if data.myCareer["VC"] >= 100:
        if data.myCareer["difficulty"] == "Normal":
            inc = 0.05
            attMax = 0.99
        elif data.myCareer["difficulty"] == "Hard":
            inc = 0.02
            attMax = 0.80
        if attribute == "Speed":
            attr = "speed"
        elif attribute == "Ball Handling":
            attr = "ballHandling"
        elif attribute == "Passing":
            attr = "passing"
        elif attribute == "Stealing":
            attr = "steal"
        elif attribute == "Shot Form":
            attr = "shotForm"
        elif attribute == "Accuracy Short":
            attr = "accuracyShort"
        elif attribute == "Accuracy Mid":
            attr = "accuracyMid"
        elif attribute == "Accuracy Long":
            attr = "accuracyLong"
        elif attribute == "Blocking":
            attr = "block"
        elif attribute == "Jump":
            attr = "jump"
        elif attribute == "Rebounding":
            attr = "rebounding"
        elif attribute == "Strength":
            attr = "strength"
        if data.myCareer[attr] != attMax:
            data.myCareer["VC"] -= 100
            data.myCareer[attr] += inc
            if data.myCareer[attr] > attMax:
                data.myCareer[attr] = attMax
            data.saved = False
            data.reset = False
            data.confirm = False
            
#mainMenuMousePressed Helper
def careerScreenMousePressed(event, data):
    if data.saveExitButton.checkIfPressed(event.pos):
        if not data.saved: #Act as discard button
            memory = data.achieveFlag
            initCareers(data)
            data.achieveFlag = memory
        elif not data.reset: #Exit button
            saveUserStats(filePath + "TeamFiles/", data)
            data.subMode = "None"
        elif not data.confirm:
            data.reset = False
        else: #Act as hard difficulty
            createNewCareer(filePath + "TeamFiles/", data, "Hard")
            initCareers(data)
    elif data.resetButton.checkIfPressed(event.pos):
        if not data.saved: #Act as save button
            memory = data.achieveFlag
            saveUserStats(filePath + "TeamFiles/", data)
            initCareers(data)
            data.achieveFlag = memory
        elif not data.reset: #Act as reset button
            data.reset = True
        elif not data.confirm: #Acts as reset confirmation button
            data.confirm = True
        else: #Act as normal difficilty
            createNewCareer(filePath + "TeamFiles/", data, "Normal")
            initCareers(data)
    elif data.careerPlayButton.checkIfPressed(event.pos):
        data.user1TeamDict = addMyPlayer(data.myDict, data.myCareer)
        data.user2TeamDict = data.opponents
        data.numPlayers = 1
        overall = dictAverage(data.myCareer)
        if overall < 0.72: #Change later if needed
            data.maxScore = 20
        elif overall < 0.85:
            data.maxScore = 20
        else:
            data.maxScore = 20
        data.grade = "C"
        data.careerGame = True
        initGameplay(data)
    elif data.helpButton.checkIfPressed(event.pos):
        if not data.reset and data.saved:
            data.help = not data.help
            data.achieveFlag = False
    elif data.nameButton.checkIfPressed(event.pos) and not data.changeName:
        data.changeName = True
        data.saved = False
        data.reset = False
        data.confirm = False
        data.myName = ""
    elif data.statsButton.checkIfPressed(event.pos):
        data.achieveFlag = False
    elif data.achievementsButton.checkIfPressed(event.pos):
        data.achieveFlag = True
    for attribute in data.upgradeButtons:
        if data.upgradeButtons[attribute].checkIfPressed(event.pos):
            if not data.achieveFlag and not data.help:
                incrementAttribute(data, attribute)
            else: #Achievement
                attributes = ["Speed", "Ball Handling", "Strength", "Passing", 
                            "Shot Form", "Stealing", "Accuracy Short", 
                            "Blocking", "Accuracy Mid", "Rebounding", 
                            "Accuracy Long", "Jump"]
                index = attributes.index(attribute)
                if data.myAchievements[index] == "Confirm":
                    data.saved = False
                    data.myAchievements[index] = "Yes"
                    data.myCareer["VC"] += data.achievements[index][3]
                    
#mousePressed Helper
def mainMenuMousePressed(event, data):
    if data.subMode == "None":
        if data.playButton.checkIfPressed(event.pos):
            data.subMode = "Player 1 Team Selection"
        elif data.careerButton.checkIfPressed(event.pos):
            initCareers(data)
            data.subMode = "Career"
        elif data.controlsButton.checkIfPressed(event.pos):
            data.subMode = "Controls"
    elif data.subMode ==  "Controls":
        if data.backButton.checkIfPressed(event.pos):
            data.subMode = "None"
    elif data.subMode ==  "Career":
        careerScreenMousePressed(event, data)
    elif data.subMode == "Player 1 Team Selection":
        player1TeamSelection(event, data)
    elif data.subMode == "Player 2 Team Selection":
        player2TeamSelection(event, data)
    elif data.subMode == "Pick Score":
        if data.backButton.checkIfPressed(event.pos):
            data.user2TeamDict = {}
            data.maxScore = 0
            data.subMode = "Player 2 Team Selection"

#pauseScreenMousePressed Helper
def pauseScreenMainMousePressed(data, event):
    for button in data.pauseButtons:
        if data.pauseButtons[button].checkIfPressed(event.pos):
            #See options
            if button == "options":
                data.subMode = "Options"
            #See controls
            elif button == "controls":
                data.subMode = "Controls"
            #See stats
            elif button == "stats":
                data.subMode = "Stats"
            #Exit to main menu
            elif button == "exit":
                if data.careerGame:
                    initPostGame(data)
                    data.mode = "Post Game"
                else:
                    initMainMenu(data)

#pauseScreenMousePressed Helper
def optionsScreenMousePressed(data, event):
    for button in data.optionsButtons:
        if data.optionsButtons[button].checkIfPressed(event.pos):
            #Toggle sounds
            if button == "toggleS":
                data.optionsButtons[button].updateSoundText(data)
                data.sound = not(data.sound)
            #Toggle music
            elif button == "toggleM":
                data.musicPlay = not(data.musicPlay)
                if data.musicPlay:
                    updateMusic(data)
                else:
                    pygame.mixer.music.pause()
                data.optionsButtons[button].updateMusicText(data)
            #Cycle music
            elif button == "cycle":
                pygame.mixer.music.fadeout(2000)
            #Toggle UI
            elif button == "ui":
                if data.ui == "Full":
                    data.ui = "Minimal"
                elif data.ui == "Minimal":
                    data.ui = "Full"
                data.optionsButtons[button].updateUIText(data)
    if data.backButton.checkIfPressed(event.pos):
        data.subMode = "None"

#mousePressed Helper
def pauseScreenMousePressed(event, data):
    if data.subMode == "None":
        pauseScreenMainMousePressed(data, event)
    elif data.subMode == "Controls" or data.subMode == "Stats":
        if data.backButton.checkIfPressed(event.pos):
            data.subMode = "None"
    elif data.subMode == "Options":
       optionsScreenMousePressed(data, event)

def mousePressed(event, data):
    if data.mode == "Main Menu":
        mainMenuMousePressed(event, data)
    elif data.mode == "Pause":
        pauseScreenMousePressed(event, data)
    elif data.mode == "Post Game":
        if data.backButton.checkIfPressed(event.pos):
            careerGame = data.careerGame
            initMainMenu(data)
            if careerGame:
                data.subMode = "Career"
                initCareers(data)

def mouseReleased(event, data):
    pass

def mouseMoved(event, data):
    #event.pos gives x, y coordinates
    pass

def musicEnd(data):
    updateMusic(data)
    # if data.mode == "Main Menu":
    #     updateTitleMusic(data)
    # else:
    #     updateInGameMusic(data)

#timerFired Helper
def updateDataPreAnimation(data):
    #Updating flags and stuff
    updateFlags(data)
    updateTeams(data)
    updateAI(data)
    calculateShootingDir(data)
    checkHeldKeys(data)
    updateUser(data)
    data.user1.removeAIMethods()
    data.user2.removeAIMethods()
    ballChangedHands = checkBallPlayer(data)
    checkBackcourt(data)
    return ballChangedHands

#timerFired Helper
def updateObjectPositions(data):
    #Updating positional data for objects
    for player in data.players:
        player.updateData(data, *data.crossSection, data.cobMatrix)
        player.updateAssistCount(data)
    data.ball.updateCoords(data)
    for basket in data.baskets:
        basket.updateCoords(data, *data.crossSection, data.cobMatrix)
    changePlayerOrder(data)
    if data.mode == "3D":
        if data.shooter is data.user1:
            data.user1.armTheta = findCrossSectAngle(*data.crossSection[0], 
                            *data.crossSection[1], data) - math.pi
        elif data.shooter is data.user2:
            data.user2.armTheta = findCrossSectAngle(*data.crossSection[0], 
                            *data.crossSection[1], data) - math.pi

#updateAnimations Helper
def animations2D(data, ballChangedHands):
    if data.firstPass2D: #First time switching back to 2D
        data.firstPass2D = False
        data.rebounding = True
        updateScoreboardData(data)
        if data.mode == "Post Game":
            initPostGame(data)
        if isinstance(data.ball.player, Player):
            data.ball.player.startDribbling(data)
    for player in data.players:
        player.resetTo2D()
    if isinstance(data.ball.player, Player) and ballChangedHands:
        data.ball.player.startDribbling(data)
    if not isinstance(data.ball.player, Player):
        for player in data.players:
            if not data.blocked:
                player.pickUpBall(data)
            else:
                if not player is data.shooter:
                    player.pickUpBall(data)
                elif player is data.shooter and data.blockCount > data.blockCountMax:
                    player.pickUpBall(data)
                data.blockCount += 1

#updateAnimations Helper
def animations3D(data):
    if data.firstPass3D: #First time switching back to 3D
        if data.user1Shoot[0]:
            data.user1.shoot(data.user1, data, data.user1shootKey, data.user1Shoot[1], data.user1Shoot[2], 
            data.user1Shoot[3], True)
        elif data.user2Shoot[0]:
            data.user2.shoot(data.user2, data, data.user2shootKey, data.user2Shoot[1], data.user2Shoot[2], 
            data.user2Shoot[3], True)
        elif data.aiShoot[0] and data.numPlayers < 2 and isinstance(data.ball.player, Player):
            data.ball.player.shoot(data.ball.player, data, data.ball.player.key, data.aiShoot[1], data.aiShoot[2],
            data.aiShoot[3], True)
        updateArmTheta3D(data)
        data.blockCount = 0
        data.blocked = False
        data.firstPass3D = False
    
#updateAnimations Helper
def executeAnimations(data):
    for player in data.players:
        if not player is data.pausePlayer:
            for executable in player.executables:
                method = executable[0]
                method(player, *executable[1:])
    for executable in data.ball.executables:
        method = executable[0]
        method(data.ball, *executable[1:])

#timerFired Helper
def updateAnimations(data, ballChangedHands):
    #Mode specific animations or AI
    if data.mode == "2D":
        animations2D(data, ballChangedHands)
    if data.mode == "3D":
        animations3D(data)
    executeAnimations(data)
    checkShotClock(data)

#timerFired Helper
def updateDataPostAnimation(data):
    if data.numPlayers < 2:
        switchUser2(data) #Switch AI User
    updatePlayerFlags(data)
    checkIfBallInBounds(data)
    if data.careerGame and data.mode == "2D": #Update Career Grade
        updateCareerGrade(data)

def timerFired(data):
    fadeInMusic(data)
    if data.mode == "Pause":
        pass
    elif data.mode == "2D" or data.mode == "3D":
        ballChangedHands = updateDataPreAnimation(data)
        updateObjectPositions(data)
        #Animation stuff
        if isinstance(data.pausePlayer, Player) or data.pauseTextOnly:
            updatePauseData(data)
        if data.pause or data.pauseNoDraw:
            updatePauseData(data)
        else:
            updateAnimations(data, ballChangedHands)
        updateDataPostAnimation(data)

##
# View Helper Functions
##

def drawCourtBorder(screen, data): #Draws the white border around the court
    margin = (data.width - data.court.width) / 2
    pygame.draw.rect(*intify(screen, data.court.lineColor, (-20, margin - data.court.lineWidth,
                    data.length + 40, data.court.width + 2 * data.court.lineWidth), data.court.lineWidth))

def drawBackground(screen, data): #Draws the court background
    ty = data.width / 2 - data.court.width / 2
    backgroundRect = intify(0, ty, data.court.length, data.court.width)
    screen.blit(data.background, backgroundRect)

def drawTopAndBottom(screen, data, noBottom = False): #Draws the black boxes above and below the court
    margin = (data.width - data.court.width) / 2
    pygame.draw.rect(*intify(screen, data.screenColor, (0, 0,
                    data.length, margin)))
    if not noBottom:
        pygame.draw.rect(*intify(screen, data.screenColor, (0, data.width - margin,
                    data.length, margin)))

#drawTopHeader Helper
def drawTopScores(screen, data): #Draws the scores at the top of the screen
    font = pygame.font.SysFont("verdana", data.length // 17, bold = True)
    margin = (data.width - data.court.width) / 2
    user1Text = data.user1TeamName + ": " + str(data.scoreboard1Text)
    u1cx = data.length / 5
    u2cx = 4 * data.length / 5
    if data.ui == "Full":
        cy = margin / 3
    else:
        cy = margin / 2
    user2Text = data.user2TeamName + ": " + str(data.scoreboard2Text)
    drawText(*intify(screen, font, u1cx, cy, user1Text, data.user1Colors["dColor"]))
    drawText(*intify(screen, font, u2cx, cy, user2Text, data.user2Colors["dColor"]))

#drawTopHeader Helper
def drawShotClock(screen, data): #Draws the shotclock
    font = pygame.font.SysFont("verdana", data.length // 20, bold = True)
    margin = (data.width - data.court.width) / 2
    text = str(data.shotClock)
    cx = data.length / 2
    if data.ui == "Full":
        cy = margin / 3
    elif data.ui == "Minimal":
        cy = margin / 2
    drawText(*intify(screen, font, cx, cy, text, data.court.lineColor))

#drawTopHeader Helper
def drawHeaderText(screen, data): #Draws the header text
    if data.ui == "Full":
        font = pygame.font.SysFont("verdana", data.length // 25, bold = True)
        margin = (data.width - data.court.width) / 2
        if data.offensiveTeam is data.user1Team:
            name = data.user1TeamName
        elif data.offensiveTeam is data.user2Team:
            name = data.user2TeamName
        if data.pauseText == "":
            if not data.careerGame:
                text = "Posession: " + name
            else:
                text = "Teammate Grade: " + data.grade
        else:
            text = data.pauseText
        cx = data.length / 2
        cy = 2 * margin / 3
        drawText(*intify(screen, font, cx, cy, text, data.court.lineColor))

def drawTopHeader(screen, data):
    drawTopScores(screen, data)
    drawShotClock(screen, data)
    drawHeaderText(screen, data)

#drawBottom Footer Helper
def drawBottomStats(screen, data): #Draws the stats at the bottom of the screen
    if data.ui == "Full":
        #Initializing the variables
        player2 = findPlayer2(data)
        oP = data.user1
        dP = player2
        if player2 in data.offensiveTeam:
            oP = player2
            dP = data.user1
        oList = ["PLAYER", "SPD", "STR", "BLH", "SHT", "ACC", "PAS"]
        dList = ["PLAYER", "SPD", "STR", "STL", "BLK", "RBD", "JMP"]
        oText = {"PLAYER":oP, "SPD":oP.speed, "STR":oP.strength, "PAS":oP.passing,
                "BLH":oP.ballHandling, "SHT":oP.shotForm, "ACC":oP.accuracy}
        dText = {"PlAYER":dP, "SPD":dP.speed, "STR":dP.strength, "JMP":dP.jump, 
                "STL":dP.steal, "BLK":dP.block, "RBD":dP.rebounding}
        margin = (data.width - data.court.width) / 2 - data.court.lineWidth
        topMargin = margin / 6
        barWidth = margin / 20
        barLength = data.length / 5
        barMargin = (margin - (barWidth * 6) - 2 * topMargin) / 5
        textMargin = barLength / 4
        font = pygame.font.SysFont("verdana", int(barWidth * 2), bold = True)
        right = data.length / 2 - barMargin
        left = data.length / 2 + barMargin
        for i in range(6):
            #Drawing all the bars in the right places
            u2T, u2L = dText, dList
            u1T, u1L = oText, oList
            if oText["PLAYER"] is player2:
                u1T, u1L = dText, dList
                u2T, u2L = oText, oList
            u1Attr = u1L[i + 1]
            u2Attr = u2L[i + 1]
            u1Length = barLength * u1T[u1Attr]
            u2Length = barLength * u2T[u2Attr]
            lx = right - u1Length
            lx2 = left
            ty = data.width - margin + topMargin + (barWidth + barMargin) * i
            lcx = lx - textMargin / 2
            rcx = lx2 + u2Length + textMargin / 2
            cy = ty + barWidth / 2
            pygame.draw.rect(*intify(screen, data.court.lineColor, (lx, ty, u1Length, barWidth)))
            drawText(*intify(screen, font, lcx, cy, u1Attr, data.court.lineColor))
            pygame.draw.rect(*intify(screen, data.court.lineColor, (lx2, ty, u2Length, barWidth)))
            drawText(*intify(screen, font, rcx, cy, u2Attr, data.court.lineColor))

#drawBottomFooter Helper
def drawBottomCountingStats(screen, data): #Draws player stats for the game
    if data.ui == "Full":
        margin = (data.width - data.court.width) / 2 - data.court.lineWidth
        u1, u2 = data.user1, findPlayer2(data)
        u1L, u2L = u1.displayStats, u2.displayStats
        u1Text1 = ("%d/%d FG, %d PTS, %d ASTS" %(u1L["FGM"], u1L["FGA"], u1L["POINTS"], u1L["ASSISTS"]))
        u1Text2 = ("%d RBDS, %d STLS, %d BLKS" %(u1L["REBOUNDS"], u1L["STEALS"], u1L["BLOCKS"]))
        u2Text1 = ("%d/%d FG, %d PTS, %d ASTS" %(u2L["FGM"], u2L["FGA"], u2L["POINTS"], u2L["ASSISTS"]))
        u2Text2 = ("%d RBDS, %d STLS, %d BLKS" %(u2L["REBOUNDS"], u2L["STEALS"], u2L["BLOCKS"]))
        fontSize = data.length // 55
        font = pygame.font.SysFont("verdana", fontSize)
        sideMargin = data.length / 8
        bottomMargin = margin / 5
        drawText(*intify(screen, font, sideMargin, data.width - bottomMargin, 
                u1Text2, data.court.lineColor))
        drawText(*intify(screen, font, sideMargin, data.width - 1.5 * fontSize - bottomMargin, 
                u1Text1, data.court.lineColor))
        drawText(*intify(screen, font, data.length - sideMargin, data.width - bottomMargin, 
                u2Text2, data.court.lineColor))
        drawText(*intify(screen, font, data.length - sideMargin, data.width - 1.5 * fontSize - bottomMargin, 
                u2Text1, data.court.lineColor))

#drawBottomNameAndHeight Helper
def convertHeight(height, data):
    feet = height // (data.length / 94)
    inches = roundHalfUp((height / (data.length / 94) - feet) * 12)
    return "%d' %d\"" % (feet, inches)

#drawBottomFooter Helper
def drawBottomNameAndHeight(screen, data):
    player2 = findPlayer2(data)
    if data.ui == "Full": #Draws names of users and their heights/weights
        margin = (data.width - data.court.width) / 2 - data.court.lineWidth
        fontSize = data.length // 40
        fontSize2 = data.length // 50
        font = pygame.font.SysFont("verdana", fontSize, bold = True)
        hwFont = pygame.font.SysFont("verdana", fontSize2, bold = True)
        sideMargin = data.length / 8
        topMargin = margin / 6
        drawText(*intify(screen, font, sideMargin, data.width - margin + topMargin, 
                str(data.user1), data.user1.userColor))
        drawText(*intify(screen, font, data.length - sideMargin, data.width - margin + topMargin, 
                str(player2), player2.userColor))
        u1Height = "Height: " + convertHeight(data.user1.height, data) 
        u1Weight = "Weight: " + str(data.user1.weight) + " lb"
        u2Height = "Height: " + convertHeight(player2.height, data)
        u2Weight = "Weight: " + str(player2.weight) + " lb"
        drawText(*intify(screen, hwFont, sideMargin, data.width - margin + topMargin + 2 * fontSize2, 
                u1Height, data.court.lineColor))
        drawText(*intify(screen, hwFont, sideMargin, data.width - margin + topMargin + 3.2 * fontSize2, 
                u1Weight, data.court.lineColor))
        drawText(*intify(screen, hwFont, data.length -  sideMargin, data.width - margin + topMargin + 2 * fontSize2, 
                u2Height, data.court.lineColor))
        drawText(*intify(screen, hwFont, data.length - sideMargin, data.width - margin + topMargin + 3.2 * fontSize2, 
                u2Weight, data.court.lineColor))
    elif data.ui == "Minimal":
        margin = (data.width - data.court.width) / 2 - data.court.lineWidth
        fontSize = data.length // 25
        font = pygame.font.SysFont("verdana", fontSize, bold = True)
        drawText(*intify(screen, font, data.length / 4, data.width - margin / 2, 
                str(data.user1), data.user1.userColor))
        drawText(*intify(screen, font, 3 * data.length / 4, data.width - margin / 2, 
                str(player2), player2.userColor))

def drawBottomFooter(screen, data):
    drawBottomStats(screen, data)
    drawBottomCountingStats(screen, data)
    drawBottomNameAndHeight(screen, data)

def drawMainMenuText(screen, data): #Draws the main menu Pyball text
    lineWidth = data.length / 40
    triangleCoords = [(data.length / 8, 0), (data.length, 3 * data.width / 7), 
                      (data.length, 3 * data.width / 14), (5 * data.length / 9, 0)]
    triangleCoords2 = [(data.length / 8 - lineWidth, 0), (data.length, 3 * data.width / 7 + lineWidth), 
                       (data.length, 3 * data.width / 14 - lineWidth), (5 * data.length / 9 + lineWidth, 0)]
    pygame.draw.polygon(*intify(screen, data.court.lineColor, triangleCoords2))
    pygame.draw.polygon(*intify(screen, data.screenColor, triangleCoords))
    screen.blit(data.mainMenuText, data.mainMenuTextRect)

def drawPauseText(screen, data): #Draws the pause text
    lineWidth = data.length / 40
    triangleCoords = [(data.length / 3, 0), (0, data.width / 4), (0, data.width / 2), (2 * data.length / 3, 0)]
    triangleCoords2 = [(data.length / 3 - lineWidth, 0), (0, data.width / 4 - lineWidth), 
                       (0, data.width / 2 + lineWidth), (2 * data.length / 3 + lineWidth, 0)]
    pygame.draw.polygon(*intify(screen, data.court.lineColor, triangleCoords2))
    pygame.draw.polygon(*intify(screen, data.screenColor, triangleCoords))
    screen.blit(data.pausedText, data.pausedTextRect)

def drawControls(screen, data, user1Rect, user2Rect, recolor = False): #Draws control screen
    user1Stats = button(data, *user1Rect, data.screenColor, data.court.lineColor, data.court.paintColor, "")
    user1Stats.draw(screen, data)
    user2Stats = button(data, *user2Rect, data.screenColor, data.court.lineColor, data.court.paintColor, "")
    user2Stats.draw(screen, data)
    font = pygame.font.SysFont("verdana", data.length // 25, bold = True)
    font2 = pygame.font.SysFont("verdana", data.length // 60, bold = True)
    font3 = pygame.font.SysFont("verdana", data.length // 40, bold = True)
    u1cx, u1cy = user1Rect[2] / 2 + user1Rect[0], user1Rect[3] / 8 + user1Rect[1]
    u2cx, u2cy = user2Rect[2] / 2 + user2Rect[0], user2Rect[3] / 8 + user2Rect[1]
    if not recolor:
        drawText(*intify(screen, font, u1cx, u1cy, "Player 1 Controls:", data.user1Colors["dColor"]))
        drawText(*intify(screen, font, u2cx, u2cy, "Player 2 Controls:", data.user2Colors["dColor"]))
    else:
        drawText(*intify(screen, font, u1cx, u1cy, "Player 1 Controls:", data.court.paintColor))
        drawText(*intify(screen, font, u2cx, u2cy, "Player 2 Controls:", data.court.paintColor))
    u1OText = ["Offense:","", "Pass:", "Initiate- Hold Shift", "Cycle Target- Space",
              "Pass- Release Shift", "", "Shoot:", "Initiate- Hold Space", "Shoot- Release Space", "", "Crossover: f"]
    u1DText = ["Defense:", "", "Move: WASD", "", "Switch Player:", "Shift", 
                "", "Steal: Space", "Only in 2D Mode!", "", "Block: Space", "Only in 3D Mode!"]
    if data.careerGame: #Change user2 text based on career game
        u1OText = ["With Ball:","", "Pass:", "Initiate- Hold Shift", "Cycle Target- Space",
                "Pass- Release Shift", "", "Shoot:", "Initiate- Hold Space", "Shoot- Release Space", "", "Crossover: f"]
        u1DText = ["Without Ball:", "", "Move: WASD", "", "Call for Pass:", "Space", 
                    "", "Steal: Space", "Only in 2D Mode!", "", "Block: Space", "Only in 3D Mode!"]
    u2OText = ["Offense:","", "Pass:", "Initiate- Hold l", "Cycle Target- '",
              "Pass- Release l", "", "Shoot:", "Initiate- Hold '", "Shoot- Release '", "", "Crossover: k"]
    u2DText = ["Defense:", "", "Move: Arrow Keys", "",  "Switch Player:", "Press l", 
                "", "Steal: 0", "Only in 2D Mode!", "", "Block: 0", "Only in 3D Mode!"]
    cx1, cy1 = 2 * user1Rect[2] / 7 + user1Rect[0], 11 * user1Rect[3] / 48 + user1Rect[1]
    cx2, cy2 = 5 * user1Rect[2] / 7 + user1Rect[0], 11 * user1Rect[3] / 48 + user1Rect[1]
    cx3, cy3 = 2 * user2Rect[2] / 7 + user2Rect[0], 11 * user2Rect[3] / 48 + user2Rect[1]
    cx4, cy4 = 5 * user2Rect[2] / 7 + user2Rect[0], 11 * user2Rect[3] / 48 + user2Rect[1]
    for i in range(max(len(u1OText), len(u1DText))):
        try: 
            if u1OText[i] == "": 
                cy1 += user1Rect[3] / 24
                cy3 += user1Rect[3] / 24
            else: 
                cy1 += user1Rect[3] / 17
                cy3 += user1Rect[3] / 17
            if u1OText[i] == "Offense:": f = font3
            else: f = font2
            drawText(*intify(screen, f, cx1, cy1, u1OText[i], data.court.lineColor))
            drawText(*intify(screen, f, cx3, cy3, u2OText[i], data.court.lineColor))
        except: pass
        try: 
            if u1DText[i] == "": 
                cy2 += user1Rect[3] / 24
                cy4 += user1Rect[3] / 24
            else: 
                cy2 += user1Rect[3] / 17
                cy4 += user1Rect[3] / 17
            if u1DText[i] == "Defense:": f = font3
            else: f = font2
            drawText(*intify(screen, f, cx2, cy2, u1DText[i], data.court.lineColor))
            drawText(*intify(screen, f, cx4, cy4, u2DText[i], data.court.lineColor))
        except: pass

def drawGameTips(screen, data, rect): #For single player, draws tips
    tips = button(data, *rect, data.screenColor, data.court.lineColor, data.court.paintColor, "")
    tips.draw(screen, data)
    font = pygame.font.SysFont("verdana", data.length // 25, bold = True)
    font2 = pygame.font.SysFont("verdana", data.length // 51, bold = True)
    cx, cy = rect[2] / 2 + rect[0], rect[3] / 8 + rect[1]
    bigGap = data.width / 25
    smallGap = data.width / 40
    if data.careerGame: #Career Mode Tips
        tip1 = "Counting stats add to your grade, and"
        tip2 = "bad shooting/turnovers take away from it"
        tip3 = "On offense, calling for pass passes the"
        tip4 = "ball to you, but bad calls hurt your grade"
        tip5 = "On defense, if the player your guarding"
        tip6 = "has a good shooting night it hurts your"
        tip7 = "grade, so make sure to defend well"
    else: #Vs. AI Tips
        tip1 = "Like a normal player, the AI can also"
        tip2 = "cross you up when you try to steal"
        tip3 = "In addition, the AI can also steal the"
        tip4 = "ball from you, so keep close watch"
        tip5 = "The AI has a tendency to play reckless,"
        tip6 = "but will punish you for aggressive"
        tip7 = "defensive rotations, so be careful"
    drawText(*intify(screen, font, cx, cy, "Tips:", data.user1Colors["dColor"]))
    drawText(*intify(screen, font2, cx, cy + bigGap + 0.6 * smallGap, 
            tip1, data.court.lineColor))
    drawText(*intify(screen, font2, cx, cy + bigGap + 1.6 * smallGap, 
            tip2, data.court.lineColor))
    drawText(*intify(screen, font2, cx, cy + 2 * bigGap + 1.6 * smallGap, 
            tip3, data.court.lineColor))
    drawText(*intify(screen, font2, cx, cy + 2 * bigGap + 2.6 * smallGap, 
            tip4, data.court.lineColor))
    drawText(*intify(screen, font2, cx, cy + 3 * bigGap + 2.6 * smallGap, 
            tip5, data.court.lineColor))
    drawText(*intify(screen, font2, cx, cy + 3 * bigGap + 3.6 * smallGap, 
            tip6, data.court.lineColor))
    drawText(*intify(screen, font2, cx, cy + 3 * bigGap + 4.6 * smallGap, 
            tip7, data.court.lineColor))

#drawPlayerStats Helper
def arrangeTeam(team):
    newTeam = []
    teamCopy = team[:]
    while len(newTeam) < 3:
        for player in teamCopy:
            if isinstance(player, Guard) and len(newTeam) == 0:
                newTeam.append(player)
            elif isinstance(player, Forward) and len(newTeam) ==1:
                newTeam.append(player)
            elif isinstance(player, Center) and len(newTeam) == 2:
                newTeam.append(player)
    return newTeam
              
def drawPlayerStats(screen, data, ext = 0): #Draws Player Stats Screen
    statsRect = (data.length / 8, 2 * data.length / 7, 11 * data.length / 14, data.length / 2)
    statsRectMod = (data.length / 8, 2 * data.length / 7, 11 * data.length / 14, data.length / 2 + ext)
    playerStats = button(data, *statsRectMod, data.screenColor, data.court.lineColor, data.court.paintColor, "")
    playerStats.draw(screen, data)
    statsList = []
    namesList = []
    u1Team, u2Team = arrangeTeam(data.user1Team), arrangeTeam(data.user2Team)
    for player in u1Team:
        L = player.displayStats
        text = ("%d/%d FG, %d PTS, %d ASTS %d RBDS, %d STLS, %d BLKS" %(L["FGM"], L["FGA"], 
                L["POINTS"], L["ASSISTS"], L["REBOUNDS"], L["STEALS"], L["BLOCKS"]))
        namesList.append(str(type(player))[20] + " " + str(player))
        statsList.append(text)
    namesList.append("")
    statsList.append("")
    for player in u2Team:
        L = player.displayStats
        text = ("%d/%d FG, %d PTS, %d ASTS %d RBDS, %d STLS, %d BLKS" %(L["FGM"], L["FGA"],
                L["POINTS"], L["ASSISTS"], L["REBOUNDS"], L["STEALS"], L["BLOCKS"]))
        namesList.append(str(type(player))[20] + " " + str(player))
        statsList.append(text)
    font = pygame.font.SysFont("verdana", data.length // 20, bold = True)
    font2 = pygame.font.SysFont("verdana", data.length // 40, bold = True)
    font3 = pygame.font.SysFont("verdana", data.length // 55, bold = True)
    cx = statsRect[2] / 2 + statsRect[0]
    cy = statsRect[3] / 8 + statsRect[1]
    drawText(*intify(screen, font, cx, cy, "Player Stats:", data.court.lineColor))
    cx1 = statsRect[2] / 5 + statsRect[0]
    cx2 = 2 * statsRect[2] / 3 + statsRect[0]
    for i in range(len(namesList)):
        cy = statsRect[3] / 3 + statsRect[1] + i * statsRect[3] / 12
        if i < 3: color = data.user1Colors["dColor"]
        else: color = data.user2Colors["dColor"]
        drawText(*intify(screen, font2, cx1, cy, namesList[i], color))
        drawText(*intify(screen, font3, cx2, cy, statsList[i], data.court.lineColor))

def drawMiscTips(screen, data): #Draws tips on player stats screen
    tipsRect = (3 * data.length / 5, 25 * data.width / 54, 7 * data.length / 20, 2 * data.width / 5)
    tips = button(data, *tipsRect, data.screenColor, data.court.lineColor, data.court.paintColor, "")
    tips.draw(screen, data)
    font = pygame.font.SysFont("verdana", data.length // 25, bold = True)
    font2 = pygame.font.SysFont("verdana", data.length // 60, bold = True)
    cx, cy = tipsRect[2] / 2 + tipsRect[0], tipsRect[3] / 8 + tipsRect[1]
    drawText(*intify(screen, font, cx, cy, "Other Tips:", data.court.paintColor))
    text = ["Press 'p' to pause/unpause", "", "To maximimze shot accuracy,", "release the shot at the top of",
            "the player's shooting motion", "", "Crossing over while the other", "player steals the ball renders",
            "them immobile for a second", "", "Centers can dunk by holding", " down the shoot button while the", 
            "ball is right above the basket"]
    cy = 9 * tipsRect[3] / 48 + tipsRect[1]
    for i in range(len(text)):
        if text[i] == "": cy += tipsRect[3] / 24
        else: cy += tipsRect[3] / 17
        drawText(*intify(screen, font2, cx, cy, text[i], data.court.lineColor))

def drawTeamsText(screen, data): #Draw the word "Teams"
    teamsRect = (-1 * data.length / 4, data.width / 16, data.length * 1.5, data.width / 5)
    teams = button(data, *teamsRect, data.screenColor, data.court.lineColor, data.court.paintColor, "")
    teams.draw(screen, data)
    screen.blit(data.teamsText, data.teamsRect)

def drawCareerText(screen, data): #Draw the word "My Career"
    careerRect = (-1 * data.length / 4, data.width / 16, data.length * 1.5, data.width / 5)
    career = button(data, *careerRect, data.screenColor, data.court.lineColor, data.court.paintColor, "")
    career.draw(screen, data)
    screen.blit(data.careerText, data.careerRect)

##
# View Functions
##

#mainMenuDraw Helper
def titleScreenDraw(screen, data, titleRect):
    screen.blit(data.mainMenu, titleRect)
    data.playButton.draw(screen, data)
    data.careerButton.draw(screen, data)
    data.controlsButton.draw(screen, data)
    drawMainMenuText(screen, data)

#mainMenuDraw Helper
def controlsScreenDraw(screen, data, titleRect):
    screen.blit(data.mainMenu, titleRect)
    user1Rect = (data.length / 20, data.width / 4, data.length / 2, data.width / 3)
    user2Rect = (data.length / 20, 5 * data.width / 8, data.length / 2, data.width / 3)
    drawControls(screen, data, user1Rect, user2Rect, True)
    drawMiscTips(screen, data)
    data.backButton.draw(screen, data)
    drawMainMenuText(screen, data)

#mainMenuDraw Helper
def player1TeamSelectionDraw(screen, data, titleRect):
    screen.blit(data.mainMenu2, titleRect)
    userRect = (data.length / 16, 15 * data.width / 48, 7 * data.length / 8, data.width / 8)
    user1 = button(data, *userRect, data.screenColor, data.court.lineColor, data.court.paintColor, 
                    "Player 1:")
    user1.draw(screen, data)
    for Button in data.teamButtons:
        Button.draw(screen, data)
    drawTeamsText(screen, data)
    data.backButton.draw(screen, data)

#mainMenuDraw Helper
def player2TeamSelectionDraw(screen, data, titleRect):
    screen.blit(data.mainMenu2, titleRect)
    userRect = (data.length / 16, 15 * data.width / 48, 7 * data.length / 8, data.width / 8)
    user2 = button(data, *userRect, data.screenColor, data.court.lineColor, data.court.paintColor, 
                    "Player 2:")
    user2.draw(screen, data)
    for i in range(len(data.teamButtons)):
        if data.user1TeamDict in data.teamDicts and i == data.teamDicts.index(data.user1TeamDict):
            #Black out the button
            data.teamButtons[i].changeColors(data.user1TeamDict["dColor"], data.court.lineColor,
                                            data.screenColor, data.screenColor)
        data.teamButtons[i].draw(screen, data)
    drawTeamsText(screen, data)
    data.backButton.draw(screen, data)
    #AI Pick
    font = pygame.font.SysFont("verdana", data.length // 40, bold = True)
    cx, cy = data.length / 2, 29 * data.width / 32
    length, width = data.length / 2, data.width / 16
    lineWidth = data.length / 160
    rect = (cx - length / 2, cy - width / 2, length, width)
    rect2 = (rect[0] + lineWidth, rect[1] + lineWidth, rect[2] - 2 * lineWidth, rect[3] - 2 * lineWidth)
    pygame.draw.rect(*intify(screen, data.court.lineColor, rect))
    pygame.draw.rect(*intify(screen, data.screenColor, rect2))
    drawText(screen, font, cx, cy, "Right click for AI", data.court.lineColor)

#mainMenuDraw Helper
def scorePickDraw(screen, data, titleRect):
    screen.blit(data.mainMenu2, titleRect)
    userRect = (data.length / 16, 15 * data.width / 48, 7 * data.length / 8, data.width / 8)
    maxScore = button(data, *userRect, data.screenColor, data.court.lineColor, data.court.paintColor, 
                    "Enter Max Score: %02d" %data.maxScore)
    maxScore.draw(screen, data)
    for i in range(len(data.teamButtons)):
        if data.user1TeamDict in data.teamDicts and i == data.teamDicts.index(data.user1TeamDict):
            #Black out the button
            data.teamButtons[i].changeColors(data.user1TeamDict["dColor"], data.court.lineColor,
                                            data.screenColor, data.screenColor)
        elif data.user2TeamDict in data.teamDicts and i == data.teamDicts.index(data.user2TeamDict):
            #Black out the button
            if data.numPlayers == 2:
                data.teamButtons[i].changeColors(data.user2TeamDict["dColor"], data.court.lineColor,
                                                data.screenColor, data.screenColor)
            else:
                data.teamButtons[i].changeColors((100, 100, 100), data.court.lineColor,
                            data.teamButtons[i].textColor, data.teamButtons[i].textColor2)
        data.teamButtons[i].draw(screen, data)
    drawTeamsText(screen, data)
    #Bottom Text
    font = pygame.font.SysFont("verdana", data.length // 40, bold = True)
    cx, cy = data.length / 2, 29 * data.width / 32
    length, width = data.length / 2, data.width / 16
    lineWidth = data.length / 160
    rect = (cx - length / 2, cy - width / 2, length, width)
    rect2 = (rect[0] + lineWidth, rect[1] + lineWidth, rect[2] - 2 * lineWidth, rect[3] - 2 * lineWidth)
    pygame.draw.rect(*intify(screen, data.court.lineColor, rect))
    pygame.draw.rect(*intify(screen, data.screenColor, rect2))
    if data.maxScore != 0:
        text = "Press 'Enter' to continue"
    else:
        text = "Two player game"
        if data.numPlayers < 2:
            text = "One player vs. AI"
    drawText(screen, font, cx, cy, text, data.court.lineColor)
    data.backButton.draw(screen, data)

#careerScreenDraw helper
def careerHeaderDraw(screen, data, statsT, statsL, statsR):
    #Draws name, team logo and basic stats
    screen.blit(data.myImage, data.myImageRect)
    margin = (data.width - data.court.width) / 2 - data.court.lineWidth
    barWidth = margin / 20
    font1 = pygame.font.SysFont("verdana", data.nameFontSize, bold = True)
    font2 = pygame.font.SysFont("verdana", int(barWidth * 2), bold = True)
    oP = data.myCareer
    sizeText = ("Size: " + str(oP["height"][0]) + "' " + str(oP["height"][1]) + '"'
                + " " + str(oP["weight"]) + " lbs")
    difficultyText = "Difficulty: " + data.myCareer["difficulty"]
    vcText = "VC: " + str(data.myCareer["VC"])
    positionText = "Position: " + oP["position"][0].upper()
    overallText = "Overall: " + str(int(dictAverage(data.myCareer) * 100))
    nameColor = data.court.lineColor
    if not data.changeName:
        nameColor = data.myDict["dColor"]
    drawText(*intify(screen, font1, (statsL + statsR) / 2, statsT + 4.5 * barWidth, 
            data.myName, nameColor, "", 1))
    drawText(*intify(screen, font2, (statsL + statsR) / 2, statsT + 8.5 * barWidth, 
            positionText, data.court.lineColor, "", 1))
    drawText(*intify(screen, font2, (statsL + statsR) / 2, statsT + 11 * barWidth, 
            sizeText, data.court.lineColor, "", 1))
    drawText(*intify(screen, font2, (statsL + statsR) / 2, statsT + 13.5 * barWidth, 
            difficultyText, data.court.lineColor, "", 1))
    drawText(*intify(screen, font2, (statsL + statsR) / 2, statsT + 16 * barWidth, 
            overallText, data.court.lineColor, "", 1))
    drawText(*intify(screen, font2, (statsL + statsR) / 2, statsT + 18.5 * barWidth, 
            vcText, data.court.lineColor, "", 1))

#careerScreenDraw helper
def careerStatsDraw(screen, data, statsT, statsL, statsR):
    #Draws user's myCareer stats
    oP = data.myCareer
    dP = data.myCareer
    oList = ["PLAYER", "Speed", "Strength", "Shot Form", "Accuracy Short", 
            "Accuracy Mid", "Accuracy Long"]
    dList = ["PLAYER", "Ball Handling", "Passing", "Stealing", "Blocking", "Rebounding", "Jump"]
    oText = {"PLAYER":oP, "Speed":oP["speed"], "Strength":oP["strength"], 
            "Shot Form":oP["shotForm"], "Accuracy Short":oP["accuracyShort"],
            "Accuracy Mid":oP["accuracyMid"], "Accuracy Long":oP["accuracyLong"]}
    dText = {"PlAYER":dP, "Passing":oP["passing"], "Ball Handling":oP["ballHandling"], 
            "Jump":dP["jump"], "Stealing":dP["steal"], "Blocking":dP["block"], 
            "Rebounding":dP["rebounding"]}
    margin = (data.width - data.court.width) / 2 - data.court.lineWidth
    topMargin = margin / 6
    barWidth = margin / 20
    barLength = data.length / 5
    barMargin = (margin - (barWidth * 6) - 2 * topMargin) / 5
    textMargin = barLength / 4
    font = pygame.font.SysFont("verdana", int(barWidth * 2), bold = True)
    right = (statsL + statsR) / 2 - barMargin
    left = (statsL + statsR) / 2 + barMargin
    for i in range(6):
        #Drawing all the bars in the right places
        u1T, u1L = oText, oList
        u2T, u2L = dText, dList
        u1Attr = u1L[i + 1]
        u2Attr = u2L[i + 1]
        u1Length = barLength * u1T[u1Attr]
        u2Length = barLength * u2T[u2Attr]
        lx = right - u1Length
        lxFull = right - barLength
        lx2 = left
        ty = statsT + 86 * data.width / 300 + (barWidth + barMargin) * i * 2
        lcx = lx - textMargin / 2
        rcx = lx2 + u2Length + textMargin / 2
        texty = ty - barMargin - barWidth / 2
        lStatsx = (right - barLength + statsL) / 2 + data.court.lineWidth / 2
        rStatsx = (left + barLength + statsR) / 2 - data.court.lineWidth / 2
        pygame.draw.rect(*intify(screen, (100, 100, 100), (lxFull, ty, barLength, barWidth)))
        pygame.draw.rect(*intify(screen, data.court.lineColor, (lx, ty, u1Length, barWidth)))
        data.upgradeButtons[u1Attr] = button(data, lx, ty, u1Length, barWidth,
                data.screenColor, data.court.lineColor, data.court.paintColor, "")
        drawText(*intify(screen, font, right, texty, u1Attr, data.court.lineColor, "", 2))
        drawText(*intify(screen, font, lStatsx, ty, str(int(u1T[u1Attr] * 100 + 0.01)), data.court.lineColor))
        pygame.draw.rect(*intify(screen, (100, 100, 100), (lx2, ty, barLength, barWidth)))
        pygame.draw.rect(*intify(screen, data.court.lineColor, (lx2, ty, u2Length, barWidth)))
        data.upgradeButtons[u2Attr] = button(data, lx2, ty, u2Length, barWidth,
                data.screenColor, data.court.lineColor, data.court.paintColor, "")
        drawText(*intify(screen, font, left, texty, u2Attr, data.court.lineColor, "", 1))
        drawText(*intify(screen, font, rStatsx, ty, str(int(u2T[u2Attr] * 100 + 0.01)), data.court.lineColor))

#careerScreenDraw helper
def careerAchievementsDraw(screen, data, statsT, statsL, statsR):
    #Draws user's myCareer stats
    oP = data.myCareer
    dP = data.myCareer
    oList = ["PLAYER", "Speed", "Strength", "Shot Form", "Accuracy Short", 
            "Accuracy Mid", "Accuracy Long"]
    dList = ["PLAYER", "Ball Handling", "Passing", "Stealing", "Blocking", "Rebounding", "Jump"]
    oText = {"PLAYER":oP, "Speed":oP["speed"], "Strength":oP["strength"], 
            "Shot Form":oP["shotForm"], "Accuracy Short":oP["accuracyShort"],
            "Accuracy Mid":oP["accuracyMid"], "Accuracy Long":oP["accuracyLong"]}
    dText = {"PlAYER":dP, "Passing":oP["passing"], "Ball Handling":oP["ballHandling"], 
            "Jump":dP["jump"], "Stealing":dP["steal"], "Blocking":dP["block"], 
            "Rebounding":dP["rebounding"]}
    margin = (data.width - data.court.width) / 2 - data.court.lineWidth
    topMargin = margin / 6
    barWidth = margin / 20
    barLength = data.length / 5
    barMargin = (margin - (barWidth * 6) - 2 * topMargin) / 5
    textMargin = barLength / 4
    font = pygame.font.SysFont("verdana", int(barWidth * 1.8), bold = True, italic = False)
    font2 = pygame.font.SysFont("verdana", int(barWidth * 1.5), bold = True)
    right = (statsL + statsR) / 2 - barMargin
    left = (statsL + statsR) / 2 + barMargin
    for i in range(6):
        a = data.achievements
        #Drawing all the bars in the right places
        u1T, u1L = oText, oList
        u2T, u2L = dText, dList
        u1Attr = u1L[i + 1]
        u2Attr = u2L[i + 1]
        u1Length = barLength * u1T[u1Attr]
        u2Length = barLength * u2T[u2Attr]
        lx = right - u1Length
        lxFull = right - barLength
        lx2 = left
        ty = statsT + 86 * data.width / 300 + (barWidth + barMargin) * i * 2
        lcx = lx - textMargin / 2
        rcx = lx2 + u2Length + textMargin / 2
        texty = ty - barMargin - barWidth / 2
        lStatsx = (right - barLength + statsL) / 2 + data.court.lineWidth / 2
        rStatsx = (left + barLength + statsR) / 2 - data.court.lineWidth / 2
        llx = statsL + data.length / 40
        rrx = statsR - data.length / 30
        lineWidth = data.width // 300
        if lineWidth <= 0:
            lineWidth = 1
        lConfirm = data.myAchievements[2*i]
        rConfirm = data.myAchievements[2*i + 1]
        lColor, rColor = data.court.lineColor, data.court.lineColor
        if lConfirm == "No":
            lColor = data.achieveColor
        if rConfirm == "No":
            rColor = data.achieveColor
        data.upgradeButtons[u1Attr] = button(data, lx, ty, u1Length, barWidth,
                data.screenColor, data.court.lineColor, data.court.paintColor, "")
        drawText(*intify(screen, font, right, texty, a[2*i][1], 
                lColor, "", 2))
        drawText(*intify(screen, font2, right, ty, a[2*i][2], data.court.lineColor, "", 2))
        if lConfirm == "Yes":
            pygame.draw.line(*intify(screen, data.court.lineColor, 
                        (llx - data.width / 200, texty - data.width / 200), (llx, texty),
                        lineWidth))
            pygame.draw.line(*intify(screen, data.court.lineColor, 
                        (llx + data.width / 120, texty - data.width / 70), (llx, texty),
                        lineWidth))
        data.upgradeButtons[u2Attr] = button(data, lx2, ty, u2Length, barWidth,
                data.screenColor, data.court.lineColor, data.court.paintColor, "")
        drawText(*intify(screen, font, left, texty, a[2*i + 1][1], 
                rColor, "", 1))
        drawText(*intify(screen, font2, left, ty, a[2*i + 1][2], data.court.lineColor, "", 1))
        if rConfirm == "Yes":
            pygame.draw.line(*intify(screen, data.court.lineColor, 
                        (rrx - data.width / 200, texty - data.width / 200), (rrx, texty),
                        lineWidth))
            pygame.draw.line(*intify(screen, data.court.lineColor, 
                        (rrx + data.width / 120, texty - data.width / 70), (rrx, texty),
                        lineWidth))

#careerScreenDraw Helper
def careerHelpDraw(screen, data, statsT, statsL, statsR):
    font = pygame.font.SysFont("verdana", int(data.width / 25), bold = True)
    font2 = pygame.font.SysFont("verdana", int(data.width / 50), bold = True)
    cx = (statsL + statsR) / 2
    textGap1 = data.width / 19
    textGap2 = data.width / 35
    headerText = "How My Career Works:"
    tip1 = "Play games, earn achievements and upgrade"
    tip2 = "your player in My Career."
    tip3 = "To delete your current career and start"
    tip4 = "over, hit the reset button."
    tip5 = "Difficulty changes opponents' OVR and"
    tip6 = "your max OVR. In Normal, you can go to"
    tip7 = "99 OVR but in Hard, the limit is 80."
    tip8 =  "The main currency is VC. VC can be used to"
    tip9 = "upgrade stats. Click a stat bar to spend"
    tip10 = "100 VC to upgrade it."
    tip11 = "Clicking your player's name lets you change it."
    tip12 = "Simply type in a new name and hit enter."
    drawText(*intify(screen, font, cx, statsT + textGap1, 
              headerText, data.myDict["dColor"]))
    drawText(*intify(screen, font2, cx, statsT + 2 * textGap1 + 0.5 * textGap2, 
              tip1, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 2 * textGap1 + 1.5 * textGap2, 
              tip2, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 3 * textGap1 + 1.5 * textGap2, 
              tip3, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 3 * textGap1 + 2.5 * textGap2, 
              tip4, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 4 * textGap1 + 2.5 * textGap2, 
              tip5, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 4 * textGap1 + 3.5 * textGap2, 
              tip6, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 4 * textGap1 + 4.5 * textGap2, 
              tip7, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 5 * textGap1 + 4.5 * textGap2, 
              tip8, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 5 * textGap1 + 5.5 * textGap2, 
              tip9, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 5 * textGap1 + 6.5 * textGap2, 
              tip10, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 6 * textGap1 + 6.5 * textGap2, 
              tip11, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 6 * textGap1 + 7.5 * textGap2, 
              tip12, data.court.lineColor))

#careerScreenDraw Helper
def careerHelpDraw2(screen, data, statsT, statsL, statsR): #Second Help Screen
    font = pygame.font.SysFont("verdana", int(data.width / 25), bold = True)
    font2 = pygame.font.SysFont("verdana", int(data.width / 50), bold = True)
    cx = (statsL + statsR) / 2
    textGap1 = data.width / 19
    textGap2 = data.width / 35
    headerText = "How My Career Works:"
    tip1 = "Games are played to 20 and provide you with"
    tip2 = "rewards depending on both a teammate grade"
    tip3 = "you earn during the game and the outcome."
    tip4 = "On offense, there is a new way to call for pass."
    tip5 = "Please check the control screen during a game."
    tip6 = "Achievements require a minimum grade of C to"
    tip7 = "complete. Colored achievements haven't been"
    tip8 = "completed whereas white ones have been."
    tip9 = "A check on the achievement tab indicates"
    tip10 = "pending achievements to be claimed."
    tip11 = "To claim rewards, click the text under a white"
    tip12 = "achievement, making a check appear. Checked"
    tip13 = "achievements cannot be claimed again."
    drawText(*intify(screen, font, cx, statsT + textGap1, 
              headerText, data.myDict["dColor"]))
    drawText(*intify(screen, font2, cx, statsT + 2 * textGap1 + 0.5 * textGap2, 
              tip1, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 2 * textGap1 + 1.5 * textGap2, 
              tip2, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 2 * textGap1 + 2.5 * textGap2, 
              tip3, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 3 * textGap1 + 2.5 * textGap2, 
              tip4, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 3 * textGap1 + 3.5 * textGap2, 
              tip5, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 4 * textGap1 + 3.5 * textGap2, 
              tip6, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 4 * textGap1 + 4.5 * textGap2, 
              tip7, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 4 * textGap1 + 5.5 * textGap2, 
              tip8, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 5 * textGap1 + 5.5 * textGap2, 
              tip9, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 5 * textGap1 + 6.5 * textGap2, 
              tip10, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 6 * textGap1 + 6.5 * textGap2, 
              tip11, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 6 * textGap1 + 7.5 * textGap2, 
              tip12, data.court.lineColor))
    drawText(*intify(screen, font2, cx, statsT + 6 * textGap1 + 8.5 * textGap2, 
              tip13, data.court.lineColor))

#mainMenuDraw Helper
def careerScreenDraw(screen, data, titleRect):
    screen.blit(data.mainMenu2, titleRect)
    drawCareerText(screen, data)
    #Play button
    data.careerPlayButton.draw(screen, data)
    screen.blit(data.oppImage, data.oppImageRect)
    oppOvr = multiDictAverage(data.opponents["guard"], data.opponents["forward"],
            data.opponents["center"])
    playText = "Play: " + str(int(oppOvr * 100)) + " OVR"
    cx = (2 * 5 * data.length / 7 + data.length / 4) / 2
    cy = (8 * 3 * data.width / 10 + 7 * 4 * data.width / 15) / 8 - data.width / 150
    margin = (data.width - data.court.width) / 2 - data.court.lineWidth
    barWidth = margin / 20
    font = pygame.font.SysFont("verdana", int(barWidth * 2.5), bold = True)
    drawText(*intify(screen, font, cx, cy, playText, data.opponents["dColor"]))
    if not data.reset and data.saved:
        #Help
        if data.help:
            back = button(data, 5 * data.length / 7, 7 * data.width / 10, 
                            data.length / 4, data.width / 15, data.screenColor, 
                            data.court.lineColor, data.court.paintColor, "Back")
            back.draw(screen, data)
        else:
            data.helpButton.draw(screen, data)
        data.resetButton.draw(screen, data)
        data.saveExitButton.draw(screen, data)
    elif data.reset and not data.confirm:
        #Reset confirmation buttons
        confirm = button(data, 5 * data.length / 7, 7 * data.width / 10, data.length / 4, data.width / 15,
                            data.screenColor, data.court.lineColor, data.lightPurple, "Reset??")
        yes = button(data, 5 * data.length / 7, 8 * data.width / 10, data.length / 4, data.width / 15,
                            data.screenColor, data.court.lineColor, data.court.paintColor, "Yes")
        no =  button(data, 5 * data.length / 7, 9 * data.width / 10, data.length / 4, data.width / 15,
                            data.screenColor, data.court.lineColor, data.court.paintColor, "No")
        confirm.draw(screen, data)
        yes.draw(screen, data)
        no.draw(screen, data)
    elif data.confirm:
        #Difficulty Buttons
        difficulty = button(data, 5 * data.length / 7, 7 * data.width / 10, data.length / 4, data.width / 15,
                            data.screenColor, data.court.lineColor, data.lightPurple, "Difficulty")
        normal = button(data, 5 * data.length / 7, 8 * data.width / 10, data.length / 4, data.width / 15,
                            data.screenColor, data.court.lineColor, data.court.paintColor, "Normal")
        hard =  button(data, 5 * data.length / 7, 9 * data.width / 10, data.length / 4, data.width / 15,
                            data.screenColor, data.court.lineColor, data.court.paintColor, "Hard")
        difficulty.draw(screen, data)
        normal.draw(screen, data)
        hard.draw(screen, data)
    else:
        #Save/discard buttons
        unsaved = button(data, 5 * data.length / 7, 7 * data.width / 10, data.length / 4, data.width / 15,
                            data.screenColor, data.court.lineColor, data.lightPurple, "Edits Made")
        save = button(data, 5 * data.length / 7, 8 * data.width / 10, data.length / 4, data.width / 15,
                            data.screenColor, data.court.lineColor, data.court.paintColor, "Save")
        discard =  button(data, 5 * data.length / 7, 9 * data.width / 10, data.length / 4, data.width / 15,
                            data.screenColor, data.court.lineColor, data.court.paintColor, "Discard")
        unsaved.draw(screen, data)
        save.draw(screen, data)
        discard.draw(screen, data)
    statsT = data.width / 3.4
    statsL = data.length / 16
    statsR = statsL + 4 * data.length / 7
    statsB = statsT + 3 * data.width / 5
    statsRect = (statsL, statsT, statsR - statsL, statsB - statsT)
    stats = button(data, *statsRect, data.screenColor, data.court.lineColor, data.court.paintColor, "")
    stats.draw(screen, data)
    if not data.help:
        careerHeaderDraw(screen, data, statsT, statsL, statsR)
        if data.achieveFlag:
            careerAchievementsDraw(screen, data, statsT, statsL, statsR)
        else:
            careerStatsDraw(screen, data, statsT, statsL, statsR)
        data.statsButton.draw(screen, data)
        data.achievementsButton.draw(screen, data)
        x = (statsL + statsR) / 2 + margin / 6
        y = 15 * data.width / 16
        lineWidth = data.width // 180
        if lineWidth <= 0:
            lineWidth = 1
        #Achievement check
        confirm = False
        for string in data.myAchievements:
            if string == "Confirm":
                confirm = True
                break
        if confirm:
            pygame.draw.line(*intify(screen, data.court.lineColor, 
                        (x - data.width / 120, y - data.width / 120), (x, y),
                        lineWidth))
            pygame.draw.line(*intify(screen, data.court.lineColor, 
                        (x + data.width / 60, y - data.width / 40), (x, y),
                        lineWidth))
        #Achievement Star
        if achievementsComplete(data.myCareer):
            drawStar(screen, x - data.width / 120, 
                    y - data.width / 60, data.width / 60, data.court.lineColor, data.screenColor)
        #Stats STar
        if statsComplete(data.myCareer):
            drawStar(screen, x - (statsR - statsL) / 2 + data.width / 120, 
                    y - data.width / 60, data.width / 60, data.court.lineColor, data.screenColor)
    else: #Help Buttons
        if not data.achieveFlag:
            careerHelpDraw(screen, data, statsT, statsL, statsR) 
        else:
            careerHelpDraw2(screen, data, statsT, statsL, statsR) 
        page1Button = button(data, (statsL + statsR) / 2 - margin / 10 - data.length / 4.5, 
                                11 * data.width / 12, data.length / 4.5, 
                                data.width / 21, data.screenColor,
                                data.court.lineColor, data.court.lineColor, "Page 1")
        page1Button.changeBorderSize(data.width / 200)
        page2Button = button(data, (statsL + statsR) / 2 + margin / 10, 
                                11 * data.width / 12, data.length / 4.5, 
                                data.width / 21, data.screenColor,
                                data.court.lineColor, data.court.lineColor, "Page 2")
        page2Button.changeBorderSize(data.width / 200)
        page1Button.draw(screen, data)
        page2Button.draw(screen, data)

#draw Helper
def mainMenuDraw(screen, data):
    screen.fill(data.screenColor)
    titleRect = (0, 0, data.length, data.width)
    if data.subMode == "None":
        titleScreenDraw(screen, data, titleRect)
    elif data.subMode == "Controls":
        controlsScreenDraw(screen, data, titleRect)
    elif data.subMode == "Career":
        careerScreenDraw(screen, data, titleRect)
    elif data.subMode == "Player 1 Team Selection":
        player1TeamSelectionDraw(screen, data, titleRect)
    elif data.subMode == "Player 2 Team Selection":
        player2TeamSelectionDraw(screen, data, titleRect)
    elif data.subMode == "Pick Score":
        scorePickDraw(screen, data, titleRect)

#draw Helper
def pauseScreenDraw(screen, data):
    screen.fill(data.screenColor)
    pauseRect = (0, 0, data.length, data.width)
    screen.blit(data.pauseImg, pauseRect)
    pygame.draw.rect(*intify(screen, data.screenColor, (
                    0, data.width - data.length / 40, data.length / 4, data.length / 50)))
    if data.subMode == "Stats":
        drawPlayerStats(screen, data)
        data.backButton.draw(screen, data)
    elif data.subMode == "Controls":
        user1Rect = (3 * data.length / 7, data.width / 4, data.length / 2, data.width / 3)
        user2Rect = (data.length / 8, 5 * data.width / 8, data.length / 2, data.width / 3)
        drawControls(screen, data, user1Rect, user2Rect)
        if data.numPlayers < 2:
            drawGameTips(screen, data, user2Rect)
        data.backButton.draw(screen, data)
    elif data.subMode == "None":
        for Button in data.pauseButtons:
            data.pauseButtons[Button].draw(screen, data)
    elif data.subMode == "Options":
        for Button in data.optionsButtons:
            data.optionsButtons[Button].draw(screen, data)
        data.backButton.draw(screen, data)
    drawPauseText(screen, data)

#draw Helper
def postGameDraw(screen, data):
    data.ui = "Full"
    screen.fill(data.screenColor)
    pauseRect = (0, 0, data.length, data.width)
    screen.blit(data.pauseImg, pauseRect)
    pygame.draw.rect(*intify(screen, data.screenColor, (
                    0, data.width - data.length / 40, data.length / 4, data.length / 50)))
    ext = 0
    if data.careerGame: #Extend box to display career rewards
        ext = data.width / 12
    drawPlayerStats(screen, data, ext)
    data.backButton.draw(screen, data, "Exit")
    drawTopAndBottom(screen, data, True)
    margin = (data.width - data.court.width) / 2
    pygame.draw.line(*intify(screen, data.court.lineColor, 
                    (0, margin), (data.length, margin), data.court.lineWidth))
    drawTopScores(screen, data)
    data.shotClock = "Final"
    data.pauseText = "Winner: " + data.winner + "!!!"
    if data.careerGame: #Draw teammate grade and vc rewards
        text = "You Lose!"
        if data.winner == data.user1TeamDict["name"]:
            text = "You Win!"
        elif data.winner == "":
            text = "You Forfeited!"
        data.pauseText = text + " Grade: " + data.grade
        font = pygame.font.SysFont("verdana", data.length // 40, bold = True)
        cx = data.length / 2
        cy = 0.8 * data.width
        cy1 = cy - data.length / 55
        cy2 = cy + data.length / 55
        drawText(*intify(screen, font, cx, cy1, data.gradeText, data.court.lineColor))
        drawText(*intify(screen, font, cx, cy2, data.winText, data.court.lineColor))
    drawShotClock(screen, data)
    drawHeaderText(screen, data)

#draw Helper
def gameplayDraw(screen, data):
    if not data.pauseNoDraw: #If animations aren't paused
        screen.fill(data.screenColor)
        if data.mode == "2D":
            data.count = 0
            data.court.drawCourt(screen, data)
            drawCourtBorder(screen, data)
            for player in data.players:
                player.draw2D(screen, data)
            data.ball.draw2D(screen, data)
            if isinstance(data.passTarget, Player):
                data.passTarget.displayName(screen, data)
            for basket in data.baskets:
                basket.draw2D(screen, data)
        elif data.mode == "3D":
            drawBackground(screen, data)
            data.shootingBasket.draw3DCrossSection(screen, data)
            for player in data.players:
                player.draw3DCrossSection(screen, data)
                if player is data.shooter:
                    data.ball.draw3D(screen, data)
            if data.ball.basketSwitch:
                data.shootingBasket.drawNet(screen, data)
                for player in data.players:
                    player.draw3DCrossSection(screen, data)
    drawTopAndBottom(screen, data)
    drawCourtBorder(screen, data)
    drawTopHeader(screen, data)
    drawBottomFooter(screen, data)

def draw(screen, data):
    if data.mode == "Main Menu":
        mainMenuDraw(screen, data)
    elif data.mode == "Pause":
        pauseScreenDraw(screen, data)
    elif data.mode == "Post Game":
        postGameDraw(screen, data)
    elif data.mode == "2D" or data.mode == "3D":
        gameplayDraw(screen, data)

##
# Main Program
##

def checkHeldKeys(data):
    for key in data.currKeys:
        keyHeld(data, key)

#Skeleton taken from pygame website

def controller(data):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            data.done = True
        if event.type == pygame.KEYDOWN:
            if chr(event.key) != "!" and chr(event.key) != "@":
                data.currKeys.add(chr(event.key))
            keyPressed(event, data)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePressed(event, data)
        elif event.type == pygame.MOUSEBUTTONUP:
            mouseReleased(event, data)
        elif event.type == pygame.MOUSEMOTION:
            mouseMoved(event, data)
        elif event.type ==  pygame.KEYUP:
            if chr(event.key) in data.currKeys:
                if chr(event.key) != "!" and chr(event.key) != "@":
                    data.currKeys.remove(chr(event.key))
            keyReleased(event, data)
        elif event.type == MUSIC_END:
            musicEnd(data)

#Skeleton taken from pygame website

def runGame(length = 600):
    width = length
    height = int(14 * length / 94)
    pygame.init()
    class Struct(object): pass
    data = Struct()
    data.length = length
    data.width = width
    data.height = height
    data.timerDelay = 70 #milliseconds
    data.count = 0
    data.properCount = 0
    data.currKeys = set()
    screen = pygame.display.set_mode((data.length, data.width))
    clock = pygame.time.Clock()
    initMainMenu(data)
    data.done = False
    while not data.done:
        try:
            controller(data)
            data.count += 1
            data.properCount += 1
            timerFired(data)
            draw(screen, data)
        except BaseException as e: #If program crashes, display error and close
            print("Program crashed!")
            print(traceback.format_exc())
            data.done = True
        pygame.display.flip()
        clock.tick(data.timerDelay)
        if data.done == True: #Close program
            pygame.mixer.music.stop()
            pygame.quit()
    print("You have closed the program!")
    
##
# Run Program
##

runGame()