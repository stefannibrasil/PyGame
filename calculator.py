class Calculator:

    def adicao(x, y):
        x + y

    def subtracao(x, y):
        x - y

    def multiplicacao(x, y):
        x * y

    def divisao(x, y):
        x / y

    var1 = 0
    var2 = 0
    total = 0
    operadores = {"+": adicao, "-": subtracao, "*": multiplicacao, "/": divisao}
    igualdade = "="
    resultado = 0
    fim = False
    leu_igual = False
    operacao = None


    def receber_tag(valor):
        print valor
        if operacao == None:
            if value.isdigit():
                var1 = var1 * 10 + valor
            elif operadores.has_key(valor):
                operacao = valor
        elif valor == igualdade:
            total = operadores[operacao](var1, var2)
            leu_igual = True
        elif leu_igual:
            if value.isdigit():
                resultado = resultado * 10 + valor
        else:
            if value.isdigit():
                var2 = var2 * 10 + valor

        if leu_igual and resultado == total:
            print "Sucesso"
