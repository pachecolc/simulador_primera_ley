from io import BytesIO
from pathlib import Path
import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# CONFIGURACION GENERAL
# ============================================================
st.set_page_config(
    page_title="Primera Ley de la Termodinamica",
    page_icon="🔥",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"
GUIDE_STUDENT = BASE_DIR / "GUIA_LABORATORIO.md"
GUIDE_TEACHER = BASE_DIR / "GUIA_DOCENTE.md"

# Constantes y parametros usados por la guia / simulador
G = 9.81                  # m/s^2
C_AL_J = 920.0            # J/(kg·°C)
C_AL_CAL = 0.220          # cal/(g·°C)
J_PER_CAL_REF = 4.18      # J/cal

GUIDE_DEFAULTS = {
    "mass_hanging": 4.985,   # kg, procedimiento virtual
    "radius_cm": 2.4,        # cm
    "mass_cylinder_g": 250,  # g
    "temp_initial": 12.0,    # °C
    "rpm": 100,
    "max_turns": 100,
    "step_turns": 10,
    "thermistor": "Aplicativo virtual - Ec. (5)",
}

for key, value in GUIDE_DEFAULTS.items():
    st.session_state.setdefault(key, value)
st.session_state.setdefault("experiments", [])

# ============================================================
# UTILIDADES
# ============================================================
def asset_path(filename: str):
    path = ASSETS / filename
    return path if path.exists() else None


def show_asset(filename: str, caption: str):
    path = asset_path(filename)
    if path is not None:
        st.image(str(path), caption=caption, use_container_width=True)
    else:
        st.warning(f"No se encontro la imagen '{filename}' en la carpeta assets/. La app puede continuar sin ella.")


def read_text_file(path: Path):
    if path.exists():
        return path.read_text(encoding="utf-8")
    return None


# ============================================================
# MODELO CIENTIFICO
# ============================================================
def work_j(turns, radius_m, mass_hanging_kg):
    """Trabajo mecanico: W = 2*pi*n*r*m*g."""
    turns = np.asarray(turns, dtype=float)
    return 2.0 * math.pi * turns * radius_m * mass_hanging_kg * G


def temp_from_resistance(r_kohm, thermistor):
    """Convierte R (kOhm) a T (°C) segun la ecuacion seleccionada."""
    r = np.asarray(r_kohm, dtype=float)
    out = np.full_like(r, np.nan, dtype=float)
    valid = r > 0
    if not np.any(valid):
        return out
    if thermistor.startswith("Aplicativo"):
        out[valid] = 217.0 / np.power(r[valid], 0.13) - 151.0
    else:
        out[valid] = -20.5 * np.log(r[valid]) + 119.4
    return out


def resistance_from_temp(temp_c, thermistor):
    """Invierte las ecuaciones del termistor para simular la lectura del multimetro."""
    t = np.asarray(temp_c, dtype=float)
    out = np.full_like(t, np.nan, dtype=float)
    if thermistor.startswith("Aplicativo"):
        den = t + 151.0
        valid = den > 0
        out[valid] = np.power(217.0 / den[valid], 1.0 / 0.13)
    else:
        out = np.exp((119.4 - t) / 20.5)
    return out


def build_profile(max_turns, step_turns, radius_m, mass_hanging_kg,
                  mass_cylinder_kg, temp_initial_c, rpm, thermistor):
    max_turns = int(max_turns)
    step_turns = int(step_turns)
    rpm = float(rpm)

    turns = list(range(0, max_turns + 1, step_turns))
    if turns[-1] != max_turns:
        turns.append(max_turns)
    turns = np.array(sorted(set(turns)), dtype=int)

    w = work_j(turns, radius_m, mass_hanging_kg)
    denominator = mass_cylinder_kg * C_AL_J
    delta_t = np.divide(w, denominator, out=np.zeros_like(w, dtype=float), where=denominator > 0)
    temp = temp_initial_c + delta_t
    resistance = resistance_from_temp(temp, thermistor)
    q_j = mass_cylinder_kg * C_AL_J * delta_t
    q_cal = mass_cylinder_kg * 1000.0 * C_AL_CAL * delta_t
    eq = np.divide(w, q_cal, out=np.full_like(w, np.nan, dtype=float), where=q_cal > 0)
    time_s = np.divide(turns * 60.0, rpm, out=np.zeros_like(turns, dtype=float), where=rpm > 0)

    return pd.DataFrame({
        "Vueltas, n": turns,
        "Tiempo (s)": time_s,
        "R (kOhm)": resistance,
        "T (°C)": temp,
        "Delta T (°C)": delta_t,
        "W (J)": w,
        "Q calorimetrico (J)": q_j,
        "Q calorimetrico (cal)": q_cal,
        "W/Q (J/cal)": eq,
    })


def experimental_excel_bytes(df_exp, df_profile):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df_exp.to_excel(writer, sheet_name="Experimentos", index=False)
        df_profile.to_excel(writer, sheet_name="Perfil_actual", index=False)
    buffer.seek(0)
    return buffer.getvalue()


# ============================================================
# GRAFICAS
# ============================================================
def schematic_figure(temp_c, turns, mass_kg, radius_cm, rpm):
    fig = go.Figure()
    fig.add_shape(type="rect", x0=1.3, x1=3.3, y0=2.4, y1=4.2,
                  line=dict(width=2), fillcolor="#d9dde3")
    fig.add_shape(type="line", x0=1.3, x1=3.3, y0=2.65, y1=2.65, line=dict(width=5))
    fig.add_shape(type="line", x0=3.3, x1=4.8, y0=3.3, y1=3.3, line=dict(width=3))
    fig.add_shape(type="line", x0=4.8, x1=4.8, y0=3.3, y1=1.55, line=dict(width=3))
    fig.add_shape(type="rect", x0=4.25, x1=5.35, y0=0.75, y1=1.55,
                  line=dict(width=2), fillcolor="#eceff3")
    fig.add_annotation(x=2.3, y=4.65, text="↻", showarrow=False, font=dict(size=34))
    fig.add_annotation(x=2.3, y=3.35, text=f"Cilindro de Al<br><b>{temp_c:.2f} °C</b>",
                       showarrow=False, align="center")
    fig.add_annotation(x=4.8, y=1.15, text=f"m = {mass_kg:.3f} kg",
                       showarrow=False, align="center")
    fig.add_annotation(x=2.3, y=1.75,
                       text=f"n = {turns} vueltas · r = {radius_cm:.2f} cm · {rpm:.0f} rpm",
                       showarrow=False)
    fig.update_xaxes(visible=False, range=[0.5, 5.8])
    fig.update_yaxes(visible=False, range=[0.3, 5.1], scaleanchor="x", scaleratio=1)
    fig.update_layout(height=390, margin=dict(l=5, r=5, t=15, b=5),
                      showlegend=False, plot_bgcolor="white", paper_bgcolor="white")
    return fig


def temperature_figure(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Vueltas, n"], y=df["T (°C)"], mode="lines+markers",
        name="Temperatura",
        hovertemplate="Vueltas: %{x}<br>T: %{y:.2f} °C<extra></extra>",
    ))
    last = df.iloc[-1]
    fig.add_trace(go.Scatter(
        x=[last["Vueltas, n"]], y=[last["T (°C)"]], mode="markers",
        marker=dict(size=13, symbol="diamond"), name="Condicion actual",
        hovertemplate="Condicion actual<br>n=%{x}<br>T=%{y:.2f} °C<extra></extra>",
    ))
    fig.add_hline(y=float(df.iloc[0]["T (°C)"]), line_dash="dash", annotation_text="T inicial")
    fig.update_layout(height=390, margin=dict(l=10, r=10, t=35, b=10),
                      xaxis_title="Numero de vueltas, n", yaxis_title="Temperatura (°C)",
                      legend=dict(orientation="h", y=1.08))
    return fig


