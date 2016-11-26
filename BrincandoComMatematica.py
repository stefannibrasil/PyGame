# -*- coding: utf-8 -*-
#!/usr/bin/python
# -*- coding: ascii -*-

# importanto as bibliotecas necessárias para o funcionamento do jogo
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

# aqui inicializamos o mixer para tocar as músicas
pygame.mixer.init(channels = 4)
os.getcwd()
game_music = mixer.Sound("resources/sounds/flight-master-short.wav")
game_music.play(-1)

# tratando eventos do usuario lidos pelo Arduino
BOTAO_AVANCAR = USEREVENT + 1
BOTAO_SAIR = USEREVENT + 2
BOTAO_RETORNAR = USEREVENT + 3
CARD = USEREVENT + 4

# dicionario das tags RFID
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

# sorteio do level_two para deixar a random_index como variavel global
numeros = [4, 5, 6, 7, 8, 9]
random_index = random.randint(4, len(numeros))
a = randrange(4, len(numeros))
b = randrange(4, len(numeros))

# tamanhos das telas
FPS = 30
WINWIDTH = 1200
WINHEIGHT = 900
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)
TILEWIDTH = 50
TILEHEIGHT = 85
TILEFLOORHEIGHT = 40

PINK = (220, 20, 60)
WHITE = (255, 255, 255)
BGCOLOR = PINK
TEXTCOLOR = WHITE
ACERTOS = 0


def main():
    global FPSCLOCK, DISPLAYSURF, IMAGESDICT, TILEMAPPING, BASICFONT

    pygame.init()
    pygame.font.init()
    FPSCLOCK = pygame.time.Clock()

    SerialThread().start()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

    pygame.display.set_caption("Brincando com Matemática")
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    IMAGESDICT = {
        'title': pygame.image.load('resources/images/bcm_title.png'),
        'resolvido': pygame.image.load('resources/images/resolvido.png'),
        'desafio': pygame.image.load('resources/images/ORDEM.png'),
        'incorreto': pygame.image.load('resources/images/TEM_CERTEZA.png')
    }

    start_screen()  # mainScreen espera o usuario apertar o botao_avancar para chamar a start_screen


def start_screen():
    titleRect = IMAGESDICT['title'].get_rect()
    topCoord = 60  # posiciona o topo do texto
    titleRect.top = topCoord
    titleRect.centerx = HALF_WINWIDTH
    topCoord += titleRect.height

    game_music.set_volume(0.2)
    game_music.play()
    instructionText = ['Aprenda Matematica de um jeito mais divertido!',
                       'Aperte os botoes para jogar']
    play_sound('titulo')
    play_sound('botao_avancar_sound')
    DISPLAYSURF.fill(BGCOLOR)

    DISPLAYSURF.blit(IMAGESDICT['title'], titleRect)

    # posicionando as instrucoes na tela
    for i in range(len(instructionText)):
        instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()
        topCoord += 5  # 10 pixels will go in between each line of text.
        instRect.top = topCoord
        instRect.centerx = HALF_WINWIDTH
        topCoord += instRect.height  # Adjust for the height of the line.
        DISPLAYSURF.blit(instSurf, instRect)

    while True:  # Main loop for the start screen.
        events = pygame.event.get()
        for event in events:
            if event.type == BOTAO_AVANCAR:
                level_one()
            elif event.type == BOTAO_SAIR:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    level_one()
                if event.key == pygame.K_l:
                    terminate()

        pygame.display.update()
        FPSCLOCK.tick()


