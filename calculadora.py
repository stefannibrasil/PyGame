class Calculator:
    
    @staticmethod     
    def adicao(x, y):
        return x + y
    
    @staticmethod
    def subtracao(x, y):
        return x - y

    @staticmethod
    def multiplicacao(x, y):
        return x * y
    
    @staticmethod
    def divisao(x, y):
        return x / y

    @staticmethod
    def is_op(value):
        operators = ["+", "-", "*", "/"]
        return value in operators

    @staticmethod
    def do_operation(operator, v1, v2):
        print "do operation: " + operator + " " + str(v1) + " " + str(v2)
        operators = {
            "+": Calculator.adicao, 
            "-": Calculator.subtracao, 
            "*": Calculator.multiplicacao, 
            "/": Calculator.divisao
        }
        func = operators.get(operator)

        #print operators.get(operator)

        return func(v1, v2)

    def toString(self):
        return str(self.var1 or 0) + " " + str(self.operacao or 0) + " " + str(self.var2 or 0) + " " + str(self.leu_igual or 0) + " " + str(self.resultado or 0) + " total: " + str(self.total or 0) 

    def __init__(self):
        self.var1 = 0
        self.var2 = 0
        self.total = 0
        self.resultado = 0
        self.fim = False
        self.leu_igual = False
        self.operacao = None

    def receber_tag(self, value):
       # print value
        if value == "fim":
            if self.leu_igual and self.resultado == self.total:
                return True
            else:
                return False
        if self.operacao == None:
            if value.isdigit():
                self.var1 = self.var1 * 10 + int(value)
            elif Calculator.is_op(value):
                self.operacao = value
        elif value == "=":
            self.total = Calculator.do_operation(self.operacao, self.var1, self.var2)
            self.leu_igual = True
        elif self.leu_igual:
            if value.isdigit():
                self.resultado = self.resultado * 10 + int(value)
        else:
            if value.isdigit():
                self.var2 = self.var2 * 10 + int(value)

        #print self.toString()

# calc = Calculator()
# calc.receber_tag("1")
# calc.receber_tag("2")
# calc.receber_tag("+")
# calc.receber_tag("5")
# calc.receber_tag("7")
# calc.receber_tag("=")
# calc.receber_tag("6")
# calc.receber_tag("9")
# calc.receber_tag("fim")
# 
# calc = Calculator()
# calc.receber_tag("2")
# calc.receber_tag("*")
# calc.receber_tag("5")
# calc.receber_tag("=")
# calc.receber_tag("1")
# calc.receber_tag("0")
# calc.receber_tag("fim")
# 
# calc = Calculator()
# calc.receber_tag("150")
# calc.receber_tag("/")
# calc.receber_tag("5")
# calc.receber_tag("=")
# calc.receber_tag("3")
# calc.receber_tag("fim")