def work_temperature_figure(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["T (°C)"], y=df["W (J)"], mode="lines+markers",
        hovertemplate="T: %{x:.2f} °C<br>W: %{y:.2f} J<extra></extra>",
    ))
    fig.update_layout(height=390, margin=dict(l=10, r=10, t=35, b=10),
                      xaxis_title="Temperatura (°C)", yaxis_title="Trabajo acumulado, W (J)")
    return fig


def comparison_figure(exp_df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=exp_df["Experimento"], y=exp_df["Eq (J/cal)"], mode="markers+lines",
        name="Mediciones", hovertemplate="Experimento %{x}<br>%{y:.3f} J/cal<extra></extra>"
    ))
    fig.add_hline(y=J_PER_CAL_REF, line_dash="dash", annotation_text="Referencia 4.18 J/cal")
    fig.update_layout(height=360, xaxis_title="Experimento", yaxis_title="Equivalente (J/cal)",
                      margin=dict(l=10, r=10, t=35, b=10))
    return fig


# ============================================================
# ENCABEZADO Y CONTEXTO
# ============================================================
st.title("🔥 Primera Ley de la Termodinámica")
st.subheader("Equivalente mecánico del calor")
st.caption(
    "Laboratorio virtual para Biofísica: observar → predecir → modificar variables → simular → "
    "medir → registrar → analizar → interpretar → aplicar → concluir."
)

