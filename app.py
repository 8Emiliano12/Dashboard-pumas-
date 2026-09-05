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
        
        'Estatus_Medico': ['Activo', 'Activo', 'Precaución Médica', 'Activo', 'Activo', 'Activo', 'Activo', 'Activo', 'Activo', 'Activo', 'Activo', 'Activo', 'Activo', 'Activo', 'Activo'],
        
        # Asistencia
        'Entrenos_Programados': [1]*15,
        'Entrenos_Asistidos': [1]*15,
        'Partidos_Programados': [1]*15,
        'Partidos_Convocados': [1]*15,
        
        # Rendimiento en campo
        'Yardas_Producidas_Partidos': [0]*15,
        'Pases_Intentados_Partidos': [0]*15,
        'Pases_Completados_Partidos': [0]*15,
        'Bloqueos_Dominio_Partidos': [0]*15,
        'Capturas_Permitidas_Partidos': [0]*15,
        'Tackleadas_Efectivas_Partidos': [0]*15,
        'Intercepciones_Partidos': [0]*15,
        'Capturas_QB_Sacks_Partidos': [0]*15,
        'Goles_Campo_Partidos': [0]*15,
        'Puntos_Extra_Partidos': [0]*15,
        
        'Yardas_Producidas_Entrenos': [0]*15,
        'Pases_Intentados_Entrenos': [0]*15,
        'Pases_Completados_Entrenos': [0]*15,
        'Bloqueos_Dominio_Entrenos': [0]*15,
        'Capturas_Permitidas_Entrenos': [0]*15,
        'Tackleadas_Efectivas_Entrenos': [0]*15,
        'Intercepciones_Entrenos': [0]*15,
        'Capturas_QB_Sacks_Entrenos': [0]*15,
        
        # Bloque Psicológico 1: Mitad de semana
        'Fatiga_Entreno': [4]*15,
        'Dolor_Muscular': [3]*15,
        'Recuperacion_Entreno': [7]*15,
        
        # Bloque Psicológico 2: Pre-partido
        'Ansiedad_Competitiva': [5]*15,
        'Confianza_Tactica': [8]*15,
        'Sueno_Prepartido': [7]*15,
        
        'Historial_Fatiga': [[4, 5, 4]]*15,
        'Historial_Rendimiento_Juego': [[0]]*15
    }
    st.session_state.df = pd.DataFrame(datos_iniciales)

# Pestañas de la aplicación (Sin mención a NCAA)
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Análisis Individual", 
    "⚙️ Base de Datos", 
    "📈 Box Score Oficial", 
    "⚡ Mesa de Anotación (Live)", 
    "📝 Registro Diario", 
    "📅 Calendario"
])

