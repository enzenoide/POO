import streamlit as st
from view import View
import time
import pandas as pd


class ListarProdutosUI:
    def main():
        st.header("Lista de Produtos")

        Produtos = View.produto_listar()
        if not Produtos:
            st.write("Nenhum produto cadastrado")
            return

        num_colunas = 2
        colunas = st.columns(num_colunas)
        largura_imagem = 200

        for index, produto in enumerate(Produtos):
            col = colunas[index % num_colunas]

            with col:
                with st.container(border=True):

                    # =====================
                    # IMAGEM
                    # =====================
                    caminho_imagem = produto.get_imagem()
                    if caminho_imagem:
                        c1, c2, c3 = st.columns([1, 4, 1])
                        with c2:
                            st.image(
                                caminho_imagem,
                                caption=f"{produto.get_descricao()}",
                                width=largura_imagem
                            )
                    else:
                        st.markdown("**(Sem imagem)**")

                    # =====================
                    # DADOS DO PRODUTO
                    # =====================
                    st.markdown(f"### {produto.get_descricao()}")
                    st.markdown(f"**Preço:** R$ {produto.get_preco():.2f}")

                    # =====================
                    # DESENVOLVEDORA / PLATAFORMA
                    # =====================
                    desenvolvedora = View.desenvolvedora_listar_id(
                        produto.get_desenvolvedora()
                    )
                    plataforma = View.plataforma_listar_id(
                        produto.get_plataforma()
                    )

                    st.markdown(
                        f"""
                        **Desenvolvedora:** {desenvolvedora.get_nome() if desenvolvedora else "—"}  
                        **Plataforma:** {plataforma.get_nome() if plataforma else "—"}
                        """
                    )



