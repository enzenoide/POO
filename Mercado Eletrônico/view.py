from models.cliente import Cliente,ClienteDAO
from models.categoria import Categoria, CategoriaDAO
from models.produto import Produto,ProdutoDAO
from models.carrinho import Carrinho,CarrinhoDAO
from models.cliente import Venda,VendaDAO
from models.vendaItem import VendaItem,VendaitemDAO
from datetime import datetime
class View:
    def cliente_criar_admin():
        for obj in View.cliente_listar():
            if obj.get_email() == "admin": return
        View.cliente_inserir("admin", "admin", "1234", "1234")
    def cliente_autenticar(email, senha):
        for obj in View.cliente_listar():
            if obj.get_email() == email and obj.get_senha() == senha:
                return obj
        return None
    def cliente_criar_conta(nome,email,fone,senha):
        for obj in View.cliente_listar():
            if obj.get_email() == email:
                print("Já existe alguém com esse email")
                return
        View.cliente_inserir(nome,email,fone,senha)
        print("Conta criada com sucesso!")
    def cliente_inserir(nome,email,fone,senha):
        id = 0
        c = Cliente(id,nome,email,fone,senha)
        ClienteDAO.inserir(c)
    def cliente_listar():
        return ClienteDAO.listar()
    def cliente_listar_id():
        return ClienteDAO.listar_id()
    def cliente_atualizar(id,nome,email,fone,senha):
        c = Cliente(id,nome,email,fone,senha)
        ClienteDAO.atualizar(c)
    def cliente_excluir(id):
        nome = ""
        email = ""
        fone = ""
        senha = ""
        c = Cliente(id,nome,email,fone,senha)
        ClienteDAO.excluir(c)
    def cliente_listar_compras(idcliente):
        vendas = VendaDAO.listar()
        itens = VendaitemDAO.listar()

        encontrou = False

        for v in vendas:
            if v.get_idcliente() == idcliente:
                encontrou = True
                print(f"Venda ID: {v.get_id()} Total: R${v.get_total()}")
            for i in itens:
                if i.get_idvenda() == v.get_id:
                    produto = ProdutoDAO.listar_id(i.get_idproduto())
                    print(f"{produto.get_descricao()} Quantidade: {i.get_qtd()} Preço: {i.get_preco()}")
        if not encontrou:
            print("Você não possui nenhuma compra")

    def categoria_inserir(id,desc):
        id = 0
        c = Categoria(id,desc)
        CategoriaDAO.inserir(c)
    def categoria_listar():
        return CategoriaDAO.listar()
    def categoria_listar_id():
        return CategoriaDAO.listar_id()
    def categoria_atualizar(id,desc):
        c = Categoria(id,desc)
        CategoriaDAO.atualizar(id,desc)
    def categoria_excluir(id,desc):
        desc = ""
        c = Categoria(id,desc)
        CategoriaDAO.excluir(c)

    def produto_inserir(desc, preco, estoque, idcategoria):
        c = Produto(None, desc, preco, estoque, idcategoria)
        ProdutoDAO.inserir(c)

    def produto_listar():
        return ProdutoDAO.listar()
    def produto_listar_id():
        return ProdutoDAO.listar_id()

    def produto_atualizar(id, desc, preco, estoque, idcategoria):
        c = Produto(id, desc, preco, estoque, idcategoria)
        ProdutoDAO.atualizar(c)

    def produto_excluir(id):
        # cria um objeto apenas para referenciar o ID a excluir
        c = Produto(id, "", 0, 0, 0)
        ProdutoDAO.excluir(c)

    def produto_reajustar(percentual):
        ProdutoDAO.reajustar(percentual)
    def produto_buscar(id):
        for p in ProdutoDAO.listar():
            if int(p.get_id()) == int(id):
                return p
        return None
            
    def carrinho_inserir(id, qtd):
        produto = View.produto_buscar(id)
        if produto is None:
            print("Produto não encontrado!")
            return
        
        if qtd > produto.get_estoque():
            print(f"Quantidade indisponível. Estoque atual: {produto.get_estoque()}")
            return
        item = Carrinho(id,qtd)
        CarrinhoDAO.inserir(item)
        print("Produto adicionado ao carrinho!")
    def carrinho_listar_detalhado():
        return CarrinhoDAO.listar_detalhado()
    def carrinho_preco():
        carrinho = CarrinhoDAO.listar_detalhado()
        total_geral = 0
        for item in carrinho:
            total_geral += item["total"]
        return total_geral

    def carrinho_comprar(idcliente):
        carrinho = CarrinhoDAO.listar()  
        
        if not carrinho:
            print("Carrinho vazio.")
            return

        total = View.carrinho_preco()

        
        venda = Venda(0, datetime.now(), carrinho, total, idcliente)
        VendaDAO.inserir(venda)

      
        idvenda = VendaDAO.listar()[-1].get_id()

        
        for item in carrinho:
            produto = ProdutoDAO.listar_id(item.get_idproduto())

            
            vi = VendaItem(0, item.get_qtd(), produto.get_preco(), idvenda, produto.get_id())
            VendaitemDAO.inserir(vi)

            
            produto.set_estoque(produto.get_estoque() - item.get_qtd())
            ProdutoDAO.atualizar(produto)

        
        CarrinhoDAO.limpar()

        print("Compra realizada com sucesso!")
        print(f"Valor total: R${total:.2f}")
