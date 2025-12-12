import streamlit as st
from view import View
import pandas as pd
import time 

class ReajustarProdutoUI:
    def main():
        st.header("Reajustar preço dos produtos")
        tab1,tab2 = st.tabs(["Preços atuais", "Reajuste" ])
        with tab1: ReajustarProdutoUI.atuais()
        with tab2: ReajustarProdutoUI.reajuste()

    def atuais():
        produtos = View.produto_listar()
        if len(produtos) == 0:
            st.write("Não existem produtos no Mercado.")
        else:
            list_dic = []
            for obj in produtos:
                list_dic.append({"Preço": obj.get_preco()})

            df = pd.DataFrame(list_dic)
            st.dataframe(df, hide_index=True)

    def reajuste():
        porc = st.text_input("Me informe a porcentagem de aumento: ")
        if st.button("Reajustar"):
            try:
                percentual = float(porc)
                View.produto_reajustar(percentual)
                st.success("Preço reajustado com sucesso!")
                time.sleep(2)
                st.rerun()
            except:
                st.error("Valor inválido! Digite um número válido.")