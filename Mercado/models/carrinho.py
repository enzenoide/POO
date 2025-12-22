import json
from models.produto import ProdutoDAO, Produto
from models.dao import DAO

class Carrinho:
    def __init__(self, idproduto, qtd):
        self.set_idproduto(idproduto)
        self.set_qtd(qtd)
    def get_idproduto(self):
        return self.__idproduto
    
    def get_qtd(self):
        return self.__qtd

    def set_idproduto(self, idproduto):
        idproduto = int(idproduto)
        if idproduto <= 0: raise ValueError("ID produto inválido")
        self.__idproduto = idproduto

    def set_qtd(self, qtd):
        qtd = int(qtd)
        if qtd <= 0: raise ValueError("Quantidade inválida")
        self.__qtd = int(qtd)

    def __str__(self):
        return f"ID: {self.get_idproduto()} Quantidade: {self.get_qtd()}"
    
    def to_json(self):
        return { "idproduto" : self.get_idproduto(),"qtd": self.get_qtd()}

    @staticmethod
    def from_json(dic):
        return Carrinho(dic["idproduto"], dic["qtd"])


class CarrinhoDAO(DAO):
    @classmethod
    def abrir(cls, idcliente):
        filename = f"json/carrinho_{idcliente}.json"
        cls.objetos = []
        try:
            with open(filename, "r") as arquivo:
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    cls.objetos.append(Carrinho(dic["idproduto"], dic["qtd"]))
        except:
            pass

    @classmethod
    def salvar(cls, idcliente):
        filename = f"json/carrinho_{idcliente}.json"
        with open(filename, "w") as arquivo:
            json.dump([{
                "idproduto": c.get_idproduto(),
                "qtd": c.get_qtd()
            } for c in cls.objetos], arquivo, indent=4)
    @classmethod
    def listar_detalhado(cls, idcliente):
        cls.abrir(idcliente)
        lista_final = []

        for item in cls.objetos:
            produto = ProdutoDAO.listar_id(item.get_idproduto())
            if produto:
                lista_final.append({
                    "id_produto": produto.get_id(),
                    "descricao": produto.get_descricao(),
                    "preco": produto.get_preco(),
                    "quantidade": item.get_qtd(),
                    "total": float(produto.get_preco()) * float(item.get_qtd())
                })
        return lista_final
    @classmethod
    def limpar(cls, idcliente):
        cls.abrir(idcliente)  
        cls.objetos = []      
        cls.salvar(idcliente)