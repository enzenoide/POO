import streamlit as st
from view import View
class LoginUI:
    def main():
        st.header("Entrar no sistema")
        email = st.text_input("Informe seu email")
        senha = st.text_input("Informe sua senha", type= "password")
        if st.button("Entrar"):
            c = View.cliente_autenticar(email,senha)
            if c == None: st.write("E-mail ou senha inválidos")
            else:
                st.session_state["cliente_id"] = c.get_id()
                st.session_state["cliente_nome"] = c.get_nome()
                st.rerun()