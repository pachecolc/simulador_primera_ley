# GUÍA DE LABORATORIO
## Primera Ley de la Termodinámica y equivalente mecánico del calor

**Asignatura:** Biofísica  
**Programa:** Medicina / Ciencias de la Salud  
**Modalidad:** Laboratorio virtual con Streamlit  
**Aplicación:** `app.py`

---

## 1. Introducción
La primera ley de la termodinámica establece que la energía no se crea ni se destruye, sino que se transforma. En este laboratorio virtual se estudia cómo el **trabajo mecánico** realizado sobre un cilindro de aluminio puede transformarse en **energía térmica** por fricción.

La simulación reproduce un montaje con un **cilindro de aluminio**, una **masa colgante**, una **cuerda de nylon**, una **manivela** y un **termistor**. A medida que el sistema gira, el trabajo mecánico se disipa por fricción y aumenta la temperatura del cilindro. A partir de ello, el estudiante puede calcular el **equivalente mecánico del calor** y contrastarlo con el valor de referencia de **4.18 J/cal**.

---

## 2. Objetivos
### Objetivo general
Analizar la relación entre trabajo mecánico, variación de temperatura y energía térmica, aplicando la primera ley de la termodinámica.

### Objetivos específicos
1. Calcular el trabajo mecánico transferido al cilindro.
2. Determinar el aumento de temperatura del cilindro en función del número de vueltas.
3. Estimar el calor absorbido por el cilindro de aluminio.
4. Calcular el equivalente mecánico del calor en J/cal.
5. Comparar resultados del simulador con cálculos manuales.
6. Interpretar el modelo ideal y sus limitaciones.

---

## 3. Fundamento teórico
En términos generales, la primera ley se expresa como:

\[
\Delta U = Q + W
\]

En este simulador, se considera un caso ideal en el cual el trabajo por fricción incrementa la energía interna del cilindro y las pérdidas netas de calor al ambiente se aproximan a cero.

### Ecuaciones del simulador
**Trabajo mecánico:**
\[
W = 2\pi n r m g
\]

**Calor absorbido por el cilindro:**
\[
Q = m_{cilindro} c_e \Delta T
\]

**Cambio de temperatura:**
\[
\Delta T = T_f - T_i
\]

**Equivalente mecánico del calor:**
\[
E_q = \frac{W}{Q}
\]

**Calor específico del aluminio usado por la app:**
\[
c_e = 920\;J/(kg\cdot ^\circ C)
\]

**Relación temperatura-resistencia del termistor:**

- Montaje físico:
\[
T(^{\circ}C) = -20.5\ln(R)+119.4
\]

- Aplicativo virtual:
\[
T = \frac{217}{R^{0.13}} - 151
\]

---

## 4. Variables del simulador
### Variables independientes
- Masa colgante (kg)
- Radio del cilindro (cm)
- Masa del cilindro (g)
- Temperatura inicial (°C)
- Velocidad angular (rpm)
- Número máximo de vueltas
- Intervalo de medición
- Tipo de relación R–T del termistor

### Variables dependientes
- Tiempo (s)
- Resistencia del termistor, R (kOhm)
- Temperatura del cilindro, T (°C)
- Cambio de temperatura, ΔT (°C)
- Trabajo acumulado, W (J)
- Calor calorimétrico, Q (J y cal)
- Equivalente mecánico, W/Q (J/cal)

### Constantes del modelo
- Aceleración de la gravedad: **9.81 m/s²**
- Calor específico del aluminio: **920 J/(kg·°C)**
- Equivalencia de referencia: **4.18 J/cal**

---

## 5. Recursos visuales incorporados en la app
La carpeta `assets/` contiene tres imágenes educativas:
1. `aparato_equivalente_calor.png`
2. `energia_trabajo_a_calor.png`
3. `flujograma_experimento.png`

La aplicación verifica su existencia antes de mostrarlas. Si una imagen falta, aparece un aviso sin detener la app.

---

## 6. Instrucciones de uso de la app
### 6.1. Panel lateral
En `st.sidebar` configure:
- masa colgante;
- radio del cilindro;
- masa del cilindro;
- temperatura inicial;
- velocidad angular;
- vueltas finales;
- intervalo de medición;
- ecuación del termistor.

Use **“Restablecer valores de la guía”** para regresar a la condición base.

### 6.2. Pestaña **Simulación**
Aquí puede:
- responder una predicción conceptual;
- observar el fenómeno físico mediante una imagen o un esquema dinámico;
- visualizar la gráfica de temperatura vs número de vueltas;
- consultar la tabla de mediciones;
- descargar la tabla actual en CSV.

### 6.3. Pestaña **Análisis**
Aquí puede:
- visualizar la gráfica de trabajo vs temperatura;
- estimar el calor específico a partir de la pendiente;
- revisar el balance energético ideal;
- comparar cálculos manuales con el simulador;
- revisar las ecuaciones del termistor.

### 6.4. Pestaña **Experimentos guiados**
Muestra el flujograma y las actividades sugeridas para desarrollar el laboratorio.

### 6.5. Pestaña **Registro experimental**
Permite:
- registrar una medición;
- borrar todas las mediciones;
- visualizar una tabla acumulativa;
- exportar resultados en CSV y Excel.

---

