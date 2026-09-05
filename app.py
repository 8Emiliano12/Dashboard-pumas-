import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Pumas CU", layout="wide")
st.title("Panel de Control: Rendimiento y Bienestar - Pumas CU")

# 1. Memoria de la sesión con Roster Real 2026 y Número de Jersey
if 'df' not in st.session_state:
    datos_iniciales = {
        'Jersey': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'Jugador': [
            'Josh Alexander Morfín González', 'Raul Rodrigo Blanco Ruiz', 'Aaron Soriano Vacasoydel', 
            'Leonardo David Garza Peña', 'Diego Mercado Sánchez', 'Julio Cesar Hernández Hernández',
            'Abraham González López', 'Luis Miguel Bañuelos Medina', 'Luis Higelin Castañeda',
            'Joaquin Aramis Carrillo Palma', 'Emiliano Sánchez Hernández', 'Raymundo Licea Gómez',
            'Christopher Bryan Cardona Padrón'
        ],
        'Posición': ['DL', 'WR', 'DB', 'QB', 'LB', 'DB', 'LB', 'DB', 'DB', 'DL', 'QB', 'DL', 'WR'],
        'Unidad': ['Defensiva', 'Ofensiva', 'Defensiva', 'Ofensiva', 'Defensiva', 'Defensiva', 'Defensiva', 'Defensiva', 'Defensiva', 'Defensiva', 'Ofensiva', 'Defensiva', 'Ofensiva'],
        'Targets_Intentos': [0]*13,
        'Completos_Recepciones': [0]*13,
        'Yardas_Totales': [0]*13,
        'Tackleadas': [0]*13,
        'Intercepciones': [0]*13,
        'Carga_Mental_Semanal': [0]*13,
        'Calidad_Sueno': [0]*13,
        'Fatiga_Traslado': [0]*13
    }
    st.session_state.df = pd.DataFrame(datos_iniciales)

# 2. Pestañas de Navegación
tab1, tab2, tab3 = st.tabs(["📊 Análisis Individual", "⚙️ Base de Datos Global", "📈 Rendimiento del Equipo"])

# --- PESTAÑA 3: RENDIMIENTO DEL EQUIPO ---
with tab3:
    st.header("Análisis General por Unidades")
    df_global = st.session_state.df.copy()
    col_ofensiva, col_defensiva = st.columns(2)
    
    with col_ofensiva:
        st.subheader("🏈 Unidad Ofensiva")
        ofensiva_df = df_global[df_global['Unidad'] == 'Ofensiva']
        st.metric("Yardas Totales Producidas", int(ofensiva_df['Yardas_Totales'].sum()))
        st.metric("Pases/Recepciones Completadas", int(ofensiva_df['Completos_Recepciones'].sum()))
        st.metric("Promedio Carga Mental", f"{ofensiva_df['Carga_Mental_Semanal'].mean():.1f}/10" if not ofensiva_df.empty else "0/10")
        
    with col_defensiva:
        st.subheader("🛡️ Unidad Defensiva")
        defensiva_df = df_global[df_global['Unidad'] == 'Defensiva']
        st.metric("Tackleadas Totales", int(defensiva_df['Tackleadas'].sum()))
        st.metric("Intercepciones Generadas", int(defensiva_df['Intercepciones'].sum()))
        st.metric("Promedio Carga Mental", f"{defensiva_df['Carga_Mental_Semanal'].mean():.1f}/10" if not defensiva_df.empty else "0/10")

# --- PESTAÑA 2: BASE DE DATOS Y EDICIÓN ---
with tab2:
    st.subheader("Gestión del Roster y Estadísticas")
    st.write("Agrega a los jugadores restantes haciendo clic en la última fila vacía.")
    
    df_editado = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True, hide_index=True)
    
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

                st.header(f"Análisis de: {jugador_filtro} - #{stats_jugador['Jersey']} ({stats_jugador['Posición']})")
                
                st.subheader("Métricas Deportivas")
                col1, col2, col3 = st.columns(3)
                
                if unidad_filtro == 'Ofensiva':
                    with col1: st.metric(label="Efectividad", value=f"{stats_jugador['Efectividad (%)']:.1f}%")
                    with col2: st.metric(label="Yardas Reales", value=int(stats_jugador['Yardas_Totales']))
                    with col3: st.metric(label="Proyección de Yardas", value=int(stats_jugador['Proyeccion_Yardas']))
                else:
                    with col1: st.metric(label="Tackleadas", value=int(stats_jugador['Tackleadas']))
                    with col2: st.metric(label="Intercepciones", value=int(stats_jugador['Intercepciones']))
                    with col3: st.metric(label="Impacto Defensivo", value="Alto")

                st.divider()

                st.subheader("Monitoreo Psicodeportivo")
                col4, col5, col6 = st.columns(3)
                with col4: st.write(f"**Carga Mental:** {stats_jugador['Carga_Mental_Semanal']}/10")
                with col5: st.write(f"**Calidad de Sueño:** {stats_jugador['Calidad_Sueno']} horas")
                with col6: st.write(f"**Fatiga:** {stats_jugador['Fatiga_Traslado']}/10")
