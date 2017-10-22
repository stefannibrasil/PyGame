# -*- coding: utf-8 -*-
#!/usr/bin/python
# -*- coding: ascii -*-

# importanto as bibliotecas necessárias para o funcionamento do jogo
import random
from random import randrange
from calculator import Calculator
import sys
import copy
import os
import serial
import threading
import pygame
from pygame.locals import *
from pygame import mixer

# aqui inicializamos o mixer para tocar as músicas
pygame.mixer.pre_init(22050, -16, 2, 10000)
pygame.mixer.init()
os.getcwd()
game_music = mixer.Sound("resources/sounds/flight-master-short.wav")
game_music.play(-1)

# tratando eventos do usuario lidos pelo Arduino, como botões e cards
BOTAO_AVANCAR = USEREVENT + 1
BOTAO_SAIR = USEREVENT + 2
BOTAO_RETORNAR = USEREVENT + 3
CARD = USEREVENT + 4

RANDOM_INDEX = 0

# dicionario das tags RFID: para adicionar novas, basta ler os codigos no monitor serial 
# do Arduino e adicionar aqui o codigo com seu respectivo significado
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


# tamanhos das telas
FPS = 30
WINWIDTH = 1200
WINHEIGHT = 900
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)
PINK = (220, 20, 60)
WHITE = (255, 255, 255)
BGCOLOR = PINK
TEXTCOLOR = WHITE

#variavel global para as fases
ACERTOS = 0


def main():
    global FPSCLOCK, DISPLAYSURF, IMAGESDICT, SOUNDSDICT, TILEMAPPING, BASICFONT

    calculadora = Calculator()
    pygame.init()
    pygame.font.init()
    FPSCLOCK = pygame.time.Clock()

    SerialThread().start()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

    pygame.display.set_caption("Brincando com Matemática")
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    #dicionario de imagens
    IMAGESDICT = {
        'title': pygame.image.load('resources/images/bcm_title.png'),
        'resolvido': pygame.image.load('resources/images/resolvido.png'),
        'desafio': pygame.image.load('resources/images/ORDEM.png'),
        'incorreto': pygame.image.load('resources/images/TEM_CERTEZA.png')
    }

    # dicionario de sons: usar arquivos com formato .wav
    SOUNDSDICT = {
        'titulo':                sound_init('BCM.wav'),
        'intro':                 sound_init('intro.wav'),
        'botao_avancar_sound':   sound_init('botao_avancar.wav'),
        'certo':                 sound_init('aplausos.wav'),
        'erro':                  sound_init('erro.wav'),
        'incorreto':             sound_init('tente_novamente.wav'),
        'expressao_mal_formada': sound_init('Expressao_mal_formada.wav'),
        'fase1':                 sound_init('fase1.wav'),
        'fase2':                 sound_init('fase2.wav'),
        'fase3':                 sound_init('fase3.wav'),
        '1':                     sound_init('Número_1.wav'),
        '2':                     sound_init('Número_2.wav'),
        '3':                     sound_init('Número_3.wav'),
        '4':                     sound_init('Número_4.wav'),
        '5':                     sound_init('Número_5.wav'),
        '6':                     sound_init('Número_6.wav'),
        '7':                     sound_init('Número_7.wav'),
        '8':                     sound_init('Número_8.wav'),
        '9':                     sound_init('Número_9.wav'),
        '=':                     sound_init('Igual_a.wav'),
        '+':                     sound_init('Mais.wav'),
        '*':                     sound_init('Vezes.wav'),
        'x':                     sound_init('x.wav')
    }

    start_screen()  # mainScreen espera o usuario apertar o botao_avancar para chamar a start_screen


