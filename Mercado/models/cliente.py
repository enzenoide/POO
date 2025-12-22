import json
import models.validacao as validacao
from datetime import datetime
from .carrinho import Carrinho    
from .produto import ProdutoDAO  
from models.dao import DAO
class Cliente:
    def __init__(self, id, nome, email, fone, senha):
        self.set_id(id)
        self.set_nome(nome)
        self.set_email(email)
        self.set_fone(fone)
        self.set_senha(senha)

    def get_id(self):
        return self.__id
    def get_nome(self):
        return self.__nome
    def get_email(self):
        return self.__email
    def get_fone(self):
        return self.__fone
    def get_senha(self):
        return self.__senha

    def set_id(self, id):
        self.__id = id
    def set_nome(self, nome):
        if nome == "": raise ValueError("Nome não pode estar vazio")
        self.__nome = nome
    def set_email(self, email):
        if not validacao.validar_email(email) and email != "admin":
            raise ValueError("E-mail inválido")
        self.__email = email
    def set_fone(self, fone):
        if not validacao.validar_telefone(fone):
            raise ValueError("Telefone inválido")
        self.__fone = fone
    def set_senha(self, senha):
        if len(senha) < 8: raise ValueError("Senha não pode ter menos de 8 caracteres")
        self.__senha = senha

    def __str__(self):
        return f"Cliente ID: {self.get_id()} | Nome: {self.get_nome()} | Email: {self.get_email()} | Fone: {self.get_fone()}"
    
    def to_json(self):
        return { "id" : self.get_id(), "nome" : self.get_nome(), "email" : self.get_email(), "fone" : self.get_fone(), "senha" : self.get_senha() }

    @staticmethod
    def from_json(dic):
        return Cliente(dic["id"], dic["nome"], dic["email"], dic["fone"], dic["senha"])
class ClienteDAO(DAO):
    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("json/clientes.json", "r") as arquivo:
                lista = json.load(arquivo)
                for dic in lista:
                    c = Cliente.from_json(dic)
                    cls.objetos.append(c)
        except(FileNotFoundError,json.JSONDecodeError):
            pass

    @classmethod
    def salvar(cls):
        print(f"DEBUG: Abrindo 'clientes.json' para escrita. Contagem de objetos: {len(cls.objetos)}")
        try:
            with open("json/clientes.json", "w") as arquivo:
                json.dump([obj.to_json() for obj in cls.objetos], arquivo, indent=4)
                print("DEBUG: Salvamento de 'clientes.json' CONCLUÍDO com sucesso.")
        except Exception as e:
            print(f"ERRO CRÍTICO no ClienteDAO.salvar: {e}")