# -*- coding: utf-8 -*-
#!/usr/bin/python
# -*- coding: ascii -*-
import random
import sys
import copy
import os
import serial
import threading
import pygame
from pygame.locals import *

BOTAO_NEXT = USEREVENT
CARD = BOTAO_NEXT + 1

class SerialThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)
    def run (self):
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 0)
        while 1 :
            value = ser.readline().strip()
            if value:
                print(value)
                event_type = ''
                if value == "botao_next":
                    event_type = BOTAO_NEXT
                elif 'Card' in value:
                    event_type = CARD

                event = pygame.event.Event(event_type, code = value)
                pygame.event.post(event)
                print("raised event_type=" + str(event_type) + " code = " + value)

FPS = 30
WINWIDTH = 700
WINHEIGHT = 500
WINWIDTH = 900
WINHEIGHT = 600
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

#Cartoes
#'64 35 15 B8': '1',
#'86 D4 31 3B': '0'

#botoes
#NEXT = 'next'
#BACK = 'back'
#ENTER = 'enter'
#EXIT = 'exit'

def main():
    global FPSCLOCK, DISPLAYSURF, IMAGESDICT, TILEMAPPING, OUTSIDEDECOMAPPING, BASICFONT, PLAYERIMAGES, currentImage

    pygame.init()
    pygame.mixer.init()
    FPSCLOCK = pygame.time.Clock()

    SerialThread().start()

    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

    pygame.display.set_caption("Brincando com Matemática")
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    IMAGESDICT = {
        'title': pygame.image.load('bcm_title.png')}
        #'resolvido': pygame.image.load('resolvido.png')}

    startScreen()  # show the title screen until the user presses a key


def startScreen():
    titleRect = IMAGESDICT['title'].get_rect()
    topCoord = 50  # topCoord tracks where to position the top of the text
    titleRect.top = topCoord
    titleRect.centerx = HALF_WINWIDTH
    topCoord += titleRect.height

    instructionText = ['Aprenda Matematica de um jeito mais divertido!']

    DISPLAYSURF.fill(BGCOLOR)

    DISPLAYSURF.blit(IMAGESDICT['title'], titleRect)

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
            elif event.type == BOTAO_NEXT:
                mainScreen()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()

        pygame.display.update()
        FPSCLOCK.tick()


def mainScreen():
    #Tela que lerá os cartões

    instructionText = ['Vamos brincar com Matematica!']

    DISPLAYSURF.fill(BGCOLOR)
    right = 0

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
                    mainScreen()
                return  # user has pressed a key, so return.

        pygame.display.update()
        FPSCLOCK.tick()

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
