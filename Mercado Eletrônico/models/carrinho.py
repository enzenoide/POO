import json
from .produto import ProdutoDAO, Produto

class Carrinho:
    def __init__(self, idproduto, qtd):
        self.set_idproduto(idproduto)
        self.set_qtd(qtd)

    def get_idproduto(self):
        return self.__idproduto
    
    def get_qtd(self):
        return self.__qtd

    def set_idproduto(self, idproduto):
        self.__idproduto = idproduto

    def set_qtd(self, qtd):
        if qtd == "":
            raise ValueError("Digite alguma quantidade")
        self.__qtd = qtd

    def __str__(self):
        return f"ID: {self.get_idproduto()} Quantidade: {self.get_qtd()}"


class CarrinhoDAO:
    objetos = []  

    @classmethod
    def abrir(cls, idcliente):
        filename = f"carrinho_{idcliente}.json"
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
        filename = f"carrinho_{idcliente}.json"
        with open(filename, "w") as arquivo:
            json.dump([{
                "idproduto": c.get_idproduto(),
                "qtd": c.get_qtd()
            } for c in cls.objetos], arquivo, indent=4)

    @classmethod
    def inserir(cls, idcliente, obj):
        cls.abrir(idcliente)

        existente = cls.listar_id(idcliente, obj.get_idproduto())
        if existente:
            existente.set_qtd(existente.get_qtd() + obj.get_qtd())
        else:
            cls.objetos.append(obj)

        cls.salvar(idcliente)

    @classmethod
    def listar(cls, idcliente):
        cls.abrir(idcliente)
        return cls.objetos

    @classmethod
    def listar_id(cls, idcliente, idproduto):
        cls.abrir(idcliente)
        for obj in cls.objetos:
            if obj.get_idproduto() == idproduto:
                return obj
        return None    

    @classmethod
    def atualizar(cls, idcliente, obj):
        cls.abrir(idcliente)

        aux = cls.listar_id(idcliente, obj.get_idproduto())
        if aux is not None:
            cls.objetos.remove(aux)
            cls.objetos.append(obj)
            cls.salvar(idcliente)

    @classmethod
    def excluir(cls, idcliente, idproduto):
        cls.abrir(idcliente)
        aux = cls.listar_id(idcliente, idproduto)
        if aux is not None:
            cls.objetos.remove(aux)
            cls.salvar(idcliente)

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
