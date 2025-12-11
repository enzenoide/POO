import streamlit as st
from view import View
import time
import pandas as pd


class ListarProdutosUI:
    def main():
        st.header("Lista de Produtos")
        Produtos= View.produto_listar()
        if len(Produtos) == 0: st.write("Nenhum produto cadastrado")
        num_colunas = 2
        colunas = st.columns(num_colunas)
        largura_imagem = 200
        altura_imagem = 300
        for index,produto in enumerate(Produtos):
            # seleciona a coluna atual (0,1,2,0,1,2)
            col = colunas[index%num_colunas]
            with col:
                with st.container(border = True):
                    caminho_imagem = produto.get_url_imagem()


                    if caminho_imagem:
                        img_col1,img_col2,img_col3 = st.columns([1,4,1])
                        with img_col2:
                            st.image(caminho_imagem,caption = f"ID: {produto.get_id()}",width = largura_imagem)
                    else:
                        st.markdown("**(sem imagem)**")
                    st.markdown(f"**{produto.get_descricao()}**")
                    st.markdown(f"**{produto.get_preco():.2f}**")


