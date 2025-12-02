import streamlit as st
from view import View
import time
class AbrirContaUI:
    def main():
        st.header("Abrir conta")
        nome = st.text_input("informe o nome")
        email = st.text_input("informe o email")
        fone = st.text_input("informe o fone")
        senha = st.text_input("informe o senha", type = "password")
        if st.button("Abrir conta"):
            View.cliente_criar_conta(nome,email,fone,senha)
            st.success("Conta criada com sucesso!")
            time.sleep(2)
            st.rerun()