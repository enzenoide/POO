from models.dao import DAO
import json

class CupomDesconto:
    def __init__(self, id, codigo, porcentagem):
        self.set_id(id)
        self.set_codigo(codigo)
        self.set_porcentagem(porcentagem)

    
    def get_id(self):
        return self.__id

    def get_codigo(self):
        return self.__codigo

    def get_porcentagem(self):
        return self.__porcentagem

    
    def set_id(self, id):
        if id is None:
            self.__id = 0 
            return
        self.__id = int(id)

    def set_codigo(self, codigo):
        if not codigo or codigo.strip() == "":
            raise ValueError("Código inválido")
        self.__codigo = codigo.upper()

    def set_porcentagem(self, porcentagem):
        if porcentagem <= 0 or porcentagem > 100:
            raise ValueError("Porcentagem inválida")
        self.__porcentagem = porcentagem

    
    def to_json(self):
        return {"id": self.get_id(),"codigo": self.get_codigo(),"porcentagem": self.get_porcentagem()}

    @staticmethod
    def from_json(dic):
        return CupomDesconto(dic["id"],dic["codigo"],dic["porcentagem"])
    def __str__(self):
        return f"ID: {self.get_id()}, Nome: {self.get_codigo()}"

class CupomDescontoDAO(DAO):
    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("json/cupom.json", "r") as arquivo:
                for dic in json.load(arquivo):
                    cls.objetos.append(CupomDesconto.from_json(dic))
        except:
            pass

    @classmethod
    def salvar(cls):
        with open("json/cupom.json", "w") as arquivo:
            json.dump(
                [c.to_json() for c in cls.objetos],
                arquivo,
                indent=4
            )

    @classmethod
    def listar_por_codigo(cls, codigo):
        for cupom in cls.objetos:
            if cupom.get_codigo() == codigo.upper():
                return cupom
        return None