def start_screen():
    titleRect = IMAGESDICT['title'].get_rect()
    topCoord = 60  # posiciona o topo do texto
    titleRect.top = topCoord
    titleRect.centerx = HALF_WINWIDTH
    topCoord += titleRect.height

    game_music.set_volume(0.2)
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
        topCoord += 5  
        instRect.top = topCoord
        instRect.centerx = HALF_WINWIDTH
        topCoord += instRect.height  
        DISPLAYSURF.blit(instSurf, instRect)

    while True:  # Main loop for the start screen.
        for event in pygame.event.get():
            if event.type == BOTAO_SAIR:
                terminate()
            if event.type == BOTAO_AVANCAR:
                level_one()
            elif event.type == BOTAO_SAIR:
                terminate()
            #enquanto os botoões nao estão funcionando, usamos teclas normais:
            # tecla 'n' para avancar e l para fechar o jogo
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    level_one()
                if event.key == pygame.K_l:
                    terminate()

        pygame.display.update()
        FPSCLOCK.tick()


def level_one():  # Tela que checa resultado da operacao escolhida pelo usuario
    global ACERTOS
    topCoord = 60  # posiciona o topo do texto
    DISPLAYSURF.fill(BGCOLOR)
    LISTA_EXPRESSAO = []
    myfont = pygame.font.SysFont('freesansbold.ttf', 60)
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
            play_sound('certo')
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
                print "oi"
                calculadora.receber_tag(value)
                play_sound(value)
                LISTA_EXPRESSAO.append(value)
                label = myfont.render(CARDSDICT[key], 1, (255, 255, 255))
                DISPLAYSURF.blit(label, (x, y))
                x = x + 100
                if len(LISTA_EXPRESSAO) == 5:
                    if check_expression(LISTA_EXPRESSAO):
                        if calculate(LISTA_EXPRESSAO):
                            play_sound(value)
                            DISPLAYSURF.fill(BGCOLOR)
                            DISPLAYSURF.blit(IMAGESDICT['resolvido'], (150, 170))
                            play_sound('certo')
                            pygame.display.flip()
                            ACERTOS = ACERTOS + 1
                            print(ACERTOS)
                            ACERTOS += 1
                        else:
                            play_sound(value)
                            DISPLAYSURF.fill(BGCOLOR)
                            DISPLAYSURF.blit(IMAGESDICT['incorreto'], (150, 170))
                            play_sound('erro')
                            play_sound('incorreto')
                            pygame.display.flip()
                        LISTA_EXPRESSAO = []
                    else:
                        instructionText = myfont.render(
                            'Expressão mal formada, tente novamente!', 1, (WHITE))
                        play_sound('expressao_mal_formada')
                        DISPLAYSURF.blit(instructionText, (50, 0))
            elif event.type == BOTAO_RETORNAR:
                mainScreen()
                return

        pygame.display.update()
        FPSCLOCK.tick()


def level_two():
    global RANDOM_INDEX, ACERTOS
    topCoord = 60  # posiciona o topo do texto
    DISPLAYSURF.fill(BGCOLOR)
    myfont = pygame.font.SysFont('freesansbold.ttf', 45)
    LISTA_EXPRESSAO = []

    RANDOM_INDEX = choose_number(2, 9)
    instructionText = ['Com quais operacoes voce consegue chegar nesse resultado?',
                       str(RANDOM_INDEX)]
    play_sound('fase2')
    play_sound(str(RANDOM_INDEX))

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
        if ACERTOS > 2:
           play_sound('certo')
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
                    print("l")
                if event.key == K_n:
                    level_two()
                    print("n")
            elif event.type == CARD:
                key = event.code
                value = CARDSDICT[key]
                play_sound(value)
                LISTA_EXPRESSAO.append(value)
                label = myfont.render(CARDSDICT[key], 1, (255, 255, 255))
                DISPLAYSURF.blit(label, (x, y))
                x = x + 100
                if len(LISTA_EXPRESSAO) == 5:
                    if check_expression(LISTA_EXPRESSAO):
                        if calculate_op(LISTA_EXPRESSAO):
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
                        LISTA_EXPRESSAO = []
                    else:
                        instructionText = myfont.render(
                            'Expressao mal formada, tente novamente!', 1, (WHITE))
                        play_sound('expressao_mal_formada')
                        DISPLAYSURF.blit(instructionText, (50, 0))
            elif event.type == BOTAO_RETORNAR:
                level_one()
                return  # usuario retorna para level_one

        pygame.display.update()
        FPSCLOCK.tick()

