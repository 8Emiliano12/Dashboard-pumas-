import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard Pumas CU", layout="wide")

# --- SISTEMA DE SEGURIDAD (LOGIN) ---
def check_password():
    """Devuelve True si el usuario ingresa la contraseña correcta."""
    def password_entered():
        if st.session_state["password"] == "Pumas2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Ingresa la contraseña del equipo para acceder:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Ingresa la contraseña del equipo para acceder:", type="password", on_change=password_entered, key="password")
        st.error("🛑 Contraseña incorrecta. Acceso denegado.")
        return False
    return True

if not check_password():
    st.stop()

# ==========================================
# CÓDIGO PRINCIPAL DEL DASHBOARD
# ==========================================
st.title("Panel de Control: Rendimiento y Bienestar - Pumas CU")

# 1. Base de datos inicial
if 'df' not in st.session_state:
    datos_iniciales = {
        'Jersey': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 73, 87],
        'Jugador': [
            'Josh Alexander Morfín González', 'Raul Rodrigo Blanco Ruiz', 'Aaron Soriano Vacasoydel', 
            'Leonardo David Garza Peña', 'Diego Mercado Sánchez', 'Julio Cesar Hernández Hernández',
            'Abraham González López', 'Luis Miguel Bañuelos Medina', 'Luis Higelin Castañeda',
            'Joaquin Aramis Carrillo Palma', 'Emiliano Sánchez Hernández', 'Raymundo Licea Gómez',
            'Christopher Bryan Cardona Padrón', 'Jesús Fernando Inzunza López', 'Emiliano Zamora Jerónimo'
        ],
        'Posición': ['DL', 'WR', 'DB', 'QB', 'LB', 'DB', 'LB', 'DB', 'DB', 'DL', 'QB', 'DL', 'WR', 'OL', 'K'],
        'Unidad': ['Defensiva', 'Ofensiva', 'Defensiva', 'Ofensiva', 'Defensiva', 'Defensiva', 'Defensiva', 'Defensiva', 'Defensiva', 'Defensiva', 'Ofensiva', 'Defensiva', 'Ofensiva', 'Ofensiva', 'Equipos Especiales'],
        'Partidos_Jugados': [1]*15, # Base para calcular promedios por partido
        'Targets_Intentos': [0]*15,
        'Completos_Recepciones': [0]*15,
        'Yardas_Totales': [0]*15,
        'Tackleadas': [0]*15,
        'Intercepciones': [0]*15,
        'Bloqueos_Efectivos': [0]*15,
        'Capturas_Permitidas': [0]*15,
        'Capturas_QB': [0]*15,
        'Goles_Campo': [0]*15,      
        'Puntos_Extra': [0]*15,     
        'Carga_Mental_Semanal': [0]*15,
        'Calidad_Sueno': [0]*15,
        'Fatiga_Traslado': [0]*15
    }
    st.session_state.df = pd.DataFrame(datos_iniciales)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Análisis Individual", "⚙️ Base de Datos", "📈 Rendimiento Equipo", "📝 Registro Diario"])

