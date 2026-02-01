from models.cliente import Cliente,ClienteDAO
from models.categoria import Categoria, CategoriaDAO
from models.produto import Produto,ProdutoDAO
from models.carrinho import Carrinho,CarrinhoDAO
from models.venda import Venda,VendaDAO
from models.vendaItem import VendaItem,VendaitemDAO
from models.avaliacao import Avaliacao, AvaliacaoDAO
from models.cupomdesconto import CupomDesconto,CupomDescontoDAO
from models.desenvolvedora import Desenvolvedora,DesenvolvedoraDAO
from models.plataforma import Plataforma,PlataformaDAO
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

    def categoria_listar_id(id):
        return CategoriaDAO.listar_id(id)

    def categoria_atualizar(id,desc):
        if id == "": raise ValueError("ID não pode estar vazio")
        c = Categoria(id,desc)
        CategoriaDAO.atualizar(c)

    def categoria_excluir(id):
        desc = "a"
        c = Categoria(id,desc)
        CategoriaDAO.excluir(c)

    def produto_inserir(desc, preco, estoque, idcategoria,imagem,plataforma,desenvolvedora):
        if not idcategoria or str(idcategoria).strip() == "":
            raise ValueError("O ID da categoria não pode ser vazio.")
    
       
        categorias_existentes = View.categoria_listar() 
        ids_validos = {str(c.get_id()) for c in categorias_existentes}

        idcategoria_str = str(idcategoria) 

        if idcategoria_str not in ids_validos:
            raise ValueError("ID da Categoria inexistente. Por favor, insira um ID válido.")

        c = Produto(None, desc, preco, estoque, idcategoria_str,imagem,plataforma,desenvolvedora)
        ProdutoDAO.inserir(c)

    def produto_listar():
        return ProdutoDAO.listar()

    def produto_listar_id(id):
        return ProdutoDAO.listar_id(id)

    def produto_atualizar(id, desc, preco, estoque, idcategoria,imagem,plataforma,desenvolvedora):
        c = Produto(id, desc, preco, estoque, idcategoria,imagem,plataforma,desenvolvedora)
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
        
        CarrinhoDAO.inserir_carrinho(idcliente, item)
        
        

        

    def carrinho_listar_detalhado(idcliente):
        return CarrinhoDAO.listar_detalhado(idcliente)

    def carrinho_preco(idcliente):
        carrinho = CarrinhoDAO.listar_detalhado(idcliente)
        total_geral = 0
        for item in carrinho:
            total_geral += item["total"]
        return total_geral

    @staticmethod
    def carrinho_comprar(idcliente, codigo_cupom=None):
        from models.carrinho import CarrinhoDAO
        from models.venda import Venda, VendaDAO
        from models.vendaItem import VendaItem, VendaitemDAO
        from models.produto import ProdutoDAO
        from models.cupomdesconto import CupomDescontoDAO
        from datetime import datetime

        # ===============================
        # 1️⃣ Abrir carrinho do cliente
        # ===============================
        CarrinhoDAO.abrir(idcliente)
        itens_carrinho = CarrinhoDAO.objetos

        if not itens_carrinho:
            raise ValueError("Carrinho vazio.")

        # ===============================
        # 2️⃣ Calcular total bruto
        # ===============================
        total_bruto = 0.0
        itens_para_venda = []

        for item in itens_carrinho:
            produto = ProdutoDAO.listar_id(item.get_idproduto())

            if not produto:
                raise ValueError("Produto não encontrado.")

            if produto.get_estoque() < item.get_qtd():
                raise ValueError(
                    f"Estoque insuficiente para {produto.get_descricao()}"
                )

            preco_unitario = float(produto.get_preco())
            subtotal = preco_unitario * item.get_qtd()
            total_bruto += subtotal

            itens_para_venda.append({
                "produto": produto,
                "qtd": item.get_qtd(),
                "preco": preco_unitario
            })

        # ===============================
        # 3️⃣ Aplicar cupom (se existir)
        # ===============================
        desconto = 0.0
        cupom_obj = None

        if codigo_cupom:
            CupomDescontoDAO.abrir()
            cupom_obj = CupomDescontoDAO.listar_por_codigo(codigo_cupom)

            if not cupom_obj:
                raise ValueError("Cupom inválido.")

            desconto = total_bruto * (cupom_obj.get_porcentagem() / 100)

        # Garante que o total nunca fique negativo
        total_pago = max(total_bruto - desconto, 0)

        # ===============================
        # 4️⃣ Criar venda
        # ===============================
        venda = Venda(
            id=0,
            data=datetime.now(),
            carrinho=itens_carrinho,
            total=total_pago,
            idcliente=idcliente,
            cupomdesconto=cupom_obj.get_codigo() if cupom_obj else None
        )

        VendaDAO.inserir(venda)
        id_venda = venda.get_id()

        if not id_venda:
            raise RuntimeError("Erro ao gerar venda.")

        # ===============================
        # 5️⃣ Criar itens da venda
        # ===============================
        for item in itens_para_venda:
            produto = item["produto"]

            vendaitem = VendaItem(
                id=None,
                qtd=item["qtd"],
                preco=item["preco"],
                idvenda=id_venda,
                idproduto=produto.get_id()
            )
            VendaitemDAO.inserir(vendaitem)

            # Atualiza estoque
            produto.set_estoque(produto.get_estoque() - item["qtd"])
            ProdutoDAO.atualizar(produto)

        # ===============================
        # 6️⃣ Limpar carrinho
        # ===============================
        CarrinhoDAO.limpar(idcliente)

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
    
    def desenvolvedora_inserir(nome):
        d = Desenvolvedora(None,nome)
        DesenvolvedoraDAO.inserir(d)
    def desenvolvedora_listar():
        return DesenvolvedoraDAO.listar()
    def desenvolvedora_listar_id(id):
        return DesenvolvedoraDAO.listar_id(id)
    def desenvolvedora_excluir(id):
        d = Desenvolvedora(id,".")
        DesenvolvedoraDAO.excluir(d)
    
    def plataforma_inserir(nome):
        p = Plataforma(None,nome)
        PlataformaDAO.inserir(p)
    def plataforma_listar():
        return PlataformaDAO.listar()
    def plataforma_listar_id(id):
        return PlataformaDAO.listar_id(id)
    def plataforma_excluir(id):
        d = Plataforma(id,".")
        PlataformaDAO.excluir(d)

    def cupomdesconto_inserir(codigo,porcentagem):
        c = CupomDesconto(None,codigo, porcentagem)
        CupomDescontoDAO.inserir(c)
    def cupomdesconto_listar():
        return CupomDescontoDAO.listar()
    def cupomdesconto_listar_id(id):
        return CupomDescontoDAO.listar_id(id)
    def cupomdesconto_listar_codigo(codigo):
        return CupomDescontoDAO.listar_por_codigo(codigo)
    def cupomdesconto_excluir(id):
        c = CupomDesconto(id,".",1)
        CupomDescontoDAO.excluir(c)
    def cupomdesconto_buscar_por_nome(nome):
        nome = nome.strip().lower()

        cupons = CupomDescontoDAO.listar()
        for cupom in cupons:
            if cupom.get_codigo().strip().lower() == nome:
                return cupom

        return None
    

    def avaliacao_existe(idvenda):
        return AvaliacaoDAO.buscar_por_venda(idvenda)

    def avaliacao_inserir(idvenda, idcliente, texto):
        if View.avaliacao_existe(idvenda):
            raise ValueError("Essa compra já foi avaliada.")

        a = Avaliacao(None, idvenda, idcliente, texto)
        AvaliacaoDAO.inserir(a)

    def avaliacao_buscar_por_venda(idvenda):
        return AvaliacaoDAO.buscar_por_venda(idvenda)

    @staticmethod
    def avaliacao_listar():
        from models.avaliacao import AvaliacaoDAO
        from models.venda import VendaDAO
        from models.cliente import ClienteDAO

        avaliacoes = AvaliacaoDAO.listar()
        vendas = VendaDAO.listar()

        # Indexa vendas por ID (performance + clareza)
        vendas_por_id = {v.get_id(): v for v in vendas}

        lista_formatada = []

        for a in avaliacoes:
            venda = vendas_por_id.get(a.get_idvenda())
            if not venda:
                continue

            cliente = ClienteDAO.listar_id(a.get_idcliente())
            nome_cliente = cliente.get_nome() if cliente else "Cliente não encontrado"

            lista_formatada.append({
                "id": a.get_id(),
                "comentario": a.get_texto(),
                "data": a.get_data(),
                "cliente": nome_cliente,
                "venda": {
                    "id": venda.get_id(),
                    "itens": venda.carrinho 
                }
            })

        return lista_formatada

    def avaliacao_excluir(id_avaliacao):
        AvaliacaoDAO.abrir()
        for a in AvaliacaoDAO.listar():
            if a.get_id() == id_avaliacao:
                AvaliacaoDAO.excluir(a)
                return
        raise ValueError("Avaliação não encontrada.")