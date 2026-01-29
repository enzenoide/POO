from datetime import datetime
import json
from models.dao import DAO
class Avaliacao:
    def __init__(self,id,idcliente,idproduto,data,texto):
        self.set_id(id)
        self.set_idcliente(idcliente)
        self.set_idproduto(idproduto)
        self.set_data(data)
        self.set_texto(texto)
    def get_id(self):
        return self.__id
    def get_idcliente(self):
        return self.__idcliente
    def get_idproduto(self):
        return self.__idproduto
    def get_data(self):
        return self.__data
    def get_texto(self):
        return self.__texto
    
    def set_id(self,id):
        if id < 0:
            raise ValueError("Não existe ID negativo")
        else:
            self.__id = id
    def set_idcliente(self,idcliente):
        if idcliente < 0:
            raise ValueError("Não existe ID negativo")
        else:
            self.__idcliente = idcliente
    def set_idproduto(self,idproduto):
        if idproduto < 0:
            raise ValueError("Não existe ID negativo")
        else:
            self.__idproduto = idproduto
    def set_data(self, data):
        if isinstance(data, str):
            data = datetime.fromisoformat(data)
        if data > datetime.now(): 
            raise ValueError("Data inválida meu mano")
    def set_texto(self,texto):
        if texto == "":
            raise ValueError("Texto não pode estar vazio")
        else:
            self.__texto = texto
    def to_json(self):
        return {"id": self.get_id(),"idcliente": self.get_idcliente(),"idproduto": self.get_idproduto(),"data": self.get_data(),"texto": self.get_texto()}
    @staticmethod
    def from_json(dic):
        return Avaliacao(dic["id"],dic["idcliente"],dic["idproduto"],dic["data"],dic["texto"])

class AvaliacaoDAO(DAO):
    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("json/avaliacao.json", "r") as arquivo:
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    c = Avaliacao.from_json(dic)
                    cls.objetos.append(c)
          
           
        except Exception as e:
            pass
    @classmethod
    def salvar(cls):
        with open("json/avaliacao.json", "w") as arquivo:
            json.dump([{
                "id": p.get_id(),
                "icliente": p.get_idcliente(),
                "idproduto": p.get_idproduto(),
                "data": p.get_data(),
                "texto": p.get_texto()
            } for p in cls.objetos], arquivo, indent=4)