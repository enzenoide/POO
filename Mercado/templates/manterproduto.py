import streamlit as st
from view import View
import pandas as pd
import time
import os

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
        preco = st.number_input("Me informe o preço do produto: ", value=0.01, min_value=0.01)
        estoque = st.number_input("Me informe a quantidade do produto em estoque: ", value=1.0, min_value=1.0)
        idcategoria = st.text_input("Me informe o ID da categoria: ", value="1")
        desenvolvedora = st.text_input("Me informe o ID da desenvolvedora: ",value="1")
        plataforma = st.text_input("Me informe o ID da plataforma: ",value="1")

        imagem = st.file_uploader(
            "Imagem do produto",
            type=["png", "jpg", "jpeg"]
        )

        if st.button("Inserir"):
            try:
                if imagem is None:
                    st.error("Selecione uma imagem do produto.")
                    return

                os.makedirs("assets/", exist_ok=True)

                nome_arquivo = f"{descricao.replace(' ', '_')}.png"
                caminho_imagem = f"assets/{nome_arquivo}"

                with open(caminho_imagem, "wb") as f:
                    f.write(imagem.getbuffer())

                View.produto_inserir(descricao, preco, estoque, idcategoria, caminho_imagem,desenvolvedora,plataforma)

                st.success("Produto inserido com sucesso!")
                time.sleep(2)
                st.rerun()

            except Exception as erro:
                st.error(erro)
    def atualizar():
        Produtos = View.produto_listar()
        
        if len(Produtos) == 0: 
            st.write("Nenhum Produto registrado.")
            return

       
        categorias = View.categoria_listar()
        
        
        opcoes_categorias = {f"{c.get_descricao()} (ID: {c.get_id()})": c.get_id() for c in categorias}
        
        if not opcoes_categorias:
            st.warning("Não há categorias cadastradas. Cadastre uma categoria antes de atualizar produtos.")
            return

       
        op = st.selectbox("Atualização do Produto: ", Produtos)
        id = op.get_id()
        
        
        
        
        id_categoria_atual = op.get_idcategoria()
        categoria_atual_str = next(
            (desc_id for desc_id, cat_id in opcoes_categorias.items() if str(cat_id) == str(id_categoria_atual)),
            "Categoria não encontrada (ID: " + str(id_categoria_atual) + ")"
        )
        
        
        descricao = st.text_input("Nova descrição: ", value=op.get_descricao()) 
        
        preco = st.number_input(
            "Novo preço: ", 
            value=op.get_preco(),
            min_value=0.01 
        )
        
        estoque = st.number_input(
            "Novo estoque: ", 
            value=op.get_estoque(),
            min_value=0.0,
            step=1.0
        )
        
        
        categoria_selecionada = st.selectbox(
            "Nova Categoria: ",
            options=list(opcoes_categorias.keys()),
            index=list(opcoes_categorias.keys()).index(categoria_atual_str) if categoria_atual_str in opcoes_categorias else 0
        )
        
       
        idcategoria = opcoes_categorias[categoria_selecionada]

        nova_imagem = st.file_uploader(
        "Nova imagem (opcional)",
        type=["png", "jpg", "jpeg"]
    )

        if st.button("Atualizar"):
            try:
                caminho_imagem = op.get_imagem()

                if nova_imagem:
                    os.makedirs("assets/", exist_ok=True)
                    nome_arquivo = f"{descricao.replace(' ', '_')}.png"
                    caminho_imagem = f"assets/{nome_arquivo}"

                    with open(caminho_imagem, "wb") as f:
                        f.write(nova_imagem.getbuffer())

                View.produto_atualizar(id, descricao, preco, estoque, idcategoria, caminho_imagem,desenvolvedora,plataforma)

                st.success("Produto atualizado com sucesso!")
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
                    st.success("Produto excluído com sucesso")
                    time.sleep(2)
                    st.rerun()
                except Exception as erro:
                    st.error(erro)
