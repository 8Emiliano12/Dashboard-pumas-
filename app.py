import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Pumas CU", layout="wide")
st.title("Panel de Control: Rendimiento y Bienestar - Pumas CU")

# 1. Memoria de la sesión con nuevas métricas defensivas
if 'df' not in st.session_state:
    datos_iniciales = {
        'Jugador': ['Juan Pérez', 'Carlos Ruiz', 'Luis Martínez', 'Pedro Gómez', 'Mario Ayala'],
        'Posición': ['QB', 'WR', 'RB', 'LB', 'CB'],
        'Unidad': ['Ofensiva', 'Ofensiva', 'Ofensiva', 'Defensiva', 'Defensiva'],
        'Targets_Intentos': [20, 10, 15, 0, 0],
        'Completos_Recepciones': [12, 6, 10, 0, 0],
        'Yardas_Totales': [150, 80, 70, 0, 0],
        'Tackleadas': [0, 0, 0, 8, 4],
        'Intercepciones': [0, 0, 0, 1, 2],
        'Carga_Mental_Semanal': [6, 8, 4, 7, 5],
        'Calidad_Sueno': [7, 5, 8, 6, 7],
        'Fatiga_Traslado': [8, 9, 3, 5, 4]
    }
    st.session_state.df = pd.DataFrame(datos_iniciales)

# 2. Pestañas de Navegación (Ahora son 3)
tab1, tab2, tab3 = st.tabs(["📊 Análisis Individual", "⚙️ Base de Datos Global", "📈 Rendimiento del Equipo"])

# --- PESTAÑA 3: RENDIMIENTO DEL EQUIPO ---
with tab3:
    st.header("Análisis General por Unidades")
    df_global = st.session_state.df.copy()
    
    col_ofensiva, col_defensiva = st.columns(2)
    
    # Métricas Ofensivas
    with col_ofensiva:
        st.subheader("🏈 Unidad Ofensiva")
        ofensiva_df = df_global[df_global['Unidad'] == 'Ofensiva']
        
        yardas_totales = ofensiva_df['Yardas_Totales'].sum()
        pases_completos = ofensiva_df['Completos_Recepciones'].sum()
        carga_ofensiva = ofensiva_df['Carga_Mental_Semanal'].mean()
        
        st.metric("Yardas Totales Producidas", int(yardas_totales))
        st.metric("Pases/Recepciones Completadas", int(pases_completos))
        st.metric("Promedio Carga Mental (Ofensiva)", f"{carga_ofensiva:.1f}/10")
        
    # Métricas Defensivas
    with col_defensiva:
        st.subheader("🛡️ Unidad Defensiva")
        defensiva_df = df_global[df_global['Unidad'] == 'Defensiva']
        
        tackleadas_totales = defensiva_df['Tackleadas'].sum()
        intercepciones_totales = defensiva_df['Intercepciones'].sum()
        carga_defensiva = defensiva_df['Carga_Mental_Semanal'].mean()
        
        st.metric("Tackleadas Totales", int(tackleadas_totales))
        st.metric("Intercepciones Generadas", int(intercepciones_totales))
        st.metric("Promedio Carga Mental (Defensiva)", f"{carga_defensiva:.1f}/10")

# --- PESTAÑA 2: BASE DE DATOS Y EDICIÓN ---
with tab2:
    st.subheader("Gestión del Roster y Estadísticas")
    st.write("Edita los números, agrega o elimina jugadores directamente en la tabla.")
    
    df_editado = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True)
    
    if st.button("Guardar Cambios Globales"):
        st.session_state.df = df_editado
        st.success("¡Base de datos actualizada correctamente!")

# --- PESTAÑA 1: ANÁLISIS DEL COACH ---
with tab1:
    df = st.session_state.df.copy()
    
    df['Targets_Intentos_Calc'] = df['Targets_Intentos'].replace(0, 1) 
    df['Efectividad (%)'] = (df['Completos_Recepciones'] / df['Targets_Intentos_Calc']) * 100
    df['Eficiencia (Yds/Intento)'] = df['Yardas_Totales'] / df['Targets_Intentos_Calc']
    df['Proyeccion_Yardas'] = df['Eficiencia (Yds/Intento)'] * 10

    st.sidebar.header("Filtros de Búsqueda")
    if not df.empty:
        unidad_filtro = st.sidebar.selectbox("Selecciona la Unidad", df['Unidad'].unique())
        posiciones_disponibles = df[df['Unidad'] == unidad_filtro]['Posición'].unique()
        
        if len(posiciones_disponibles) > 0:
            posicion_filtro = st.sidebar.selectbox("Selecciona la Posición", posiciones_disponibles)
            jugadores_disponibles = df[df['Posición'] == posicion_filtro]['Jugador']
            
            if not jugadores_disponibles.empty:
                jugador_filtro = st.sidebar.selectbox("Selecciona al Jugador", jugadores_disponibles)
                stats_jugador = df[df['Jugador'] == jugador_filtro].iloc[0]

                st.header(f"Análisis de: {jugador_filtro} ({stats_jugador['Posición']})")
                
                st.subheader("Métricas Deportivas")
                col1, col2, col3 = st.columns(3)
                
                # Mostrar métricas según la unidad
                if unidad_filtro == 'Ofensiva':
                    with col1:
                        st.metric(label="Efectividad", value=f"{stats_jugador['Efectividad (%)']:.1f}%")
                    with col2:
                        st.metric(label="Yardas Reales", value=int(stats_jugador['Yardas_Totales']))
                    with col3:
                        st.metric(label="Proyección de Yardas", value=int(stats_jugador['Proyeccion_Yardas']))
                else:
                    with col1:
                        st.metric(label="Tackleadas", value=int(stats_jugador['Tackleadas']))
                    with col2:
                        st.metric(label="Intercepciones", value=int(stats_jugador['Intercepciones']))
                    with col3:
                        st.metric(label="Impacto Defensivo", value="Alto")

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
