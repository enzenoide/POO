import json
from models.dao import DAO
class Produto:
    def __init__(self, id, descricao, preco, estoque, idcategoria,url_imagem=None):
        self.set_id(id)
        self.set_descricao(descricao)
        self.set_preco(preco)
        self.set_estoque(estoque)
        self.set_idcategoria(idcategoria)
        self.set_url_imagem(url_imagem)

    def get_url_imagem(self):
        return self.__url_imagem
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
        if id is None:
            self.__id = 0 
            return
        self.__id = int(id)
    def set_descricao(self, descricao):
        if descricao == "":
            raise ValueError("Descrição não pode estar vazio")
        self.__descricao = descricao
    def set_preco(self, preco):
        if preco is None or str(preco).strip() == "":
             raise ValueError("O produto precisa possuir preço.")
             
        preco = float(preco)
        if preco <= 0 : 
            raise ValueError("O produto precisa possuir preço positivo")
        self.__preco = preco
    def set_estoque(self, estoque):
        if estoque is None or str(estoque).strip() == "":
             raise ValueError("O estoque precisa ser informado.")
             
        estoque = float(estoque)
        if estoque < 0: 
            raise ValueError("O estoque não pode ser negativo")
        self.__estoque = estoque
        
    def set_idcategoria(self, idcategoria):
        if idcategoria is None or str(idcategoria).strip() == "":
            raise ValueError("ID da Categoria não pode ser vazio.")
        self.__idcategoria = int(idcategoria)
    def set_url_imagem(self,url_imagem):
        self.__url_imagem = url_imagem

    def __str__(self):
        return f"Produto ID: {self.get_id()} | Descrição: {self.get_descricao()} | Preço: R${self.get_preco():.2f} | Estoque: {self.get_estoque()} | Categoria ID: {self.get_idcategoria()}"
    
    def to_json(self):
        return { "id" : self.get_id(), "descricao" : self.get_descricao(), "preco" : self.get_preco(), "estoque" : self.get_estoque(), "idcategoria" : self.get_idcategoria(), "url_imagem": self.get_url_imagem() }

    @staticmethod
    def from_json(dic):
        return Produto(dic["id"], dic["descricao"], dic["preco"], dic["estoque"], dic["idcategoria"],dic.get("url_imagem", None))

class ProdutoDAO(DAO):
    @classmethod
    def abrir(cls):
        cls.objetos = []
        try:
            with open("json/produto.json", "r") as arquivo:
                list_dic = json.load(arquivo)
                for dic in list_dic:
                    c = Produto.from_json(dic)
                    cls.objetos.append(c)
          
            print(f"ProdutoDAO: {len(cls.objetos)} produtos carregados com sucesso.")
        except Exception as e:
            print(f"ProdutoDAO: ERRO AO ABRIR (Lista de objetos vazia). Detalhes: {e}")
            pass
    @classmethod
    def salvar(cls):
        with open("json/produto.json", "w") as arquivo:
            json.dump([{
                "id": p.get_id(),
                "descricao": p.get_descricao(),
                "preco": p.get_preco(),
                "estoque": p.get_estoque(),
                "idcategoria": p.get_idcategoria(),
                "url_imagem": p.get_url_imagem()
            } for p in cls.objetos], arquivo, indent=4)

    @classmethod
    def reajustar(cls, percentual):
        for obj in cls.objetos:
            novo_preco = obj.get_preco() + (obj.get_preco() * (percentual / 100))
            obj.set_preco(novo_preco)
            cls.atualizar(obj)