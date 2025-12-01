import streamlit as st
from templates.mantercliente import ManterClienteUI
from templates.mantercategoria import ManterCategoriaUI
from templates.manterproduto import ManterProdutoUI
from templates.reajustarproduto import ReajustarProdutoUI
from templates.login import LoginUI
from view import View
class IndexUI:
    def menu_visitante():
        op = st.sidebar.selectbox("Menu", [
                                    "Entrar no Sistema", 
                                    "Abrir conta", "Sair do Sistema"
                                    ])
        if op == "Entrar no Sistema": LoginUI.main()
        if op == "Abrir conta": pass
        if op == "Sair do Sistema": pass
    def menu_admin():
        op = st.sidebar.selectbox("Menu", [
                                  "Cadastro de Categorias", 
                                   "Cadastro de Clientes",
                                   "Cadastro de Produtos",
                                   "Reajustar Produtos"])
       # st.session_state["opcao"].append(op) 
        if op == "Cadastro de Categorias": ManterCategoriaUI.main()
        if op == "Cadastro de Clientes": ManterClienteUI.main()
        if op == "Cadastro de Produtos": ManterProdutoUI.main()
        if op == "Reajustar Produtos": ReajustarProdutoUI.main()
    def menu_cliente():
        op = st.sidebar.selectbox("Menu", [
                                  "Listar produtos", 
                                   "Inserir produto no carrinho",
                                   "Visualizar carrinho",
                                   "Comprar carrinho",
                                   "Listar minhas compras"])
        if op == "Listar produtos": pass
        if op == "Inserir produto no carrinho": pass
        if op == "Visualizar carrinho": pass
        if op == "Comprar carrinho": pass
        if op == "Listar minhas compras": pass
    def sidebar():
        if "cliente_id" not in st.session_state:
            IndexUI.menu_visitante()
        else:
            st.sidebar.write("Bem vindo(a)," + st.session_state["cliente_nome"])
            admin = st.session_state["cliente_nome"] == "admin"
            if admin: IndexUI.menu_admin()
            else: IndexUI.menu_cliente()
            IndexUI.sair_do_sistema()
    def sair_do_sistema():
        if st.sidebar.button("Sair"):
            del st.session_state["cliente_id"]
            del st.session_state["cliente_nome"]
            st.rerun()

    def main():
        #if "opcao" not in st.session_state: st.session_state["opcao"] = []
        #st.write(st.session_state)

        # verifica se existe o usuario admin
        View.cliente_criar_admin()
        #mostrar o menu lateral
        IndexUI.sidebar()
IndexUI.main()
