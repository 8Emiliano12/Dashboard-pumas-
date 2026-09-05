import streamlit as st
import pandas as pd

# Configuración inicial de la página
st.set_page_config(page_title="Dashboard Pumas CU", layout="wide")
st.title("Panel de Control: Rendimiento y Bienestar - Pumas CU")

# Base de datos simulada (Prototipo inicial)
datos = {
    'Jugador': ['Juan Pérez', 'Carlos Ruiz', 'Luis Martínez'],
    'Posición': ['QB', 'WR', 'RB'],
    'Targets_Intentos': [20, 10, 15],
    'Completos_Recepciones': [12, 6, 10],
    'Yardas_Totales': [150, 80, 70],
    'Carga_Mental_Semanal': [6, 8, 4],  # Escala 1-10
    'Calidad_Sueno': [7, 5, 8],          # Horas promedio
    'Fatiga_Traslado': [8, 9, 3]         # Escala 1-10
}
df = pd.DataFrame(datos)

# Modelos Matemáticos Avanzados (Next Gen Stats)
df['Efectividad (%)'] = (df['Completos_Recepciones'] / df['Targets_Intentos']) * 100
df['Eficiencia (Yds/Intento)'] = df['Yardas_Totales'] / df['Targets_Intentos']
df['Proyeccion_Yardas'] = df['Eficiencia (Yds/Intento)'] * 10 # Proyección si tuviera 10 intentos extra

# Barra lateral interactiva para el Coach
st.sidebar.header("Filtros de Búsqueda")
posicion_filtro = st.sidebar.selectbox("Selecciona la Posición", df['Posición'].unique())
jugador_filtro = st.sidebar.selectbox("Selecciona al Jugador", df[df['Posición'] == posicion_filtro]['Jugador'])

# Aislamiento de datos del jugador seleccionado
stats_jugador = df[df['Jugador'] == jugador_filtro].iloc[0]

st.header(f"Análisis de: {jugador_filtro} ({stats_jugador['Posición']})")

# Módulo 1: KPIs de Rendimiento en el Campo
st.subheader("Métricas Deportivas")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Efectividad (Catch Rate / Completos)", value=f"{stats_jugador['Efectividad (%)']:.1f}%")
with col2:
    st.metric(label="Yardas Reales (Último Juego)", value=int(stats_jugador['Yardas_Totales']))
with col3:
    st.metric(label="Proyección de Yardas (Siguiente Juego)", value=int(stats_jugador['Proyeccion_Yardas']), delta="Basado en volumen esperado")

st.divider()

# Módulo 2: Intervención Psicológica
st.subheader("Monitoreo Psicodeportivo")
col4, col5, col6 = st.columns(3)
with col4:
    st.write(f"**Carga Académica/Mental:** {stats_jugador['Carga_Mental_Semanal']}/10")
with col5:
    st.write(f"**Calidad de Sueño:** {stats_jugador['Calidad_Sueno']} horas")
with col6:
    st.write(f"**Fatiga Acumulada:** {stats_jugador['Fatiga_Traslado']}/10")

# Motor de Alertas Automáticas
if stats_jugador['Carga_Mental_Semanal'] >= 8 or stats_jugador['Fatiga_Traslado'] >= 8:
    st.error("🚨 ALERTA: Atleta en zona de riesgo. Se sugiere intervención psicoeducativa u optimización de descanso.")
else:
    st.success("✅ Estado emocional y de fatiga dentro de rangos óptimos para competencia.")

st.divider()

# Módulo 3: Observaciones de Campo (Scouting)
st.subheader("Registro de Observaciones")
observaciones = st.text_area(f"Notas tácticas y conductuales sobre {jugador_filtro}:", placeholder="Ej: Lenguaje corporal tras soltar el pase, nivel de concentración en el huddle...")
