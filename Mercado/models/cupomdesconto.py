from models.dao import DAO
import json
class CupomDesconto:
    def __init__(self,id,idvenda,porcentagem):
        self.set_id(id)
        self.set_idvenda(idvenda)
        self.set_porcentagem(porcentagem)
    def get_id(self):
        return self.__id
    def get_idvenda(self):
        return self.__idvenda 
    def get_porcentagem(self):
        return self.__porcentagem

    def set_id(self,id):
        if id < 0:
            raise ValueError("ID não pode ser negativo")
        else:
            self.__id = id
    def set_idvenda(self,idvenda):
        if idvenda < 0:
                raise ValueError("ID não pode ser negativo")
        else:
            self.__idvenda = idvenda
    def set_porcentagem(self,porcentagem):
        if porcentagem < 0:
            raise ValueError("Porcentagem não pode ser negativo")
        else:
            self.__porcentagem = porcentagem
    def to_json(self):
        return {"id":self.get_id(),"idvenda": self.get_idvenda(), "porcentagem": self.get_porcentagem()}
    @staticmethod
    def from_json(dic):
        return CupomDesconto(dic["id"],dic["idvenda"],dic["porcentagem"])

class CupomDescontoDAO(DAO):
    def abrir(cls):
        cls.objetos = []
        try:
            with open("json/cupom.json", "r") as arquivo:
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    c = CupomDesconto.from_json(dic)
                    cls.objetos.append(c)
          
           
        except Exception as e:
            pass
    @classmethod
    def salvar(cls):
        with open("json/cupom.json", "w") as arquivo:
            json.dump([{
                "id": p.get_id(),
                "idvenda": p.get_idvenda(),
                "porcentagem": p.get_porcentagem()
            } for p in cls.objetos], arquivo, indent=4)