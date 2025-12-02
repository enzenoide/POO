import streamlit as st
from view import View
import pandas as pd

class ListarComprasUI:
    def main():
        st.header("Suas Compras")
        compras = View.cliente_listar_compras(st.session_state["cliente_id"])
        
        if len(compras) == 0:
            st.write("Nenhuma compra registrada.")
            return
        
        list_dic = []

        for v in compras:
            carrinho_formatado = []
            for item in v["carrinho"]:
                nome = item.get("descricao_produto", "Produto não encontrado")
                qtd = item.get("qtd", 0)
                carrinho_formatado.append(f"{qtd}x {nome}")

            list_dic.append({
                "id": v["id"],
                "data": v["data"],
                "carrinho": "\n".join(carrinho_formatado),
                "total": v.get("total", 0),
                "idcliente": v["idcliente"],
                "nome_cliente": v.get("nome_cliente", "Desconhecido")
            })
        
        df = pd.DataFrame(list_dic)

        st.dataframe(df,hide_index=True,column_order=["id", "data", "carrinho", "total", "idcliente", "nome_cliente"])