hero1, hero2 = st.columns(2)
with hero1:
    show_asset("aparato_equivalente_calor.png", "Montaje conceptual del equivalente mecánico del calor.")
with hero2:
    show_asset("energia_trabajo_a_calor.png", "Trabajo mecánico transformado en energía térmica por fricción.")

with st.expander("Objetivo de aprendizaje y modelo científico", expanded=False):
    st.markdown("""
**Objetivo de aprendizaje:** relacionar el trabajo mecánico con el aumento de energía interna y temperatura de un cilindro de aluminio, y estimar el equivalente mecánico del calor.

**Variables independientes:** masa colgante, radio del cilindro, masa del cilindro, temperatura inicial, rpm, número de vueltas e intervalo de medición.

**Variables dependientes:** tiempo, resistencia del termistor, temperatura, cambio de temperatura, trabajo, calor calorimétrico y W/Q.

**Constantes:** gravedad, calor específico del aluminio y referencia 4.18 J/cal.
""")
    st.latex(r"\Delta U = Q + W")
    st.latex(r"W = 2\pi n r\,m_{\mathrm{colgante}}g")
    st.latex(r"Q = m_{\mathrm{cilindro}}c_e\Delta T")
    st.latex(r"E_q = \frac{W}{Q}")
    st.markdown(r"""
En el modelo ideal de la app, el trabajo por fricción aumenta la energía interna del cilindro. La expresión
\(m c\Delta T\) se utiliza como **medida calorimétrica equivalente** del incremento energético y no se suma nuevamente al trabajo para evitar doble conteo.
""")

with st.expander("Contexto fisiológico, biomédico y limitaciones", expanded=False):
    st.markdown("""
**Relevancia para ciencias de la salud**  
La termodinámica ayuda a interpretar la producción y disipación de calor en el organismo, la eficiencia energética de sistemas biológicos y el funcionamiento de equipos biomédicos que transforman energía.

**Aplicaciones para discusión**
- generación de calor durante la contracción muscular;
- balance energético y termorregulación;
- disipación térmica en tejidos y dispositivos;
- conversión entre formas de energía en procesos fisiológicos.

**Clasificación del laboratorio:** **D. híbrido.** El montaje físico puede conservarse, mientras que la predicción, comparación de condiciones, análisis y registro pueden realizarse virtualmente.

**Supuestos y limitaciones**
- cilindro homogéneo de aluminio;
- transferencia ideal de trabajo por fricción;
- sin pérdidas térmicas netas al ambiente;
- las rpm modifican el tiempo, no el trabajo total para un mismo número de vueltas;
- las ecuaciones del termistor se usan con fines didácticos.
""")

# ============================================================
# CONTROLES
# ============================================================
st.sidebar.header("Condiciones experimentales")
if st.sidebar.button("Restablecer valores de la guía", use_container_width=True):
    for key, value in GUIDE_DEFAULTS.items():
        st.session_state[key] = value
    st.rerun()

with st.sidebar.form("control_form"):
    mass_hanging = st.number_input("Masa colgante (kg)", min_value=0.10, max_value=20.0,
                                   step=0.005, format="%.3f", key="mass_hanging")
    radius_cm = st.number_input("Radio del cilindro (cm)", min_value=0.50, max_value=10.0,
                                step=0.10, format="%.2f", key="radius_cm")
    mass_cylinder_g = st.number_input("Masa del cilindro (g)", min_value=50, max_value=2000,
                                      step=10, key="mass_cylinder_g")
    temp_initial = st.number_input("Temperatura inicial (°C)", min_value=-20.0, max_value=60.0,
                                   step=0.5, key="temp_initial")
    rpm = st.number_input("Velocidad angular (rpm)", min_value=10, max_value=500,
                          step=10, key="rpm")
    max_turns = st.number_input("Vueltas finales", min_value=10, max_value=500,
                                step=10, key="max_turns")
    step_turns = st.selectbox("Intervalo de medición (vueltas)", [5, 10, 20], key="step_turns")
    thermistor = st.selectbox(
        "Relación R-T del termistor",
        ["Aplicativo virtual - Ec. (5)", "Montaje físico - Ec. (4)"],
        key="thermistor",
    )
    st.form_submit_button("Simular / actualizar", type="primary", use_container_width=True)

