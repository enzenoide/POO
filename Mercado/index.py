import streamlit as st
from templates.mantercliente import ManterClienteUI
from templates.mantercategoria import ManterCategoriaUI
from templates.manterproduto import ManterProdutoUI
from templates.reajustarproduto import ReajustarProdutoUI

class IndexUI:
    def menu_admin():
        op = st.sidebar.selectbox("Menu", [
                                  "Cadastro de Categorias", 
                                   "Cadastro de Clientes",
                                   "Cadastro de Produtos",
                                   "Reajustar Produtos"])
        if op == "Cadastro de Categorias": ManterCategoriaUI.main()
        if op == "Cadastro de Clientes": ManterClienteUI.main()
        if op == "Cadastro de Produtos": ManterProdutoUI.main()
        if op == "Reajustar Produtos": ReajustarProdutoUI.main()
    def sidebar():
        IndexUI.menu_admin() 

    def main():
        IndexUI.sidebar()
IndexUI.main()
