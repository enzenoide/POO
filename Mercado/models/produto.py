import json

class Produto:
    def __init__(self, id, descricao, preco, estoque, idcategoria):
        self.set_id(id)
        self.set_descricao(descricao)
        self.set_preco(preco)
        self.set_estoque(estoque)
        self.set_idcategoria(idcategoria)

    def get_id(self):
        return self.__id
    def get_descricao(self):
        return self.__descricao
    def get_preco(self):
        return self.__preco
    def get_estoque(self):
        return self.__estoque
    def get_idcategoria(self):
        return self.__idcategoria

    def set_id(self, id):
        self.__id = id
    def set_descricao(self, descricao):
        if descricao == "": raise ValueError("Tem que possuir descrição")
        self.__descricao = descricao
    def set_preco(self, preco):
        preco = float(preco)
        if preco <= 0: raise ValueError("O produto precisa possuir preço")
        self.__preco = preco
    def set_estoque(self, estoque):
        estoque = int(estoque)
        if estoque < 0: raise ValueError("O estoque precisa conter algum valor")
        self.__estoque = estoque
    def set_idcategoria(self, idcategoria):
        self.__idcategoria = idcategoria

    def __str__(self):
        return f"Produto ID: {self.get_id()} | Descrição: {self.get_descricao()} | Preço: R${self.get_preco():.2f} | Estoque: {self.get_estoque()} | Categoria ID: {self.get_idcategoria()}"

class ProdutoDAO:
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
            if int(obj.get_id()) == int(id):
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
            with open("produto.json", "r") as arquivo:
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    c = Produto(int(dic["id"]), dic["descricao"], float(dic["preco"]), int(dic["estoque"]), int(dic["idcategoria"]))
                    cls.objetos.append(c)
        except:
            pass

    @classmethod
    def salvar(cls):
        with open("produto.json", "w") as arquivo:
            json.dump([{
                "id": p.get_id(),
                "descricao": p.get_descricao(),
                "preco": p.get_preco(),
                "estoque": p.get_estoque(),
                "idcategoria": p.get_idcategoria()
            } for p in cls.objetos], arquivo, indent=4)

    @classmethod
    def reajustar(cls, percentual):
        for obj in cls.objetos:
            novo_preco = obj.get_preco() + (obj.get_preco() * (percentual / 100))
            obj.set_preco(novo_preco)
            cls.atualizar(obj)
    @classmethod
    def buscar(cls, id):
        produtos = cls.listar()
        for p in produtos:
            if p.get_id() == id:
                return p
        return None