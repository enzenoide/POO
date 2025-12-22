
class Funcionario:
        def __init__(self,nome,salario_base) -> None:
            self.__nome = nome
            self._salariobase = salario_base
        def get_nome(self):
            return self.__nome
        def get_salario_base(self):
            return self._salariobase
    
        def __str__(self) -> str:
            return f"{self.get_nome()} recebe {self.get_salario_base()} reais"
class Gerente(Funcionario):
    def __init__(self, nome, salario_base,gratificacao) -> None:
        super().__init__(nome, salario_base)
        self.__gratificacao = gratificacao
    def get_salario_base(self):
        return self._salariobase + self.__gratificacao # sem super, usando protected. Com super pode usar SEM protected
        #return super().get_salario() + self.__gratificacao
x = Gerente("Henze",1000,500)
y = Funcionario("Alan",1000)
print(x)
print(y)
        