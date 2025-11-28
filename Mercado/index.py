import streamlit as st
from templates.mantercliente import ManterClienteUI
from templates.mantercategoria import ManterCategoriaUI
from templates.manterproduto import ManterProdutoUI
from templates.reajustarproduto import ReajustarProduto

class IndexUI:
    def menu_admin():
        op = st.sidebar.selectbox("Menu", [
                                  "Cadastro de Categorias", 
                                   "Cadastro de Clientes",
                                   "Cadastro de Produtos",
                                   "Reajustar produtos"])
        if op == "Cadastro de Categorias": ManterCategoriaUI.main()
        if op == "Cadastro de Clientes": ManterClienteUI.main()
        if op == "Cadastro de Produtos": ManterProdutoUI.main()
        if op == "Reajustar Produtos": ReajustarProduto.main()
    def sidebar():
        IndexUI.menu_admin() 

    def main():
        IndexUI.sidebar()
IndexUI.main()
