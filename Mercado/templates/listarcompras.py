import streamlit as st
from view import View


class ListarComprasUI:
    def main():
        st.header("🛒 Histórico de Compras")

        id_cliente = st.session_state["cliente_id"]
        compras = View.cliente_listar_compras(id_cliente)

        if not compras:
            st.info("Nenhuma compra registrada.")
            return

        for venda in reversed(compras):

            venda_id = venda['id']
            total = venda['total']
            data_venda = venda['data']

            with st.expander(
                f"💰 Venda #{venda_id} | Total: R$ {total:.2f} | Data: {data_venda}"
            ):

                # ================= ITENS =================
                colunas = st.columns(3)
                for i, item in enumerate(venda["carrinho"]):
                    with colunas[i % 3]:
                        with st.container(border=True):
                            st.image(item["url_imagem"], width=140)
                            st.markdown(f"**{item['descricao_produto']}**")
                            st.markdown(f"Qtd: {item['qtd']}")
                            st.markdown(f"Preço: R$ {item['preco']:.2f}")

                st.markdown("---")

                # ================= AVALIAÇÃO =================
                avaliacao = View.avaliacao_buscar_por_venda(venda_id)

                if avaliacao:
                    st.success("✅ Compra avaliada")
                    st.markdown(f"📝 *{avaliacao.get_texto()}*")
                else:
                    deseja = st.checkbox(
                        "Deseja avaliar esta compra?",
                        key=f"avaliar_{venda_id}"
                    )

                    if deseja:
                        texto = st.text_area(
                            "Escreva sua avaliação:",
                            key=f"texto_{venda_id}"
                        )

                        if st.button(
                            "Enviar avaliação",
                            key=f"btn_{venda_id}"
                        ):
                            try:
                                View.avaliacao_inserir(
                                    venda_id,
                                    id_cliente,
                                    texto
                                )
                                st.success("Avaliação enviada!")
                                st.rerun()
                            except Exception as e:
                                st.error(e)