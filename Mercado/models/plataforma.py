import json
from models.dao import DAO
class Plataforma:
    def __init__(self,id,nome):
        self.set_id(id)
        self.set_nome(nome)
    def get_id(self):
        return self.__id
    def get_nome(self):
        return self.__nome
    
    def set_id(self,id):
        if id is None:
            self.__id = 0 
            return
        self.__id = int(id)
    def set_nome(self,nome):
        if nome == "":
            raise ValueError("Nome não pode estar vazio")
        else:
            self.__nome = nome
    def to_json(self):
        return {"id":self.get_id(),"nome":self.get_nome()}
    @staticmethod
    def from_json(dic):
        return Plataforma(dic["id"],dic["nome"])
    def __str__(self):
        return f"ID:{self.get_id()} Nome: {self.get_nome()}"
class PlataformaDAO(DAO):
    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("json/plataforma.json", "r") as arquivo:
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    c = Plataforma.from_json(dic)
                    cls.objetos.append(c)
          
           
        except Exception as e:
            pass
    @classmethod
    def salvar(cls):
        with open("json/plataforma.json", "w") as arquivo:
            json.dump([{
                "id": p.get_id(),
                "nome": p.get_nome()
            } for p in cls.objetos], arquivo, indent=4)