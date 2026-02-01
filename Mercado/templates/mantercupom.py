import streamlit as st
from view import View
import pandas as pd
import time
import os

class CupomDescontoUI:
    def main():
        st.header("Cadastro de Cupons")
        tab1,tab2,tab3 = st.tabs(["Listar", "Inserir", "Excluir"])
        with tab1: CupomDescontoUI.listar()
        with tab2: CupomDescontoUI.inserir()
        with tab3: CupomDescontoUI.excluir()
    def listar():
        cupomdesconto = View.cupomdesconto_listar()
        if len(cupomdesconto) == 0: st.write("Nenhuma cupomdesconto cadastrada")
        else:
            list_dic = []
            for obj in cupomdesconto: list_dic.append(obj.to_json())
            df = pd.DataFrame(list_dic)
            st.dataframe(df, hide_index = True, column_order = ["id","codigo","porcentagem"])
    def inserir():
        nome = st.text_input("Me informe o nome do Cupom: ")
        porcentagem = st.number_input("Porcentagem de desconto (%)",min_value=1,max_value=100,step=1)


        if st.button("Inserir"):
            try:
                View.cupomdesconto_inserir(nome,porcentagem)

                st.success("Cupom inserido com sucesso!")
                time.sleep(2)
                st.rerun()

            except Exception as erro:
                st.error(erro)
    def excluir():
        cupomdescontos = View.cupomdesconto_listar()
        if len(cupomdescontos) == 0: st.write("Nenhum cupom registrad")
        else:
            op = st.selectbox("Exclusão de Cupons", cupomdescontos)
            if st.button("Excluir"):
                try:
                    id = op.get_id()
                    View.cupomdesconto_excluir(id)
                    st.success("Cupom excluido com sucesso")
                    time.sleep(2)
                    st.rerun()
                except Exception as erro:
                    st.error(erro)
