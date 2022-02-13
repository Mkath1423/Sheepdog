#-----------------------------------------------------------------------------
# Name:        Sheepdog (assignment.py)
# Purpose:     A game were you play as a sheepdog that needs to herd a group of sheep towards a goal.
#
# Author:      Lex Stapleton
# Created:     15-Mar-2021
# Updated:     2-Apr-2021
#-----------------------------------------------------------------------------
#    I think this project deserves a level 4+ because my program fits all the requirements
# for level 4 and goes beyond that. My program includes user-friendly UI to encapsulate the game,
# lists, dictionaries, file reading, and data sanitization, microbit sensor input, loops, conditionals,
# classes, and function. My code also runs efficiently without any errors and is properly documented.
# 
#    Furthermore, my program includes many more features, like a multiplayer camera and control system, and
# an implementation of the boids algorithm for emergent behavior within the sheep's movement.
# 
# Features:
#   Multiplayer Gameplay
#     Two player movement with keyboard and microbit input
#     Two player camera that follows the center of both players
#     Split-screen camera that activates when the players are too far apart
#
#   Behaviour algorithm to move sheep
#     Based on boids algorithm
#     Includes attractors and obstacle avoidance
#
#   Menu system
#     Start, help, level select, game and end screens with buttons to navigate the menus
#     Automatic button creation in columns and arrays
#     File loading used to create level select buttons
#
#   Automatic Level Creation
#     Levels are created by loading level files that contain the information for each object
#     Bad inputs in the files are handled properly and won't crash the program
#-----------------------------------------------------------------------------
import pygame
import serial
import serial.tools.list_ports as list_ports

from moveable import *
from wall import Wall
from button import Button
from attractor import Attractor
from scene import Scene
from goal import Goal
from decal import Decal

pygame.init()

# Colors
MENUBACKGROUNDCOLOR = pygame.Color(32, 145, 41)
GAMEBACKGROUNDCOLOR = pygame.Color(255, 255, 255)
SCENEBACKGROUNDCOLOR = pygame.Color(32, 145, 41)

WALLCOLOR = pygame.Color(108, 51, 24)
BUTTONCOLOR = pygame.Color(35, 45, 241)
TEXTCOLOR = pygame.Color(0, 0, 0)

# Fonts
TITLETEXT = pygame.font.SysFont("Impact", 70)
SUBTITLETEXT = pygame.font.SysFont("Impact", 40)
LARGETEXT = pygame.font.SysFont("Impact", 25)
SMALLTEXT = pygame.font.SysFont("Impact", 20)
TINYTEXT = pygame.font.SysFont("Impact", 15)
 
# findMicrobitComPort function code by Mr. Brooks
def findMicrobitComPort(pid=516, vid=3368, baud=115200):
    '''
    This function finds a device connected to usb by it's PID and VID and returns a serial connection
    Parameters
    ----------
    pid: int
        Product id of device to search for
    vid: int
        Vendor id of device to search for
    baud:
        Baud rate to open the serial connection at
    
    ReturnsGAMEBACKGROUNDCOLOR
    -------
    Serial
        If a device is found a serial connection for the device is configured and returned
    '''
    #Required information about the microbit so it can be found
    #PID_MICROBIT = 516
    #VID_MICROBIT = 3368
    TIMEOUT = 0.1
    
    #Create the serial object
    serPort = serial.Serial(timeout=TIMEOUT)
    serPort.baudrate = baud
    
    #Search for device on open ports and return connection if found
    ports = list(list_ports.comports())
    print('scanning ports')
    for p in ports:
        print(f'port: {p}')
        try:
            print(f'pid: {p.pid} vid: {p.vid}')
        except AttributeError:
            continue
        if (p.pid == pid) and (p.vid == vid):
            print(f'found target device pid: {p.pid} vid: {p.vid} port: {p.device}')
            serPort.port = str(p.device)
            return serPort
    
    #If nothing found then return None
    return None

def loadLevelPaths(filepath):
    '''
    Loads the paths of the levels
    
    Reads the lines in the levelPaths file and returns them.
    
    Parameters
    ----------
    filepath: str
        The filepath of the file containing the paths to each game file.
    
    Returns
    -------
    List<str>
        The paths of each level in the game.
        
    Raises
    ------
    FileNotFoundError
        If the file at the specified path is not found
    '''
    # open the file and return its contents
    try:
        file = open(filepath, 'r')
        lines = file.read().split('\n')
        file.close()
    except FileNotFoundError:
        raise FileNotFoundError(f'file {filepath} does not exist')
    
    return lines