# --- PESTAÑA 4: MESA DE ANOTACIÓN EN VIVO (LIVE SCORING CORREGIDO) ---
with tab4:
    st.header("⚡ Mesa de Anotación Táctil en Vivo")
    st.write("Selecciona al jugador por su unidad o captura su número de jersey exprés para registrar acciones jugada a jugada.")

    tipo_seleccion_mesa = st.radio("Método de captura:", ["Lista del Roster", "Número de Jersey Exprés"], horizontal=True, key="tipo_mesa_sel")

    idx_live = None
    jugador_live = None
    pos_live = None

    if tipo_seleccion_mesa == "Lista del Roster":
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            unidad_live = st.selectbox("Unidad", st.session_state.df['Unidad'].unique(), key="live_unidad_box")
        
        jugadores_live_list = st.session_state.df[st.session_state.df['Unidad'] == unidad_live]['Jugador'].tolist()
        
        def format_live_player(nombre):
            sub_df = st.session_state.df[st.session_state.df['Jugador'] == nombre]
            if not sub_df.empty:
                pos = sub_df['Posición'].values[0]
                jersey = sub_df['Jersey'].values[0]
                return f"#{jersey} - {nombre} ({pos})"
            return nombre

        with col_m2:
            if len(jugadores_live_list) > 0:
                jugador_live = st.selectbox("Jugador", jugadores_live_list, format_func=format_live_player, key="live_jugador_box")
        
        if jugador_live:
            match_j = st.session_state.df[st.session_state.df['Jugador'] == jugador_live]
            if not match_j.empty:
                idx_live = match_j.index[0]
                pos_live = match_j['Posición'].values[0]

    else:
        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            jersey_exprs = st.number_input("Número de Jersey", min_value=0, max_value=99, value=12, key="num_jersey_exprs")
        with col_ex2:
            pos_exprs = st.selectbox("Posición", ["QB", "RB", "WR", "OL", "DL", "LB", "DB", "K", "P"], key="pos_exprs_box")
            
        match_jersey = st.session_state.df[st.session_state.df['Jersey'] == int(jersey_exprs)]
        
        if not match_jersey.empty:
            idx_live = match_jersey.index[0]
            jugador_live = st.session_state.df.at[idx_live, 'Jugador']
            pos_live = st.session_state.df.at[idx_live, 'Posición']
            st.info(f"Atendiendo a: **{jugador_live}** (#{jersey_exprs} - {pos_live})")
        else:
            nombre_provisional = f"Jugador #{int(jersey_exprs)}"
            unidad_asignada = "Ofensiva" if pos_exprs in ["QB", "RB", "WR", "OL"] else ("Defensiva" if pos_exprs in ["DL", "LB", "DB"] else "Equipos Especiales")
            
            nuevo_registro = {
                'Jersey': int(jersey_exprs),
                'Jugador': nombre_provisional,
                'Posición': pos_exprs,
                'Unidad': unidad_asignada,
                'Estatus_Medico': 'Activo',
                'Entrenos_Programados': 1, 'Entrenos_Asistidos': 1, 'Partidos_Programados': 1, 'Partidos_Convocados': 1,
                'Yardas_Producidas_Partidos': 0, 'Pases_Intentados_Partidos': 0, 'Pases_Completados_Partidos': 0,
                'Bloqueos_Dominio_Partidos': 0, 'Capturas_Permitidas_Partidos': 0, 'Tackleadas_Efectivas_Partidos': 0,
                'Intercepciones_Partidos': 0, 'Capturas_QB_Sacks_Partidos': 0, 'Goles_Campo_Partidos': 0, 'Puntos_Extra_Partidos': 0,
                'Yardas_Producidas_Entrenos': 0, 'Pases_Intentados_Entrenos': 0, 'Pases_Completados_Entrenos': 0,
                'Bloqueos_Dominio_Entrenos': 0, 'Capturas_Permitidas_Entrenos': 0, 'Tackleadas_Efectivas_Entrenos': 0,
                'Intercepciones_Entrenos': 0, 'Capturas_QB_Sacks_Entrenos': 0,
                'Fatiga_Entreno': 4, 'Dolor_Muscular': 3, 'Recuperacion_Entreno': 7,
                'Ansiedad_Competitiva': 5, 'Confianza_Tactica': 8, 'Sueno_Prepartido': 7,
                'Historial_Fatiga': [4, 5, 4], 'Historial_Rendimiento_Juego': [0]
            }
            st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([nuevo_registro])], ignore_index=True)
            idx_live = st.session_state.df.index[-1]
            jugador_live = nombre_provisional
            pos_live = pos_exprs
            st.success(f"⚡ Perfil provisional creado para Jersey #{jersey_exprs}. Puedes renombrarlo en la pestaña 'Base de Datos'.")

    if idx_live is not None and jugador_live:
        st.divider()
        st.subheader(f"🎮 Registrar Jugada para: {jugador_live} ({pos_live})")

        if pos_live == 'QB':
            col_q1, col_q2, col_q3 = st.columns(3)
            with col_q1:
                yds_plus = st.number_input("Yardas en la Jugada", min_value=-15, max_value=99, value=5, step=1, key="qb_yds_live")
                if st.button("➕ Sumar Yardas"):
                    st.session_state.df.at[idx_live, 'Yardas_Producidas_Partidos'] += yds_plus
                    st.success(f"¡{yds_plus} yardas sumadas a {jugador_live}!")
            with col_q2:
                if st.button("✅ Pase Completado"):
                    st.session_state.df.at[idx_live, 'Pases_Intentados_Partidos'] += 1
                    st.session_state.df.at[idx_live, 'Pases_Completados_Partidos'] += 1
                    st.success("¡Pase completado registrado!")
            with col_q3:
                if st.button("❌ Pase Incompleto"):
                    st.session_state.df.at[idx_live, 'Pases_Intentados_Partidos'] += 1
                    st.success("¡Pase incompleto registrado!")

        elif pos_live in ['WR', 'RB']:
            col_w1 = st.columns(1)[0]
            with col_w1:
                yds_plus = st.number_input("Yardas en la Jugada", min_value=-5, max_value=99, value=5, step=1, key="wr_yds_live")
                if st.button("➕ Sumar Yardas de Avance"):
                    st.session_state.df.at[idx_live, 'Yardas_Producidas_Partidos'] += yds_plus
                    st.success(f"¡{yds_plus} yardas sumadas a {jugador_live}!")

        elif pos_live == 'OL':
            col_ol1, col_ol2 = st.columns(2)
            with col_ol1:
                if st.button("🥞 Bloqueo de Dominio (Pancake)"):
                    st.session_state.df.at[idx_live, 'Bloqueos_Dominio_Partidos'] += 1
                    st.success("¡Pancake registrado!")
            with col_ol2:
                if st.button("🛑 Sack Permitido"):
                    st.session_state.df.at[idx_live, 'Capturas_Permitidas_Partidos'] += 1
                    st.success("¡Sack permitido registrado!")

        elif pos_live in ['DL', 'LB']:
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                if st.button("🎯 Tackleada Efectiva"):
                    st.session_state.df.at[idx_live, 'Tackleadas_Efectivas_Partidos'] += 1
                    st.success("¡Tackleada registrada!")
            with col_d2:
                if st.button("💥 Sack Defensivo"):
                    st.session_state.df.at[idx_live, 'Capturas_QB_Sacks_Partidos'] += 1
                    st.success("¡Sack registrado!")

        elif pos_live == 'DB':
            col_db1, col_db2 = st.columns(2)
            with col_db1:
                if st.button("🎯 Tackleada Efectiva"):
                    st.session_state.df.at[idx_live, 'Tackleadas_Efectivas_Partidos'] += 1
                    st.success("¡Tackleada registrada!")
            with col_db2:
                if st.button("🏈 Intercepción (INT)"):
                    st.session_state.df.at[idx_live, 'Intercepciones_Partidos'] += 1
                    st.success("¡Intercepción registrada!")

        elif pos_live in ['K', 'P']:
            col_k1, col_k2 = st.columns(2)
            with col_k1:
                if st.button("🎯 Gol de Campo (3 pts)"):
                    st.session_state.df.at[idx_live, 'Goles_Campo_Partidos'] += 1
                    st.success("¡Gol de campo registrado!")
            with col_k2:
                if st.button("⭐ Punto Extra (PAT)"):
                    st.session_state.df.at[idx_live, 'Puntos_Extra_Partidos'] += 1
                    st.success("¡Punto extra registrado!")

