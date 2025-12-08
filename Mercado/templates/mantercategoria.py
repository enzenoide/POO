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
        categorias= View.categoria_listar()
        if len(categorias) == 0: st.write("Nenhum cliente cadastrado")
        else:
            list_dic = []
            for obj in categorias: list_dic.append(obj.to_json())
            df = pd.DataFrame(list_dic)
            st.dataframe(df, hide_index = True, column_order = ["id","descricao"])
    def inserir():
        descricao = st.text_input("Me informe o nome da categoria")
        if st.button("Inserir"):
            try:
                View.categoria_inserir(descricao)
                st.success("Categoria inserida com sucesso!")
                time.sleep(2)
                st.rerun()
            except:
                st.error("Descrição não pode estar vazio")
    def atualizar():
        categorias = View.categoria_listar()
        if len(categorias) == 0: st.write("Nenhuma categoria registada.")
        else:
            op = st.selectbox("Atualização da categoria: ", categorias)
            id = st.text_input("ID da categoria a ser atualizada: ", op.get_id())
            descricao = st.text_input("Novo nome da categoria: ", op.get_descricao())
            if st.button("Atualizar"):
                id = op.get_id()
                View.categoria_atualizar(id,descricao)
                st.success("Categoria atualizada com sucesso")
                time.sleep(2)
                st.rerun()
    def excluir():
        categorias = View.categoria_listar()
        if len(categorias) == 0: st.write("Nenhuma categoria registrada")
        else:
            op = st.selectbox("Exclusão de categorias", categorias)
            if st.button("Excluir"):
                id = op.get_id()
                View.categoria_excluir(id)
                st.success("Categoria excluída com sucesso")
                time.sleep(2)
                st.rerun()



