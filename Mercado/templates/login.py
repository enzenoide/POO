import streamlit as st
from view import View
import time
class LoginUI:
    def main():
        st.header("Entrar no sistema")
        email = st.text_input("Informe seu email")
        senha = st.text_input("Informe sua senha", type= "password")
        if st.button("Entrar"):
            try:
                c = View.cliente_autenticar(email,senha)
                st.success("Cliente autenticado com sucesso!")
                st.session_state["cliente_id"] = c.get_id()
                st.session_state["cliente_nome"] = c.get_nome()
                time.sleep(2)
                st.rerun()
            except Exception as erro:
                st.error(erro)
                