# --- PESTAÑA 4: REGISTRO DIARIO ---
with tab4:
    st.header("Captura de Entrenamientos y Partidos")
    
    col_filtro1, col_filtro2 = st.columns(2)
    with col_filtro1:
        unidad_registro = st.selectbox("1. Selecciona la Unidad", st.session_state.df['Unidad'].unique(), key="unidad_reg")
    
    jugadores_filtrados = st.session_state.df[st.session_state.df['Unidad'] == unidad_registro]['Jugador'].tolist()
    
    def mostrar_nombre_con_posicion(nombre_jugador):
        pos = st.session_state.df[st.session_state.df['Jugador'] == nombre_jugador]['Posición'].values[0]
        return f"{nombre_jugador} ({pos})"
    
    with col_filtro2:
        jugador_seleccionado = st.selectbox("2. Selecciona al Jugador", jugadores_filtrados, format_func=mostrar_nombre_con_posicion, key="jugador_reg")
    
    idx = st.session_state.df.index[st.session_state.df['Jugador'] == jugador_seleccionado].tolist()[0]
    pos_actual = st.session_state.df.at[idx, 'Posición']
    
    with st.form("registro_diario_form"):
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.subheader("Estado de Bienestar Diario")
            carga_nueva = st.slider("Carga Mental/Académica (1-10)", 1, 10, 5)
            sueno_nuevo = st.slider("Horas de Sueño", 1, 12, 7)
            fatiga_nueva = st.slider("Nivel de Fatiga Física (1-10)", 1, 10, 5)

        with col_b:
            st.subheader("Rendimiento en Campo (Este Juego)")
            st.write(f"*(Métricas adaptadas para: **{pos_actual}**)*")
            
            n_intentos, n_completos, n_yardas = 0, 0, 0
            n_tackleadas, n_intercepciones, n_capturas_qb = 0, 0, 0
            n_bloqueos, n_capturas_perm = 0, 0
            n_goles_campo, n_puntos_extra = 0, 0
            
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
            elif pos_actual in ['K', 'P']:
                n_goles_campo = st.number_input("Goles de Campo Anotados", min_value=0, value=0)
                n_puntos_extra = st.number_input("Puntos Extra Anotados (PATs)", min_value=0, value=0)
        
        submitted = st.form_submit_button("Guardar Registro del Día")
        
        if submitted:
            # Incrementar partidos jugados en 1 cada vez que se registran stats de juego
            st.session_state.df.at[idx, 'Partidos_Jugados'] += 1
            
            st.session_state.df.at[idx, 'Targets_Intentos'] += n_intentos
            st.session_state.df.at[idx, 'Completos_Recepciones'] += n_completos
            st.session_state.df.at[idx, 'Yardas_Totales'] += n_yardas
            st.session_state.df.at[idx, 'Tackleadas'] += n_tackleadas
            st.session_state.df.at[idx, 'Intercepciones'] += n_intercepciones
            st.session_state.df.at[idx, 'Capturas_QB'] += n_capturas_qb
            st.session_state.df.at[idx, 'Bloqueos_Efectivos'] += n_bloqueos
            st.session_state.df.at[idx, 'Capturas_Permitidas'] += n_capturas_perm
            st.session_state.df.at[idx, 'Goles_Campo'] += n_goles_campo
            st.session_state.df.at[idx, 'Puntos_Extra'] += n_puntos_extra
            
            st.session_state.df.at[idx, 'Carga_Mental_Semanal'] = carga_nueva
            st.session_state.df.at[idx, 'Calidad_Sueno'] = sueno_nuevo
            st.session_state.df.at[idx, 'Fatiga_Traslado'] = fatiga_nueva
            
            st.success(f"✅ ¡Datos de {jugador_seleccionado} ({pos_actual}) actualizados!")

# --- PESTAÑA 3: RENDIMIENTO DEL EQUIPO ---
with tab3:
    st.header("Análisis General por Unidades")
    df_global = st.session_state.df.copy()
    col_of, col_def, col_st = st.columns(3)
    
    with col_of:
        st.subheader("🏈 Ofensiva")
        of_df = df_global[df_global['Unidad'] == 'Ofensiva']
        st.metric("Yardas Totales", int(of_df['Yardas_Totales'].sum()))
        st.metric("Promedio Carga Mental", f"{of_df['Carga_Mental_Semanal'].mean():.1f}/10" if not of_df.empty else "0/10")
        
    with col_def:
        st.subheader("🛡️ Defensiva")
        def_df = df_global[df_global['Unidad'] == 'Defensiva']
        st.metric("Tackleadas Totales", int(def_df['Tackleadas'].sum()))
        st.metric("Promedio Carga Mental", f"{def_df['Carga_Mental_Semanal'].mean():.1f}/10" if not def_df.empty else "0/10")
        
    with col_st:
        st.subheader("🦵 Equipos Especiales")
        st_df = df_global[df_global['Unidad'] == 'Equipos Especiales']
        st.metric("Puntos Totales (Kicking)", int((st_df['Goles_Campo'].sum() * 3) + (st_df['Puntos_Extra'].sum() * 1)))
        st.metric("Promedio Carga Mental", f"{st_df['Carga_Mental_Semanal'].mean():.1f}/10" if not st_df.empty else "0/10")

# --- PESTAÑA 2: BASE DE DATOS Y EDICIÓN ---
with tab2:
    st.subheader("Gestión del Roster y Estadísticas")
    df_editado = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True, hide_index=True)
    if st.button("Guardar Cambios Globales"):
        st.session_state.df = df_editado
        st.success("¡Base de datos actualizada correctamente!")