st.sidebar.caption(
    "Modelo ideal: para el mismo número de vueltas, las rpm cambian el tiempo de ejecución, pero no el trabajo total."
)

# Calculo de la condicion actual
radius_m = radius_cm / 100.0
mass_cylinder_kg = mass_cylinder_g / 1000.0
df = build_profile(max_turns, step_turns, radius_m, mass_hanging,
                   mass_cylinder_kg, temp_initial, rpm, thermistor)
last = df.iloc[-1]
eq_mech = float(last["W/Q (J/cal)"])
eq_error = abs(eq_mech - J_PER_CAL_REF) / J_PER_CAL_REF * 100.0

# ============================================================
# PESTANAS PRINCIPALES
# ============================================================
tab_sim, tab_analysis, tab_guided, tab_log, tab_guide = st.tabs([
    "🔬 Simulación",
    "📈 Análisis",
    "🧪 Experimentos guiados",
    "🗂️ Registro experimental",
    "📘 Guía de laboratorio",
])

with tab_sim:
    st.markdown("### 1. Predecir")
    prediction = st.radio(
        "Si aumenta la masa colgante y todo lo demás permanece constante, ¿qué ocurrirá con ΔT después del mismo número de vueltas?",
        ["Aumentará", "Disminuirá", "No cambiará"],
        horizontal=True,
        key="prediction_mass",
    )

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Trabajo W", f"{last['W (J)']:.2f} J")
    c2.metric("Temperatura final", f"{last['T (°C)']:.2f} °C")
    c3.metric("ΔT", f"{last['Delta T (°C)']:.2f} °C")
    c4.metric("Q calorimétrico", f"{last['Q calorimetrico (cal)']:.2f} cal")
    c5.metric("Equivalente", f"{eq_mech:.3f} J/cal")
    c6.metric("Error vs 4.18", f"{eq_error:.2f} %")

    if st.checkbox("Mostrar retroalimentación de la predicción", key="show_prediction_feedback"):
        if prediction == "Aumentará":
            st.success("Correcto: W es proporcional a la masa colgante y, en este modelo, un W mayor produce un ΔT mayor.")
        else:
            st.info("En el modelo ideal, W = 2πnrm g. Si aumenta la masa colgante, aumenta W y también ΔT.")

    st.markdown("### 2. Observar y simular")
    col_physical, col_math = st.columns([1, 1.05])
    with col_physical:
        st.markdown("**Fenómeno físico**")
        img_tab, sketch_tab = st.tabs(["Imagen", "Esquema dinámico"])
        with img_tab:
            show_asset("aparato_equivalente_calor.png", "Aparato del equivalente mecánico del calor.")
        with sketch_tab:
            st.plotly_chart(
                schematic_figure(float(last["T (°C)"]), int(last["Vueltas, n"]),
                                 mass_hanging, radius_cm, rpm),
                use_container_width=True,
                config={"displaylogo": False},
            )
    with col_math:
        st.markdown("**Gráfica / modelo matemático**")
        st.plotly_chart(temperature_figure(df), use_container_width=True,
                        config={"displaylogo": False})

    st.markdown("### 3. Medir")
    table_view = df.copy()
    for col in table_view.columns[1:]:
        table_view[col] = table_view[col].round(4)
    st.dataframe(table_view, use_container_width=True, hide_index=True)
    st.download_button(
        "Descargar tabla actual (CSV)",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name="perfil_primera_ley_termodinamica.csv",
        mime="text/csv",
    )