def loadLevel(filepath):
    '''
    Loads a level

    From the data within a level file, create the objects in the level and
    return them.
    
    Parameters
    ----------
    filepath: str
        The filepath of the level file.
        
    Returns:
    Scene()
        The scene for this level.
        
    Int
        The time the player has to complete this level.
    
    List<Moveable()>
        The sheepdogs that are in the level.
    
    List<Sheep()>
        The sheep that are in the level.
    
    List<Wall()>
        The walls that are in the level.
    
    List<Attractor()>
        The attractots that are in the level.
        
    List<Goal()>
        The goals that are in the level.
        
    List<Decal()>
        The decals that are in the level
        
    Raises
    ------
    FileNotFoundError
        If the file at the specified path is not found
    '''
    
    print(f'Loading data: {filepath}')
    
    try:
        file = open(filepath, 'r')
        lines = file.read().split('\n')
        file.close()
    except FileNotFoundError:
        raise FileNotFoundError(f'file {filepath} does not exist')
        
    sheepdogs = []
    herd = []
    walls = []
    attractors = []
    goals = []
    decals = []
    gameScene = Scene([500, 500], SCENEBACKGROUNDCOLOR)
    timeToComplete = 40
    
    # loop through each line in the file
    for lineNumber, line in enumerate(lines):
        lineInfo = line.split(' ')
        try:
            # If the line is a scene
            # Make a new scene and store it
            if(lineInfo[0] == 'scene'):
                if(not len(lineInfo) == 3):
                    raise ValueError(f'Scenes must have 3 parameters not {len(lineInfo)}')
                gameScene = Scene([int(lineInfo[1]), int(lineInfo[2])], SCENEBACKGROUNDCOLOR)
            
            # If the line is the timeToComplete variable
            # Store its value
            elif(lineInfo[0] == 'timeToComplete'):
                timeToComplete = int(lineInfo[1])
            
            # If that line is a sheepdog
            # Make a new sheepdog and add it to the sheepdogs list
            elif(lineInfo[0] == 'sheepdog'):
                # If the line does not contain 4 parameters then raise an error
                if(not len(lineInfo) == 4):
                    raise ValueError(f'Sheepdogs must have 4 parameters not {len(lineInfo)}')
                    
                img = pygame.image.load(lineInfo[1])
                pos = [int(lineInfo[2]), int(lineInfo[3])]
                    
                sheepdogs.append(Moveable(img, pos))
                
            # If that line is a sheep
            # Make a new sheep and add it to the herd list   
            elif(lineInfo[0] == 'sheep'):
                # If the line does not contain 4 parameters then raise an error
                if(not len(lineInfo) == 4):
                    raise ValueError(f'Sheep must have 4 parameters not {len(lineInfo)}')
                    
                img = pygame.image.load(lineInfo[1])
                pos = [int(lineInfo[2]), int(lineInfo[3])]
                
                herd.append(Sheep(img, pos))
                
            # If that line is a wall
            # Make a new wall and add it to the walls list
            elif(lineInfo[0] == 'wall'):
                # If the line does not contain 5 parameters then raise an error
                if(not len(lineInfo) == 5):
                    raise ValueError(f'Walls must have 5 parameters not {len(lineInfo)}')
                    
                walls.append(Wall([int(lineInfo[1]), int(lineInfo[2]), int(lineInfo[3]), int(lineInfo[4])], WALLCOLOR))
            
            # If that line is an attractor
            # Make a new attractor and add it to the attractors list
            elif(lineInfo[0] == 'attractor'):
                # If the line does not contain 4 parameters then raise an error
                if(not len(lineInfo) == 4):
                    raise ValueError(f'Attractors must have 4 parameters not {len(lineInfo)}')

                attractors.append(Attractor([int(lineInfo[1]), int(lineInfo[2])], int(lineInfo[3])))
            
            # If that line is a goal
            # Make a new goal and add it to the goals list
            elif(lineInfo[0] == 'goal'):
                # If the line does not contain 5 parameters then raise an error
                if(not len(lineInfo) == 5):
                    raise ValueError(f'Goals must have 5 parameters not {len(lineInfo)}')
                    

                goals.append(Goal([int(lineInfo[1]), int(lineInfo[2]), int(lineInfo[3]), int(lineInfo[4])]))
            
            # If that line is a decal
            # Make a new decal and add it to the decal list
            elif(lineInfo[0] == 'decal'):
                # If the line does not contain 4 parameters then raise an error
                if(not len(lineInfo) == 6):
                    raise ValueError(f'Decals must have 6 parameters not {len(lineInfo)}')
                    
                img = pygame.image.load(lineInfo[1])
                pos = [int(lineInfo[2]), int(lineInfo[3])]
                size = [int(lineInfo[4]), int(lineInfo[5])]
                    
                decals.append(Decal(img, pos, size))
            
            # Raise an error if the line does not have a valid gameobject type
            else:
                raise ValueError(f'{lineInfo[0]} is not a valid gameobject object type.')
        
        # If something goes wrong with the line then skip the line and print the error
        except ValueError as e:
            print(f'Line {lineNumber} Skiped: {e}')
        
        # If there are not enough sheepdogs in the level
        # Make two sheepdogs so that the game does not break
    if(len(sheepdogs) < 2):
        
        sheepdogs = [Moveable(pygame.image.load('img//dog1.png'), [0, 0]),
                     Moveable(pygame.image.load('img//dog2.png'), [0, 0])]
    
    return(gameScene, timeToComplete, sheepdogs, herd, walls, attractors, goals, decals)

