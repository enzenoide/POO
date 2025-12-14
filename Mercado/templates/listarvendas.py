import streamlit as st
from view import View


class ListarvendasUI:
    def main():
        st.header("🛒 Histórico de Vendas")
        
        
        vendas = View.cliente_listar_vendas() 

        # Itera sobre cada VENDA (venda)
        # Usamos reversed para mostrar as vendas mais recentes primeiro
        for venda in reversed(vendas): 
            
            # Formata os dados da Venda
            venda_id = venda['id']
            total_venda = venda['total']
            # PEGA O NOME DO CLIENTE (Chave adicionada no View.cliente_listar_vendas)
            nome_cliente = venda.get('nome_cliente', 'Cliente Desconhecido') 
            
            # Verifica se o campo 'data' é uma string (formato JSON/ISO como "YYYY-MM-DDT...").
            # SE for uma string, usa .split('T')[0] para obter apenas a parte da data.
            # SENÃO (else), assume que pode ser um objeto datetime ou outra string
            # com espaço como separador, converte para string e usa .split(' ')[0] para extrair a data.
            data_venda = venda["data"].split('T')[0] if isinstance(venda["data"], str) else str(venda["data"]).split(' ')[0]
            
            
            
            with st.expander(f"💰 Venda ID: **{venda_id}** | Cliente: **{nome_cliente}** | Total: R$ **{total_venda:.2f}** | Data: {data_venda}"):
                
                itens_na_venda = venda.get("carrinho", []) 
                
                if not itens_na_venda:
                    st.warning("Nenhum item detalhado encontrado nesta venda.")
                    continue
                
                st.markdown("---") 
                
                
                num_colunas = 3
                colunas = st.columns(num_colunas)
                
                for index, item in enumerate(itens_na_venda):
                    col = colunas[index % num_colunas]
                    
                    descricao = item.get("descricao_produto", "Produto não encontrado")
                    quantidade = item.get("qtd", 0)
                    preco_unitario = item.get("preco", 0.0)
                    total_item = quantidade * preco_unitario
                    
                    
                    url_imagem = item.get("url_imagem", "assets/placeholder.png")
                    
                    with col:
                        with st.container(border=True):
                            
                            img_col1, img_col2, img_col3 = st.columns([1, 4, 1])
                            with img_col2:
                                try:
                                    st.image(url_imagem, width=150)
                                except:
                                    st.warning("(Imagem não carregada)")

                            st.markdown("---") 

                            st.markdown(f"**{descricao}**")
                            st.markdown(f"R$ {preco_unitario:.2f} (un.)")
                            st.markdown(f"**Qtd vendida:** {quantidade}")
                            st.markdown(f"**Subtotal:** R$ {total_item:.2f}")

                st.markdown("---")
          