# --- PESTAÑA 1: ANÁLISIS DEL COACH (CON PROYECCIONES NFL) ---
with tab1:
    df = st.session_state.df.copy()
    
    # Evitar división por cero en partidos jugados
    df['PJ_Calc'] = df['Partidos_Jugados'].replace(0, 1)
    df['Targets_Calc'] = df['Targets_Intentos'].replace(0, 1)
    
    # Cálculos y Proyecciones estilo Next Gen Stats
    df['Efectividad (%)'] = (df['Completos_Recepciones'] / df['Targets_Calc']) * 100
    
    # Proyecciones a ritmo de temporada completa (estimando 10 juegos totales)
    df['Proyeccion_Yardas_Temp'] = (df['Yardas_Totales'] / df['PJ_Calc']) * 10
    df['Proyeccion_Tackles_Temp'] = (df['Tackleadas'] / df['PJ_Calc']) * 10
    df['Proyeccion_Sacks_Temp'] = (df['Capturas_QB'] / df['PJ_Calc']) * 10

    st.subheader("Filtros de Búsqueda")
    if not df.empty:
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            unidad_filtro = st.selectbox("Selecciona la Unidad", df['Unidad'].unique(), key="unidad_coach")
            
        posiciones_disponibles = df[df['Unidad'] == unidad_filtro]['Posición'].unique()
        
        if len(posiciones_disponibles) > 0:
            with col_f2:
                posicion_filtro = st.selectbox("Selecciona la Posición", posiciones_disponibles, key="posicion_coach")
                
            jugadores_disponibles = df[df['Posición'] == posicion_filtro]['Jugador']
            
            if not jugadores_disponibles.empty:
                with col_f3:
                    jugador_filtro = st.selectbox("Selecciona al Jugador", jugadores_disponibles, key="jugador_coach")
                    
                stats_jugador = df[df['Jugador'] == jugador_filtro].iloc[0]
                pos = stats_jugador['Posición']

                st.divider()
                st.header(f"Análisis de: {jugador_filtro} - #{stats_jugador['Jersey']} ({pos})")
                
                st.subheader("📊 Métricas Reales y Proyecciones (Estilo NFL)")
                col1, col2, col3 = st.columns(3)
                
                if pos in ['QB', 'WR', 'RB']:
                    with col1: 
                        st.metric(label="Yardas Reales", value=int(stats_jugador['Yardas_Totales']))
                    with col2: 
                        st.metric(label="Promedio por Partido", value=f"{stats_jugador['Yardas_Totales'] / stats_jugador['PJ_Calc']:.1f} yds")
                    with col3: 
                        st.metric(label="Proyección Temporada (10 J)", value=int(stats_jugador['Proyeccion_Yardas_Temp']), delta="Ritmo Estimado")
                
                elif pos == 'OL':
                    with col1: 
                        st.metric(label="Bloqueos Efectivos (Pancakes)", value=int(stats_jugador['Bloqueos_Efectivos']))
                    with col2: 
                        st.metric(label="Capturas Permitidas (Sacks)", value=int(stats_jugador['Capturas_Permitidas']))
                    with col3: 
                        eficiencia_ol = "Óptima" if stats_jugador['Capturas_Permitidas'] == 0 else "Revisar Cobertura"
                        st.metric(label="Calificación de Protección", value=eficiencia_ol)
                
                elif pos in ['DL', 'LB']:
                    with col1: 
                        st.metric(label="Tackleadas Totales", value=int(stats_jugador['Tackleadas']))
                    with col2: 
                        st.metric(label="Capturas al QB (Sacks)", value=int(stats_jugador['Capturas_QB']))
                    with col3: 
                        st.metric(label="Proyección de Tackleadas (10 J)", value=int(stats_jugador['Proyeccion_Tackles_Temp']), delta="Ritmo Estimado")
                
                elif pos == 'DB':
                    with col1: 
                        st.metric(label="Tackleadas", value=int(stats_jugador['Tackleadas']))
                    with col2: 
                        st.metric(label="Intercepciones", value=int(stats_jugador['Intercepciones']))
                    with col3: 
                        st.metric(label="Proyección de Intercepciones", value=f"{stats_jugador['Intercepciones'] / stats_jugador['PJ_Calc'] * 10:.1f}")
                
                elif pos in ['K', 'P']:
                    with col1: 
                        st.metric(label="Goles de Campo", value=int(stats_jugador['Goles_Campo']))
                    with col2: 
                        st.metric(label="Puntos Extra (PATs)", value=int(stats_jugador['Puntos_Extra']))
                    with col3: 
                        st.metric(label="Puntos Totales", value=int((stats_jugador['Goles_Campo'] * 3) + stats_jugador['Puntos_Extra']))

                st.divider()

                st.subheader("🧠 Monitoreo Psicodeportivo")
                col4, col5, col6 = st.columns(3)
                with col4: st.write(f"**Carga Mental:** {stats_jugador['Carga_Mental_Semanal']}/10")
                with col5: st.write(f"**Calidad de Sueño:** {stats_jugador['Calidad_Sueno']} horas")
                with col6: st.write(f"**Fatiga Física:** {stats_jugador['Fatiga_Traslado']}/10")

                # Alertas inteligentes cruzadas con fatiga y rendimiento
                if stats_jugador['Carga_Mental_Semanal'] >= 8 or stats_jugador['Fatiga_Traslado'] >= 8:
                    st.error("🚨 ALERTA PSICOLÓGICA: Atleta con índices elevados de fatiga o carga mental. Se sugiere intervención de descanso.")
                else:
                    st.success("✅ Estabilidad psico-física en rangos óptimos para competencia.")