# Function addButtonColumn taken from maze-game project
def addButtonColumn(buttonsToAdd, buttonInfo):
    '''
    Creates a column of buttons

    Creates a column of different buttons that all look the same (except for the text).

    Parameters
    ----------
    buttonsToAdd: Dictionary<string, string>
        The text on each button and the returnData value of the button.
        {nextGameState: text}
    
    buttonInfo: Dictionary<string, dynamic>
        The parameters of each buttons.
        Must include these parameters:
        {'buttonXCenter': int,
        'buttonYCenter': int,
        'buttonHeight' int,
        'buttonWidth': int,
        'buttonPadding': int,
        'font': font
        }
        
    Returns
    -------
    List<Button()>
        The buttons that have been created
        
    Raises
    -------
    KeyError
        If one of the specified keys in the buttonInfo is not added this will be raised
    '''
    buttons = []
    # For every button that needs to be added
    for i, button in enumerate(list(buttonsToAdd.items())):
        
        # Calculate the top-left position of the button
        buttonX = buttonInfo['buttonXCenter'] - buttonInfo['buttonWidth'] * 0.5
        buttonY = buttonInfo['buttonYCenter'] + (buttonInfo['buttonHeight'] + buttonInfo['buttonPadding']) * i
        
        # Create a new button object according to the given specs
        # add the button to buttons
        buttons.append(
            Button(button[0],
                   [buttonX, buttonY, buttonInfo['buttonWidth'],
                   buttonInfo['buttonHeight']],
                   BUTTONCOLOR,
                   button[1],
                   TEXTCOLOR,
                   buttonInfo['font'])
            )
    return buttons
    

