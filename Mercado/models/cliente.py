import json
import models.validacao as validacao
from datetime import datetime
from .carrinho import Carrinho    
from .produto import ProdutoDAO  
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
class ClienteDAO:
    objetos = []

    @classmethod
    def inserir(cls, obj):
        print("DEBUG: Executando ClienteDAO.inserir...")
        cls.abrir()
        max_id = 0
        for aux in cls.objetos:
            if aux.get_id() > max_id: 
                max_id = aux.get_id()
        obj.set_id(max_id + 1)
        cls.objetos.append(obj)
        print(f"DEBUG: Cliente adicionado à lista: {obj.get_nome()} (ID: {obj.get_id()}). Total na lista: {len(cls.objetos)}")
        cls.salvar()
        print("DEBUG: ClienteDAO.salvar chamado.")

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
    def excluir(cls, id):
        aux = cls.listar_id(id)
        if aux is not None:
            if aux.get_email() == "admin":
                print("❌ Não é permitido excluir o administrador!")
                return
            cls.objetos.remove(aux)
            cls.salvar()
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


class Venda:
    def __init__(self, id, data, carrinho, total, idcliente):
        self.set_id(id)
        self.set_data(data)
        self.carrinho = carrinho
        self.set_total(total)
        self.set_idcliente(idcliente)

    def get_id(self):
        return self.__id
    def get_data(self):
        return self.__data
    def get_total(self):
        return self.__total
    def get_idcliente(self):
        return self.__idcliente

    def set_id(self, id):
        self.__id = int(id)
    def set_data(self, data):
        if isinstance(data, str):
            data = datetime.fromisoformat(data)
        if data > datetime.now(): 
            raise ValueError("Data inválida meu mano")
        self.__data = data
    def set_total(self, total):
        self.__total = total
    def set_idcliente(self, idcliente):
        self.__idcliente = idcliente

    def __str__(self):
        return f"Venda ID: {self.get_id()}, Data: {self.get_data()}, Total: R${self.get_total():.2f}, Cliente: {self.get_idcliente()}"
    
    def to_json(self):
        return { "id" : self.get_id(), "data" : self.get_data(), "carrinho" : self.carrinho, "total" : self.get_total(), "idcliente" : self.get_idcliente() }

    @staticmethod
    def from_json(dic):
        return Venda(dic["id"], dic["data"], dic["carrinho"], dic["total"], dic["idcliente"])

class VendaDAO:
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
            with open("json/vendas.json", "r") as arquivo:
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    carrinho_objs = [Carrinho(i["idproduto"], i["qtd"]) for i in dic.get("carrinho", [])]
                    c = Venda(dic["id"], dic["data"], carrinho_objs, dic["total"], dic["idcliente"])

                   
                    if "nome_cliente" in dic:
                        c.nome_cliente = dic["nome_cliente"]

                    cls.objetos.append(c)
        except:
            pass

    @classmethod
    def salvar(cls):
        dados = []

        for v in cls.objetos:
            
            cliente = ClienteDAO.listar_id(v.get_idcliente())
            nome_cliente = cliente.get_nome() if cliente else "Cliente não encontrado"

            itens_carrinho = []
            for item in v.carrinho:
               
                produto = ProdutoDAO.listar_id(item.get_idproduto())
                descricao_produto = produto.get_descricao() if produto else "Produto não encontrado"

                itens_carrinho.append({
                    "idproduto": item.get_idproduto(),
                    "descricao_produto": descricao_produto,
                    "qtd": item.get_qtd()
                })

            dados.append({
                "id": v.get_id(),
                "data": v.get_data().isoformat(),
                "carrinho": itens_carrinho,
                "total": v.get_total(),
                "idcliente": v.get_idcliente(),
                "nome_cliente": nome_cliente
            })

        with open("json/vendas.json", "w") as arquivo:
            json.dump(dados, arquivo, indent=4)