# --- PESTAÑA 2: BASE DE DATOS Y GESTIÓN DE ROSTER ---
with tab2:
    st.header("⚙️ Gestión del Roster y Base de Datos Analítica")
    st.write("Consulta y administra el roster. Aquí puedes renombrar a los jugadores provisionales creados en la mesa en vivo.")

    with st.expander("👤 Administrar Roster (Alta / Baja / Edición de Nombres)", expanded=False):
        col_alta, col_baja = st.columns(2)
        
        with col_alta:
            st.subheader("Registrar Nuevo Jugador")
            with st.form("form_alta_jugador"):
                nuevo_nombre = st.text_input("Nombre Completo del Jugador")
                nuevo_jersey = st.number_input("Número de Jersey", min_value=0, max_value=99, value=0)
                nueva_unidad = st.selectbox("Unidad", ["Ofensiva", "Defensiva", "Equipos Especiales"])
                nueva_posicion = st.selectbox("Posición", ["QB", "RB", "WR", "OL", "DL", "LB", "DB", "K", "P"])
                
                submitted_alta = st.form_submit_button("Dar de Alta en el Roster")
                if submitted_alta:
                    if nuevo_nombre.strip() == "":
                        st.error("🛑 El nombre del jugador no puede estar vacío.")
                    elif nuevo_nombre in st.session_state.df['Jugador'].values:
                        st.error("🛑 Ya existe un jugador registrado con ese nombre.")
                    else:
                        nuevo_registro = {
                            'Jersey': int(nuevo_jersey), 'Jugador': nuevo_nombre.strip(), 'Posición': nueva_posicion, 'Unidad': nueva_unidad,
                            'Estatus_Medico': 'Activo', 'Entrenos_Programados': 1, 'Entrenos_Asistidos': 1, 'Partidos_Programados': 1, 'Partidos_Convocados': 1,
                            'Yardas_Producidas_Partidos': 0, 'Pases_Intentados_Partidos': 0, 'Pases_Completados_Partidos': 0,
                            'Bloqueos_Dominio_Partidos': 0, 'Capturas_Permitidas_Partidos': 0, 'Tackleadas_Efectivas_Partidos': 0,
                            'Intercepciones_Partidos': 0, 'Capturas_QB_Sacks_Partidos': 0, 'Goles_Campo_Partidos': 0, 'Puntos_Extra_Partidos': 0,
                            'Yardas_Producidas_Entrenos': 0, 'Pases_Intentados_Entrenos': 0, 'Pases_Completados_Entrenos': 0,
                            'Bloqueos_Dominio_Entrenos': 0, 'Capturas_Permitidas_Entrenos': 0, 'Tackleadas_Efectivas_Entrenos': 0,
                            'Intercepciones_Entrenos': 0, 'Capturas_QB_Sacks_Entrenos': 0,
                            'Fatiga_Entreno': 4, 'Dolor_Muscular': 3, 'Recuperacion_Entreno': 7,
                            'Ansiedad_Competitiva': 5, 'Confianza_Tactica': 8, 'Sueno_Prepartido': 7,
                            'Historial_Fatiga': [4, 5, 4], 'Historial_Rendimiento_Juego': [0]
                        }
                        st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([nuevo_registro])], ignore_index=True)
                        st.success(f"✅ ¡{nuevo_nombre} dado de alta exitosamente!")
                        st.rerun()

        with col_baja:
            st.subheader("Dar de Baja a un Jugador")
            with st.form("form_baja_jugador"):
                jugador_a_borrar = st.selectbox("Selecciona al Jugador a Remover", st.session_state.df['Jugador'].tolist())
                submitted_baja = st.form_submit_button("Eliminar del Roster")
                if submitted_baja:
                    st.session_state.df = st.session_state.df[st.session_state.df['Jugador'] != jugador_a_borrar].reset_index(drop=True)
                    st.success(f"🗑️ ¡Jugador removido del roster exitosamente!")
                    st.rerun()

    st.divider()

    sub_psi, sub_of, sub_def, sub_st = st.tabs([
        "🧠 Psicodeportivo y Bienestar", 
        "🏈 Unidad Ofensiva (PPG & AVG)", 
        "🛡️ Unidad Defensiva (PPG & AVG)", 
        "🦵 Equipos Especiales (PPG)"
    ])

    with sub_psi:
        st.subheader("Bienestar Psicodeportivo y Disponibilidad Médica")
        cols_psi = [
            'Jersey', 'Jugador', 'Posición', 'Unidad', 'Estatus_Medico',
            'Fatiga_Entreno', 'Dolor_Muscular', 'Recuperacion_Entreno',
            'Ansiedad_Competitiva', 'Confianza_Tactica', 'Sueno_Prepartido'
        ]
        df_psi_edit = st.data_editor(st.session_state.df[cols_psi], use_container_width=True, hide_index=True, key="editor_psi")
        if st.button("Guardar Cambios Psicodeportivos"):
            st.session_state.df.update(df_psi_edit)
            st.success("¡Datos psicodeportivos actualizados correctamente!")

    with sub_of:
        st.subheader("Rendimiento Ofensivo (Aquí puedes renombrar a los jugadores provisionales)")
        df_of = st.session_state.df[st.session_state.df['Unidad'] == 'Ofensiva'].copy()
        pj_safe = df_of['Partidos_Convocados'].replace(0, 1)
        
        df_of['PPG_Yardas'] = (df_of['Yardas_Producidas_Partidos'] / pj_safe).round(1)
        df_of['AVG_Pases_Comp_%'] = ((df_of['Pases_Completados_Partidos'] / df_of['Pases_Intentados_Partidos'].replace(0, 1)) * 100).round(1)
        
        cols_of_view = [
            'Jersey', 'Jugador', 'Posición', 'Partidos_Convocados', 
            'Yardas_Producidas_Partidos', 'PPG_Yardas', 
            'Pases_Intentados_Partidos', 'Pases_Completados_Partidos', 'AVG_Pases_Comp_%',
            'Bloqueos_Dominio_Partidos', 'Capturas_Permitidas_Partidos'
        ]
        df_of_edited = st.data_editor(df_of[cols_of_view], use_container_width=True, hide_index=True, key="edit_of_table")
        if st.button("Guardar Cambios Nombres / Ofensiva"):
            st.session_state.df.update(df_of_edited)
            st.success("¡Nombres y estadísticas ofensivas actualizados!")

    with sub_def:
        st.subheader("Rendimiento Defensivo")
        df_def = st.session_state.df[st.session_state.df['Unidad'] == 'Defensiva'].copy()
        pj_safe_def = df_def['Partidos_Convocados'].replace(0, 1)
        
        df_def['PPG_Tackleadas'] = (df_def['Tackleadas_Efectivas_Partidos'] / pj_safe_def).round(1)
        df_def['PPG_Sacks'] = (df_def['Capturas_QB_Sacks_Partidos'] / pj_safe_def).round(2)
        
        cols_def_view = [
            'Jersey', 'Jugador', 'Posición', 'Partidos_Convocados',
            'Tackleadas_Efectivas_Partidos', 'PPG_Tackleadas',
            'Intercepciones_Partidos',
            'Capturas_QB_Sacks_Partidos', 'PPG_Sacks'
        ]
        df_def_edited = st.data_editor(df_def[cols_def_view], use_container_width=True, hide_index=True, key="edit_def_table")
        if st.button("Guardar Cambios Nombres / Defensiva"):
            st.session_state.df.update(df_def_edited)
            st.success("¡Nombres y estadísticas defensivas actualizados!")

    with sub_st:
        st.subheader("Rendimiento Equipos Especiales")
        df_st = st.session_state.df[st.session_state.df['Unidad'] == 'Equipos Especiales'].copy()
        pj_safe_st = df_st['Partidos_Convocados'].replace(0, 1)
        
        df_st['Puntos_Totales'] = (df_st['Goles_Campo_Partidos'] * 3) + df_st['Puntos_Extra_Partidos']
        df_st['PPG_Puntos'] = (df_st['Puntos_Totales'] / pj_safe_st).round(1)
        
        cols_st_view = [
            'Jersey', 'Jugador', 'Posición', 'Partidos_Convocados',
            'Goles_Campo_Partidos', 'Puntos_Extra_Partidos', 'Puntos_Totales', 'PPG_Puntos'
        ]
        df_st_edited = st.data_editor(df_st[cols_st_view], use_container_width=True, hide_index=True, key="edit_st_table")
        if st.button("Guardar Cambios Nombres / ST"):
            st.session_state.df.update(df_st_edited)
            st.success("¡Nombres y estadísticas actualizados!")

