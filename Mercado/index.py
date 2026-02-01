import streamlit as st
from templates.mantercliente import ManterClienteUI
from templates.mantercategoria import ManterCategoriaUI
from templates.manterproduto import ManterProdutoUI
from templates.reajustarproduto import ReajustarProdutoUI
from templates.login import LoginUI
from templates.abrirconta import AbrirContaUI
from view import View
from templates.listarprodutos import ListarProdutosUI
from templates.carrinho import CarrinhoUI
from templates.listarcompras import ListarComprasUI
from templates.listarvendas import ListarvendasUI
from templates.relatorio import RelatorioVendasUI
from templates.desenvolvedora import DesenvolvedoraUI
from templates.plataforma import PlataformaUI
from templates.mantercupom import CupomDescontoUI
from templates.avaliacao import AvaliacoesUI
class IndexUI:
    def menu_visitante():
        op = st.sidebar.selectbox("Menu", [
                                    "Entrar no Sistema", 
                                    "Abrir conta",
                                    ])
        if op == "Entrar no Sistema": LoginUI.main()
        if op == "Abrir conta": AbrirContaUI.main()
    def menu_admin():
        op = st.sidebar.selectbox("Menu", [
                                  "Cadastro de Categorias", 
                                   "Cadastro de Clientes",
                                   "Cadastro de Produtos",
                                   "Cadastro de Desenvolvedora",
                                   "Cadastro de Plataforma",
                                   "Cadastro de Cupons",
                                   "Avaliações",
                                   "Reajustar Produtos",
                                   "Listar Vendas",
                                   "Relatório de Vendas"])
       # st.session_state["opcao"].append(op) 
        if op == "Cadastro de Categorias": ManterCategoriaUI.main()
        if op == "Cadastro de Clientes": ManterClienteUI.main()
        if op == "Cadastro de Produtos": ManterProdutoUI.main()
        if op == "Cadastro de Desenvolvedora": DesenvolvedoraUI.main()
        if op == "Cadastro de Plataforma": PlataformaUI.main()
        if op == "Cadastro de Cupons": CupomDescontoUI.main()
        if op == "Avaliações": AvaliacoesUI.main()
        if op == "Reajustar Produtos": ReajustarProdutoUI.main()
        if op == "Listar Vendas": ListarvendasUI.main()
        if op == "Relatório de Vendas": RelatorioVendasUI.main()
    def menu_cliente():
        op = st.sidebar.selectbox("Menu", [
                                  "Listar produtos", 
                                   "Inserir produto no carrinho",
                                   "Visualizar carrinho",
                                   "Comprar carrinho",
                                   "Listar minhas compras"])
        if op == "Listar produtos": ListarProdutosUI.main()
        if op == "Inserir produto no carrinho": CarrinhoUI.inserir()
        if op == "Visualizar carrinho": CarrinhoUI.listar()
        if op == "Comprar carrinho": CarrinhoUI.comprar()
        if op == "Listar minhas compras": ListarComprasUI.main()
    def sidebar():
        if "cliente_id" not in st.session_state: IndexUI.menu_visitante()
        else:
            st.sidebar.write("Bem-vindo(a), " + st.session_state["cliente_nome"] + "😊")
            # usuário está logado, verifica se é o admin
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
