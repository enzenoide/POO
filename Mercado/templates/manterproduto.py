import streamlit as st
from view import View
import pandas as pd
import time

class ManterProdutoUI:
    def main():
        st.header("Cadastro de Produtos")
        tab1,tab2,tab3,tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterProdutoUI.listar()
        with tab2: ManterProdutoUI.inserir()
        with tab3: ManterProdutoUI.atualizar()
        with tab4: ManterProdutoUI.excluir()
    def listar():
        Produtos= View.produto_listar()
        if len(Produtos) == 0: st.write("Nenhum produto cadastrado")
        else:
            list_dic = []
            for obj in Produtos: list_dic.append(obj.to_json())
            df = pd.DataFrame(list_dic)
            st.dataframe(df, hide_index = True, column_order = ["id","descricao","preco","estoque","idcategoria"])
    def inserir():
        descricao = st.text_input("Me informe o nome do produto: ")
        preco = st.number_input("Me informe o novo preço do produto: ")
        estoque = st.number_input("Me informe a quantidade do produto em estoque: ")
        idcategoria = st.text_input("Me informe o ID da categoria: ")
        if st.button("Inserir"):
            try:
                View.produto_inserir(descricao,preco,estoque,idcategoria)
                st.success("Produto inserido com sucesso!")
                time.sleep(2)
                st.rerun()
            except ValueError:
                st.error("O preço,estoque e ID precisam ser números válidos e positivos")
            except KeyError as erro:
                st.error(f"falta o campo {erro} na entrada de dados")
            except Exception as erro:
                st.error(erro)
    def atualizar():
        Produtos = View.produto_listar()
        if len(Produtos) == 0: st.write("Nenhumo Produto registado.")
        else:
            op = st.selectbox("Atualização do Produto: ", Produtos)
            id = op.get_id()
            descricao = st.text_input("Nova descrição: ")
            preco = st.number_input("Novo preço: ", op.get_preco())
            estoque = st.number_input("Novo estoque: ", op.get_estoque())
            idcategoria = st.text_input("ID da categoria: ", op.get_idcategoria())
            if st.button("Atualizar"):
                try:
                    View.produto_atualizar(id,descricao,preco,estoque,idcategoria)
                    st.success("Produto atualizada com sucesso")
                    time.sleep(2)
                    st.rerun()
                except Exception as erro:
                    st.error(erro)
    def excluir():
        Produtos = View.produto_listar()
        if len(Produtos) == 0: st.write("Nenhum Produto registrada")
        else:
            op = st.selectbox("Exclusão de Produtos", Produtos)
            if st.button("Excluir"):
                try:
                    id = op.get_id()
                    View.produto_excluir(id)
                    st.success("Produto excluída com sucesso")
                    time.sleep(2)
                    st.rerun()
                except Exception as erro:
                    st.error(erro)
