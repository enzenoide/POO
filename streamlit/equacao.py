import math

class Equacao:
    def __init__(self, a, b, c):
        self.__a = float(a)
        self.__b = float(b)
        self.__c = float(c)

    def getA(self):
        return self.__a

    def getB(self):
        return self.__b

    def getC(self):
        return self.__c
    
    def setA(self, a):
        self.__a = float(a)

    def setB(self, b):
        self.__b = float(b)

    def setC(self, c):
        self.__c = float(c)
    
    def Delta(self):
        return self.__b**2 - 4 * self.__a * self.__c

    # Valor de y
    def Y(self, x):
        return self.__a * x**2 + self.__b * x + self.__c

    # Raiz 1
    def X1(self):
        d = self.Delta()
        if d < 0:
            return None
        return (-self.__b + math.sqrt(d)) / (2 * self.__a)

    # Raiz 2
    def X2(self):
        d = self.Delta()
        if d < 0:
            return None
        return (-self.__b - math.sqrt(d)) / (2 * self.__a)

    # Representação da equação
    def __str__(self):
        d = self.Delta()
        x1 = self.X1()
        x2 = self.X2()

        if d < 0:
            return f"Delta = {d} (não possui raízes reais)"
        else:
            return f"Delta = {d}, x1 = {x1}, x2 = {x2}"