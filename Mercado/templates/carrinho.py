import streamlit as st
from view import View
import time
import pandas as pd

class CarrinhoUI:
    def inserir():
        st.header("Inserir produto no carrinho")
        Produtos= View.produto_listar()
        if len(Produtos) == 0: st.write("Nenhum cliente cadastrado")
        else:
            list_dic = []
            for obj in Produtos: list_dic.append(obj.to_json())
            df = pd.DataFrame(list_dic)
            st.dataframe(df, hide_index = True, column_order = ["id","descricao","preco","estoque","idcategoria"])
        idproduto = st.text_input("ID do produto que deseja adicionar")
        qtd = st.text_input("Quantidade")
        if st.button("Inserir"):
            try:
                View.carrinho_inserir(st.session_state["cliente_id"],idproduto,qtd)
                st.success("Produto adicionado no carrinho com sucesso!")
                time.sleep(2)
                st.rerun()
            except Exception as erro:
                st.error(erro)

    def listar():
        st.header("Produtos no carrinho")
        carrinho = View.carrinho_listar_detalhado(st.session_state["cliente_id"])
        if len(carrinho) == 0: st.write("Nenhum produto no carrinho")
        else:
            df = pd.DataFrame(carrinho)
            st.dataframe(df, hide_index = True, column_order = ["id_produto","descricao","preco","quantidade","total"])
    def comprar():
        st.header("Comprar Carrinho")
        carrinho = View.carrinho_listar_detalhado(st.session_state["cliente_id"])
        if len(carrinho) == 0: st.write("Nenhum produto no carrinho")
        else:
            df = pd.DataFrame(carrinho)
            st.dataframe(df, hide_index = True, column_order = ["id_produto","descricao","preco","quantidade","total"])
            if st.button("Comprar"):
                View.carrinho_comprar(st.session_state["cliente_id"])
                st.success("Carrinho comprado com sucesso")
                time.sleep(2)
                st.rerun()