def level_one(): # Tela que checa resultado da operacao escolhida pelo usuario
    global ACERTOS
    topCoord = 60  # posiciona o topo do texto
    DISPLAYSURF.fill(BGCOLOR)
    LISTA_NUMEROS = []
    myfont = pygame.font.SysFont('freesansbold.ttf', 45)
    instructionText = ['Vamos brincar com Matematica!',
                       'Forme operacoes e veja se seu resultado esta correto']
    play_sound('fase1')
    # posicionando as instrucoes na tela
    for i in range(len(instructionText)):
        instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()
        topCoord += 5  # 10 pixels will go in between each line of text.
        instRect.top = topCoord
        instRect.centerx = HALF_WINWIDTH
        topCoord += instRect.height  # Adjust for the height of the line.
        DISPLAYSURF.blit(instSurf, instRect)

    # variaveis para ajustar os dados na tela
    x = 40
    y = 180

    while True:
        if ACERTOS > 1:
            ACERTOS = 0
            level_two()
        for event in pygame.event.get():
            if event.type == BOTAO_RETORNAR:
                start_screen()
            elif event.type == BOTAO_AVANCAR:
                level_one()
            elif event.type == BOTAO_SAIR:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_l:
                    terminate()
                if event.key == K_n:
                    level_one()
            elif event.type == CARD:
                key = event.code
                value = CARDSDICT[key]
                play_sound(value)
                LISTA_NUMEROS.append(value)
                label = myfont.render(CARDSDICT[key], 1, (255, 255, 255))
                DISPLAYSURF.blit(label, (x, y))
                x = x + 100
                if len(LISTA_NUMEROS) == 5:
                    if check_expression(LISTA_NUMEROS):
                        if calculate(LISTA_NUMEROS):
                            play_sound(value)
                            DISPLAYSURF.fill(BGCOLOR)
                            DISPLAYSURF.blit(IMAGESDICT['resolvido'], (150, 170))
                            play_sound('certo')
                            pygame.display.flip()
                            ACERTOS += 1
                            print(ACERTOS)
                        else:
                            play_sound(value)
                            DISPLAYSURF.fill(BGCOLOR)
                            DISPLAYSURF.blit(IMAGESDICT['incorreto'], (150, 170))
                            play_sound('erro')
                            play_sound('incorreto')
                            pygame.display.flip()
                        LISTA_NUMEROS = []
                    else:
                        instructionText = myfont.render('Expressão mal formada, tente novamente!', 1, (WHITE))
                        play_sound('expressao_mal_formada')
                        DISPLAYSURF.blit(instructionText, (50, 0))
            elif event.type == BOTAO_RETORNAR:
                mainScreen()
                return
        pygame.display.update()
        FPSCLOCK.tick()


def level_two():
    global random_index, ACERTOS
    topCoord = 60  # posiciona o topo do texto
    DISPLAYSURF.fill(BGCOLOR)
    myfont = pygame.font.SysFont('freesansbold.ttf', 45)
    LISTA_NUMEROS = []
    instructionText = ['Como voce consegue chegar no seguinte resultado?',
                       str(random_index)]
    play_sound('fase2')
    play_sound(str(random_index))
    # posicionando as instrucoes na tela
    for i in range(len(instructionText)):
        instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()
        topCoord += 5  # 10 pixels will go in between each line of text.
        instRect.top = topCoord
        instRect.centerx = HALF_WINWIDTH
        topCoord += instRect.height  # Adjust for the height of the line.
        DISPLAYSURF.blit(instSurf, instRect)

    x = 40
    y = 140

    while True:
        if ACERTOS > 1:
           ACERTOS = 0
           level_three()
        for event in pygame.event.get():
            if event.type == BOTAO_RETORNAR:
                start_screen()
            elif event.type == BOTAO_AVANCAR:
                level_two()
            elif event.type == BOTAO_SAIR:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_l:
                    terminate()
                if event.key == K_n:
                    level_two()
            elif event.type == CARD:
                key = event.code
                value = CARDSDICT[key]
                play_sound(value)
                LISTA_NUMEROS.append(value)
                label = myfont.render(CARDSDICT[key], 1, (255, 255, 255))
                DISPLAYSURF.blit(label, (x, y))
                x = x + 100
                if len(LISTA_NUMEROS) == 5:
                    if check_expression(LISTA_NUMEROS):
                        if calculate_op(LISTA_NUMEROS):
                            DISPLAYSURF.fill(BGCOLOR)
                            DISPLAYSURF.blit(IMAGESDICT['resolvido'], (150, 170))
                            play_sound('certo')
                            pygame.display.flip()
                            ACERTOS += 1
                        else:
                            DISPLAYSURF.fill(BGCOLOR)
                            DISPLAYSURF.blit(IMAGESDICT['incorreto'], (150, 170))
                            play_sound('erro')
                            play_sound('incorreto')
                            pygame.display.flip()
                        LISTA_NUMEROS = []
                    else:
                        instructionText = myfont.render('Expressão mal formada, tente novamente!', 1, (WHITE))
                        play_sound('expressao_mal_formada')
                        DISPLAYSURF.blit(instructionText, (50, 0))
            elif event.type == BOTAO_RETORNAR:
                level_one()
                return  # usuario retorna para level_one

        pygame.display.update()
        FPSCLOCK.tick()

