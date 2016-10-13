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
from pygame import mixer

mixer.init()
game_music = mixer.Sound("letyourbodymove.ogg")

BOTAO_AVANCAR = USEREVENT + 1
BOTAO_SAIR = USEREVENT + 2
BOTAO_RETORNAR = USEREVENT + 3
CARD = USEREVENT + 1

CARDSDICT = {
    'Card UID: 64 35 15 B8': '2',
    'Card UID: 5A 43 06 4C': '3',
    'Card UID: 86 20 48 49': '+',
    'Card UID: 06 DA 3E 49': '5',
    'Card UID: 8A 7D 0F 64': '6',
    'Card UID: 66 82 4A 49': '8',
    'Card UID: 3A 17 FF 4B': '9',
    'Card UID: 8A 5D 0F 64': '7',
    'Card UID: 66 DE 2B 49': '4',
    'Card UID: CA 94 10 64': '=',
    'Card UID: 86 D4 31 3B': '*',
    }

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
                event_type = USEREVENT
                if value == "botao_avancar":
                    event_type = BOTAO_AVANCAR
                if value == "botao_sair":
                    event_type = BOTAO_SAIR
                if value == "botao_retornar":
                    event_type = BOTAO_RETORNAR
                elif 'Card' in value:
                    event_type = CARD

                event = pygame.event.Event(event_type, code = value)
                pygame.event.post(event)
                print("raised event_type = " + str(event_type) + " code = " + value)

FPS = 30
WINWIDTH = 700
WINHEIGHT = 600
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

# The total width and height of each tile in pixels.
TILEWIDTH = 50
TILEHEIGHT = 85
TILEFLOORHEIGHT = 40

PINK = (220, 20, 60)
WHITE = (255, 255, 255)
BGCOLOR = PINK
TEXTCOLOR = WHITE


def main():
    global FPSCLOCK, DISPLAYSURF, IMAGESDICT, TILEMAPPING, OUTSIDEDECOMAPPING, BASICFONT, PLAYERIMAGES, currentImage, game_music

    pygame.init()
    pygame.font.init()
    FPSCLOCK = pygame.time.Clock()

    SerialThread().start()

    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

    pygame.display.set_caption("Brincando com Matemática")
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    IMAGESDICT = {
        'title': pygame.image.load('bcm_title.png'),
        'resolvido': pygame.image.load('resolvido.png'),
        'desafio': pygame.image.load('ORDEM.png'),
        'incorreto': pygame.image.load('TEM_CERTEZA.png')}

    startScreen()  # show the title screen until the user presses a key


def startScreen():
    titleRect = IMAGESDICT['title'].get_rect()
    topCoord = 50  # topCoord tracks where to position the top of the text
    titleRect.top = topCoord
    titleRect.centerx = HALF_WINWIDTH
    topCoord += titleRect.height

    game_music.play()
    instructionText = ['Aprenda Matematica de um jeito mais divertido!']

    DISPLAYSURF.fill(BGCOLOR)

    DISPLAYSURF.blit(IMAGESDICT['title'], titleRect)

    for i in range(len(instructionText)):
        instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()
        topCoord += 5  # 10 pixels will go in between each line of text.
        instRect.top = topCoord
        instRect.centerx = HALF_WINWIDTH
        topCoord += instRect.height  # Adjust for the height of the line.
        DISPLAYSURF.blit(instSurf, instRect)

    while True:  # Main loop for the start screen.
        for event in pygame.event.get():
            if event.type == BOTAO_SAIR:
                terminate()
            elif event.type == BOTAO_AVANCAR:
                #if event.key == K_SPACE:
                    mainScreen()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()

        pygame.display.update()
        FPSCLOCK.tick()


def mainScreen():
    #Tela que lerá os cartões
    DISPLAYSURF.fill(BGCOLOR)
    LISTA_NUMEROS = []
    myfont = pygame.font.SysFont('freesansbold.ttf', 45)

    instructionText = myfont.render('Vamos brincar com Matematica!', 1, (WHITE))
    DISPLAYSURF.blit(instructionText, (50, 0))

    x = 20
    y = 60

    while True:  # Main loop for the start screen.
        for event in pygame.event.get():
            if event.type == BOTAO_SAIR:
                terminate()
            elif event.type == CARD:
                key = event.code
                value = CARDSDICT[key]
                LISTA_NUMEROS.append(value)
                label = myfont.render(CARDSDICT[key], 1, (255,255,255))
                DISPLAYSURF.blit(label, (x,y))
                x = x + 100
                if len(LISTA_NUMEROS) == 5:
                    resultado_calculate = calculate(LISTA_NUMEROS)
                    if resultado_calculate:
                        pygame.display.blit(IMAGESDICT['resolvido'], (0,0))
                        pygame.display.flip()
                    else:
                        pygame.display.blit(IMAGESDICT['incorreto'], (0,0))
                        pygame.display.flip()
                    LISTA_NUMEROS = []
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == BOTAO_RETORNAR:
                    mainScreen()
                return  # user has pressed a key, so return.

        pygame.display.update()
        FPSCLOCK.tick()

def calculate(LISTA_NUMEROS):

    num_1 = int(LISTA_NUMEROS[0])
    operacao = LISTA_NUMEROS[1]
    num_2 = int(LISTA_NUMEROS[2])
    resultado = int(LISTA_NUMEROS[4])
    resultado_certo = 0

    if operacao == '+':
        resultado_certo = num_1 + num_2
    elif operacao == '-':
        resultado_certo = num_1 - num_2
    elif operacao == '*':
        resultado_certo = num_1 * num_2
    elif operacao == '/':
        resultado_certo = num_1 / num_2

    if resultado_certo == resultado:
        return True
    else:
        return False


def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
