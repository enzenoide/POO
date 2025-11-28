import streamlit as st
from view import View
import pandas as pd
import time

class ManterCategoriaUI:
    def main():
        st.header("Cadastro de categorias")
        tab1,tab2,tab3,tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterCategoriaUI.listar()
        with tab2: ManterCategoriaUI.inserir()
        with tab3: ManterCategoriaUI.atualizar()
        with tab4: ManterCategoriaUI.excluir()
    def listar():
        categorias= View.cliente_listar()
        if len(categorias) == 0: st.write("Nenhum cliente cadastrado")
        else:
            list_dic = []
            for obj in categorias: list_dic.append(obj.to_json())
            df = pd.DataFrame(list_dic)
            st.dataframe(df, hide_index = True, column_order = ["id","descricao"])
    def inserir():
        descricao = st.text_input("Me informe o nome da categoria")
        if st.button("Inserir"):
            View.categoria_inserir(descricao)
            st.success("Categoria inserida com sucesso!")
            time.sleep(2)
            st.rerun()
    def atualizar():
        categorias = View.categoria_listar()
        if len(categorias) == 0: st.write("Nenhuma categoria registada.")
        else:
            op = st.selectbox("Atualização da categoria: ", categorias)
            id = st.write("Me informe o ID da categoria a ser atualizada.", op.get_id())
            descricao = st.write("Me informe o novo nome.", op.get_descricao())
            View.categoria_atualizar(id,descricao)
            st.success("Categoria atualizada com sucesso")
            time.sleep(2)
            st.rerun
    def excluir():
        categorias = View.categoria_listar()
        if len(categorias) == 0: st.write("Nenhuma categoria registrada")
        else:
            op = st.selectbox("Exclusão de categorias", categorias)
            if st.button("Inserir"):
                id = op.get_id()
                View.categoria_excluir(id)
                st.success("Categoria excluída com sucesso")
                time.sleep(2)
                st.rerun()



