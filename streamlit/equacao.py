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
        if a == 0:
            raise ValueError("O A não pode ser igual a 0")
        self.__a = float(a)

    def setB(self, b):
        self.__b = float(b)

    def setC(self, c):
        self.__c = float(c)
    
    def Delta(self):
        return self.getB()**2 - 4 * self.getA() * self.getC()

    def Y(self, x):
        return self.getA() * x**2 + self.getB() * x + self.getC()

    def X1(self):
        d = selfDelta = self.Delta()
        a = self.getA()
        b = self.getB()

        if d < 0:
            return f"{-b / (2*a)} + {math.sqrt(-d) / (2*a)}"
        return (-b + math.sqrt(d)) / (2 * a)

    def X2(self):
        d = self.Delta()
        a = self.getA()
        b = self.getB()

        if d < 0:
            return None
        return (-b - math.sqrt(d)) / (2 * a)

    def __str__(self):
        d = self.Delta()
        x1 = self.X1()
        x2 = self.X2()

        if d < 0:
            return f"Delta = {d} (não possui raízes reais)"
        else:
            return f"Delta = {d}, x1 = {x1}, x2 = {x2}"