# --- PESTAÑA 5: REGISTRO DIARIO ---
with tab5:
    st.header("Captura de Datos Operativos por Jornada")
    
    col_filtro1, col_filtro2, col_filtro3, col_filtro4 = st.columns(4)
    with col_filtro1:
        tipo_registro_principal = st.selectbox("¿Qué deseas registrar?", ["Estadísticas de Partido", "Monitoreo Psicodeportivo y Bienestar"])
    with col_filtro2:
        jornada_seleccionada = st.selectbox("Selecciona la Jornada", [
            "J1 - Leones Anáhuac (Visita)", 
            "J2 - Burros Blancos (Local - EOU)", 
            "J3 - ITESM Puebla (Local - EOU)", 
            "J4 - ITESM Mty (Local)", 
            "J5 - ITESM CEM (Local - EOU)", 
            "J6 - Linces UVM (Visita)", 
            "J7 - Águilas Blancas (Local - EOU)", 
            "J8 - Aztecas UDLAP (Local)", 
            "J9 - Leones UAC (Local - EOU)", 
            "Entrenamiento Semanal Regular"
        ])
    with col_filtro3:
        unidad_registro = st.selectbox("Unidad", st.session_state.df['Unidad'].unique(), key="unidad_reg")
    
    jugadores_filtrados = st.session_state.df[st.session_state.df['Unidad'] == unidad_registro]['Jugador'].tolist()
    
    def mostrar_nombre_con_posicion(nombre_jugador):
        pos = st.session_state.df[st.session_state.df['Jugador'] == nombre_jugador]['Posición'].values[0]
        return f"{nombre_jugador} ({pos})"
    
    with col_filtro4:
        if len(jugadores_filtrados) > 0:
            jugador_seleccionado = st.selectbox("Jugador", jugadores_filtrados, format_func=mostrar_nombre_con_posicion, key="jugador_reg")
        else:
            jugador_seleccionado = None
            st.warning("No hay jugadores en esta unidad.")
    
    if jugador_seleccionado:
        idx = st.session_state.df.index[st.session_state.df['Jugador'] == jugador_seleccionado].tolist()[0]
        pos_actual = st.session_state.df.at[idx, 'Posición']
        
        st.divider()

        if tipo_registro_principal == "Estadísticas de Partido":
            st.subheader(f"🏟️ Registro de Partido ({jornada_seleccionada}) para: {jugador_seleccionado} ({pos_actual})")
            
            with st.form("form_partido"):
                convocatoria_partido = st.selectbox("Estatus de Convocatoria / Participación", ["Jugó (Convocado con acción)", "Inactivo / No Convocado"])
                
                st.write("---")
                st.subheader("Métricas de Rendimiento en el Emparrillado")
                
                n_yardas, n_intentos_pase, n_completados_pase = 0, 0, 0
                n_tackleadas, n_intercepciones = 0, 0
                n_bloqueos_dom, n_sacks_perm, n_sacks_qb = 0, 0, 0
                n_gc, n_pe = 0, 0
                
                if pos_actual == 'QB':
                    n_yardas = st.number_input("Yardas Producidas Totales (Aéreas y Terrestres)", min_value=0, value=0)
                    n_intentos_pase = st.number_input("Pases Intentados", min_value=0, value=0)
                    n_completados_pase = st.number_input("Pases Completados", min_value=0, value=0)
                elif pos_actual in ['WR', 'RB']:
                    n_yardas = st.number_input("Yardas Producidas Totales", min_value=0, value=0)
                elif pos_actual == 'OL':
                    n_bloqueos_dom = st.number_input("Bloqueos de Dominio (Pancake Blocks)", min_value=0, value=0)
                    n_sacks_perm = st.number_input("Capturas Permitidas al QB (Sacks)", min_value=0, value=0)
                elif pos_actual in ['DL', 'LB']:
                    n_tackleadas = st.number_input("Tackleadas Efectivas", min_value=0, value=0)
                    n_sacks_qb = st.number_input("Capturas al Mariscal (Sacks)", min_value=0, value=0)
                elif pos_actual == 'DB':
                    n_tackleadas = st.number_input("Tackleadas Efectivas", min_value=0, value=0)
                    n_intercepciones = st.number_input("Intercepciones Logradas", min_value=0, value=0)
                elif pos_actual in ['K', 'P']:
                    n_gc = st.number_input("Goles de Campo Concretados", min_value=0, value=0)
                    n_pe = st.number_input("Puntos Extra Concretados (PATs)", min_value=0, value=0)
                
                submitted_partido = st.form_submit_button("Guardar Estadísticas de Partido")
                
                if submitted_partido:
                    st.session_state.df.at[idx, 'Partidos_Programados'] += 1
                    if convocatoria_partido == "Jugó (Convocado con acción)":
                        st.session_state.df.at[idx, 'Partidos_Convocados'] += 1
                    
                    st.session_state.df.at[idx, 'Yardas_Producidas_Partidos'] += n_yardas
                    st.session_state.df.at[idx, 'Pases_Intentados_Partidos'] += n_intentos_pase
                    st.session_state.df.at[idx, 'Pases_Completados_Partidos'] += n_completados_pase
                    st.session_state.df.at[idx, 'Tackleadas_Efectivas_Partidos'] += n_tackleadas
                    st.session_state.df.at[idx, 'Intercepciones_Partidos'] += n_intercepciones
                    st.session_state.df.at[idx, 'Bloqueos_Dominio_Partidos'] += n_bloqueos_dom
                    st.session_state.df.at[idx, 'Capturas_Permitidas_Partidos'] += n_sacks_perm
                    st.session_state.df.at[idx, 'Capturas_QB_Sacks_Partidos'] += n_sacks_qb
                    st.session_state.df.at[idx, 'Goles_Campo_Partidos'] += n_gc
                    st.session_state.df.at[idx, 'Puntos_Extra_Partidos'] += n_pe
                    
                    val_juego = n_yardas if pos_actual in ['QB', 'WR', 'RB'] else (n_tackleadas + n_sacks_qb*2 if pos_actual in ['DL', 'LB'] else n_bloqueos_dom)
                    hist_rend = st.session_state.df.at[idx, 'Historial_Rendimiento_Juego']
                    hist_rend.append(val_juego)
                    if len(hist_rend) > 5: hist_rend.pop(0)
                    st.session_state.df.at[idx, 'Historial_Rendimiento_Juego'] = hist_rend
                    
                    st.success(f"✅ ¡Estadísticas guardadas para {jugador_seleccionado}!")

        else:
            st.subheader(f"🧠 Monitoreo Psicodeportivo para: {jugador_seleccionado} ({pos_actual})")
            
            tipo_encuesta = st.selectbox(
                "Selecciona el tipo de evaluación psicológica:", 
                ["Evaluación de Mitad de Semana (Entrenamiento)", "Evaluación Pre-partido (Matchday)"]
            )
            
            st.write("---")
            
            with st.form("form_psico"):
                fatiga_entreno_val = int(st.session_state.df.at[idx, 'Fatiga_Entreno'])
                dolor_muscular_val = int(st.session_state.df.at[idx, 'Dolor_Muscular'])
                recuperacion_val = int(st.session_state.df.at[idx, 'Recuperacion_Entreno'])
                
                ansiedad_val = int(st.session_state.df.at[idx, 'Ansiedad_Competitiva'])
                confianza_val = int(st.session_state.df.at[idx, 'Confianza_Tactica'])
                sueno_pre_val = int(st.session_state.df.at[idx, 'Sueno_Prepartido'])

                if tipo_encuesta == "Evaluación de Mitad de Semana (Entrenamiento)":
                    st.markdown("#### 🏋️ Factores de Carga y Fatiga en Entrenamientos")
                    fatiga_entreno_nueva = st.slider("Fatiga Física Acumulada (1-10)", 1, 10, fatiga_entreno_val)
                    dolor_muscular_nuevo = st.slider("Dolor Muscular / Molestias Menores (1-10)", 1, 10, dolor_muscular_val)
                    recuperacion_nueva = st.slider("Nivel de Recuperación / Frescura (1-10)", 1, 10, recuperacion_val)
                else:
                    st.markdown("#### 🏟️ Factores Psicológicos y de Activación Pre-partido")
                    ansiedad_nueva = st.slider("Nivel de Ansiedad / Activación Competitiva (1-10)", 1, 10, ansiedad_val)
                    confianza_nueva = st.slider("Confianza en el Plan de Juego (1-10)", 1, 10, confianza_val)
                    sueno_previo_nuevo = st.slider("Horas de Sueño Noche Previa (Matchday)", 1, 12, sueno_pre_val)
                
                asistencia_entreno = st.selectbox("Asistencia a la Sesión de Entrenamiento", ["Asistió", "No Asistió"])
                nuevo_estatus = st.selectbox("Estatus Médico / Disponibilidad", ["Activo", "Precaución Médica", "Lesionado / Inactivo"], index=["Activo", "Precaución Médica", "Lesionado / Inactivo"].index(st.session_state.df.at[idx, 'Estatus_Medico']) if st.session_state.df.at[idx, 'Estatus_Medico'] in ["Activo", "Precaución Médica", "Lesionado / Inactivo"] else 0)
                
                submitted_psico = st.form_submit_button("Guardar Datos Psicodeportivos")
                
                if submitted_psico:
                    if jornada_seleccionada == "Entrenamiento Semanal Regular":
                        st.session_state.df.at[idx, 'Entrenos_Programados'] += 1
                        if asistencia_entreno == "Asistió":
                            st.session_state.df.at[idx, 'Entrenos_Asistidos'] += 1
                    
                    st.session_state.df.at[idx, 'Estatus_Medico'] = nuevo_estatus
                    
                    if tipo_encuesta == "Evaluación de Mitad de Semana (Entrenamiento)":
                        st.session_state.df.at[idx, 'Fatiga_Entreno'] = fatiga_entreno_nueva
                        st.session_state.df.at[idx, 'Dolor_Muscular'] = dolor_muscular_nuevo
                        st.session_state.df.at[idx, 'Recuperacion_Entreno'] = recuperacion_nueva
                    else:
                        st.session_state.df.at[idx, 'Ansiedad_Competitiva'] = ansiedad_nueva
                        st.session_state.df.at[idx, 'Confianza_Tactica'] = confianza_nueva
                        st.session_state.df.at[idx, 'Sueno_Prepartido'] = sueno_previo_nuevo
                    
                    st.success(f"✅ ¡{tipo_encuesta} guardada para {jugador_seleccionado}!")

