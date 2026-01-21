from models.cliente import Cliente,ClienteDAO
from models.categoria import Categoria, CategoriaDAO
from models.produto import Produto,ProdutoDAO
from models.carrinho import Carrinho,CarrinhoDAO
from models.venda import Venda,VendaDAO
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
        for obj in View.cliente_listar():
            if obj.get_email() == email: raise ValueError("Já existe alguém com esse email")
            elif obj.get_fone() == fone: raise ValueError("Já existe algúem com esse telefone")
        c = Cliente(id,nome,email,fone,senha)
        ClienteDAO.inserir(c)

    def cliente_listar():
        return ClienteDAO.listar()

    def cliente_listar_id():
        return ClienteDAO.listar_id()

    def cliente_atualizar(id,nome,email,fone,senha):
        c = Cliente(id,nome,email,fone,senha)
        for obj in View.cliente_listar():
            if obj.get_email() == email: raise ValueError("Já existe alguém com esse email")
            elif obj.get_fone() == fone: raise ValueError("Já existe algúem com esse telefone")
        ClienteDAO.atualizar(c)

    def cliente_excluir(id):
        if id == 1:
            raise ValueError("Admin não pode ser excluido")
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
        
        
        vendas_formatadas = []

        
        itens_por_venda = {}
        for i in itens:
            id_venda = i.get_idvenda()
            if id_venda not in itens_por_venda:
                itens_por_venda[id_venda] = []
            itens_por_venda[id_venda].append(i)

        
        for v in vendas:
            venda_id = v.get_id()
            
            
            cliente = ClienteDAO.listar_id(v.get_idcliente())
            nome_cliente = cliente.get_nome() if cliente else "Cliente não encontrado"

            
            carrinho = []
            
           
            itens_relacionados = itens_por_venda.get(venda_id, [])

            for item_obj in itens_relacionados:
                produto = ProdutoDAO.listar_id(item_obj.get_idproduto())
                
                nome_produto = produto.get_descricao() if produto else "Produto não encontrado"
                url_img = produto.get_url_imagem() if produto and hasattr(produto, 'get_url_imagem') else "assets/placeholder.png"

                carrinho.append({
                    "descricao_produto": nome_produto,
                    "qtd": item_obj.get_qtd(),
                    "preco": item_obj.get_preco(),
                    "url_imagem": url_img,
                    "id_produto": item_obj.get_idproduto() 
                })

            
            vendas_formatadas.append({
                "id": venda_id,
                "total": v.get_total(),
                "data": v.get_data(),  
                "nome_cliente": nome_cliente,
                "carrinho": carrinho
            })

        # 3. Retornar a lista formatada
        return vendas_formatadas


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
        if not idcategoria or str(idcategoria).strip() == "":
            raise ValueError("O ID da categoria não pode ser vazio.")
    
       
        categorias_existentes = View.categoria_listar() 
        ids_validos = {str(c.get_id()) for c in categorias_existentes}

        idcategoria_str = str(idcategoria) 

        if idcategoria_str not in ids_validos:
            raise ValueError("ID da Categoria inexistente. Por favor, insira um ID válido.")

        c = Produto(None, desc, preco, estoque, idcategoria_str)
        ProdutoDAO.inserir(c)

    def produto_listar():
        return ProdutoDAO.listar()

    def produto_listar_id(id):
        return ProdutoDAO.listar_id(id)

    def produto_atualizar(id, desc, preco, estoque, idcategoria):
        c = Produto(id, desc, preco, estoque, idcategoria)
        ProdutoDAO.atualizar(c)

    def produto_excluir(id):
        c = Produto(id, ".", 1, 0, 0)
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
        from models.cliente import Venda, VendaDAO 
        from models.vendaItem import VendaItem, VendaitemDAO 
        from datetime import datetime
        from models.produto import ProdutoDAO

        carrinho = CarrinhoDAO.listar(idcliente) 

        if not carrinho:
            print("Carrinho vazio! Nada para comprar.")
            return False

        total_compra = 0
        itens_para_venda_data = [] 
        
       
        for item_carrinho in carrinho:
            id_produto = item_carrinho.get_idproduto()
            qtd = item_carrinho.get_qtd()
            produto = ProdutoDAO.listar_id(id_produto)
            
            if produto is None or produto.get_estoque() < qtd:
                return False 

            preco_unitario = float(produto.get_preco())
            total_compra += preco_unitario * qtd
            
            itens_para_venda_data.append({
                'produto': produto, 
                'qtd': qtd, 
                'preco': preco_unitario
            })
        
        if not itens_para_venda_data:
            print("Nenhum item válido para compra no carrinho.")
            return False

        
        venda = Venda(id=0, data=datetime.now(), carrinho=carrinho, total=total_compra, idcliente=idcliente)
        
        VendaDAO.inserir(venda)
        id_venda_gerado = venda.get_id() 

        if not id_venda_gerado:
                print("ERRO CRÍTICO: Falha ao obter o ID da Venda após a inserção.")
                return False 

        # SALVAMENTO DOS ITENS NO VENDAITEMDAO E ATUALIZAÇÃO DO ESTOQUE (Mantido)
        for item_data in itens_para_venda_data:
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

            
            produto.set_estoque(produto.get_estoque() - qtd)
            ProdutoDAO.atualizar(produto)

        
        CarrinhoDAO.limpar(idcliente)

        print(f"Compra finalizada com sucesso. Venda ID: {id_venda_gerado}")
        return True
    @classmethod
    def relatorio_consumo(cls):
        #
        produtos = ProdutoDAO.listar()
        vendas = VendaDAO.listar()
        
        total_vendido = 0       
        qtd_vendida = 0         
        
        # Lista de Vendas está OK, entramos no loop
        for venda in vendas:
            
            #ACESSO AO CARRINHO (Contém Objetos Carrinho)
            # Assumimos que o VendaDAO.listar() carrega o atributo 'carrinho' com os itens.
            itens_da_venda = venda.carrinho
            
            if not itens_da_venda:
                continue
                
           
            for item in itens_da_venda:
                
                # Obtém ID e Quantidade do Objeto Carrinho
                id_produto = item.get_idproduto() 
                quantidade = float(item.get_qtd())
                
                if id_produto is not None:
                    # Busca o produto atual para obter preço e descrição (Se o produto ainda existe)
                    produto_vendido = ProdutoDAO.listar_id(id_produto)
                    
                    if produto_vendido:
                        
                        # Usa o preço atual de venda do produto no estoque
                        preco_venda_item = float(produto_vendido.get_preco()) 
                        
                        total_vendido += preco_venda_item * quantidade
                        qtd_vendida += quantidade
        
        
        total_estoque_valor_venda = sum(float(p.get_preco()) * float(p.get_estoque()) for p in produtos)
        
        
       
        print("\n📊 ======= RELATÓRIO DE CONSUMO/VENDAS =======")
        print(f"💰 Total arrecadado com vendas : R${total_vendido:.2f}")
        print(f"🛒 Quantidade total de itens vendidos : {qtd_vendida:.2f}")
        print(f"💼 Valor total do estoque atual (P.V.) : R${total_estoque_valor_venda:.2f}")
        print("=============================================\n")
        
        return {
            'total_vendido': total_vendido,
            'qtd_vendida': qtd_vendida,
            'estoque_valor_venda': total_estoque_valor_venda,
        }