## 7. Procedimiento general
1. Abra la aplicación en Streamlit.
2. Revise la imagen del montaje y el esquema de conversión de energía.
3. Defina las condiciones experimentales en la barra lateral.
4. Ejecute la simulación.
5. Observe la tabla de resultados y la gráfica de temperatura.
6. Analice el trabajo, el calor absorbido y el equivalente mecánico.
7. Registre las condiciones de interés.
8. Exporte sus datos para el informe.

---

## 8. Experimentos guiados
### Experimento 1. Condición basal
Use los valores por defecto de la guía:
- Temperatura inicial: 12 °C
- Velocidad angular: 100 rpm
- Masa colgante: 4.985 kg
- Radio: 2.4 cm
- Masa del cilindro: 250 g
- Vueltas finales: 100
- Intervalo de medición: 10 vueltas

**Actividad:** registre la evolución de T, W y Q.

### Experimento 2. Efecto del número de vueltas
Compare al menos tres condiciones:
- 50 vueltas
- 100 vueltas
- 150 vueltas

**Actividad:** determine si W, Q y ΔT crecen linealmente.

### Experimento 3. Efecto de la masa colgante
Compare tres masas colgantes manteniendo constantes las demás variables.

**Actividad:** analice cómo cambia el trabajo mecánico y la temperatura final.

### Experimento 4. Equivalente mecánico del calor
Seleccione una condición y calcule manualmente:
- W (J)
- ΔT (°C)
- Q (cal)
- W/Q (J/cal)

Luego compare con el simulador.

### Experimento 5. Estimación del calor específico
Use la gráfica **W vs T** y el valor de la pendiente.

**Actividad:** estime el calor específico del aluminio y compárelo con el valor teórico del simulador.

### Experimento 6. Investigación libre
Formule una pregunta propia, por ejemplo:
- ¿cómo cambia el tiempo experimental al variar rpm?
- ¿qué variable produce mayor cambio en ΔT?
- ¿qué sucede si se duplica la masa colgante?

---

## 9. Tabla sugerida para el registro de resultados
### 9.1. Tabla de medición por condición
| n (vueltas) | Tiempo (s) | R (kOhm) | T (°C) | ΔT (°C) | W (J) | Q (cal) | W/Q (J/cal) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 |  |  |  |  |  |  |  |
| 10 |  |  |  |  |  |  |  |
| 20 |  |  |  |  |  |  |  |
| ... |  |  |  |  |  |  |  |

### 9.2. Tabla de comparación manual vs simulador
| Magnitud | Manual | Simulador | Diferencia | % error |
|---|---:|---:|---:|---:|
| Trabajo W (J) |  |  |  |  |
| ΔT (°C) |  |  |  |  |
| Q (cal) |  |  |  |  |
| Equivalente (J/cal) |  |  |  |  |

---

## 10. Cálculos a realizar
1. Calcule manualmente el trabajo mecánico para una condición dada.
2. Calcule el incremento de temperatura usando la relación calorimétrica.
3. Calcule el calor absorbido en calorías.
4. Calcule el equivalente mecánico del calor.
5. Compare el resultado con 4.18 J/cal.

---

## 11. Preguntas de análisis
1. ¿Por qué aumentar la masa colgante incrementa el trabajo mecánico?
2. ¿Qué relación observa entre el número de vueltas y la temperatura final?
3. ¿Por qué en este modelo ideal las rpm cambian el tiempo, pero no el trabajo total para un mismo número de vueltas?
4. ¿Qué significado físico tiene el cociente W/Q?
5. ¿Por qué el valor experimental puede diferir del valor de referencia de 4.18 J/cal?
6. ¿Cómo se interpreta la primera ley en este experimento?
7. ¿Qué limitaciones tiene suponer que no hay pérdidas térmicas al ambiente?
8. ¿Qué aplicaciones biomédicas o tecnológicas pueden relacionarse con la transformación de energía mecánica en térmica?

---

## 12. Conclusiones esperadas
Al finalizar el laboratorio, el estudiante debe ser capaz de concluir que:
- el trabajo mecánico puede transformarse en energía térmica;
- el incremento de temperatura depende del trabajo transferido al sistema;
- el equivalente mecánico del calor relaciona cuantitativamente joules y calorías;
- el modelo ideal facilita la comprensión, pero no representa todas las pérdidas del sistema real.

---

## 13. Producto a entregar
Entregar un informe breve con:
1. objetivo;
2. fundamento teórico resumido;
3. tabla(s) de datos;
4. gráficas relevantes;
5. cálculos manuales;
6. comparación con el simulador;
7. respuestas a las preguntas de análisis;
8. conclusiones.

---

## 14. Criterios de evaluación sugeridos
| Criterio | Porcentaje |
|---|---:|
| Comprensión conceptual | 20% |
| Uso correcto del simulador | 15% |
| Registro y organización de datos | 15% |
| Cálculos manuales y comparación | 20% |
| Interpretación y análisis | 20% |
| Presentación del informe | 10% |

---

## 15. Limitaciones del modelo
- No se incluyen pérdidas térmicas cuantitativas al ambiente.
- El sistema se trata como ideal y homogéneo.
- Se asume transferencia eficiente del trabajo al cilindro.
- Las ecuaciones del termistor se usan con fines didácticos.

---

## 16. Bibliografía breve sugerida
- Material base de la guía de laboratorio de Primera Ley de la Termodinámica.
- Textos introductorios de Biofísica y Termodinámica.
- Recursos docentes sobre equivalente mecánico del calor y calorimetría.
