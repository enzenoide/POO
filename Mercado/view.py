from models.cliente import Cliente,ClienteDAO
from models.categoria import Categoria, CategoriaDAO
from models.produto import Produto,ProdutoDAO
from models.carrinho import Carrinho,CarrinhoDAO
from models.cliente import Venda,VendaDAO
from models.vendaItem import VendaItem,VendaitemDAO
from datetime import datetime
import json

class View:
    def cliente_criar_admin():
        for obj in View.cliente_listar():
            if obj.get_email() == "admin": return
        View.cliente_inserir("admin", "admin", "(84)991012814", "12345678")

    def cliente_autenticar(email, senha):
        if email == "":
            raise ValueError("O email não pode estar vazio")
        elif senha == "":
            raise ValueError("A senha não pode estar vazia")
        for obj in View.cliente_listar():
            if obj.get_email() == email and obj.get_senha() == senha:
                return obj
        raise ValueError("O usuário não existe")

    def cliente_criar_conta(nome,email,fone,senha):
        if nome == "":
            raise ValueError("Nome não pode estar vazio")
        elif nome.isdigit():
            raise TypeError("Nome não pode ser um digito")
        for obj in View.cliente_listar():
            if obj.get_email() == email:
                raise ValueError("Já existe alguém com esse email")
            elif obj.get_fone() == fone:
                raise ValueError("Já existe alguém com esse telefone")
        try:
            View.cliente_inserir(nome,email,fone,senha)
        except (ValueError,TypeError) as e:
            raise e
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
        input
        ClienteDAO.excluir(id)

    def cliente_listar_compras(idcliente):
        try:
            with open("vendas.json", "r") as arquivo:
                vendas = json.load(arquivo)
        except:
            print("Nenhuma venda registrada ainda.")
            return []

        compras = []

        for v in vendas:
            if int(v["idcliente"]) == int(idcliente):
                
                compras.append(v)

                print(f"\n🧾 Venda ID: {v['id']} | Total: R${v['total']:.2f} | Data: {v['data']}")
                print("Itens:")

                for item in v["carrinho"]:
                    nome_produto = item.get("descricao_produto", "Produto não encontrado")
                    qtd = item.get("qtd", 0)
                    print(f"  - {nome_produto} | Quantidade: {qtd}")

        if not compras:
            print("❌ Você não possui nenhuma compra.")
        return compras
    def cliente_listar_vendas():
        vendas = VendaDAO.listar()
        itens = VendaitemDAO.listar()
        encontrou = False

        for v in vendas:
            cliente = ClienteDAO.listar_id(v.get_idcliente())
            nome_cliente = cliente.get_nome() if cliente else "Cliente não encontrado"

            print(f"\n🧾 Venda ID: {v.get_id()} | Cliente: {nome_cliente} | Total: R${v.get_total():.2f} | Data: {v.get_data()}")

            encontrou_itens = False
            for i in itens:
                if i.get_idvenda() == v.get_id():
                    produto = ProdutoDAO.listar_id(i.get_idproduto())
                    nome_produto = produto.get_descricao() if produto else "Produto não encontrado"
                    print(f"  - Produto: {nome_produto} | Quantidade: {i.get_qtd()} | Preço unitário: R${i.get_preco():.2f}")
                    encontrou_itens = True

            if not encontrou_itens:
                print("  (Nenhum item encontrado para esta venda)")

            encontrou = True

        if not encontrou:
            print("❌ Nenhuma venda registrada.")


    def categoria_inserir(desc):
        if desc == "":
            raise ValueError("Descrição não pode estar vazio")
        id = 0
        c = Categoria(id,desc)
        CategoriaDAO.inserir(c)

    def categoria_listar():
        return CategoriaDAO.listar()

    def categoria_listar_id():
        return CategoriaDAO.listar_id()

    def categoria_atualizar(id,desc):
        c = Categoria(id,desc)
        CategoriaDAO.atualizar(c)

    def categoria_excluir(id):
        desc = "a"
        c = Categoria(id,desc)
        CategoriaDAO.excluir(c)

    def produto_inserir(desc, preco, estoque, idcategoria):
        c = Produto(None, desc, preco, estoque, idcategoria)
        ProdutoDAO.inserir(c)

    def produto_listar():
        return ProdutoDAO.listar()

    def produto_listar_id(id):
        return ProdutoDAO.listar_id(id)

    def produto_atualizar(id, desc, preco, estoque, idcategoria):
        c = Produto(id, desc, preco, estoque, idcategoria)
        ProdutoDAO.atualizar(c)

    def produto_excluir(id):
        c = Produto(id, "", 1, 0, 0)
        ProdutoDAO.excluir(c)

    def produto_reajustar(percentual):
        ProdutoDAO.reajustar(percentual)

    def produto_buscar(id):
        for p in ProdutoDAO.listar():
            if int(p.get_id()) == int(id):
                return p
        return None

    
    def carrinho_inserir(idcliente, idproduto, qtd):
        if idproduto == "":
            raise ValueError("ID produto não pode estar vazio")
        elif qtd == "":
            raise ValueError("Quantidade não pode estar vazio")
        try:
            produto = View.produto_listar_id(idproduto)
            if produto is None:
                raise ValueError(f"O produto com ID:{idproduto} não foi encontrado no sistema")
            if produto.get_estoque() < int(qtd):
                raise ValueError(f"estoque insuficiente para {produto.get_descricao()}")
            item = Carrinho(idproduto, qtd)
        except ValueError as e:
            mensagem = "literal for int() with base 10"
            if mensagem in str(e):
                raise ValueError("O ID e a Quantidade precisam ser números")
            raise e
            
        CarrinhoDAO.inserir(idcliente, item)
        

        

    def carrinho_listar_detalhado(idcliente):
        return CarrinhoDAO.listar_detalhado(idcliente)

    def carrinho_preco(idcliente):
        carrinho = CarrinhoDAO.listar_detalhado(idcliente)
        total_geral = 0
        for item in carrinho:
            total_geral += item["total"]
        return total_geral

    @staticmethod
    def carrinho_comprar(idcliente):
        from models.carrinho import CarrinhoDAO
        from models.cliente import Venda, VendaDAO
        from datetime import datetime
        from models.produto import ProdutoDAO

        
        carrinho = CarrinhoDAO.listar(idcliente)

        if not carrinho:  
            print("Carrinho vazio! Nada para comprar.")
            return False

        total = 0

        
        for item in carrinho:
            produto = ProdutoDAO.listar_id(item.get_idproduto())
            if produto is None:
                print(f"Produto ID {item.get_idproduto()} não encontrado. Operação cancelada.")
                return False

            if produto.get_estoque() < item.get_qtd():
                print(f"Estoque insuficiente para o produto '{produto.get_descricao()}'.")
                return False

            total += float(produto.get_preco()) * float(item.get_qtd())

        
        for item in carrinho:
            produto = ProdutoDAO.listar_id(item.get_idproduto())
            produto.set_estoque(produto.get_estoque() - item.get_qtd())
            ProdutoDAO.atualizar(produto)

        
        venda = Venda(0, datetime.now(), carrinho.copy(), total, idcliente)
        VendaDAO.inserir(venda)

        for item in venda.carrinho:
            vendaitem = VendaItem(
                id=None,
                qtd=item.get_qtd(),
                preco=ProdutoDAO.listar_id(item.get_idproduto()).get_preco(),
                idvenda=venda.get_id(),
                idproduto=item.get_idproduto()
            )
            VendaitemDAO.inserir(vendaitem)

        
        CarrinhoDAO.limpar(idcliente)

        return True
    @classmethod
    def lucro(cls):
        produtos = ProdutoDAO.listar()
        vendas = VendaDAO.listar()

        total_vendido = 0
        qtd_vendida = 0

       
        for venda in vendas:
            for item in venda.carrinho:
                produto = ProdutoDAO.listar_id(item.get_idproduto())
                if produto:
                    total_vendido += float(produto.get_preco()) * float(item.get_qtd())
                    qtd_vendida += item.get_qtd()

    
        total_estoque = sum(float(p.get_preco()) * float(p.get_estoque()) for p in produtos)

        lucro = total_vendido - total_estoque

        print("\n📊 ======= RELATÓRIO FINANCEIRO =======")
        print(f"💼 Valor total do estoque atual : R${total_estoque:.2f}")
        print(f"🛒 Quantidade total vendida     : {qtd_vendida}")
        print(f"💰 Total arrecadado com vendas  : R${total_vendido:.2f}")
        print("--------------------------------------")

        if lucro >= 0:
            print(f"🟢 Situação: LUCRO de R${lucro:.2f}")
        else:
            print(f"🔴 Situação: PREJUÍZO de R${lucro:.2f}")

        print("=======================================\n")

        return lucro