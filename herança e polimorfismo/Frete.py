class Frete:
    def __init__(self,d,p):
        self.__d = d
        self.__p = p
    def get_distancia(self):
        return self.__d
    def get_peso(self):
        return self.__p
    
    def set_distancia(self,d):
        self.__d = d
    def set_peso(self,p):
        self.__p = p
    
    def ValorFrete(self):
        return 0.01 *(self.get_peso() * self.get_distancia())
    def __str__(self):
        return (f"Frete Comum - Distância {self.get_distancia()}km, Peso: {self.get_peso()}kg, Valor: R$ {self.ValorFrete():.2f}")
class FreteExpresso(Frete):
    def __init__(self, d, p, s):
        super().__init__(d, p)
        self.__s = s
    def ValorFrete(self):
        return (super().ValorFrete() * 2)+ self.__s * 0.01
    def __str__(self):
        return (f"Frete Expresso - Seguro: R$ {self.__s:.2f} Valor Total: R$ {self.ValorFrete():.2f}")
f1 = Frete(10,2)
f2 = FreteExpresso(10,2,400)
print(f1)
print(f2)