# --- PESTAÑA 5: CALENDARIO Y PLANIFICACIÓN SEMANAL ---
with tab5:
    st.header("📅 Calendario Oficial ONEFA 2026 y Planificación Psicológica")
    st.write("Consulta las fechas de la temporada, sedes actualizadas (Estadio Olímpico Universitario - EOU) y el programa de evaluaciones.")
    
    df_calendario = pd.DataFrame({
        'Jornada': ['J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10'],
        'Fecha': ['4 Sep', '12 Sep', '18 Sep', '25 Sep', '3 Oct', '9 Oct', '17 Oct', '24 Oct', '30 Oct', 'Noviembre'],
        'Rival': ['Leones Anáhuac', 'Burros Blancos', 'ITESM Puebla', 'ITESM Mty', 'ITESM CEM', 'Linces UVM', 'Águilas Blancas', 'Aztecas UDLAP', 'Leones UAC', 'BYE (Descanso)'],
        'Sede / Condición': [
            'Visita (Cueva del León)', 'Local (EOU)', 'Local (EOU)', 'Local (Borregos)', 
            'Local (EOU)', 'Visita (JOM)', 'Local (EOU)', 'Local (Templo del Dolor)', 'Local (EOU)', 'Descanso'
        ],
        'Evaluaciones Clave': [
            'Mié (Fatiga/Dolor) & Vie (Ansiedad/Confianza)', 'Mié & Vie', 'Mié & Vie', 'Mié & Vie', 
            'Mié & Vie', 'Mié & Vie', 'Mié & Vie', 'Mié & Vie', 'Mié & Vie', 'Descanso'
        ]
    })
    
    st.dataframe(df_calendario, use_container_width=True, hide_index=True)

