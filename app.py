with st.expander("Objetivo de aprendizaje, modelo y uso de imágenes", expanded=False):
    st.markdown("""
**Objetivos:** calcular el trabajo mecánico, el aumento de temperatura y la energía térmica ganada por un cilindro de aluminio; determinar el equivalente mecánico del calor y relacionarlo con la primera ley.

**Representación visual de la app**
- **Fenómeno físico:** cilindro, cuerda, masa colgante y sensor de temperatura.
- **Modelo matemático:** gráficas de temperatura, trabajo y calorimetría en función de las variables seleccionadas.

**Ecuaciones principales**
""")
    st.latex(r"\Delta U = Q + W")
    st.latex(r"W = 2\pi n r\,m_{\mathrm{colgante}}g")
    st.latex(r"Q = m_{\mathrm{cilindro}}c_e\Delta T")
    st.latex(r"E_q = \frac{W}{Q}")
    st.markdown(r"""
En el modelo ideal de esta app, el trabajo de fricción transferido al cilindro se refleja como aumento de su energía interna, de modo que
\(W\approx m c\Delta T\). El término \(Q=m c\Delta T\) se muestra como **medida calorimétrica equivalente** de ese incremento y no se suma nuevamente a \(W\).

Las imágenes generadas para la app se guardan en la carpeta `assets/`. Si alguna no existe, la aplicación mostrará un aviso sin detener la ejecución.
""")


with st.expander("Contexto fisiológico, biomédico y limitaciones", expanded=False):
    st.markdown("""
**¿Por qué es importante en ciencias de la salud?**  
La termodinámica permite entender fenómenos como la producción de calor en el músculo, la disipación térmica en tejidos, la eficiencia energética del organismo y el comportamiento de equipos biomédicos que convierten energía mecánica en térmica.

**Aplicaciones biomédicas y clínicas**
- generación de calor por contracción muscular y fricción interna;
- control térmico en instrumental biomédico;
- interpretación de balance energético en sistemas biológicos;
- comprensión de la equivalencia entre distintas formas de energía en procesos fisiológicos.

**Clasificación didáctica del laboratorio**
Este laboratorio se clasifica como **D. híbrido**: el montaje real puede conservarse como experiencia física, mientras que el análisis, la predicción, la medición virtual y la comparación de condiciones pueden realizarse con la app.

**Supuestos y limitaciones**
- Se asume un cilindro homogéneo de aluminio.
- La energía mecánica se transfiere idealmente al cilindro por fricción.
- No se modelan pérdidas netas de calor al ambiente.
- Las ecuaciones del termistor se usan con propósito didáctico.
""")

# ============================================================
# CONTROLES
# ============================================================
