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

# 1. Base de datos inicial con desglose Partidos vs Entrenamientos
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
        
        # Contadores de eventos
        'Partidos_Jugados': [1]*15,
        'Entrenamientos_Asistidos': [1]*15,
        
        # Métricas de Partido
        'Yardas_Partidos': [0]*15,
        'Tackleadas_Partidos': [0]*15,
        'Intercepciones_Partidos': [0]*15,
        'Pancakes_Partidos': [0]*15,
        'Sacks_Permitidos_Partidos': [0]*15,
        'Sacks_QB_Partidos': [0]*15,
        'Goles_Campo_Partidos': [0]*15,
        'Puntos_Extra_Partidos': [0]*15,
        
        # Métricas de Entrenamiento
        'Yardas_Entrenamientos': [0]*15,
        'Tackleadas_Entrenamientos': [0]*15,
        'Intercepciones_Entrenamientos': [0]*15,
        'Pancakes_Entrenamientos': [0]*15,
        'Sacks_Permitidos_Entrenamientos': [0]*15,
        'Sacks_QB_Entrenamientos': [0]*15,
        'Goles_Campo_Entrenamientos': [0]*15,
        'Puntos_Extra_Entrenamientos': [0]*15,
        
        # Bienestar separado
        'Carga_Mental_Partido': [0]*15,
        'Sueño_Partido': [0]*15,
        'Fatiga_Partido': [0]*15,
        'Carga_Mental_Entreno': [0]*15,
        'Sueño_Entreno': [0]*15,
        'Fatiga_Entreno': [0]*15
    }
    st.session_state.df = pd.DataFrame(datos_iniciales)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Análisis Individual", "⚙️ Base de Datos", "📈 Rendimiento Equipo", "📝 Registro Diario"])

