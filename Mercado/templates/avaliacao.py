import streamlit as st
from view import View
from models.produto import ProdutoDAO

class AvaliacoesUI:
    def main():
        st.header("🛠️ Avaliações dos Clientes")

        avaliacoes = View.avaliacao_listar()

        if not avaliacoes:
            st.info("Nenhuma avaliação cadastrada.")
            return

        for avaliacao in reversed(avaliacoes):

            with st.container(border=True):

                st.markdown(
                    f"""
                    **🧾 Venda:** {avaliacao["venda"]["id"]}  
                    **👤 Cliente:** {avaliacao["cliente"]}  
                    **📅 Data:** {avaliacao["data"]}
                    """
                )

                st.markdown("### 🎮 Itens da Compra")

                for item in avaliacao["venda"]["itens"]:
                    produto = ProdutoDAO.listar_id(item.get_idproduto())

                    descricao = produto.get_descricao() if produto else "Produto removido"
                    preco = produto.get_preco() if produto else 0.0
                    qtd = item.get_qtd()

                    st.markdown(
                        f"- **{descricao}** | "
                        f"Qtd: {qtd} | "
                        f"R$ {preco:.2f}"
                    )
                st.markdown("---")
                st.markdown(f"📝 *{avaliacao['comentario']}*")

                col1, col2 = st.columns([4, 1])

                with col2:
                    if st.button(
                        "🗑️ Excluir",
                        key=f"excluir_{avaliacao['id']}"
                    ):
                        View.avaliacao_excluir(avaliacao["id"])
                        st.success("Avaliação excluída.")
                        st.rerun()