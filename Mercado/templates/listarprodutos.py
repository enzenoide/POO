import streamlit as st
from view import View
import time
import pandas as pd

class ListarProdutosUI:
    def main():
        st.header("Lista de Produtos")
        Produtos= View.produto_listar()
        if len(Produtos) == 0: st.write("Nenhum cliente cadastrado")
        else:
            list_dic = []
            for obj in Produtos: list_dic.append(obj.to_json())
            df = pd.DataFrame(list_dic)
            st.dataframe(df, hide_index = True, column_order = ["id","descricao","preco","estoque","idcategoria"])
   