# --- PESTAÑA 3: BOX SCORE OFICIAL ---
with tab3:
    st.header("📊 Box Score Oficial y Estadísticas por Categoría")
    st.write("Consulta el reporte general del equipo desglosado por bloques técnicos.")
    
    df_global = st.session_state.df.copy()
    
    st.markdown("### 🏈 OFENSIVA: PASSING & RUSHING (QB, WR, RB)")
    df_of = df_global[df_global['Unidad'] == 'Ofensiva'].copy()
    if not df_of.empty:
        df_of['Pases_C_ATT'] = df_of['Pases_Completados_Partidos'].astype(str) + "-" + df_of['Pases_Intentados_Partidos'].astype(str)
        box_passing = df_of[['Jersey', 'Jugador', 'Posición', 'Pases_C_ATT', 'Yardas_Producidas_Partidos']].rename(columns={
            'Jersey': 'NO.', 'Jugador': 'JUGADOR', 'Posición': 'POS', 'Pases_C_ATT': 'CP-ATT', 'Yardas_Producidas_Partidos': 'YDS'
        })
        st.dataframe(box_passing, use_container_width=True, hide_index=True)

    st.markdown("### 🛑 BLOQUEOS Y PROTECCIÓN (OFFENSIVE LINE - OL)")
    df_ol = df_global[df_global['Posición'] == 'OL'].copy()
    if not df_ol.empty:
        box_blocking = df_ol[['Jersey', 'Jugador', 'Posición', 'Bloqueos_Dominio_Partidos', 'Capturas_Permitidas_Partidos']].rename(columns={
            'Jersey': 'NO.', 'Jugador': 'JUGADOR', 'Posición': 'POS', 'Bloqueos_Dominio_Partidos': 'BLOQUEOS DOMINIO (PANCAKES)', 'Capturas_Permitidas_Partidos': 'SACKS PERMITIDOS'
        })
        st.dataframe(box_blocking, use_container_width=True, hide_index=True)

    st.markdown("### 🛡️ DEFENSE (FRONT 7 & SECUNDARIA)")
    df_def = df_global[df_global['Unidad'] == 'Defensiva'].copy()
    if not df_def.empty:
        box_defense = df_def[['Jersey', 'Jugador', 'Posición', 'Tackleadas_Efectivas_Partidos', 'Capturas_QB_Sacks_Partidos', 'Intercepciones_Partidos']].rename(columns={
            'Jersey': 'NO.', 'Jugador': 'JUGADOR', 'Posición': 'POS', 'Tackleadas_Efectivas_Partidos': 'TACKLES', 'Capturas_QB_Sacks_Partidos': 'SACKS', 'Intercepciones_Partidos': 'INT'
        })
        st.dataframe(box_defense, use_container_width=True, hide_index=True)

    st.markdown("### 🦵 KICKING & SPECIAL TEAMS")
    df_st = df_global[df_global['Unidad'] == 'Equipos Especiales'].copy()
    if not df_st.empty:
        box_st = df_st[['Jersey', 'Jugador', 'Posición', 'Goles_Campo_Partidos', 'Puntos_Extra_Partidos']].rename(columns={
            'Jersey': 'NO.', 'Jugador': 'JUGADOR', 'Posición': 'POS', 'Goles_Campo_Partidos': 'GOLES DE CAMPO (FG)', 'Puntos_Extra_Partidos': 'PUNTOS EXTRA (PAT)'
        })
        st.dataframe(box_st, use_container_width=True, hide_index=True)

