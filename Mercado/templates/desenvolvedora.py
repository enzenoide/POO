import streamlit as st
from view import View
import pandas as pd
import time
import os

class DesenvolvedoraUI:
    def main():
        st.header("Cadastro de Produtos")
        tab1,tab2,tab3 = st.tabs(["Listar", "Inserir", "Excluir"])
        with tab1: DesenvolvedoraUI.listar()
        with tab2: DesenvolvedoraUI.inserir()
        with tab3: DesenvolvedoraUI.excluir()
    def listar():
        Desenvolvedoras = View.desenvolvedora_listar()
        if len(Desenvolvedoras) == 0: st.write("Nenhum produto cadastrado")
        else:
            list_dic = []
            for obj in Desenvolvedoras: list_dic.append(obj.to_json())
            df = pd.DataFrame(list_dic)
            st.dataframe(df, hide_index = True, column_order = ["id","nome"])
    def inserir():
        nome = st.text_input("Me informe o nome da desenvolvedora: ")

        if st.button("Inserir"):
            try:
                View.desenvolvedora_inserir(nome)

                st.success("Desenvolvedora inserida com sucesso!")
                time.sleep(2)
                st.rerun()

            except Exception as erro:
                st.error(erro)
    def excluir():
        Desenvolvedoras = View.desenvolvedora_listar()
        if len(Desenvolvedoras) == 0: st.write("Nenhuma Desenvolvedoras registrada")
        else:
            op = st.selectbox("Exclusão de Desenvolvedoras", Desenvolvedoras)
            if st.button("Excluir"):
                try:
                    id = op.get_id()
                    View.desenvolvedora_excluir(id)
                    st.success("Desenvolvedora excluída com sucesso")
                    time.sleep(2)
                    st.rerun()
                except Exception as erro:
                    st.error(erro)