with tab_analysis:
    st.markdown("### Analizar: trabajo, temperatura y calor específico")
    a1, a2 = st.columns(2)
    with a1:
        st.plotly_chart(work_temperature_figure(df), use_container_width=True,
                        config={"displaylogo": False})
    with a2:
        if np.ptp(df["T (°C)"].to_numpy()) > 1e-12:
            slope, intercept = np.polyfit(df["T (°C)"], df["W (J)"], 1)
            c_est = slope / mass_cylinder_kg
        else:
            slope, intercept, c_est = np.nan, np.nan, np.nan
        st.latex(r"W \approx m_{\mathrm{cilindro}}c_e(T-T_i)")
        st.latex(r"\frac{dW}{dT}=m_{\mathrm{cilindro}}c_e")
        st.metric("Pendiente W vs T", f"{slope:.2f} J/°C")
        st.metric("c estimado", f"{c_est:.1f} J/(kg·°C)")
        st.caption(f"Valor usado por la app: {C_AL_J:.0f} J/(kg·°C).")

    st.markdown("### Interpretar: balance energético del modelo")
    b1, b2, b3, b4 = st.columns(4)
    delta_u = float(last["W (J)"])
    q_ambient = 0.0
    closure = abs(float(last["Q calorimetrico (J)"]) - delta_u)
    b1.metric("W sobre el cilindro", f"+{last['W (J)']:.2f} J")
    b2.metric("Q ambiente (ideal)", f"{q_ambient:.2f} J")
    b3.metric("ΔU ideal", f"{delta_u:.2f} J")
    b4.metric("|mcΔT - ΔU|", f"{closure:.3e} J")
    st.info(
        "Para este simulador ideal se aproxima el intercambio térmico neto con el ambiente a cero. "
        "El trabajo por fricción aumenta la energía interna y mcΔT estima calorimétricamente ese mismo incremento."
    )

    concept1, concept2 = st.columns([1.05, 0.95])
    with concept1:
        show_asset("energia_trabajo_a_calor.png", "Conversión de trabajo mecánico en energía térmica.")
    with concept2:
        st.markdown("### Cálculo manual vs simulador")
        with st.form("manual_calc"):
            m1, m2, m3 = st.columns(3)
            manual_w = m1.number_input("W manual (J)", min_value=0.0, value=0.0, step=1.0)
            manual_dt = m2.number_input("ΔT manual (°C)", min_value=0.0, value=0.0, step=0.1)
            manual_qcal = m3.number_input("Q manual (cal)", min_value=0.0, value=0.0, step=1.0)
            compare = st.form_submit_button("Comparar")
        if compare:
            rows = []
            pairs = [
                ("Trabajo W (J)", manual_w, float(last["W (J)"])),
                ("ΔT (°C)", manual_dt, float(last["Delta T (°C)"])),
                ("Q (cal)", manual_qcal, float(last["Q calorimetrico (cal)"])),
            ]
            for name, manual, sim in pairs:
                if manual > 0:
                    diff = manual - sim
                    err = abs(diff) / abs(sim) * 100 if sim != 0 else np.nan
                    rows.append([name, manual, sim, diff, err])
            if manual_w > 0 and manual_qcal > 0:
                manual_eq = manual_w / manual_qcal
                diff = manual_eq - eq_mech
                err = abs(diff) / abs(eq_mech) * 100 if eq_mech != 0 else np.nan
                rows.append(["Equivalente (J/cal)", manual_eq, eq_mech, diff, err])
            if rows:
                comp = pd.DataFrame(rows, columns=["Magnitud", "Manual", "Simulador", "Diferencia", "% error"])
                st.dataframe(comp.round(4), use_container_width=True, hide_index=True)
            else:
                st.warning("Ingrese al menos un valor manual mayor que cero para comparar.")

    with st.expander("Relaciones del termistor"):
        st.markdown("**Montaje físico:**")
        st.latex(r"T(^{\circ}C)=-20.5\ln(R)+119.4")
        st.markdown("**Aplicativo virtual:**")
        st.latex(r"T=\frac{217}{R^{0.13}}-151")
        st.caption("R se expresa en kΩ. La app invierte estas ecuaciones para simular la lectura de resistencia correspondiente a cada temperatura.")

