import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Pumas CU", layout="wide")
st.title("Panel de Control: Rendimiento y Bienestar - Pumas CU")

# 1. Memoria de la sesión con métricas específicas por posición
if 'df' not in st.session_state:
    datos_iniciales = {
        'Jersey': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 73],
        'Jugador': [
            'Josh Alexander Morfín González', 'Raul Rodrigo Blanco Ruiz', 'Aaron Soriano Vacasoydel', 
            'Leonardo David Garza Peña', 'Diego Mercado Sánchez', 'Julio Cesar Hernández Hernández',
            'Abraham González López', 'Luis Miguel Bañuelos Medina', 'Luis Higelin Castañeda',
            'Joaquin Aramis Carrillo Palma', 'Emiliano Sánchez Hernández', 'Raymundo Licea Gómez',
            'Christopher Bryan Cardona Padrón', 'Jesús Fernando Inzunza López'
        ],
        'Posición': ['DL', 'WR', 'DB', 'QB', 'LB', 'DB', 'LB', 'DB', 'DB', 'DL', 'QB', 'DL', 'WR', 'OL'],
        'Unidad': ['Defensiva', 'Ofensiva', 'Defensiva', 'Ofensiva', 'Defensiva', 'Defensiva', 'Defensiva', 'Defensiva', 'Defensiva', 'Defensiva', 'Ofensiva', 'Defensiva', 'Ofensiva', 'Ofensiva'],
        'Targets_Intentos': [0]*14,
        'Completos_Recepciones': [0]*14,
        'Yardas_Totales': [0]*14,
        'Tackleadas': [0]*14,
        'Intercepciones': [0]*14,
        'Bloqueos_Efectivos': [0]*14,
        'Capturas_Permitidas': [0]*14,
        'Capturas_QB': [0]*14,
        'Carga_Mental_Semanal': [0]*14,
        'Calidad_Sueno': [0]*14,
        'Fatiga_Traslado': [0]*14
    }
    st.session_state.df = pd.DataFrame(datos_iniciales)

# 2. Pestañas de Navegación
tab1, tab2, tab3, tab4 = st.tabs(["📊 Análisis Individual", "⚙️ Base de Datos", "📈 Rendimiento Equipo", "📝 Registro Diario"])

# --- PESTAÑA 4: REGISTRO DIARIO (CORREGIDO) ---
with tab4:
    st.header("Captura de Entrenamientos y Partidos")
    
    # ¡LA CLAVE! El selector debe estar FUERA del formulario para que actualice en tiempo real
    jugador_seleccionado = st.selectbox("Selecciona al Jugador a evaluar", st.session_state.df['Jugador'].tolist())
    idx = st.session_state.df.index[st.session_state.df['Jugador'] == jugador_seleccionado].tolist()[0]
    pos_actual = st.session_state.df.at[idx, 'Posición']
    
    with st.form("registro_diario_form"):
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.subheader("1. Bienestar de Hoy")
            carga_nueva = st.slider("Carga Mental/Académica (1-10)", 1, 10, 5)
            sueno_nuevo = st.slider("Horas de Sueño", 1, 12, 7)
            fatiga_nueva = st.slider("Nivel de Fatiga Física (1-10)", 1, 10, 5)

        with col_b:
            st.subheader("2. Rendimiento en Campo")
            st.write(f"*(Campos adaptados para la posición: **{pos_actual}**)*")
            
            n_intentos, n_completos, n_yardas = 0, 0, 0
            n_tackleadas, n_intercepciones, n_capturas_qb = 0, 0, 0
            n_bloqueos, n_capturas_perm = 0, 0
            
            if pos_actual in ['QB', 'WR', 'RB']:
                n_intentos = st.number_input("Targets/Intentos de Pase", min_value=0, value=0)
                n_completos = st.number_input("Pases Completos/Recepciones", min_value=0, value=0)
                n_yardas = st.number_input("Yardas Totales", min_value=0, value=0)
            elif pos_actual == 'OL':
                n_bloqueos = st.number_input("Bloqueos Efectivos (Pancakes)", min_value=0, value=0)
                n_capturas_perm = st.number_input("Capturas Permitidas (Sacks)", min_value=0, value=0)
            elif pos_actual in ['DL', 'LB']:
                n_tackleadas = st.number_input("Tackleadas", min_value=0, value=0)
                n_capturas_qb = st.number_input("Capturas al QB (Sacks Generados)", min_value=0, value=0)
            elif pos_actual == 'DB':
                n_tackleadas = st.number_input("Tackleadas", min_value=0, value=0)
                n_intercepciones = st.number_input("Intercepciones", min_value=0, value=0)
        
        submitted = st.form_submit_button("Guardar Registro del Día")
        
        if submitted:
            st.session_state.df.at[idx, 'Targets_Intentos'] += n_intentos
            st.session_state.df.at[idx, 'Completos_Recepciones'] += n_completos
            st.session_state.df.at[idx, 'Yardas_Totales'] += n_yardas
            st.session_state.df.at[idx, 'Tackleadas'] += n_tackleadas
            st.session_state.df.at[idx, 'Intercepciones'] += n_intercepciones
            st.session_state.df.at[idx, 'Capturas_QB'] += n_capturas_qb
            st.session_state.df.at[idx, 'Bloqueos_Efectivos'] += n_bloqueos
            st.session_state.df.at[idx, 'Capturas_Permitidas'] += n_capturas_perm
            
            st.session_state.df.at[idx, 'Carga_Mental_Semanal'] = carga_nueva
            st.session_state.df.at[idx, 'Calidad_Sueno'] = sueno_nuevo
            st.session_state.df.at[idx, 'Fatiga_Traslado'] = fatiga_nueva
            
            st.success(f"✅ ¡Datos de {jugador_seleccionado} ({pos_actual}) actualizados con éxito!")