# --- PESTAÑA 4: REGISTRO DIARIO (CON TIPO DE EVENTO) ---
with tab4:
    st.header("Captura de Entrenamientos y Partidos")
    
    col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
    with col_filtro1:
        tipo_evento = st.selectbox("1. Tipo de Registro", ["Entrenamiento", "Partido"])
    with col_filtro2:
        unidad_registro = st.selectbox("2. Selecciona la Unidad", st.session_state.df['Unidad'].unique(), key="unidad_reg")
    
    jugadores_filtrados = st.session_state.df[st.session_state.df['Unidad'] == unidad_registro]['Jugador'].tolist()
    
    def mostrar_nombre_con_posicion(nombre_jugador):
        pos = st.session_state.df[st.session_state.df['Jugador'] == nombre_jugador]['Posición'].values[0]
        return f"{nombre_jugador} ({pos})"
    
    with col_filtro3:
        jugador_seleccionado = st.selectbox("3. Selecciona al Jugador", jugadores_filtrados, format_func=mostrar_nombre_con_posicion, key="jugador_reg")
    
    idx = st.session_state.df.index[st.session_state.df['Jugador'] == jugador_seleccionado].tolist()[0]
    pos_actual = st.session_state.df.at[idx, 'Posición']
    
    with st.form("registro_diario_form"):
        st.info(Registrando actividad tipo: **{tipo_evento}** para **{jugador_seleccionado}** ({pos_actual}))
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.subheader("Estado Psicodeportivo")
            carga_nueva = st.slider("Carga Mental / Estrés (1-10)", 1, 10, 5)
            sueno_nuevo = st.slider("Horas de Sueño", 1, 12, 7)
            fatiga_nueva = st.slider("Nivel de Fatiga Física (1-10)", 1, 10, 5)

        with col_b:
            st.subheader("Rendimiento Registrado")
            
            n_yardas, n_tackleadas, n_intercepciones = 0, 0, 0
            n_pancakes, n_sacks_perm, n_sacks_qb = 0, 0, 0
            n_gc, n_pe = 0, 0
            
            if pos_actual in ['QB', 'WR', 'RB']:
                n_yardas = st.number_input("Yardas Producidas", min_value=0, value=0)
            elif pos_actual == 'OL':
                n_pancakes = st.number_input("Bloqueos Efectivos (Pancakes)", min_value=0, value=0)
                n_sacks_perm = st.number_input("Capturas Permitidas (Sacks)", min_value=0, value=0)
            elif pos_actual in ['DL', 'LB']:
                n_tackleadas = st.number_input("Tackleadas", min_value=0, value=0)
                n_sacks_qb = st.number_input("Capturas al QB (Sacks)", min_value=0, value=0)
            elif pos_actual == 'DB':
                n_tackleadas = st.number_input("Tackleadas", min_value=0, value=0)
                n_intercepciones = st.number_input("Intercepciones", min_value=0, value=0)
            elif pos_actual in ['K', 'P']:
                n_gc = st.number_input("Goles de Campo Anotados", min_value=0, value=0)
                n_pe = st.number_input("Puntos Extra Anotados (PATs)", min_value=0, value=0)
        
        submitted = st.form_submit_button("Guardar Registro")
        
        if submitted:
            if tipo_evento == "Partido":
                st.session_state.df.at[idx, 'Partidos_Jugados'] += 1
                st.session_state.df.at[idx, 'Yardas_Partidos'] += n_yardas
                st.session_state.df.at[idx, 'Tackleadas_Partidos'] += n_tackleadas
                st.session_state.df.at[idx, 'Intercepciones_Partidos'] += n_intercepciones
                st.session_state.df.at[idx, 'Pancakes_Partidos'] += n_pancakes
                st.session_state.df.at[idx, 'Sacks_Permitidos_Partidos'] += n_sacks_perm
                st.session_state.df.at[idx, 'Sacks_QB_Partidos'] += n_sacks_qb
                st.session_state.df.at[idx, 'Goles_Campo_Partidos'] += n_gc
                st.session_state.df.at[idx, 'Puntos_Extra_Partidos'] += n_pe
                
                st.session_state.df.at[idx, 'Carga_Mental_Partido'] = carga_nueva
                st.session_state.df.at[idx, 'Sueño_Partido'] = sueno_nuevo
                st.session_state.df.at[idx, 'Fatiga_Partido'] = fatiga_nueva
            else:
                st.session_state.df.at[idx, 'Entrenamientos_Asistidos'] += 1
                st.session_state.df.at[idx, 'Yardas_Entrenamientos'] += n_yardas
                st.session_state.df.at[idx, 'Tackleadas_Entrenamientos'] += n_tackleadas
                st.session_state.df.at[idx, 'Intercepciones_Entrenamientos'] += n_intercepciones
                st.session_state.df.at[idx, 'Pancakes_Entrenamientos'] += n_pancakes
                st.session_state.df.at[idx, 'Sacks_Permitidos_Entrenamientos'] += n_sacks_perm
                st.session_state.df.at[idx, 'Sacks_QB_Entrenamientos'] += n_sacks_qb
                st.session_state.df.at[idx, 'Goles_Campo_Entrenamientos'] += n_gc
                st.session_state.df.at[idx, 'Puntos_Extra_Entrenamientos'] += n_pe
                
                st.session_state.df.at[idx, 'Carga_Mental_Entreno'] = carga_nueva
                st.session_state.df.at[idx, 'Sueño_Entreno'] = sueno_nuevo
                st.session_state.df.at[idx, 'Fatiga_Entreno'] = fatiga_nueva
            
            st.success(f"✅ ¡Registro de {tipo_evento} guardado para {jugador_seleccionado}!")

# --- PESTAÑA 3: RENDIMIENTO DEL EQUIPO ---
with tab3:
    st.header("Análisis General por Unidades")
    df_global = st.session_state.df.copy()
    col_of, col_def, col_st = st.columns(3)
    
    with col_of:
        st.subheader("🏈 Ofensiva")
        of_df = df_global[df_global['Unidad'] == 'Ofensiva']
        st.metric("Yardas Totales (Partidos)", int(of_df['Yardas_Partidos'].sum()))
        st.metric("Yardas Totales (Entrenamientos)", int(of_df['Yardas_Entrenamientos'].sum()))
        
    with col_def:
        st.subheader("🛡️ Defensiva")
        def_df = df_global[df_global['Unidad'] == 'Defensiva']
        st.metric("Tackleadas (Partidos)", int(def_df['Tackleadas_Partidos'].sum()))
        st.metric("Tackleadas (Entrenamientos)", int(def_df['Tackleadas_Entrenamientos'].sum()))
        
    with col_st:
        st.subheader("🦵 Equipos Especiales")
        st_df = df_global[df_global['Unidad'] == 'Equipos Especiales']
        st.metric("Puntos (Partidos)", int((st_df['Goles_Campo_Partidos'].sum() * 3) + (st_df['Puntos_Extra_Partidos'].sum() * 1)))
        st.metric("Puntos (Entrenamientos)", int((st_df['Goles_Campo_Entrenamientos'].sum() * 3) + (st_df['Puntos_Extra_Entrenamientos'].sum() * 1)))

