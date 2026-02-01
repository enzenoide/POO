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
        Produtos = View.produto_listar()
        if not Produtos:
            st.write("Nenhum produto cadastrado")
            return

        num_colunas = 2
        colunas = st.columns(num_colunas)

        largura_imagem = 180

        for index, produto in enumerate(Produtos):
            col = colunas[index % num_colunas]

            with col:
                with st.container(border=True):

                    caminho_imagem = produto.get_imagem()

                    # Imagem
                    if caminho_imagem:
                        img_c1, img_c2, img_c3 = st.columns([1, 4, 1])
                        with img_c2:
                            st.image(
                                caminho_imagem,
                                caption=f"ID: {produto.get_id()}",
                                width=largura_imagem
                            )
                    else:
                        st.markdown("**(Sem imagem)**")

                    # Dados
                    st.markdown(f"### {produto.get_descricao()}")
                    st.markdown(f"**ID:** {produto.get_id()}")
                    st.markdown(f"**Preço:** R$ {produto.get_preco():.2f}")
                    st.markdown(f"**Estoque:** {produto.get_estoque()}")


                    categoria = View.categoria_listar_id(produto.get_idcategoria())
                    plataforma = View.plataforma_listar_id(produto.get_plataforma())
                    desenvolvedora = View.desenvolvedora_listar_id(produto.get_desenvolvedora())

                    st.markdown(
                        f"""
                        **Categoria:** {categoria.get_descricao() if categoria else "—"}  
                        **Plataforma:** {plataforma.get_nome() if plataforma else "—"}  
                        **Desenvolvedora:** {desenvolvedora.get_nome() if desenvolvedora else "—"}
                        """
                    )

    def inserir():
        descricao = st.text_input("Nome do produto:")
        preco = st.number_input("Preço:", value=0.01, min_value=0.01)
        estoque = st.number_input("Estoque:", value=1, min_value=1, step=1)

        
        categorias = View.categoria_listar()
        if not categorias:
            st.warning("Cadastre uma categoria antes de inserir produtos.")
            return

        opcoes_categorias = {
            f"{c.get_descricao()} (ID: {c.get_id()})": c.get_id()
            for c in categorias
        }

        categoria_sel = st.selectbox(
            "Categoria:",
            options=list(opcoes_categorias.keys())
        )
        idcategoria = opcoes_categorias[categoria_sel]

       
        plataformas = View.plataforma_listar()
        if not plataformas:
            st.warning("Cadastre uma plataforma antes de inserir produtos.")
            return

        opcoes_plataformas = {
            f"{p.get_nome()} (ID: {p.get_id()})": p.get_id()
            for p in plataformas
        }

        plataforma_sel = st.selectbox(
            "Plataforma:",
            options=list(opcoes_plataformas.keys())
        )
        idplataforma = opcoes_plataformas[plataforma_sel]

        
        desenvolvedoras = View.desenvolvedora_listar()
        if not desenvolvedoras:
            st.warning("Cadastre uma desenvolvedora antes de inserir produtos.")
            return

        opcoes_desenvolvedoras = {
            f"{d.get_nome()} (ID: {d.get_id()})": d.get_id()
            for d in desenvolvedoras
        }

        desenvolvedora_sel = st.selectbox(
            "Desenvolvedora:",
            options=list(opcoes_desenvolvedoras.keys())
        )
        iddesenvolvedora = opcoes_desenvolvedoras[desenvolvedora_sel]

        
        imagem = st.file_uploader(
            "Imagem do produto",
            type=["png", "jpg", "jpeg"]
        )

        if st.button("Inserir"):
            try:
                if not imagem:
                    st.error("Selecione uma imagem do produto.")
                    return

                os.makedirs("assets", exist_ok=True)

                nome_arquivo = f"{descricao.replace(' ', '_')}.png"
                caminho_imagem = f"assets/{nome_arquivo}"

                with open(caminho_imagem, "wb") as f:
                    f.write(imagem.getbuffer())

                View.produto_inserir(
                    descricao,
                    preco,
                    estoque,
                    idcategoria,
                    caminho_imagem,
                    idplataforma,
                    iddesenvolvedora
                )

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

                View.produto_atualizar(id, descricao, preco, estoque, idcategoria, caminho_imagem,plataforma,desenvolvedora)

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
