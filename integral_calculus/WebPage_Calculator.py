import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

# 1. Configuración de la página
st.set_page_config(page_title="Cálculo Diferencial MAC", layout="wide")

# 2. Barra lateral con el Logo de la UMNG, créditos y enlaces
with st.sidebar:
    # Ajustamos la ruta para que busque el logo en la misma carpeta del script
    try:
        st.image("logo_umng.png", width=120)
    except:
        st.write("Logo UMNG")
    
    st.title("Cálculo Diferencial MAC 📐")
    st.markdown("---")
    st.subheader("Creadores:")
    st.write("• Kevin Wilder Cardozo Vivas")
    st.write("• David Antonio Mora Forero")
    st.markdown("---")
    st.markdown("🛠 **Asistido por IA**")
    st.markdown("---")
    st.markdown("🔗 [Visita mis repositorios en GitHub](https://github.com/eljaimejia?tab=repositories)")

# Título principal
st.title("Calculadora de Sumas de Riemann")
st.write("Escribe tu función (ej: `sin(x)`, `exp(x)`, `log(x)`, `x**2`), ajusta los límites y mira la gráfica.")

# 3. Entradas principales
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    func_input = st.text_input("Ingresa la función f(x):", value="x**2")
with col2:
    a = st.number_input("Límite a:", value=0.0)
with col3:
    b = st.number_input("Límite b:", value=2.0)

try:
    # 4. Preparación matemática
    x = sp.symbols('x')
    f_sym = sp.sympify(func_input)
    f_num = sp.lambdify(x, f_sym, 'numpy')
    antiderivada = sp.integrate(f_sym, x)

    st.divider()

    st.subheader("Análisis de la Integral")
    col_int1, col_int2 = st.columns(2)
    with col_int1:
        st.markdown("**Integral Definida:**")
        st.latex(f"\\int_{{{a}}}^{{{b}}} {sp.latex(f_sym)} \\, dx")
    with col_int2:
        st.markdown("**Antiderivada:**")
        st.latex(f"\\int {sp.latex(f_sym)} \\, dx = {sp.latex(antiderivada)} + C")

    # 5. Controles
    col4, col5 = st.columns(2)
    with col4:
        method = st.selectbox("Método de Riemann:", ["Izquierda", "Derecha"])
    with col5:
        n = st.slider("Número de rectángulos (n):", 1, 200, 20)

    # 6. Cálculos
    integral_exacta = sp.integrate(f_sym, (x, a, b)).evalf()
    delta_x = (b - a) / n
    x_edges = np.linspace(a, b, n + 1)

    if method == "Izquierda":
        x_eval = x_edges[:-1]
        align = 'edge'
        width = delta_x
    else:
        x_eval = x_edges[1:]
        align = 'edge'
        width = -delta_x

    y_eval = f_num(x_eval)
    area_aprox = np.sum(y_eval * delta_x)
    error = abs(integral_exacta - area_aprox)

    st.divider()
    
    st.subheader("Resultados")
    c_a, c_b, c_dx, c_n = st.columns(4)
    c_a.metric("Límite a", f"{a}")
    c_b.metric("Límite b", f"{b}")
    c_dx.metric("Base (Δx)", f"{delta_x:.4f}")
    c_n.metric("Rectángulos (n)", f"{n}")

    c_res1, c_res2, c_res3 = st.columns(3)
    c_res1.metric("Área Real", f"{integral_exacta:.4f}")
    c_res2.metric("Suma Riemann", f"{area_aprox:.4f}")
    c_res3.metric("Error", f"{error:.4f}")

    # 7. Gráfica blindada
    st.subheader("Representación Gráfica")
    fig, ax = plt.subplots(figsize=(10, 5))
    
    margen = (b - a) * 0.1 if b != a else 1
    x_vals = np.linspace(a - margen, b + margen, 500)
    
    # Cálculo seguro de valores de y
    try:
        y_vals = f_num(x_vals)
        mask = np.isfinite(y_vals)
        ax.plot(x_vals[mask], y_vals[mask], 'b-', linewidth=2.5, label=f'$f(x) = {sp.latex(f_sym)}$')
    except:
        st.warning("La función no está definida en todo el rango.")

    ax.bar(x_eval, y_eval, width=width, align=align, alpha=0.5, color='orange', edgecolor='black', linewidth=1)
    
    ax.set_xlim(a - margen, b + margen)
    ax.axhline(0, color='black', linewidth=1) 
    ax.axvline(a, color='red', linestyle='--', alpha=0.7, label='Límite a') 
    ax.axvline(b, color='red', linestyle='--', alpha=0.7, label='Límite b') 
    ax.legend()
    ax.grid(True, linestyle=':', alpha=0.6)

    st.pyplot(fig)
    plt.close(fig)

except Exception as e:
    st.error("Revisa la función o los límites. Asegúrate de usar la sintaxis correcta.")