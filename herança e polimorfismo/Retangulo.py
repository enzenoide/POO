import math
class Retangulo:
    def __init__(self,b,h):
        self.__h = h
        self.__b = b

    def get_base(self):
        return self.__b
    def get_altura(self):
        return self.__h
        
    def set_base(self,b):
        self.__b = b
    def set_altura(self,h):
        self.__h = h
        
    def CalcArea(self):
        return self.get_altura() * self.get_base()
    def CalcDiagonal(self):
        return math.sqrt((self.get_altura()**2) + (self.get_base()** 2) )
    def __str__(self):
        return f"Base:{self.get_base()},Altura:{self.get_altura()},Área:{self.CalcArea()} e Diagonal:{self.CalcDiagonal()}"
class Quadrado(Retangulo):
    def __init__(self,l):
        super().__init__(l,l)
    def __str__(self):
        return f"Área:{self.CalcArea()} e Diagonal:{self.CalcDiagonal()}"
q = Quadrado(4)
r = Retangulo(4,3)

print(q)
print(r)