with tab_guided:
    st.markdown("### Aplicar: secuencia experimental")
    show_asset("flujograma_experimento.png", "Flujograma del experimento virtual.")

    st.markdown(r"""
**Experimento 1 — Condición basal.** Restablezca los valores de la guía: \(T_i=12\,°C\), 100 rpm, masa colgante de 4.985 kg, radio de 2.4 cm, masa del cilindro de 250 g y 100 vueltas. Registre los valores cada 10 vueltas.

**Experimento 2 — Variar el número de vueltas.** Compare 50, 100 y 150 vueltas. Prediga primero cómo cambiarán \(W\), \(\Delta T\) y \(Q\). Determine si las tendencias son lineales.

**Experimento 3 — Variar la masa colgante.** Compare al menos tres masas manteniendo constantes \(n\), \(r\), \(m_{cilindro}\) y \(T_i\). Analice la relación masa → trabajo → temperatura.

**Experimento 4 — Comparación cuantitativa.** Calcule manualmente \(W\), \(Q\) y \(W/Q\) para una condición y compare con el simulador usando diferencia y % error.

**Experimento 5 — Aplicación biomédica.** Discuta la analogía entre conversión de energía y producción/disipación de calor en sistemas biológicos. Identifique al menos una similitud y una limitación de la analogía.

**Experimento 6 — Investigación libre.** Formule una pregunta propia, proponga una hipótesis, seleccione la variable independiente, registre varias mediciones, exporte los datos y redacte una conclusión basada en tendencias.
""")
    st.warning(
        "Limitación del modelo: no se incluye una ecuación cuantitativa de pérdidas térmicas al ambiente. "
        "Por ello, las rpm cambian el tiempo, pero no el trabajo total para un mismo número de vueltas."
    )

with tab_log:
    st.markdown("### Registrar y comparar mediciones")
    condition = (
        f"n={int(max_turns)}; m={mass_hanging:.3f} kg; r={radius_cm:.2f} cm; "
        f"m_cil={mass_cylinder_g} g; Ti={temp_initial:.1f} °C; rpm={int(rpm)}"
    )
    r1, r2 = st.columns(2)
    if r1.button("Registrar medición", type="primary", use_container_width=True):
        st.session_state.experiments.append({
            "Experimento": len(st.session_state.experiments) + 1,
            "Condición": condition,
            "Vueltas": int(max_turns),
            "Masa colgante (kg)": float(mass_hanging),
            "Radio (cm)": float(radius_cm),
            "Masa cilindro (g)": int(mass_cylinder_g),
            "Ti (°C)": float(temp_initial),
            "Tf (°C)": float(last["T (°C)"]),
            "rpm": int(rpm),
            "Tiempo (s)": float(last["Tiempo (s)"]),
            "W (J)": float(last["W (J)"]),
            "Q (cal)": float(last["Q calorimetrico (cal)"]),
            "Eq (J/cal)": float(eq_mech),
            "Error vs 4.18 (%)": float(eq_error),
        })
        st.success("Medición registrada.")

    if r2.button("Borrar todas las mediciones", use_container_width=True):
        st.session_state.experiments = []
        st.rerun()

    if st.session_state.experiments:
        exp_df = pd.DataFrame(st.session_state.experiments)
        st.dataframe(exp_df.round(4), use_container_width=True, hide_index=True)
        st.plotly_chart(comparison_figure(exp_df), use_container_width=True,
                        config={"displaylogo": False})
        d1, d2 = st.columns(2)
        d1.download_button(
            "Descargar experimentos (CSV)",
            data=exp_df.to_csv(index=False).encode("utf-8-sig"),
            file_name="experimentos_primera_ley.csv",
            mime="text/csv",
            use_container_width=True,
        )
        d2.download_button(
            "Descargar experimentos (Excel)",
            data=experimental_excel_bytes(exp_df, df),
            file_name="experimentos_primera_ley.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
    else:
        st.info("Aún no hay mediciones registradas. Ejecute una condición y presione 'Registrar medición'.")

with tab_guide:
    st.markdown("### Guía de laboratorio del estudiante")
    guide_text = read_text_file(GUIDE_STUDENT)
    if guide_text:
        g1, g2 = st.columns([1, 1])
        g1.download_button(
            "Descargar GUIA_LABORATORIO.md",
            data=guide_text.encode("utf-8"),
            file_name="GUIA_LABORATORIO.md",
            mime="text/markdown",
            use_container_width=True,
        )
        teacher_text = read_text_file(GUIDE_TEACHER)
        if teacher_text:
            g2.download_button(
                "Descargar GUIA_DOCENTE.md",
                data=teacher_text.encode("utf-8"),
                file_name="GUIA_DOCENTE.md",
                mime="text/markdown",
                use_container_width=True,
            )
        st.divider()
        st.markdown(guide_text)
    else:
        st.warning("No se encontró GUIA_LABORATORIO.md en la carpeta del proyecto.")

st.divider()
st.caption(
    "Modelo educativo ideal basado en cilindro de aluminio, fricción mecánica y termistor. "
    "Proyecto preparado para GitHub y Streamlit Community Cloud."
)
