from datetime import datetime
import json
from models.dao import DAO


class Avaliacao:
    def __init__(self, id, idvenda, idcliente, texto, data=None):
        self.set_id(id)
        self.set_idvenda(idvenda)
        self.set_idcliente(idcliente)
        self.set_texto(texto)
        self.set_data(data if data else datetime.now())

    def get_id(self): return self.__id
    def get_idvenda(self): return self.__idvenda
    def get_idcliente(self): return self.__idcliente
    def get_texto(self): return self.__texto
    def get_data(self): return self.__data

    def set_id(self, id):
        self.__id = int(id) if id else 0

    def set_idvenda(self, idvenda):
        if not idvenda:
            raise ValueError("Venda inválida")
        self.__idvenda = idvenda

    def set_idcliente(self, idcliente):
        self.__idcliente = idcliente

    def set_texto(self, texto):
        if not texto.strip():
            raise ValueError("Avaliação não pode estar vazia")
        self.__texto = texto

    def set_data(self, data):
        self.__data = data

    def to_json(self):
        return {
            "id": self.get_id(),
            "idvenda": self.get_idvenda(),
            "idcliente": self.get_idcliente(),
            "texto": self.get_texto(),
            "data": self.get_data().isoformat()
        }

    @staticmethod
    def from_json(dic):
        return Avaliacao(
            dic["id"],
            dic["idvenda"],
            dic["idcliente"],
            dic["texto"],
            datetime.fromisoformat(dic["data"])
        )


class AvaliacaoDAO(DAO):

    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("json/avaliacoes.json", "r") as arq:
                for dic in json.load(arq):
                    cls.objetos.append(Avaliacao.from_json(dic))
        except:
            pass

    @classmethod
    def salvar(cls):
        with open("json/avaliacoes.json", "w") as arq:
            json.dump([a.to_json() for a in cls.objetos], arq, indent=4)

    @classmethod
    def buscar_por_venda(cls, idvenda):
        cls.abrir()
        for a in cls.objetos:
            if a.get_idvenda() == idvenda:
                return a
        return None