# --- PESTAÑA 2: BASE DE DATOS Y EDICIÓN ---
with tab2:
    st.subheader("Gestión del Roster y Estadísticas")
    df_editado = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True, hide_index=True)
    if st.button("Guardar Cambios Globales"):
        st.session_state.df = df_editado
        st.success("¡Base de datos actualizada correctamente!")

# --- PESTAÑA 1: ANÁLISIS DEL COACH (CON DESGLOSE Y PROYECCIONES) ---
with tab1:
    df = st.session_state.df.copy()
    
    df['PJ_Calc'] = df['Partidos_Jugados'].replace(0, 1)
    df['PE_Calc'] = df['Entrenamientos_Asistidos'].replace(0, 1)

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
                
                st.subheader("📊 Rendimiento en Partidos vs Entrenamientos")
                col1, col2, col3 = st.columns(3)
                
                if pos in ['QB', 'WR', 'RB']:
                    with col1: st.metric(label="Yardas en Partidos", value=int(stats_jugador['Yardas_Partidos']))
                    with col2: st.metric(label="Yardas en Entrenamientos", value=int(stats_jugador['Yardas_Entrenamientos']))
                    with col3: st.metric(label="Proyección Temp. (10 Partidos)", value=int((stats_jugador['Yardas_Partidos'] / stats_jugador['PJ_Calc']) * 10), delta="Ritmo de Juego")
                
                elif pos == 'OL':
                    with col1: st.metric(label="Pancakes (Partidos)", value=int(stats_jugador['Pancakes_Partidos']))
                    with col2: st.metric(label="Pancakes (Entrenamientos)", value=int(stats_jugador['Pancakes_Entrenamientos']))
                    with col3: st.metric(label="Sacks Permitidos (Partidos)", value=int(stats_jugador['Sacks_Permitidos_Partidos']))
                
                elif pos in ['DL', 'LB']:
                    with col1: st.metric(label="Tackleadas (Partidos)", value=int(stats_jugador['Tackleadas_Partidos']))
                    with col2: st.metric(label="Tackleadas (Entrenamientos)", value=int(stats_jugador['Tackleadas_Entrenamientos']))
                    with col3: st.metric(label="Proyección Tackles (10 Partidos)", value=int((stats_jugador['Tackleadas_Partidos'] / stats_jugador['PJ_Calc']) * 10), delta="Ritmo de Juego")
                
                elif pos == 'DB':
                    with col1: st.metric(label="Intercepciones (Partidos)", value=int(stats_jugador['Intercepciones_Partidos']))
                    with col2: st.metric(label="Intercepciones (Entrenamientos)", value=int(stats_jugador['Intercepciones_Entrenamientos']))
                    with col3: st.metric(label="Tackleadas (Partidos)", value=int(stats_jugador['Tackleadas_Partidos']))
                
                elif pos in ['K', 'P']:
                    with col1: st.metric(label="Goles de Campo (Partidos)", value=int(stats_jugador['Goles_Campo_Partidos']))
                    with col2: st.metric(label="Goles de Campo (Entrenamientos)", value=int(stats_jugador['Goles_Campo_Entrenamientos']))
                    with col3: st.metric(label="Puntos Totales (Partidos)", value=int((stats_jugador['Goles_Campo_Partidos'] * 3) + stats_jugador['Puntos_Extra_Partidos']))

                st.divider()

                st.subheader("🧠 Monitoreo Psicodeportivo Desglosado")
                col_psi1, col_psi2 = st.columns(2)
                
                with col_psi1:
                    st.markdown("### 🏟️ En Partidos")
                    st.write(f"**Carga Mental:** {stats_jugador['Carga_Mental_Partido']}/10")
                    st.write(f"**Sueño:** {stats_jugador['Sueño_Partido']} hrs")
                    st.write(f"**Fatiga:** {stats_jugador['Fatiga_Partido']}/10")
                
                with col_psi2:
                    st.markdown("### 🏋️ En Entrenamientos")
                    st.write(f"**Carga Mental:** {stats_jugador['Carga_Mental_Entreno']}/10")
                    st.write(f"**Sueño:** {stats_jugador['Sueño_Entreno']} hrs")
                    st.write(f"**Fatiga:** {stats_jugador['Fatiga_Entreno']}/10")

                # Alertas basadas en fatiga de partido
                if stats_jugador['Carga_Mental_Partido'] >= 8 or stats_jugador['Fatiga_Partido'] >= 8:
                    st.error("🚨 ALERTA: Altos niveles de desgaste detectados en días de partido.")
                else:
                    st.success("✅ Estabilidad psico-física en rangos óptimos.")