# --- PESTAÑA 1: ANÁLISIS INDIVIDUAL ---
with tab1:
    df = st.session_state.df.copy()
    df['PJ_Calc'] = df['Partidos_Convocados'].replace(0, 1)
    df['PE_Calc'] = df['Entrenos_Asistidos'].replace(0, 1)

    st.subheader("Filtros de Búsqueda Individual")
    if not df.empty:
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            unidad_filtro = st.selectbox("Unidad", df['Unidad'].unique(), key="u_coach")
        posiciones_disponibles = df[df['Unidad'] == unidad_filtro]['Posición'].unique()
        if len(posiciones_disponibles) > 0:
            with col_f2:
                posicion_filtro = st.selectbox("Posición", posiciones_disponibles, key="p_coach")
            jugadores_disponibles = df[df['Posición'] == posicion_filtro]['Jugador']
            if not jugadores_disponibles.empty:
                with col_f3:
                    jugador_filtro = st.selectbox("Jugador", jugadores_disponibles, key="j_coach")
                stats_jugador = df[df['Jugador'] == jugador_filtro].iloc[0]
                pos = stats_jugador['Posición']

                st.divider()
                st.header(f"Análisis: {jugador_filtro} - #{stats_jugador['Jersey']} ({pos})")
                
                pj = stats_jugador['PJ_Calc']
                col1, col2, col3 = st.columns(3)
                if pos == 'QB':
                    with col1: st.metric("PPG (Yardas / Partido)", f"{stats_jugador['Yardas_Producidas_Partidos'] / pj:.1f} yds")
                    with col2: st.metric("Total Yardas", int(stats_jugador['Yardas_Producidas_Partidos']))
                elif pos in ['WR', 'RB']:
                    with col1: st.metric("PPG (Yardas / Partido)", f"{stats_jugador['Yardas_Producidas_Partidos'] / pj:.1f} yds")
                elif pos == 'OL':
                    with col1: st.metric("PPG (Pancakes / Partido)", f"{stats_jugador['Bloqueos_Dominio_Partidos'] / pj:.1f}")
                elif pos in ['DL', 'LB']:
                    with col1: st.metric("PPG (Tackleadas / Partido)", f"{stats_jugador['Tackleadas_Efectivas_Partidos'] / pj:.1f}")
                elif pos == 'DB':
                    with col1: st.metric("PPG (Intercepciones / P.)", f"{stats_jugador['Intercepciones_Partidos'] / pj:.2f}")
                elif pos in ['K', 'P']:
                    with col1: st.metric("Puntos Totales", int((stats_jugador['Goles_Campo_Partidos'] * 3) + stats_jugador['Puntos_Extra_Partidos']))
