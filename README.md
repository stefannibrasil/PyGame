# PyGame

Jogo desenvolvido para o Projeto de Iniciação Científica da linha de pesquisa em Tecnologia Aplicada à Educação usando Hardware e Software livres.

## Como rodar o jogo

### Arduino

Baixe as bibliotecas [MFRC522](https://github.com/miguelbalboa/rfid) e [Button.h](https://playground.arduino.cc/Code/Button). Para adicioná-las, vá em Sketch > Include library > ADD zip library. Depois compile normalmente. No repositório da biblioteca MFRC522 você encontra os pinos para ligar o leitor RFID ao Arduino.


Caso dê algum erro de compilação relacionado à biblioteca Button.h, dê uma olhada [aqui](http://labdegaragem.com/forum/topics/wprogram-h)

Na IDE do Arduino, abra o arquivo `LeitorRFID.ino`. Para saber se está funcionando, teste o código com alguma peça abrindo o Monitor Serial. Você deve ver o Arduino lendo normalmente os códigos das peças.


### PyGame

Certifique-se de ter a versão 2.7 de Python instalada:

`python -V `

Para rodar o jogo, rode os comandos:

`sudo pip install serial`

`sudo pip install pygame`


Dando tudo certo, rode finalmente:

`python BrincandoComMatematica.py` 

O jogo deve abrir normalmente numa janela. Para finalizar, dê Ctrl + c no terminal ou pressione a tecla 'l' no teclado.