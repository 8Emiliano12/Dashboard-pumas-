import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Pumas CU", layout="wide")
st.title("Panel de Control: Rendimiento y Bienestar - Pumas CU")

# 1. Memoria de la sesión: Evita que los datos se borren al interactuar
if 'df' not in st.session_state:
    datos_iniciales = {
        'Jugador': ['Juan Pérez', 'Carlos Ruiz', 'Luis Martínez'],
        'Posición': ['QB', 'WR', 'RB'],
        'Targets_Intentos': [20, 10, 15],
        'Completos_Recepciones': [12, 6, 10],
        'Yardas_Totales': [150, 80, 70],
        'Carga_Mental_Semanal': [6, 8, 4],
        'Calidad_Sueno': [7, 5, 8],
        'Fatiga_Traslado': [8, 9, 3]
    }
    st.session_state.df = pd.DataFrame(datos_iniciales)

# 2. Pestañas de Navegación
tab1, tab2 = st.tabs(["📊 Análisis Individual", "⚙️ Base de Datos Global"])

# --- PESTAÑA 2: BASE DE DATOS Y EDICIÓN ---
with tab2:
    st.subheader("Gestión del Roster y Estadísticas")
    st.write("Edita los números haciendo doble clic en las celdas. Para **agregar** un jugador, haz clic en la última fila vacía. Para **eliminar**, selecciona la fila y presiona 'Suprimir/Delete' en tu teclado.")
    
    # Tabla interactiva
    df_editado = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True)
    
    if st.button("Guardar Cambios"):
        st.session_state.df = df_editado
        st.success("¡Base de datos actualizada correctamente!")

# --- PESTAÑA 1: ANÁLISIS DEL COACH ---
with tab1:
    df = st.session_state.df.copy()
    
    # Prevención de errores si una fila está vacía
    df['Targets_Intentos'] = df['Targets_Intentos'].replace(0, 1) 
    
    # Cálculos
    df['Efectividad (%)'] = (df['Completos_Recepciones'] / df['Targets_Intentos']) * 100
    df['Eficiencia (Yds/Intento)'] = df['Yardas_Totales'] / df['Targets_Intentos']
    df['Proyeccion_Yardas'] = df['Eficiencia (Yds/Intento)'] * 10

    st.sidebar.header("Filtros de Búsqueda")
    if not df.empty:
        posicion_filtro = st.sidebar.selectbox("Selecciona la Posición", df['Posición'].unique())
        jugadores_disponibles = df[df['Posición'] == posicion_filtro]['Jugador']
        
        if not jugadores_disponibles.empty:
            jugador_filtro = st.sidebar.selectbox("Selecciona al Jugador", jugadores_disponibles)
            stats_jugador = df[df['Jugador'] == jugador_filtro].iloc[0]

            st.header(f"Análisis de: {jugador_filtro} ({stats_jugador['Posición']})")
            
            st.subheader("Métricas Deportivas")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="Efectividad", value=f"{stats_jugador['Efectividad (%)']:.1f}%")
            with col2:
                st.metric(label="Yardas Reales", value=int(stats_jugador['Yardas_Totales']))
            with col3:
                st.metric(label="Proyección de Yardas", value=int(stats_jugador['Proyeccion_Yardas']))

            st.divider()

            st.subheader("Monitoreo Psicodeportivo")
            col4, col5, col6 = st.columns(3)
            with col4:
                st.write(f"**Carga Mental:** {stats_jugador['Carga_Mental_Semanal']}/10")
            with col5:
                st.write(f"**Calidad de Sueño:** {stats_jugador['Calidad_Sueno']} horas")
            with col6:
                st.write(f"**Fatiga:** {stats_jugador['Fatiga_Traslado']}/10")

            if stats_jugador['Carga_Mental_Semanal'] >= 8 or stats_jugador['Fatiga_Traslado'] >= 8:
                st.error("🚨 ALERTA: Atleta en zona de riesgo psico-físico.")
            else:
                st.success("✅ Estado emocional y de fatiga óptimos.")
