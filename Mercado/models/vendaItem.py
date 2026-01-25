from .produto import ProdutoDAO  
import json
from models.dao import DAO
class VendaItem:
    def __init__(self, id, qtd, preco, idvenda, idproduto):
        self.set_id(id)
        self.set_qtd(qtd)
        self.set_preco(preco)
        self.set_idvenda(idvenda)
        self.set_idproduto(idproduto)

    def get_id(self):
        return self.__id
    def get_qtd(self):
        return self.__qtd
    def get_preco(self):
        return self.__preco
    def get_idvenda(self):
        return self.__idvenda
    def get_idproduto(self):
        return self.__idproduto

    def set_id(self, id):
        self.__id = id
    def set_qtd(self, qtd):
        self.__qtd = qtd
    def set_preco(self, preco):
        self.__preco = preco
    def set_idvenda(self, idvenda):
        self.__idvenda = idvenda
    def set_idproduto(self, idproduto):
        self.__idproduto = int(idproduto)

    def __str__(self):
        return f"Item ID: {self.get_id()} | Prod ID: {self.get_idproduto()} | Qtd: {self.get_qtd()} | Preço: R${self.get_preco():.2f}"
    def to_json(self):
        return { "id" : self.get_id(), "qtd" : self.get_qtd(), "preco" : self.get_preco(), "idvenda" : self.get_idvenda(), "idproduto" : self.get_idproduto() }

    @staticmethod
    def from_json(dic):
        return VendaItem(dic["id"], dic["qtd"], dic["preco"], dic["idvenda"], dic["idproduto"])
class VendaitemDAO(DAO):
    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("json/vendaitens.json", "r") as arquivo:
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    c = VendaItem(dic["id"], dic["qtd"], dic["preco"], dic["idvenda"], dic["idproduto"])
                    cls.objetos.append(c)
        except:
            pass

    @classmethod
    def salvar(cls):
        dados = []
        for v in cls.objetos:
           
            produto = ProdutoDAO.listar_id(str(v.get_idproduto()))

            
            descricao = produto.get_descricao() if produto else "Produto não encontrado"
            
            print(f"VendaitemDAO.salvar: Gravando item {v.get_idproduto()}. Descrição: '{descricao}'")
           
            dados.append({
                "id": v.get_id(),
                "qtd": v.get_qtd(),
                "preco": v.get_preco(),
                "idvenda": v.get_idvenda(),
                "idproduto": v.get_idproduto(),
                "descricao_produto": descricao
            })

        with open("json/vendaitens.json", "w") as arquivo:
            json.dump(dados, arquivo, indent=4)
    @classmethod
    def listar_por_venda(cls, idvenda):
        cls.abrir()
        itens_venda = []
        for obj in cls.objetos:
            if obj.get_idvenda() == idvenda:
                item_dic = obj.to_json()
                produto = ProdutoDAO.listar_id(obj.get_idproduto())
                descricao = produto.get_descricao() if produto else "Produto não encontrado"
                url_imagem = produto.get_imagem() if produto else "assets/nao_encontrado.png"
                item_dic["descricao_produto"] = descricao
                item_dic["url_imagem"] = url_imagem
                itens_venda.append(item_dic) 
        return itens_venda