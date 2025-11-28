from .produto import ProdutoDAO  
import json

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
        self.__idproduto = idproduto

    def __str__(self):
        return f"Item ID: {self.get_id()} | Prod ID: {self.get_idproduto()} | Qtd: {self.get_qtd()} | Preço: R${self.get_preco():.2f}"


class VendaitemDAO:
    objetos = []

    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        max_id = 0
        for aux in cls.objetos:
            if aux.get_id() > max_id:
                max_id = aux.get_id()
        obj.set_id(max_id + 1)
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
            if obj.get_id() == id:
                return obj
        return None    

    @classmethod
    def atualizar(cls, obj):
        aux = cls.listar_id(obj.get_id())
        if aux is not None:
            cls.objetos.remove(aux)
            cls.objetos.append(obj)
            cls.salvar()

    @classmethod
    def excluir(cls, obj):
        aux = cls.listar_id(obj.get_id())
        if aux is not None:
            cls.objetos.remove(aux)
            cls.salvar()

    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("vendaitens.json", "r") as arquivo:
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
           
            produto = ProdutoDAO.buscar(v.get_idproduto())

            
            descricao = produto.get_descricao() if produto else "Produto não encontrado"

           
            dados.append({
                "id": v.get_id(),
                "qtd": v.get_qtd(),
                "preco": v.get_preco(),
                "idvenda": v.get_idvenda(),
                "idproduto": v.get_idproduto(),
                "descricao_produto": descricao
            })

        with open("vendaitens.json", "w") as arquivo:
            json.dump(dados, arquivo, indent=4)