import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
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

            x = np.linspace(-20, 20, 400)
            y = a * x**2 + b * x + c

            fig, ax = plt.subplots()
            ax.plot(x, y)
            st.pyplot(fig)