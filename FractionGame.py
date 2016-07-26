# -*- coding: utf-8 -*-
#!/usr/bin/python
# -*- coding: ascii -*-
import random
import sys
import copy
import os
import serial
import pygame
from pygame.locals import *

pygame.mixer.init()
FPS = 30  # frames per second to update the screen
WINWIDTH = 700  # width of the program's window, in pixels
WINHEIGHT = 500  # height in pixels
WINWIDTH = 900  # width of the program's window, in pixels
WINHEIGHT = 600  # height in pixels
THIRD_WINWIDTH = int(WINWIDTH / 3)
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

# The total width and height of each tile in pixels.
TILEWIDTH = 50
TILEHEIGHT = 85
TILEFLOORHEIGHT = 40

CAM_MOVE_SPEED = 5  # how many pixels per frame the camera moves

PINK = (220, 20, 60)
WHITE = (255, 255, 255)
BGCOLOR = PINK
TEXTCOLOR = WHITE

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

click_sound = pygame.mixer.Sound("letyourbodymove.mp3")
#botoes
#NEXT = 'next'
#BACK = 'back'
#ENTER = 'enter'
#EXIT = 'exit'

def main():
    global FPSCLOCK, DISPLAYSURF, IMAGESDICT, TILEMAPPING, OUTSIDEDECOMAPPING, BASICFONT, PLAYERIMAGES, currentImage

    # Pygame initialization and basic set up of the global variables.
    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    # Because the Surface object stored in DISPLAYSURF was returned
    # from the pygame.display.set_mode() function, this is the
    # Surface object that is drawn to the actual computer screen
    # when pygame.display.update() is called.
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

    pygame.display.set_caption("Brincando com Matemática")
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    # A global dict value that will contain all the Pygame
    # Surface objects returned by pygame.image.load().
    IMAGESDICT = {
        'title': pygame.image.load('bcm_title.png'),
        'resolvido': pygame.image.load('resolvido.png'),}

    #IDCARDS = {
     #   '64 35 15 B8': '1',
      #  '86 D4 31 3B': '0'
       # }

    startScreen()  # show the title screen until the user presses a key

        # if result in ('solved', 'next'):
            # Go to the next level.
        # elif result == 'back':
            # Go to the previous level.
        #    if currentLevelIndex < 0:
                # If there are no previous levels, go to the last one.
        #        currentLevelIndex = len(levels)-1
        # elif result == 'reset':
        #    pass # Do nothing. Loop re-calls runLevel() to reset the level

def readCard():
    ser = serial.Serial('/dev/ttyACM0', 9600)
    while 1 :
	line = ser.readline().strip()
	print(line)
	if 'Card' in line:
            return line

