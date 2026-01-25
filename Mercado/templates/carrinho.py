import streamlit as st
from view import View
import time
import pandas as pd

class CarrinhoUI:
    def inserir():
        st.header("Inserir produto no carrinho")
        Produtos = View.produto_listar()
        
        if len(Produtos) == 0: 
            st.write("Nenhum produto cadastrado.")
            return

        num_colunas = 3
        colunas = st.columns(num_colunas)
        largura_imagem = 150
        
        for index, produto in enumerate(Produtos):
            produto_id = produto.get_id()
            # GARANTE QUE O ESTOQUE É FLOAT
            estoque_atual = float(produto.get_estoque())
            
            pode_adicionar = estoque_atual > 0 
            
            # GARANTE QUE O MIN_VALUE É FLOAT
            min_valor_input = 1.0 if pode_adicionar else 0.0
            
            col = colunas[index % num_colunas]
            
            with col:
                with st.container(border=True): 
                    caminho_imagem = produto.get_imagem()

                    if caminho_imagem:
                        img_col1, img_col2, img_col3 = st.columns([1, 4, 1])
                        with img_col2:
                            st.image(caminho_imagem, 
                                     caption=f"ID: {produto_id}", 
                                     width=largura_imagem)
                    else:
                        st.markdown(f"<div align='center'>**(sem imagem) - ID: {produto_id}**</div>", unsafe_allow_html=True)

                    st.markdown("---") 
                    
                    st.markdown(f"**{produto.get_descricao()}**")
                    st.markdown(f"**R$ {produto.get_preco():.2f}**")
                    
                    if not pode_adicionar:
                        st.markdown("<div align='center'><font color='red'>ESTOQUE ESGOTADO</font></div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div align='center'>Estoque: {estoque_atual:.2f}</div>", unsafe_allow_html=True)

                    # 3. number_input agora usa apenas floats (1.0, 0.0)
                    qtd = st.number_input(
                        "Qtd:", 
                        min_value=min_valor_input, 
                        max_value=estoque_atual, 
                        value=min_valor_input, 
                        step=1.0, # Adiciona step=1.0 para manter o tipo consistente
                        disabled=not pode_adicionar, 
                        key=f"qtd_{produto_id}"
                    )

                    if st.button("🛒 Adicionar", key=f"add_{produto_id}", disabled=not pode_adicionar):
                        # Lógica de adição
                        try:
                            # Garante que a quantidade seja convertida para o tipo que a View espera (provavelmente float ou int)
                            qtd_para_inserir = int(qtd) if qtd == int(qtd) else qtd 
                            
                            View.carrinho_inserir(st.session_state["cliente_id"], produto_id, qtd_para_inserir)
                            
                            st.success(f"'{produto.get_descricao()}' adicionado(a) com sucesso!")
                            time.sleep(1)
                            st.rerun()
                        except ValueError as error:
                            st.error(error)
                        except Exception as error:
                            st.error(f"Erro ao adicionar produto: {error}")
            
    def listar():
        st.header("Produtos no carrinho")
        carrinho_detalhado = View.carrinho_listar_detalhado(st.session_state["cliente_id"])

        if not carrinho_detalhado:
            st.write("Nenhum produto no carrinho.")
            return

        num_colunas = 3 # Exibe os itens do carrinho em 3 colunas
        colunas = st.columns(num_colunas)

       
        df = pd.DataFrame(carrinho_detalhado)
        
        for index, item in enumerate(carrinho_detalhado):
            col = colunas[index % num_colunas]
            
            
            
            id_produto = item.get('id_produto')
            descricao = item.get('descricao')
            preco = item.get('preco')
            quantidade = item.get('quantidade')
            total_item = item.get('total')
            caminho_imagem = View.produto_listar_id(id_produto).get_imagem() 
            
            with col:
                with st.container(border=True): 
                    img_col1, img_col2, img_col3 = st.columns([1, 4, 1])
                    with img_col2:
                        st.image(caminho_imagem, width=150) 
                    
                    st.markdown("---") 

                    st.markdown(f"**{descricao}**")
                    st.markdown(f"**Qtd: {quantidade}**")
                    st.markdown(f"R$ {preco:.2f} (un.)")
                    st.markdown(f"**Subtotal: R$ {total_item:.2f}**")
        
        st.markdown("---")
        
        total_geral = df['total'].sum()
        st.markdown(f"## 💰 Total no Carrinho: R$ {total_geral:.2f}")

        
    def comprar():
        st.header("Comprar Carrinho")
        carrinho_detalhado = View.carrinho_listar_detalhado(st.session_state["cliente_id"])

        if not carrinho_detalhado:
            st.write("Nenhum produto no carrinho.")
            return
        
        
        df = pd.DataFrame(carrinho_detalhado)
        st.dataframe(df, 
                    hide_index=True, 
                    column_order=["id_produto", "descricao", "preco", "quantidade", "total"])

        total_geral = df['total'].sum()

        st.markdown("---")
        st.success(f"## Total a Pagar: R$ {total_geral:.2f}")

        if st.button("✅ Confirmar Compra e Pagar"):
            try:
                View.carrinho_comprar(st.session_state["cliente_id"])
                st.success("Carrinho comprado com sucesso!")
                time.sleep(2)
                st.rerun()
            except Exception as error:
                st.error(error)
