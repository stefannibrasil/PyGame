# -*- coding: utf-8 -*-
#!/usr/bin/python
# -*- coding: ascii -*-
import random
from random import randrange
import sys
import copy
import os
import serial
import threading
import pygame
from pygame.locals import *
from pygame import mixer

#sons do jogo
mixer.init()
os.getcwd()
game_music = mixer.Sound("letyourbodymove.ogg")

INSTRUCTIONSDICT = { }

SOUNDSDICT = {
    '1': 'Número_1.mp3',
    '2': 'Número_2.mp3',
    '3': 'Número_3.mp3',
    '4': 'Número_4.mp3',
    '5': 'Número_5.mp3',
    '6': 'Número_6.mp3',
    '7': 'Número_7.mp3',
    '8': 'Número_8.mp3',
    '9': 'Número_9.mp3',
    '=': 'Igual_a.mp3',
    '+': 'Mais.mp3',
    '*': 'Vezes.mp3'
}

#tratando eventos do Arduino
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
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)
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
OUTSIDE_DECORATION_PCT = 20

# The total width and height of each tile in pixels.
TILEWIDTH = 50
TILEHEIGHT = 85
TILEFLOORHEIGHT = 40

PINK = (220, 20, 60)
WHITE = (255, 255, 255)
BGCOLOR = PINK
TEXTCOLOR = WHITE


def main():
    numeros = [2, 3, 4, 5, 6, 7, 8, 9];
    random_index = randrange(0,len(numeros))
    print numeros[random_index]
    global FPSCLOCK, DISPLAYSURF, IMAGESDICT, TILEMAPPING, OUTSIDEDECOMAPPING, BASICFONT, PLAYERIMAGES, game_music, random_index

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
        'incorreto': pygame.image.load('TEM_CERTEZA.png'),
        'princess': pygame.image.load('princess.png'),
        'boy': pygame.image.load('boy.png'),
        'catgirl': pygame.image.load('catgirl.png'),
        'horngirl': pygame.image.load('horngirl.png'),
        'pinkgirl': pygame.image.load('pinkgirl.png')}

    startScreen()  # show the title screen until the user presses a key


def startScreen():
    titleRect = IMAGESDICT['title'].get_rect()
    topCoord = 50  # topCoord tracks where to position the top of the text
    titleRect.top = topCoord
    titleRect.centerx = HALF_WINWIDTH
    topCoord += titleRect.height

    game_music.set_volume(0.3)
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
                level_one()
            elif event.type == K_n:
                level_two()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()

        pygame.display.update()
        FPSCLOCK.tick()


def level_one():
    #Tela que checa resultado da operacao escolhida pelo usuario
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
                playSound(value)
                LISTA_NUMEROS.append(value)
                label = myfont.render(CARDSDICT[key], 1, (255,255,255))
                DISPLAYSURF.blit(label, (x,y))
                x = x + 100
                if len(LISTA_NUMEROS) == 5:
                    if check_expression(LISTA_NUMEROS):
                        if calculate(LISTA_NUMEROS):
                            DISPLAYSURF.fill(BGCOLOR)
                            DISPLAYSURF.blit(IMAGESDICT['resolvido'], (30,50))
                            pygame.display.flip()
                        else:
                            DISPLAYSURF.fill(BGCOLOR)
                            DISPLAYSURF.blit(IMAGESDICT['incorreto'], (30,50))
                            pygame.display.flip()
                        LISTA_NUMEROS = []
                    else:
                        instructionText = myfont.render('Expressão mal formada, tente novamente!', 1, (WHITE))
                        DISPLAYSURF.blit(instructionText, (50, 0))
            elif event.type == BOTAO_RETORNAR:
                mainScreen()
                return  # user has pressed a key, so return.

        pygame.display.update()
        FPSCLOCK.tick()


def level_two():
    DISPLAYSURF.fill(BGCOLOR)
    myfont = pygame.font.SysFont('freesansbold.ttf', 45)
    LISTA_NUMEROS = []
    instructionText = myfont.render('Qual operacao voce consegue chegar no seguinte resultado?', 1, (WHITE))
    instructionText = myfont.render(random_index, 1, (WHITE))
    DISPLAYSURF.blit(instructionText, (50, 0))

    x = 20
    y = 60

    while True:  # Loop principal para a tela atual
        for event in pygame.event.get():
            if event.type == BOTAO_SAIR:
                terminate()
            elif event.type == CARD:
                key = event.code
                value = CARDSDICT[key]
                playSound(value)
                LISTA_NUMEROS.append(value)
                label = myfont.render(CARDSDICT[key], 1, (255,255,255))
                DISPLAYSURF.blit(label, (x,y))
                x = x + 100
                if len(LISTA_NUMEROS) == 5:
                    if check_expression(LISTA_NUMEROS):
                        if calculate_op(LISTA_NUMEROS):
                            DISPLAYSURF.fill(BGCOLOR)
                            DISPLAYSURF.blit(IMAGESDICT['resolvido'], (30,50))
                            pygame.display.flip()
                        else:
                            DISPLAYSURF.fill(BGCOLOR)
                            DISPLAYSURF.blit(IMAGESDICT['incorreto'], (30,50))
                            pygame.display.flip()
                        LISTA_NUMEROS = []
                    else:
                        instructionText = myfont.render('Expressão mal formada, tente novamente!', 1, (WHITE))
                        DISPLAYSURF.blit(instructionText, (50, 0))
            elif event.type == BOTAO_RETORNAR:
                level_one()
                return  # user has pressed a key, so return.

        pygame.display.update()
        FPSCLOCK.tick()

def check_expression(LISTA_NUMEROS):
    return (LISTA_NUMEROS[0].isdigit()
    and (LISTA_NUMEROS[1] == '+' or LISTA_NUMEROS[1] == '*')
    and LISTA_NUMEROS[2].isdigit()
    and LISTA_NUMEROS[4].isdigit()
    and LISTA_NUMEROS[3] == '=')

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


def calculate_op():
    num_1 = int(LISTA_NUMEROS[0])
    operacao = LISTA_NUMEROS[1]
    num_2 = int(LISTA_NUMEROS[2])

    resultado = random_index
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

def playSound(value):
    if SOUNDSDICT.has_key(value):
        value = SOUNDSDICT[value]
        play_sound(value)

def play_sound(path):
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    pygame.mixer.music.load(canonicalized_path)
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()

def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
