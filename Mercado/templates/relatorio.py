import streamlit as st
import pandas as pd
from view import View 

class RelatorioVendasUI:
    def main():
        st.header("📈 Relatório de Vendas e Consumo")
        st.markdown("---")
        
        
      
        dados_relatorio = View.relatorio_consumo()
        
            
            

        

        # Extrai os dados totais
        total_vendido = dados_relatorio['total_vendido']
        qtd_vendida = dados_relatorio['qtd_vendida']
        total_estoque_valor_venda = dados_relatorio['estoque_valor_venda']
        
        
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="💰 Total Arrecadado (Vendas)",
                value=f"R$ {total_vendido:,.2f}"
            )

        with col2:
            st.metric(
                label="🛒 Total de Itens Vendidos",
                value=f"{qtd_vendida:,.0f} un."
            )
        
        with col3:
            st.metric(
                label="💼 Valor Total do Estoque (Preço de Venda)",
                value=f"R$ {total_estoque_valor_venda:,.2f}"
            )
        
        st.markdown("---")


