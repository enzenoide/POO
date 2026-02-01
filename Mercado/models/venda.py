import json
import models.validacao as validacao
from datetime import datetime
from .carrinho import Carrinho    
from .produto import ProdutoDAO  
from models.dao import DAO
from models.cliente import ClienteDAO
class Venda:
    def __init__(self, id, data, carrinho, total, idcliente,cupomdesconto):
        self.set_id(id)
        self.set_data(data)
        self.carrinho = carrinho
        self.set_total(total)
        self.set_idcliente(idcliente)
        self.set_cupomdesconto(cupomdesconto)

    def get_id(self):
        return self.__id
    def get_data(self):
        return self.__data
    def get_total(self):
        return self.__total
    def get_idcliente(self):
        return self.__idcliente
    def get_cupomdesconto(self):
        return self.__cupomdesconto

    def set_cupomdesconto(self,cupomdesconto):
        if cupomdesconto == "":
            raise ValueError("Cupom não pode estar vazio")
        else:
            self.__cupomdesconto = cupomdesconto
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
        return { "id" : self.get_id(), "data" : self.get_data(), "carrinho" : self.carrinho, "total" : self.get_total(), "idcliente" : self.get_idcliente(),"cupomdesconto": self.get_cupomdesconto() }

    @staticmethod
    def from_json(dic):
        return Venda(dic["id"], dic["data"], dic["carrinho"], dic["total"], dic["idcliente"],dic["cupomdesconto"])

class VendaDAO(DAO):
    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("json/vendas.json", "r") as arquivo:
                for dic in json.load(arquivo):
                    carrinho_objs = [
                        Carrinho(i["idproduto"], i["qtd"])
                        for i in dic.get("carrinho", [])
                    ]

                    venda = Venda(
                        dic["id"],
                        dic["data"],
                        carrinho_objs,
                        dic["total"],
                        dic["idcliente"],
                        dic.get("cupomdesconto")  
                    )

                    cls.objetos.append(venda)
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
                itens_carrinho.append({
                    "idproduto": item.get_idproduto(),
                    "descricao_produto": produto.get_descricao() if produto else "Produto não encontrado",
                    "qtd": item.get_qtd(),
                    "preco": produto.get_preco() if produto else 0.0
                })

            dados.append({
                "id": v.get_id(),
                "data": v.get_data().isoformat(),
                "carrinho": itens_carrinho,
                "total": v.get_total(),
                "idcliente": v.get_idcliente(),
                "cupomdesconto": v.get_cupomdesconto(),  # 🔥 AGORA SALVA
                "nome_cliente": nome_cliente
            })

        with open("json/vendas.json", "w") as arquivo:
            json.dump(dados, arquivo, indent=4)
                
    @classmethod
    def listar_por_cliente(cls, idcliente):
        """Lista todas as vendas de um cliente específico."""
        cls.abrir() 
        
        vendas_cliente = []
        for obj in cls.objetos:
            if obj.get_idcliente() == idcliente:
                # Retorna o dicionário serializado da venda (com dados básicos)
                vendas_cliente.append(obj.to_json()) 
                
        return vendas_cliente       