import streamlit as st
from equacao import Equacao

class EquacaoUI:
    def main():
        st.header("Equação do II grau: y = ax² + bx + c")

        a = st.number_input("a", value=1.0)
        b = st.number_input("b", value=0.0)
        c = st.number_input("c", value=0.0)

        if st.button("Calcular"):
            e = Equacao(a, b, c)
            st.write(e)