def runLevel(levels, levelNum):
    global currentImage
    levelObj = levels[levelNum]
    mapObj = decorateMap(levelObj['mapObj'], levelObj['startState']['player'])
    gameStateObj = copy.deepcopy(levelObj['startState'])
    mapNeedsRedraw = True  # set to True to call drawMap()
    levelSurf = BASICFONT.render('Nivel %s de %s' % (
        levelNum + 1, len(levels)), 1, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.bottomleft = (20, WINHEIGHT - 35)
    mapWidth = len(mapObj) * TILEWIDTH
    mapHeight = (len(mapObj[0]) - 1) * TILEFLOORHEIGHT + TILEHEIGHT
    MAX_CAM_X_PAN = abs(HALF_WINHEIGHT - int(mapHeight / 2)) + TILEWIDTH
    MAX_CAM_Y_PAN = abs(HALF_WINWIDTH - int(mapWidth / 2)) + TILEHEIGHT

    levelIsComplete = False
    # Track how much the camera has moved:
    cameraOffsetX = 0
    cameraOffsetY = 0
    # Track if the keys to move the camera are being held down:
    cameraUp = False
    cameraDown = False
    cameraLeft = False
    cameraRight = False

    while True:  # main game loop
        # Reset these variables:
        playerMoveTo = None
        keyPressed = False

        for event in pygame.event.get():  # event handling loop

            if event.type == QUIT:
                # Player clicked the "X" at the corner of the window.
                terminate()

            elif event.type == KEYDOWN:
                # Handle key presses
                keyPressed = True
                if event.key == K_LEFT:
                    playerMoveTo = LEFT
                elif event.key == K_RIGHT:
                    playerMoveTo = RIGHT
                elif event.key == K_UP:
                    playerMoveTo = UP
                elif event.key == K_DOWN:
                    playerMoveTo = DOWN

                elif event.key == K_n:
                    return 'next'
                    click_sound.play()
                elif event.key == K_b:
                    return 'back'

                elif event.key == K_ESCAPE:
                    terminate()  # Esc key quits.
                elif event.key == K_BACKSPACE:
                    return 'reset'  # Reset the level.
                elif event.key == K_p:
                    # Change the player image to the next one.
                    currentImage += 1
                    if currentImage >= len(PLAYERIMAGES):
                        # After the last player image, use the first one.
                        currentImage = 0
                    mapNeedsRedraw = True

        if playerMoveTo != None and not levelIsComplete:
            # If the player pushed a key to move, make the move
            # (if possible) and push any stars that are pushable.
            moved = makeMove(mapObj, gameStateObj, playerMoveTo)

            if moved:
                # increment the step counter.
                gameStateObj['stepCounter'] += 1
                mapNeedsRedraw = True

            if isLevelFinished(levelObj, gameStateObj):
                # level is solved, we should show the "Solved!" image.
                levelIsComplete = True
                keyPressed = False

        DISPLAYSURF.fill(PINK)

        if levelIsComplete:
            # is solved, show the "Solved!" image until the player
            # has pressed a key.
            solvedRect = IMAGESDICT['resolvido'].get_rect()
            solvedRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)
            DISPLAYSURF.blit(IMAGESDICT['resolvido'], solvedRect)

            if keyPressed:
                return 'solved'

        pygame.display.update()  # draw DISPLAYSURF to the screen.
        FPSCLOCK.tick()


def startScreen():
    """Display the start screen (which has the title and instructions)
    until the player presses a key. Returns None."""

    # Position the title image.
    titleRect = IMAGESDICT['title'].get_rect()
    topCoord = 50  # topCoord tracks where to position the top of the text
    titleRect.top = topCoord
    titleRect.centerx = HALF_WINWIDTH
    topCoord += titleRect.height

    # Unfortunately, Pygame's font & text system only shows one line at
    # a time, so we can't use strings with \n newline characters in them.
    # So we will use a list with each line in it.
    instructionText = ['Aprenda Matematica de um jeito mais divertido!']

    # Start with drawing a blank color to the entire window:
    DISPLAYSURF.fill(BGCOLOR)

    # Draw the title image to the window:
    DISPLAYSURF.blit(IMAGESDICT['title'], titleRect)

    # Position and draw the text.
    for i in range(len(instructionText)):
        instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()
        topCoord += 10  # 10 pixels will go in between each line of text.
        instRect.top = topCoord
        instRect.centerx = HALF_WINWIDTH
        topCoord += instRect.height  # Adjust for the height of the line.
        DISPLAYSURF.blit(instSurf, instRect)

    while True:  # Main loop for the start screen.
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                else:
                    mainScreen()

        # Display the DISPLAYSURF contents to the actual screen.
        pygame.display.update()
        FPSCLOCK.tick()


def mainScreen():
    """Aqui troca a imagem"""

    # Unfortunately, Pygame's font & text system only shows one line at
    # a time, so we can't use strings with \n newline characters in them.
    # So we will use a list with each line in it.
    instructionText = ['Vamos brincar com Matematica!'
                       ]

    # Start with drawing a blank color to the entire window:
    DISPLAYSURF.fill(BGCOLOR)
    right = 0

    # Position and draw the text.
    for i in range(len(instructionText)):
        instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()
        right += 100  # 10 pixels will go in between each line of text.
        instRect.left = right
        #instRect.centerx = THIRD_WINWIDTH
#        topCoord += 30 # Adjust for the height of the line.
        DISPLAYSURF.blit(instSurf, instRect)


    while True:  # Main loop for the start screen.
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_n:
                    line = readCard()
                return  # user has pressed a key, so return.

        # Display the DISPLAYSURF contents to the actual screen.
        pygame.display.update()
        FPSCLOCK.tick()

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
