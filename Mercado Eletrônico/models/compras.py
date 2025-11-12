import json

class Compras:
    def __init__(self, email, senha, id):
        self.set_id(id)
        self.set_email(email)
        self.set_senha(senha)

    def get_id(self):
        return self.__id
    def get_email(self):
        return self.__email
    def get_senha(self):
        return self.__senha

    def set_id(self, id):
        self.__id = id
    def set_email(self, email):
        self.__email = email
    def set_senha(self, senha):
        self.__senha = senha

    def __str__(self):
        return f"E-mail: {self.get_email()} Senha: *****"

class ComprasDAO:
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
            with open("Compras.json", "r") as arquivo:
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    c = Compras(dic["email"], dic["senha"], dic.get("id", 0))
                    cls.objetos.append(c)
        except:
            pass

    @classmethod
    def salvar(cls):
        with open("Compras.json", "w") as arquivo:
            json.dump(
                [{"id": c.get_id(), "email": c.get_email(), "senha": c.get_senha()} for c in cls.objetos],
                arquivo, indent=4
            )