def level_three():
    global ACERTOS, a, b
    topCoord = 60  # posiciona o topo do texto
    DISPLAYSURF.fill(BGCOLOR)
    myfont = pygame.font.SysFont('freesansbold.ttf', 45)
    LISTA_NUMEROS = []
    instructionText = ['Qual o valor de x?',
                       'x + str(a) = str(b)']
    play_sound('fase3')
    play_sound('x.mp3')
    play_sound('mais')
    play_sound(str(a))
    play_sound('Igual_a')
    play_sound(str(b))
    
    # posicionando as instrucoes na tela
    for i in range(len(instructionText)):
        instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()
        topCoord += 5  # 10 pixels will go in between each line of text.
        instRect.top = topCoord
        instRect.centerx = HALF_WINWIDTH
        topCoord += instRect.height  # Adjust for the height of the line.
        DISPLAYSURF.blit(instSurf, instRect)

    x = 60
    y = 180

    while True:  # Loop principal para a tela nivel_three
        if ACERTOS > 1:
            start_screen()
        for event in pygame.event.get():
            if event.type == BOTAO_RETORNAR:
                start_screen()
            elif event.type == BOTAO_AVANCAR:
                level_three()
            elif event.type == BOTAO_SAIR:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_l:
                    terminate()
                if event.key == K_n:
                    level_two()
            elif event.type == CARD:
                key = event.code
                value = CARDSDICT[key]
                playSound(value)
                label = myfont.render(CARDSDICT[key], 1, (255,255,255))
                DISPLAYSURF.blit(label, (x,y))
                x = x + 100
                if calculate_equacao(a, b, value):
                    DISPLAYSURF.fill(BGCOLOR)
                    DISPLAYSURF.blit(IMAGESDICT['resolvido'], (150, 170))
                    playSound('certo')
                    pygame.display.flip()
                    ACERTOS += 1
                else:
                    DISPLAYSURF.fill(BGCOLOR)
                    DISPLAYSURF.blit(IMAGESDICT['incorreto'], (150, 170))
                    playSound('erro')
                    playSound('incorreto')
                    pygame.display.flip()
            elif event.type == BOTAO_RETORNAR:
                level_two()
                return

        pygame.display.update()
        FPSCLOCK.tick()

# aqui o jogo verifica se a operacao foi feita na ordem certa
def check_expression(LISTA_NUMEROS):
    return (LISTA_NUMEROS[0].isdigit()
            and (LISTA_NUMEROS[1] == '+' or LISTA_NUMEROS[1] == '*')
            and LISTA_NUMEROS[2].isdigit()
            and LISTA_NUMEROS[4].isdigit()
            and LISTA_NUMEROS[3] == '=')

# esta funcao calcula a operacao do level_one


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

# esta calcula do level_two


def calculate_op(LISTA_NUMEROS):
    num_1 = int(LISTA_NUMEROS[0])
    operacao = LISTA_NUMEROS[1]
    num_2 = int(LISTA_NUMEROS[2])
    resultado = int(LISTA_NUMEROS[4])

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


def calculate_equacao(a, b, value):
    resultado_certo = b - a

    if resultado_certo == value:
        return True
    else:
        return False


# sounds

# dicionario sonoro de instrucoes
INSTRUCTIONSDICT = {
    'titulo': 'BCM.mp3',
    'intro': 'intro.mp3',
    'botao_avancar_sound': 'botao_avancar.mp3',
    'certo': 'aplausos.mp3',
    'erro': 'erro.mp3',
    'incorreto': 'tente_novamente.mp3',
    'expressao_mal_formada': 'Expressao_mal_formada.mp3',
    'fase1': 'fase1.mp3',
    'fase2': 'fase2.mp3',
    'fase3': 'fase3.mp3'
}

# dicionario sonoro dos numeros e operacoes
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
    '*': 'Vezes.mp3',
    'x': 'x.mp3'
}


def play_sound(value):
    if SOUNDSDICT.has_key(value):
        value = SOUNDSDICT[value]
        play(value)
    elif INSTRUCTIONSDICT.has_key(value):
        value = INSTRUCTIONSDICT[value]
        play(value)


# metodo para acessar os arquivos mp3 da pasta
def play(path):
    path = "resources/sounds/" + path
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    pygame.mixer.music.load(canonicalized_path)
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()
    #sound = mixer.Sound(canonicalized_path)
    #channel = mixer.find_channel()
    #channel.queue(sound)


def terminate():
    pygame.quit()
    sys.exit()

# serial reading

class SerialThread (threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)

    def run(self):
        # aqui criamos a thread que permite que a leitura dos cartões ao mesmo
        # tempo em que o jogo esta rodando
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        while 1:
            value = ser.readline().strip()
            if value:
                event_type = USEREVENT
                if value == "botao_avancar":
                    event_type = BOTAO_AVANCAR
                if value == "botao_sair":
                    event_type = BOTAO_SAIR
                if value == "botao_retornar":
                    event_type = BOTAO_RETORNAR
                elif 'Card' in value:
                    event_type = CARD

                event = pygame.event.Event(event_type, code=value)
                pygame.event.post(event)
                print("raised event_type = " +
                      str(event_type) + " code = " + value)


if __name__ == '__main__':
    main()
