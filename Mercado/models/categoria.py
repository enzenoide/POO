import json

class Categoria:
    def __init__(self, id, descricao):
        self.set_id(id)
        self.set_descricao(descricao)

    def get_id(self):
        return self.__id

    def get_descricao(self):
        return self.__descricao

    def set_id(self, id):
        if id <= 0: raise ValueError("ID não pode ser vazio")
        self.__id = id

    def set_descricao(self, descricao):
        if descricao == "":raise ValueError("Descrição não pode estar vazio.")
        self.__descricao = descricao

    def __str__(self):
        return f"Categoria ID: {self.get_id()} | Descrição: {self.get_descricao()}"

    def to_json(self):
        return { "id" : self.get_id(), "descricao" : self.get_descricao() }

    @staticmethod
    def from_json(dic):
        return Categoria(dic["id"], dic["descricao"])
    
    

class CategoriaDAO:
    objetos = []  # atributo da classe

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
            with open("json/categoria.json", "r") as arquivo:
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    c = Categoria(dic["id"], dic["descricao"])
                    cls.objetos.append(c)
        except:
            pass

    @classmethod
    def salvar(cls):
        with open("json/categoria.json", "w") as arquivo:
            json.dump(
                [{"id": c.get_id(), "descricao": c.get_descricao()} for c in cls.objetos],
                arquivo,
                indent=4
            )