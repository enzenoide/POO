from abc import ABC,abstractmethod
import math

class Figura3D(ABC):
    def __init__(self):
        super().__init__()
    @abstractmethod
    def get_volume(self):
        pass
class Esfera(Figura3D):
    def __init__(self,raio):
        super().__init__()
        self.__raio = raio
    def get_volume(self):
        return 4/3 * math.pi * (self.__raio**3)
class Cubo(Figura3D):
    def __init__(self,lado):
        super().__init__()
        self.__lado = lado
    def get_volume(self):
        return self.__lado ** 3
x  = Esfera(10)
y = Cubo(20)
print(x.get_volume())
print(y.get_volume())