# --- PESTAÑA 3: RENDIMIENTO DEL EQUIPO ---
with tab3:
    st.header("Análisis General por Unidades")
    df_global = st.session_state.df.copy()
    col_ofensiva, col_defensiva = st.columns(2)
    
    with col_ofensiva:
        st.subheader("🏈 Unidad Ofensiva")
        ofensiva_df = df_global[df_global['Unidad'] == 'Ofensiva']
        st.metric("Yardas Totales Producidas", int(ofensiva_df['Yardas_Totales'].sum()))
        st.metric("Promedio Carga Mental (Ofensiva)", f"{ofensiva_df['Carga_Mental_Semanal'].mean():.1f}/10" if not ofensiva_df.empty else "0/10")
        
    with col_defensiva:
        st.subheader("🛡️ Unidad Defensiva")
        defensiva_df = df_global[df_global['Unidad'] == 'Defensiva']
        st.metric("Tackleadas Totales", int(defensiva_df['Tackleadas'].sum()))
        st.metric("Promedio Carga Mental (Defensiva)", f"{defensiva_df['Carga_Mental_Semanal'].mean():.1f}/10" if not defensiva_df.empty else "0/10")

# --- PESTAÑA 2: BASE DE DATOS Y EDICIÓN ---
with tab2:
    st.subheader("Gestión del Roster y Estadísticas")
    df_editado = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True, hide_index=True)
    if st.button("Guardar Cambios Globales"):
        st.session_state.df = df_editado
        st.success("¡Base de datos actualizada correctamente!")

# --- PESTAÑA 1: ANÁLISIS DEL COACH (DINÁMICO) ---
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
                pos = stats_jugador['Posición']

                st.header(f"Análisis de: {jugador_filtro} - #{stats_jugador['Jersey']} ({pos})")
                
                st.subheader("Métricas Deportivas")
                col1, col2, col3 = st.columns(3)
                
                if pos in ['QB', 'WR', 'RB']:
                    with col1: st.metric(label="Efectividad", value=f"{stats_jugador['Efectividad (%)']:.1f}%")
                    with col2: st.metric(label="Yardas Reales", value=int(stats_jugador['Yardas_Totales']))
                    with col3: st.metric(label="Proyección de Yardas", value=int(stats_jugador['Proyeccion_Yardas']))
                elif pos == 'OL':
                    with col1: st.metric(label="Bloqueos Efectivos (Pancakes)", value=int(stats_jugador['Bloqueos_Efectivos']))
                    with col2: st.metric(label="Capturas Permitidas", value=int(stats_jugador['Capturas_Permitidas']))
                elif pos in ['DL', 'LB']:
                    with col1: st.metric(label="Tackleadas", value=int(stats_jugador['Tackleadas']))
                    with col2: st.metric(label="Capturas al QB (Sacks)", value=int(stats_jugador['Capturas_QB']))
                elif pos == 'DB':
                    with col1: st.metric(label="Tackleadas", value=int(stats_jugador['Tackleadas']))
                    with col2: st.metric(label="Intercepciones", value=int(stats_jugador['Intercepciones']))

                st.divider()

                st.subheader("Monitoreo Psicodeportivo")
                col4, col5, col6 = st.columns(3)
                with col4: st.write(f"**Carga Mental:** {stats_jugador['Carga_Mental_Semanal']}/10")
                with col5: st.write(f"**Calidad de Sueño:** {stats_jugador['Calidad_Sueno']} horas")
                with col6: st.write(f"**Fatiga:** {stats_jugador['Fatiga_Traslado']}/10")