def level_three():
    global ACERTOS, a, b
    DISPLAYSURF.fill(BGCOLOR)
    myfont = pygame.font.SysFont('freesansbold.ttf', 45)
    LISTA_EXPRESSAO = []
    instrucao_1 = myfont.render('Qual o valor de x?', 1, WHITE)

    a = choose_number(2, 8)
    b = choose_number(a+1, 9)

    DISPLAYSURF.blit(instrucao_1, (60, 120))
    instructionText = myfont.render('x + ' + str(a) + ' = ' + str(b), 1, WHITE)
    DISPLAYSURF.blit(instructionText, (150, 160))
    play_sound('fase3')
    play_sound('x')
    play_sound('+')
    play_sound(str(a))
    play_sound('=')
    play_sound(str(b))


    x = 60
    y = 180

    while True:  # Loop principal para a tela nivel_three
        if ACERTOS > 2:
            play_sound('certo')
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
                    level_three()
            elif event.type == CARD:
                key = event.code
                value = CARDSDICT[key]
                play_sound(value)
                label = myfont.render(CARDSDICT[key], 1, (255,255,255))
                DISPLAYSURF.blit(label, (x,y))
                x = x + 100
                if calculate_equacao(a, b, value):
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
            elif event.type == BOTAO_RETORNAR:
                level_two()
                return

        pygame.display.update()
        FPSCLOCK.tick()

# aqui o jogo verifica se a operacao foi feita na ordem certa
def check_expression(LISTA_EXPRESSAO):
    return (LISTA_EXPRESSAO[0].isdigit()
            and (LISTA_EXPRESSAO[1] == '+' or LISTA_EXPRESSAO[1] == '*')
            and LISTA_EXPRESSAO[2].isdigit()
            and LISTA_EXPRESSAO[4].isdigit()
            and LISTA_EXPRESSAO[3] == '=')

# esta funcao calcula a operacao do level_one


def calculate(LISTA_EXPRESSAO):
    num_1 = int(LISTA_EXPRESSAO[0])
    operacao = LISTA_EXPRESSAO[1]
    num_2 = int(LISTA_EXPRESSAO[2])
    resultado = int(LISTA_EXPRESSAO[4])
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


def calculate_op(LISTA_EXPRESSAO):
    num_1 = int(LISTA_EXPRESSAO[0])
    operacao = LISTA_EXPRESSAO[1]
    num_2 = int(LISTA_EXPRESSAO[2])
    resultado = int(LISTA_EXPRESSAO[4])

    resultado = RANDOM_INDEX
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

def choose_number(start, end):
    return randrange(start, end)

def calculate_equacao(a, b, value):
    resultado_certo = b - a


    print(resultado_certo == int(value))
    if resultado_certo == int(value):
        return True
    else:
        return False


def sound_init(path):
    path = "resources/sounds/" + path
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    sound = mixer.Sound(canonicalized_path)
    return sound

def play_sound(value):
    if SOUNDSDICT.has_key(value):
        sound = SOUNDSDICT[value]
        channel = mixer.Channel(1)
        channel.queue(sound)
        print(value + ' - playing!')
    else:
        print(value + ' - sound not found on sounds dictionary!')


def terminate():
    pygame.quit()
    sys.exit()

# Comunicação entre o Arduino e o código em Python, usando a biblioteca serial e thread
class SerialThread (threading.Thread):

        # aqui criamos a thread que permite que a leitura dos cartões ao mesmo
        # tempo em que o jogo esta rodando
    def __init__(self):
        threading.Thread.__init__(self)
        self.setDaemon(True)

    def run(self):
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
                # printa no console os valores lidos pelo arduino, muito bom para
                print("raised event_type = " +
                      str(event_type) + " code = " + value)


if __name__ == '__main__':
    main()