def addNumberedButtonArray(buttonsToAdd, buttonInfo):
    '''
    Creates an array of buttons

    Creates an array of buttons with a specified row length.
    Buttons are numbered in order starting from 1.

    Parameters
    ----------
    buttonsToAdd: List<str>
        The returnData value of the button.
    
    buttonInfo: Dictionary<string, dynamic>
        The parameters of each buttons.
        Must include these parameters:
        {
        buttonWidth: int
        buttonHeight: int
        arrayCenterX: int
        arrayPosY: int
        buttonPadding: int
        maxRowSize: int
        font: font
        }
        
    Returns
    -------
    List<Button()>
        The buttons that have been created
        
    Raises
    -------
    KeyError
        If one of the specified keys in the buttonInfo is not added this will be raised
    '''
    
    buttons = []
    
    # Calculate the starting position of the button array
    startingPositionX = buttonInfo['arrayCenterX'] - (buttonInfo['buttonWidth'] * buttonInfo['maxRowSize']
                                                    + buttonInfo['buttonPadding'] * (buttonInfo['maxRowSize'] - 1))/2
    startingPositionY = buttonInfo['arrayPositionY']
    
    # for every button that needs to be added
    for buttonNumber, buttonReturnData in enumerate(buttonsToAdd):
        # Calculate the top left position of the button
        buttonX = startingPositionX + (buttonInfo['buttonPadding'] + buttonInfo['buttonWidth']) * (buttonNumber % buttonInfo['maxRowSize'])
        buttonY = startingPositionY + (buttonInfo['buttonPadding'] + buttonInfo['buttonHeight']) * (buttonNumber // buttonInfo['maxRowSize']) 
        
        # Make the button and add it to buttons
        buttons.append(Button(buttonReturnData,
                             [buttonX, buttonY,
                              buttonInfo['buttonWidth'], buttonInfo['buttonHeight']],
                              BUTTONCOLOR,
                              str(buttonNumber + 1),
                              TEXTCOLOR,
                              buttonInfo['font']))
        
    return buttons

# Function writeText taken from maze game project
def writeText(surface, text, textPos, font, textColor):
    '''
    Draws the text on the screen

    Renders and blits text onto a given surface. The parameters control the
    font, color, position, and text displayed.

    Parameters
    ----------
    surface: pygame.Surface()
        The surface that the text will be drawn onto
        
    text: string
        What the text will say
        
    textPos: List<int> [x, y]
        The top left corner of the text on the surface
    
    font: pygame.Font()
        The font that will be used to render the text
        
    textColor: pygame.Color()
        The color of the text
        
    Returns
    -------
    None
    '''
    # Render the text onto a surface
    textSurface = font.render(text, 1, textColor)
    
    # blit the surface onto surfaceIn at the given position
    surface.blit(textSurface, textPos)
    
# Function writeTextCentered taken from maze game project 
def writeTextCentered(surfaceIn, text, textCenter, font, textColor):
    '''
    Draws the text on the screen

    Renders and blits text onto a given surface. The parameters control the
    font, color, position, and text displayed. The text will be centered on
    the given position

    Parameters
    ----------
    surface: pygame.Surface()
        The surface that the text will be drawn onto
        
    text: string
        What the text will say
        
    textCenter: List<int> [x, y]
        The center of the text on the surface
       
    
    font: pygame.Font()
        The font that will be used to render the text
        
    textColor: pygame.Color()
        The color of the text
        
    Returns
    -------
    None
    '''
    # Render the text onto a surface
    textSurface = font.render(text, 1, textColor)
    
    # blit the surface onto surfaceIn using the given position as a center
    surfaceIn.blit(textSurface, (textCenter[0] - textSurface.get_width()/2,
                                 textCenter[1] - textSurface.get_height()/2))

def normalizeGyroValue(gyroX, gyroY, threshold):
    '''
    This function normalizes the gyro values from +/- 2000 to 1, -1 or 0
    
    Parameters
    ----------
    gyroX: float
        The x value of the gyro.
        
    gyroY: float
        The y value of the gyro.
        
    threshold: float
        The smallest gyro value that will not be set to 0.
    
    
    Returns
    -------
    List<int>
        The normalized x and y gyro values. 
    '''
    
    # Change the gyroX value to be 1 if its over the threshold
    # Change the gyroX value to be -1 if its below the negative threshold
    # Change the gyroX value to be 0 if its between the positive and negative thresholds
    if(gyroX > threshold): gyroX = 1
    elif(gyroX < threshold * -1): gyroX = -1
    else: gyroX = 0
    
    # Change the gyroY value to be 1 if its over the threshold
    # Change the gyroY value to be -1 if its below the negative threshold
    # Change the gyroY value to be 0 if its between the positive and negative thresholds
    if(gyroY > threshold): gyroY = 1
    elif(gyroY < threshold * -1): gyroY = -1
    else: gyroY = 0
    
    return [gyroX, gyroY]

def main():
    '''
    Controls the game
    
    Call this once to run the game
    
    Parameters
    ----------
    None
    
    Returns
    -------
    None
    '''
    # Set up the surface, clock and scene
    surfaceSize = 500
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))
    
    clock = pygame.time.Clock()
    
    gameScene = None
    
    # Game variables
    timeToCompleteLevel = 40
    timeLeft = 0
    
    # Gameobjects
    sheepdogs = []
    attractors = []
    herd = []
    walls = []
    goals = []
    decals = []
    
    # Buttons
    gameStateButtons = []
    levelSelectButtons = []
    
    selectedLevelPath = ''
    
    # Values for movement inputs
    isWPressed = False
    isSPressed = False
    isAPressed = False
    isDPressed = False
    
    microbit = None
    THRESHOLD = 100
    
    gameState = 'initializeMain'
    play = True
    while(play):
        
        # Time elapsed from last frame
        deltatime = clock.tick(120)/1000
        
        # If the quit event is triggered
        events = pygame.event.get()
        for event in events:
            if(event.type == pygame.QUIT):
                # exit the loop
                play = False
        
        # MAIN MENU
        if(gameState == 'initializeMain'):
            # Make Buttons: Start, Help, Quit
            buttonPositionInfo = {
                'buttonWidth':100,
                'buttonHeight':50, 
                'buttonXCenter':surfaceSize * 0.5,
                'buttonYCenter':surfaceSize * 0.5,
                'buttonPadding':10,
                'font':SMALLTEXT
                }
            
            buttonsToAdd = {
                'initializeLevelSelect':'Start',
                'initializeHelp':'Help',
                'quit':'Quit'
                }
            
            gameStateButtons.clear()
            gameStateButtons = addButtonColumn(buttonsToAdd, buttonPositionInfo)
            
            # switch to the start screen
            gameState = 'main'
        
        elif(gameState == 'main'):
            for event in events:
                if(event.type == pygame.MOUSEBUTTONUP):
                    # Check if any of the buttons were clicked
                    for button in gameStateButtons:
                        # if they were clicked switch to their associated game state
                        if(button.isMouseColliding(pygame.mouse.get_pos())):
                            gameState = button.returnData
                            
            mainSurface.fill(MENUBACKGROUNDCOLOR)
            
            # write the title
            writeTextCentered(mainSurface, 'SHEEPDOG', (surfaceSize * 0.5, surfaceSize * 0.3), TITLETEXT, TEXTCOLOR)
            
            # Draw Buttons: Start, Help, Quit
            for button in gameStateButtons: button.update(mainSurface, pygame.mouse.get_pos())
            
        # HELP MENU
        elif(gameState == 'initializeHelp'):
            # Make Buttons: Back, Quit
            gameStateButtonPositionInfo = {
                'buttonWidth':50,
                'buttonHeight':25, 
                'buttonXCenter':surfaceSize * 0.9,
                'buttonYCenter':surfaceSize * 0.85,
                'buttonPadding':5,
                'font':TINYTEXT
                }
            
            gameStateButtonsToAdd = {
                'initializeMain':'Back',
                'quit':'Quit'
                }
            
            gameStateButtons.clear()
            gameStateButtons = addButtonColumn(gameStateButtonsToAdd, gameStateButtonPositionInfo)
            gameState = 'help'
        
        elif(gameState == 'help'):
            for event in events:
                if(event.type == pygame.MOUSEBUTTONUP):
                    # Check if any of the buttons were clicked
                    for button in gameStateButtons:
                        # if they were clicked switch to their associated game state
                        if(button.isMouseColliding(pygame.mouse.get_pos())):
                            gameState = button.returnData
                    
            mainSurface.fill(MENUBACKGROUNDCOLOR)
           
            # Draw Buttons: Back, Exit
            for button in gameStateButtons: button.update(mainSurface, pygame.mouse.get_pos())
            
            # Write the menu's name
            subTitlePos = [surfaceSize * 0.5,
                        surfaceSize * 0.05]
            writeTextCentered(mainSurface, 'Help Menu', subTitlePos, SUBTITLETEXT, TEXTCOLOR)
            
            # Write the game instructions
            writeText(mainSurface, 'Chase the sheep into the designated area', (surfaceSize * 0.10, surfaceSize * 0.30), LARGETEXT, TEXTCOLOR)
            writeText(mainSurface, 'Arrows on the ground will guide you', (surfaceSize * 0.10, surfaceSize * 0.30 + 50), LARGETEXT, TEXTCOLOR)
            writeText(mainSurface, 'WASD to control the brown dog', (surfaceSize * 0.10, surfaceSize * 0.30 + 100), LARGETEXT, TEXTCOLOR)
            writeText(mainSurface, 'Tilt the microbit to control the beige dog', (surfaceSize * 0.10, surfaceSize * 0.30 + 150), LARGETEXT, TEXTCOLOR)
        
        # LEVEL SELECT MENU
        elif(gameState == 'initializeLevelSelect'):
            # Make Buttons: Start, Back, Quit
            gameStateButtonPositionInfo = {
                'buttonWidth':50,
                'buttonHeight':25, 
                'buttonXCenter':surfaceSize * 0.9,
                'buttonYCenter':surfaceSize * 0.8,
                'buttonPadding':5,
                'font':TINYTEXT
                }
            
            gameStateButtonsToAdd = {
                'initializeGame':'Start',
                'initializeMain':'Back',
                'quit':'Quit'
                }
            
            gameStateButtons.clear()
            gameStateButtons = addButtonColumn(gameStateButtonsToAdd, gameStateButtonPositionInfo)
            
            # Make Buttons: 1 for each level
            buttonPositionInfo = {
                'buttonWidth':50,
                'buttonHeight':25, 
                'arrayCenterX':surfaceSize * 0.5,
                'arrayPositionY':surfaceSize * 0.1,
                'buttonPadding':5,
                'maxRowSize':3,
                'font':TINYTEXT
                }
            
            buttonsToAdd = loadLevelPaths('level data//levelpaths.txt')
            
            levelSelectButtons.clear()
            levelSelectButtons = addNumberedButtonArray(buttonsToAdd, buttonPositionInfo)
            
            
            gameState = 'levelSelect'
        
        elif(gameState == 'levelSelect'):
            for event in events:
                if(event.type == pygame.MOUSEBUTTONUP):
                    # Check if any of the buttons were clicked
                    for button in gameStateButtons:
                        # if a gameStateButton was clicked switch to their associated game state
                        if(button.isMouseColliding(pygame.mouse.get_pos())):
                            gameState = button.returnData
                            
                            
                        for button in levelSelectButtons:
                            # if a levelSelectButton was clicked store the level path
                            if(button.isMouseColliding(pygame.mouse.get_pos())):
                                selectedLevelPath = button.returnData
                                
                                
                                
            mainSurface.fill(MENUBACKGROUNDCOLOR)
            # Draw Buttons: Back, Quit, Level Selectors
            for button in gameStateButtons + levelSelectButtons: button.update(mainSurface, pygame.mouse.get_pos())
            
            # Write the menu's name
            subTitlePos = [surfaceSize * 0.5,
                        surfaceSize * 0.05]
            writeTextCentered(mainSurface, 'Level Select', subTitlePos, SUBTITLETEXT, TEXTCOLOR)
               
        # GAME MENU   
        elif(gameState == 'initializeGame'):
            # Try to load the level
            # If something goes wrong return to the level selector
            try: 
                levelData = loadLevel(selectedLevelPath)
            except FileNotFoundError as e:
                print(f'Level {selectedLevelPath} not loaded: {e}')
                gameState = 'initializeLevelSelect'
                continue
            
            gameScene, timeToCompleteLevel, sheepdogs, herd, walls, attractors, goals, decals = levelData
            
            # If there are not 2 sheepdogs in the level, return to the level selector
            if(not len(sheepdogs) == 2):
                print(f'Level {selectedLevelPath} has does not have the right amount of sheepdogs')
                gameState = 'initializeLevelSelect'
                continue
            
            # Make Buttons: Back, Quit
            gameStateButtonPositionInfo = {
                'buttonWidth':50,
                'buttonHeight':25, 
                'buttonXCenter':surfaceSize * 0.9,
                'buttonYCenter':surfaceSize * 0.85,
                'buttonPadding':5,
                'font':TINYTEXT
                }
            
            gameStateButtonsToAdd = {
                'initializeMain':'Back',
                'quit':'Quit'
                }
            
            gameStateButtons.clear()
            gameStateButtons = addButtonColumn(gameStateButtonsToAdd, gameStateButtonPositionInfo)
            
            timeLeft = timeToCompleteLevel
            
            gameState = 'initializeMicrobit'
        
        elif(gameState == 'initializeMicrobit'):
            # find the microbit and open the connection
            microbit = findMicrobitComPort()
            if(not microbit):
                microbit = None
                print('microbit not found')
                
            else:
                microbit.open()
                
            gameState = 'game'
            
        
        elif(gameState == 'game'):
            
            for event in events:
                if(event.type == pygame.MOUSEBUTTONUP):
                    # Check if any of the buttons were clicked
                    for button in gameStateButtons:
                        # if they were clicked switch to their associated game state
                        if(button.isMouseColliding(pygame.mouse.get_pos())):
                            gameState = button.returnData
                            
            # PLAYER KEYBOARD CONTROLS
                if(event.type == pygame.KEYDOWN):
                    # Record which key is pressed and record the opposite key as unpressed
                    if(event.key == 119): isWPressed, isSPressed   = True, False 
                    elif(event.key == 97): isAPressed, isDPressed  = True, False  
                    elif(event.key == 115): isWPressed, isSPressed = False, True                        
                    elif(event.key == 100): isAPressed, isDPressed = False, True 
            
                # If a key is unpressed
                elif(event.type == pygame.KEYUP):
                    # Record which key is unpressed
                    if(event.key == 119): isWPressed = False     
                    elif(event.key == 97): isAPressed = False           
                    elif(event.key == 115): isSPressed = False
                    elif(event.key == 100): isDPressed = False
            
            # Rotate and move the first sheepdog according to the inputs
            if(isAPressed): sheepdogs[0].rotate(1, deltatime)
            elif(isDPressed): sheepdogs[0].rotate(-1, deltatime)
            
            if(isWPressed): sheepdogs[0].accelerate(1, deltatime)
            elif(isSPressed): sheepdogs[0].accelerate(-1, deltatime)
            else: sheepdogs[0].accelerate(0, deltatime)
            
            # PLAYER MICRO BIT CONTROLS
            if(not microbit == None):
                line = microbit.readline()
                
                # If it isn't a blank line
                if(not line == None):  
                    #Update the data
                    try:
                        data = line.decode('utf-8').split()
                        data = [int(data[0]), int(data[1])]
                        
                        gyroX, gyroY, = normalizeGyroValue(data[0], data[1], THRESHOLD)
                        
                        # Rotate and move the second sheepdog according to the microbit inputs
                        sheepdogs[1].rotate(gyroX * -1, deltatime)
                        sheepdogs[1].accelerate(gyroY * -1, deltatime)
                    
                    except Exception as e:
                        print(f'Something went wrong with the microbit: {e}')
            
            # DRAWING
            mainSurface.fill(GAMEBACKGROUNDCOLOR)
            
            renderedObjects = decals + sheepdogs + herd + walls
            
            # initialize the camera size 
            cameraSize = [int(surfaceSize * 0.80), int(surfaceSize * 0.5)]
            
            # If the sheepdogs are close enough, display one screen otherwise display 2 screens
            xDistance = abs(sheepdogs[0].position[0] - sheepdogs[1].position[0])
            yDistance = abs(sheepdogs[0].position[1] - sheepdogs[1].position[1])
            
            
            if(xDistance < cameraSize[0] - 50 and yDistance < cameraSize[1] - 50):
                # Single Screen
                # Set the camera position to be inbetween the two sheeepdogs
                cameraPosition = [(sheepdogs[0].position[0] + sheepdogs[1].position[0]) / 2 - cameraSize[0]/2,
                                  (sheepdogs[0].position[1] + sheepdogs[1].position[1]) / 2 - cameraSize[1]/2]
                
                gameScene.boundCameraPosition(cameraPosition, cameraSize)
                
                # Render the objects and blit the output to mainSurface
                mainSurface.blit(gameScene.render(renderedObjects, cameraPosition + cameraSize, cameraSize), (surfaceSize * 0.10, surfaceSize * 0.15))
            else:
                # Split Screen
                cameraSize[0] = int(cameraSize[0] / 2)
                
                # Set each camera position to be centered on one sheepdog
                cameraOnePosition = [sheepdogs[0].position[0] - cameraSize[0]/2,
                                     sheepdogs[0].position[1] - cameraSize[1]/2]
                                      
                gameScene.boundCameraPosition(cameraOnePosition, cameraSize)
                
                cameraTwoPosition = [sheepdogs[1].position[0] - cameraSize[1]/2,
                                     sheepdogs[1].position[1] - cameraSize[1]/2]
                    
                gameScene.boundCameraPosition(cameraTwoPosition, cameraSize)
                
                # Render the cameras and bit them to mainSurface
                mainSurface.blit(gameScene.render(renderedObjects, cameraOnePosition + cameraSize, (int(surfaceSize * 0.40), int(surfaceSize * 0.5))), (surfaceSize * 0.10, surfaceSize * 0.15))
                mainSurface.blit(gameScene.render(renderedObjects, cameraTwoPosition + cameraSize, (int(surfaceSize * 0.40), int(surfaceSize * 0.5))), (surfaceSize * 0.50, surfaceSize * 0.15))                      
            
            # Update sheep, sheepdogs and buttons
            for sheepdog in sheepdogs:
                sheepdog.update(walls, deltatime)
        
            for sheep in herd:
                sheep.update(herd, sheepdogs, attractors, walls, deltatime)
                
                # If a sheep has reached the goal remove it from the game
                for goal in goals:
                    if(goal.isSheepInGoal(sheep.position)): 
                        herd.remove(sheep)
            
            for button in gameStateButtons: button.update(mainSurface, pygame.mouse.get_pos())
            
            # Write the menu's name
            subTitlePos = [surfaceSize * 0.5,
                        surfaceSize * 0.05]
            writeTextCentered(mainSurface, 'Game', subTitlePos, SUBTITLETEXT, TEXTCOLOR)
            
            # Write the time and sheep left
            writeText(mainSurface, f'Sheep left: {len(herd)}', (surfaceSize * 0.1, surfaceSize * 0.8), SMALLTEXT, TEXTCOLOR)
            writeText(mainSurface, f'Time left: {int(timeLeft)}', (surfaceSize * 0.1, surfaceSize * 0.8 + 30), SMALLTEXT, TEXTCOLOR)
            
            # Deincrement the time
            timeLeft -= deltatime
            
            # If the time has run out or there are no sheep left them go to the game over menu
            if(len(herd) == 0 or timeLeft < 0.000001):
                gameState = 'initializeGameOver'
            
                
        # GAME OVER MENU
        elif(gameState == 'initializeGameOver'):
            # Make Buttons: Main Menu, Play Again, Quit
            gameStateButtonPositionInfo = {
                'buttonWidth':80,
                'buttonHeight':25, 
                'buttonXCenter':surfaceSize * 0.9,
                'buttonYCenter':surfaceSize * 0.8,
                'buttonPadding':5,
                'font':TINYTEXT
                }
            
            gameStateButtonsToAdd = {
                'initializeMain':'Main Menu',
                'initializeLevelSelect':'Play Again',
                'quit':'Quit'
                }
            
            gameStateButtons.clear()
            gameStateButtons = addButtonColumn(gameStateButtonsToAdd, gameStateButtonPositionInfo)
            
            gameState = 'gameOver'
        
        elif(gameState == 'gameOver'):
            # Draw Buttons: Main Menu, Play Again, Quit
            for event in events:
                if(event.type == pygame.MOUSEBUTTONUP):
                    # Check if any of the buttons were clicked
                    for button in gameStateButtons:
                        # if they were clicked switch to their associated game state
                        if(button.isMouseColliding(pygame.mouse.get_pos())):
                            gameState = button.returnData
                    
            
            mainSurface.fill(MENUBACKGROUNDCOLOR)
            
            # Write the menu's name
            writeTextCentered(mainSurface, 'Game Over', (surfaceSize * 0.5, surfaceSize * 0.1), TITLETEXT, TEXTCOLOR)
            
            # If the players won
            if(len(herd) == 0):
                writeTextCentered(mainSurface, 'YOU WIN!', (surfaceSize * 0.5, surfaceSize * 0.30), SUBTITLETEXT, TEXTCOLOR)
                writeTextCentered(mainSurface, f'Time Left: {int(timeLeft)}', (surfaceSize * 0.5, surfaceSize * 0.5), LARGETEXT, TEXTCOLOR)
            
            # If the players lost
            elif(timeLeft < 0.00001):
                writeTextCentered(mainSurface, 'YOU LOSE!', (surfaceSize * 0.5, surfaceSize * 0.30), SUBTITLETEXT, TEXTCOLOR)
                writeTextCentered(mainSurface, f'Sheep Left: {len(herd)}', (surfaceSize * 0.5, surfaceSize * 0.5), LARGETEXT, TEXTCOLOR)
            
            # Draw Buttons: Main Menu, Play Again, Quit
            for button in gameStateButtons: button.update(mainSurface, pygame.mouse.get_pos())
        

        elif gameState == 'quit':
            play = False
    
        else:
            print(f'{gameState} is not a valid gameState')
        
        
        pygame.display.flip()
            
    pygame.quit()
    
main()