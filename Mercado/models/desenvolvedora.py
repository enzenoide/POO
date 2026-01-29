from models.dao import DAO
import json
class Desenvolvedora:
    def __init__(self,id,nome):
        self.set_id(id)
        self.set_nome(nome)
    def get_id(self):
        return self.__id
    def get_nome(self):
        return self.__nome
    
    def set_id(self,id):
        if id < 0:
            raise ValueError("Não existe ID negativo")
        else:
            self.__id = id
    def set_nome(self,nome):
        if nome == "":
            raise ValueError("Nome não pode estar vazio")
    def to_json(self):
        return {"id":self.get_id(),"nome":self.get_nome()}
    @staticmethod
    def from_json(dic):
        return Desenvolvedora(dic["id"],dic["nome"])
class PlataformaDAO(DAO):
    def abrir(cls):
        cls.objetos = []
        try:
            with open("json/desenvolvedora.json", "r") as arquivo:
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    c = Desenvolvedora.from_json(dic)
                    cls.objetos.append(c)
          
           
        except Exception as e:
            pass
    @classmethod
    def salvar(cls):
        with open("json/desenvolvedora.json", "w") as arquivo:
            json.dump([{
                "id": p.get_id(),
                "nome": p.get_nome()
            } for p in cls.objetos], arquivo, indent=4)