import json
from models.dao import DAO
class Categoria:
    def __init__(self, id, descricao):
        self.set_id(id)
        self.set_descricao(descricao)

    def get_id(self):
        return self.__id

    def get_descricao(self):
        return self.__descricao

    def set_id(self, id):
        self.__id = id

    def set_descricao(self, descricao):
        if descricao == "":raise ValueError("Descrição não pode estar vazio.")
        self.__descricao = descricao

    def __str__(self):
        return f"Categoria ID: {self.get_id()} | Descrição: {self.get_descricao()}"

    def to_json(self):
        return { "id" : self.get_id(), "descricao" : self.get_descricao() }

    @staticmethod
    def from_json(dic):
        return Categoria(dic["id"], dic["descricao"])
    
    

class CategoriaDAO(DAO):
    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("json/categoria.json", "r") as arquivo:
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    c = Categoria(dic["id"], dic["descricao"])
                    cls.objetos.append(c)
        except:
            pass

    @classmethod
    def salvar(cls):
        with open("json/categoria.json", "w") as arquivo:
            json.dump(
                [{"id": c.get_id(), "descricao": c.get_descricao()} for c in cls.objetos],
                arquivo,
                indent=4
            )