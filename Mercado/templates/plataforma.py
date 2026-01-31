import streamlit as st
from view import View
import pandas as pd
import time
import os

class PlataformaUI:
    def main():
        st.header("Cadastro de Plataformas")
        tab1,tab2,tab3 = st.tabs(["Listar", "Inserir", "Excluir"])
        with tab1: PlataformaUI.listar()
        with tab2: PlataformaUI.inserir()
        with tab3: PlataformaUI.excluir()
    def listar():
        Plataformas = View.plataforma_listar()
        if len(Plataformas) == 0: st.write("Nenhuma plataforma cadastrada")
        else:
            list_dic = []
            for obj in Plataformas: list_dic.append(obj.to_json())
            df = pd.DataFrame(list_dic)
            st.dataframe(df, hide_index = True, column_order = ["id","nome"])
    def inserir():
        nome = st.text_input("Me informe a plataforma: ")

        if st.button("Inserir"):
            try:
                View.plataforma_inserir(nome)

                st.success("Plataforma inserida com sucesso!")
                time.sleep(2)
                st.rerun()

            except Exception as erro:
                st.error(erro)
    def excluir():
        Plataformas = View.plataforma_listar()
        if len(Plataformas) == 0: st.write("Nenhuma Plataforma registrada")
        else:
            op = st.selectbox("Exclusão de Plataformas", Plataformas)
            if st.button("Excluir"):
                try:
                    id = op.get_id()
                    View.desenvolvedora_excluir(id)
                    st.success("Plataforma excluída com sucesso")
                    time.sleep(2)
                    st.rerun()
                except Exception as erro:
                    st.error(erro)
