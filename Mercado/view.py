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
        vendas = VendaDAO.listar_por_cliente(idcliente)
    
        lista_vendas_detalhadas = []
        
        
        for venda_dic in vendas:
            id_venda = venda_dic.get('id')
            
           
            if id_venda:
                
                itens_comprados = VendaitemDAO.listar_por_venda(id_venda)
                
                venda_dic['carrinho'] = itens_comprados
            else:
                venda_dic['carrinho'] = []
                
            lista_vendas_detalhadas.append(venda_dic)
        
        
        if not lista_vendas_detalhadas:
            print("❌ Você não possui nenhuma compra.")
            
        return lista_vendas_detalhadas
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
        if id == "": raise ValueError("ID não pode estar vazio")
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
        if percentual < 0:
            raise ValueError("Percentual não pode ser negativo.")
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
        from models.cliente import Venda, VendaDAO # Assumindo que Venda e VendaDAO estão aqui
        from models.vendaItem import VendaItem, VendaitemDAO # Importar VendaItem e VendaitemDAO
        from datetime import datetime
        from models.produto import ProdutoDAO

        carrinho = CarrinhoDAO.listar(idcliente)

        if not carrinho:
            print("Carrinho vazio! Nada para comprar.")
            return False

        total_compra = 0
        itens_para_venda = [] 

        
        for item_carrinho in carrinho:
            id_produto = item_carrinho.get_idproduto()
            qtd = item_carrinho.get_qtd()
            produto = ProdutoDAO.listar_id(id_produto)
            
            # IGNORA ITEM INVÁLIDO (SOLUÇÃO PARA O ID 10)
            if produto is None:
                # O produto será ignorado na compra, mas permanece no carrinho até a limpeza final
                print(f"AVISO: Produto ID {id_produto} não encontrado. Item ignorado na compra.")
                continue 
                
            #INTERROMPE COMPRA POR ESTOQUE (ISSO AINDA É UM ERRO CRÍTICO DE NEGÓCIO)
            if produto.get_estoque() < qtd:
                print(f"Estoque insuficiente para o produto '{produto.get_descricao()}'. Operação cancelada.")
                return False 

            preco_unitario = float(produto.get_preco())
            total_compra += preco_unitario * qtd
            
            itens_para_venda.append({
                'produto': produto, 
                'qtd': qtd, 
                'preco': preco_unitario
            })
        
        
        if not itens_para_venda:
            print("Nenhum item válido para compra no carrinho.")
            return False

        

        #Passa o carrinho vazio pra evitar o NoneType
        venda = Venda(id=0, data=datetime.now(), carrinho=[], total=total_compra, idcliente=idcliente)
        
        VendaDAO.inserir(venda)
        id_venda_gerado = venda.get_id() 

        if not id_venda_gerado:
             print("ERRO CRÍTICO: Falha ao obter o ID da Venda após a inserção.")
             return False # A transação falhou

        #REGISTRAR ITENS E ATUALIZAR ESTOQUE
        for item_data in itens_para_venda:
            produto = item_data['produto']
            qtd = item_data['qtd']
            preco = item_data['preco']
            
            # Cria e insere VendaItem
            vendaitem = VendaItem(
                id=None,
                qtd=qtd,
                preco=preco,
                idvenda=id_venda_gerado, 
                idproduto=produto.get_id()
            )
            VendaitemDAO.inserir(vendaitem)

            # Atualiza o estoque
            produto.set_estoque(produto.get_estoque() - qtd)
            ProdutoDAO.atualizar(produto)

        #LIMPAR O CARRINHO INTEIRO (Remove itens comprados + o ID 10 inválido)
        CarrinhoDAO.limpar(idcliente)

        print(f"Compra finalizada com sucesso. Venda ID: {id_venda_gerado}")
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