# Simulador: Primera Ley de la Termodinámica

Laboratorio virtual interactivo en **Python + Streamlit + Plotly** orientado a estudiantes de Medicina y otras ciencias de la salud. La app simula la transformación de **trabajo mecánico en energía térmica** mediante fricción sobre un cilindro de aluminio y permite calcular el **equivalente mecánico del calor**.

---

## 1. Descripción
Este simulador reproduce un montaje didáctico con:
- cilindro de aluminio;
- manivela;
- cuerda de nylon;
- masa colgante;
- termistor/multímetro.

A partir de variables controlables, el estudiante puede:
- **observar** el sistema;
- **predecir** tendencias;
- **modificar** condiciones;
- **simular** el comportamiento;
- **medir** temperatura, resistencia, trabajo y calor;
- **registrar** múltiples mediciones;
- **analizar** relaciones entre variables;
- **interpretar** el significado termodinámico;
- **aplicar** los resultados a contextos biomédicos;
- **concluir** con base en evidencia.

---

## 2. Objetivo
Analizar la relación entre trabajo mecánico, cambio de temperatura y calorimetría en un cilindro de aluminio, aplicando la primera ley de la termodinámica y estimando el equivalente mecánico del calor.

---

## 3. Modelo científico
### Ecuaciones principales
\[
\Delta U = Q + W
\]

\[
W = 2\pi n r m g
\]

\[
Q = m_{cilindro} c_e \Delta T
\]

\[
E_q = \frac{W}{Q}
\]

### Parámetros usados por la app
- gravedad: **9.81 m/s²**
- calor específico del aluminio: **920 J/(kg·°C)**
- referencia del equivalente mecánico del calor: **4.18 J/cal**

### Relación del termistor
**Montaje físico:**
\[
T(^{\circ}C)=-20.5\ln(R)+119.4
\]

**Aplicativo virtual:**
\[
T=\frac{217}{R^{0.13}}-151
\]

### Supuestos del modelo
- el cilindro es homogéneo;
- el trabajo mecánico se transfiere idealmente al cilindro;
- no se modelan pérdidas térmicas netas al ambiente;
- las rpm afectan el tiempo experimental, pero no el trabajo total para un mismo número de vueltas.

---

## 4. Características de la app
- interfaz compacta con **sidebar**;
- pestañas para simulación, análisis, experimentos guiados y registro;
- gráficas interactivas con **Plotly**;
- imágenes educativas en `assets/`;
- verificación de existencia de imágenes;
- cálculo manual vs simulador;
- registro de múltiples mediciones con `st.session_state`;
- exportación a **CSV** y **Excel**;
- guía de laboratorio y guía docente incluidas.

---

## 5. Instalación local
### Requisitos
- Python 3.10 o superior

### Instalar dependencias
```bash
pip install -r requirements.txt
```

### Ejecutar localmente
```bash
streamlit run app.py
```

---

## 6. Estructura del proyecto
```text
simulador_primera_ley/
├── app.py
├── requirements.txt
├── README.md
├── GUIA_LABORATORIO.md
├── GUIA_DOCENTE.md
└── assets/
    ├── aparato_equivalente_calor.png
    ├── energia_trabajo_a_calor.png
    └── flujograma_experimento.png
```

---

## 7. Uso
1. Abra la app.
2. Revise el contexto visual y teórico.
3. Defina las condiciones experimentales en la barra lateral.
4. Ejecute la simulación.
5. Observe la tabla y las gráficas.
6. Analice el trabajo, el calor y el equivalente mecánico.
7. Registre la medición si desea comparar condiciones.
8. Exporte los datos en CSV o Excel.

---

## 8. Despliegue en Streamlit Community Cloud
Esta app está preparada para desplegarse con:
- **Repository:** su repositorio GitHub
- **Branch:** `main`
- **Main file path:** `app.py`

### Pasos sugeridos
1. Cree un repositorio en GitHub.
2. Suba el contenido completo de esta carpeta.
3. Inicie sesión en Streamlit Community Cloud.
4. Seleccione el repositorio.
5. Indique `app.py` como archivo principal.
6. Despliegue la app.

---

## 9. Limitaciones
- Es un modelo ideal y didáctico.
- No representa pérdidas térmicas reales al ambiente.
- No incorpora variaciones del calor específico con la temperatura.
- No sustituye completamente la experiencia experimental física.

---

## 10. Clasificación del laboratorio
**D. Híbrido**  
El montaje real puede mantenerse, mientras que el análisis, la comparación de condiciones y la interpretación pueden realizarse en la simulación.

---

## 11. Referencias
- Guía de laboratorio de Primera Ley de la Termodinámica aportada por el usuario.
- Material docente de Biofísica.
- Principios generales de termodinámica y calorimetría.
