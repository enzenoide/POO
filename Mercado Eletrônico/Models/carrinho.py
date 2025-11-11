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
    def inserir(cls, obj):
        cls.abrir()
        # Se o produto já estiver no carrinho, apenas atualiza a quantidade
        existente = cls.listar_id(obj.get_idproduto())
        if existente:
            existente.set_qtd(existente.get_qtd() + obj.get_qtd())
        else:
            cls.objetos.append(obj)
        cls.salvar()

    @classmethod
    def listar(cls):
        cls.abrir()
        return cls.objetos

    @classmethod
    def listar_id(cls, id):
        cls.abrir()
        for obj in cls.objetos:
            if obj.get_idproduto() == id:
                return obj
        return None    

    @classmethod
    def atualizar(cls, obj):
        aux = cls.listar_id(obj.get_idproduto())
        if aux is not None:
            cls.objetos.remove(aux)
            cls.objetos.append(obj)
            cls.salvar()

    @classmethod
    def excluir(cls, obj):
        aux = cls.listar_id(obj.get_idproduto())
        if aux is not None:
            cls.objetos.remove(aux)
            cls.salvar()

    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("carrinho.json", "r") as arquivo:
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    c = Carrinho(dic["idproduto"], dic["qtd"])
                    cls.objetos.append(c)
        except:
            pass

    @classmethod
    def salvar(cls):
        with open("carrinho.json", "w") as arquivo:
            json.dump([{
                "idproduto": c.get_idproduto(),
                "qtd": c.get_qtd()
            } for c in cls.objetos], arquivo, indent=4)

    @classmethod
    def listar_detalhado(cls):
        cls.abrir()
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
    def limpar(cls):
        cls.objetos = []
        cls.salvar()