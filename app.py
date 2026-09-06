import streamlit as st
import pandas as pd
from datetime import date

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

# 1. Base de datos con el Roster Completo Precargado
if 'df' not in st.session_state:
    roster_data = [
        (0, "Jioshi Alexander Morrison González", "DL"),
        (1, "Raúl Rodrigo Blanco Ruiz", "WR"),
        (2, "Aarón Soriano Vacaseydel", "DB"),
        (3, "Leonardo David Garza Peña Villamil", "QB"),
        (4, "Diego Mercado Sánchez", "LB"),
        (5, "Julio César Hernández Hernández", "DB"),
        (6, "Abraham González López", "LB"),
        (7, "Luis Miguel Bañuelos Medina", "DB"),
        (8, "Luis Higelin Castañón", "DB"),
        (9, "Joaquín Aramis Carriles Palma", "DL"),
        (10, "Emiliano Sánchez Hernández", "QB"),
        (11, "Raymundo Liceá Solano", "DL"),
        (12, "Christopher Bryan Cardona Padrón", "WR"),
        (13, "Javier Santiago Vivas Rodríguez", "WR"),
        (14, "Luis Mario Medrano Silva", "WR"),
        (15, "Emiliano Álvarez Reyes", "CB"),
        (16, "Ian Jeyden Aguilar Rodríguez", "LB"),
        (17, "Jorge Emilio Corona Sandoval", "QB"),
        (18, "Jahdiel Alejandro Ponce Hernández", "WR"),
        (19, "Jirvan Velasco González", "LB"),
        (21, "Armando Moreno Martínez", "DB"),
        (22, "Juan Pablo Acosta Gutiérrez", "LB"),
        (23, "Rodrigo Pérez Rivera", "RB"),
        (24, "David Ceballos Gutiérrez", "CB"),
        (25, "Diego Jack Cerda Álvarez", "DB"),
        (26, "Luis Antonio Schrader Rodríguez", "RB"),
        (27, "Rodrigo Eugenio Villegas Delgado", "LB"),
        (28, "Sergio Alejandro Cervantes Franzoni", "LB"),
        (29, "Santiago Yael Juárez González", "CB"),
        (30, "Néstor Milan Cabrera Botello", "CB"),
        (31, "Juan Carlos Arreola Ramírez", "LB"),
        (32, "Alonso Báez Jimarez", "RB"),
        (33, "Diego Ángel Bañuelos Medina", "LB"),
        (34, "Emilio Melo Robles", "RB"),
        (35, "Hussein Manzur Santillán Ríos", "RB"),
        (39, "Santiago de Cristo Saldaña Sarabia", "LB"),
        (40, "Yeshua Ocampo García", "LB"),
        (42, "Alexis Trejo Caudillo", "LB"),
        (43, "Erick Yael Rodríguez Pérez", "CB"),
        (44, "Manlio Fabio Hernández Hernández", "RB"),
        (51, "Francisco Nogueda Carmona", "OL"),
        (52, "Diego Eliel Contreras Cervantez", "LB"),
        (53, "Jesús Hernández Álvarez", "OL"),
        (54, "Victor Barrientos García", "OL"),
        (58, "Luis Vadhir Corona Torices", "OL"),
        (59, "Óscar González Real", "LB"),
        (68, "Jesús Gael Puente Basañez", "OL"),
        (70, "Carlos Eduardo Aparicio Gasca", "OL"),
        (71, "Pedro Brito Almaguer", "OL"),
        (72, "Jesús Eduardo Trejo López", "OL"),
        (73, "Jesús Fernando Inzunza López", "OL"),
        (74, "Daniel Romero Quezada", "OL"),
        (76, "Andrik Sánchez Benítez", "OL"),
        (77, "Luis Enrique Fernández Vera", "OL"),
        (80, "Alan Andrés Mariano Malagón", "DB"),
        (81, "César Adonai Román Castrejón", "WR"),
        (82, "Jonathan Michel Reyes Pérez", "WR"),
        (83, "Ángel Santiago Reyes Pérez", "WR"),
        (84, "Bruno Said Granados Almeida", "WR"),
        (87, "Emiliano Zamora Jerónimo", "K"),
        (88, "Kin Xanhun Villafuerte Rodríguez", "WR"),
        (89, "Ollin Núñez Solano", "OL"),
        (90, "Rafael Uriel Saavedra Mendoza", "LB"),
        (91, "Miguel Martínez Ayala", "DL"),
        (92, "Sergio Paul Bautista Balderrama", "DL"),
        (94, "Juan Maximiliano Soriano Silva", "DL"),
        (95, "Saul Bautista Balderrama", "DL"),
        (98, "Óscar Alan Miranda Becerril", "WR"),
        (99, "José Manuel Valdéz Orea", "DL")
    ]

    n_jugadores = len(roster_data)
    
    unidades = []
    for _, _, pos in roster_data:
        if pos in ["QB", "RB", "WR", "OL"]:
            unidades.append("Ofensiva")
        elif pos == "K":
            unidades.append("Equipos Especiales")
        else:
            unidades.append("Defensiva")

    datos_iniciales = {
        'Jersey': [item[0] for item in roster_data],
        'Jugador': [item[1] for item in roster_data],
        'Posición': [item[2] for item in roster_data],
        'Unidad': unidades,
        'Estatus_Medico': ['Activo']*n_jugadores,
        
        # Asistencia
        'Entrenos_Programados': [1]*n_jugadores,
        'Entrenos_Asistidos': [1]*n_jugadores,
        'Partidos_Programados': [1]*n_jugadores,
        'Partidos_Convocados': [1]*n_jugadores,
        
        # Rendimiento en campo (Partidos)
        'Yardas_Producidas_Partidos': [0.0]*n_jugadores,
        'Pases_Intentados_Partidos': [0]*n_jugadores,
        'Pases_Completados_Partidos': [0]*n_jugadores,
        'Bloqueos_Dominio_Partidos': [0]*n_jugadores,
        'Capturas_Permitidas_Partidos': [0]*n_jugadores,
        'Tackleadas_Efectivas_Partidos': [0]*n_jugadores,
        'Intercepciones_Partidos': [0]*n_jugadores,
        'Capturas_QB_Sacks_Partidos': [0.0]*n_jugadores,
        'Goles_Campo_Partidos': [0]*n_jugadores,
        'Puntos_Extra_Partidos': [0]*n_jugadores,
        
        # Rendimiento en campo (Entrenamientos)
        'Yardas_Producidas_Entrenos': [0.0]*n_jugadores,
        'Pases_Intentados_Entrenos': [0]*n_jugadores,
        'Pases_Completados_Entrenos': [0]*n_jugadores,
        'Bloqueos_Dominio_Entrenos': [0]*n_jugadores,
        'Capturas_Permitidas_Entrenos': [0]*n_jugadores,
        'Tackleadas_Efectivas_Entrenos': [0]*n_jugadores,
        'Intercepciones_Entrenos': [0]*n_jugadores,
        'Capturas_QB_Sacks_Entrenos': [0.0]*n_jugadores,
        
        # Psico 1
        'Fatiga_Entreno': [4]*n_jugadores,
        'Dolor_Muscular': [3]*n_jugadores,
        'Recuperacion_Entreno': [7]*n_jugadores,
        
        # Psico 2
        'Ansiedad_Competitiva': [5]*n_jugadores,
        'Confianza_Tactica': [8]*n_jugadores,
        'Sueno_Prepartido': [7]*n_jugadores,
        
        'Historial_Fatiga': [[4, 5, 4]]*n_jugadores,
        'Historial_Rendimiento_Juego': [[0.0]]*n_jugadores
    }
    st.session_state.df = pd.DataFrame(datos_iniciales)

if 'active_idx' not in st.session_state:
    st.session_state.active_idx = None
if 'active_jugador_nombre' not in st.session_state:
    st.session_state.active_jugador_nombre = None
if 'active_pos' not in st.session_state:
    st.session_state.active_pos = None

# Pestañas principales
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Análisis Individual", 
    "⚙️ Base de Datos", 
    "📈 Box Score Oficial", 
    "📝 Registro de Datos (Live)", 
    "🧠 Evaluación Psicodeportiva",
    "📅 Calendario"
])

# --- PESTAÑA 4: REGISTRO DE DATOS EN VIVO (PARTIDOS O ENTRENAMIENTOS CON TÉCNICA) ---
with tab4:
    st.header("Registro de Datos y Mesa Táctil en Vivo")
    st.write("Elige el modo de operación para registrar estadísticas de partido o métricas técnicas y físicas en entrenamientos.")

    tipo_modo_registro = st.radio("Modo de Operación:", ["Partido Oficial (Mesa Táctil)", "Entrenamiento Semanal (Mesa Técnica y Carga)"], horizontal=True, key="modo_reg_live")

    st.divider()

    if tipo_modo_registro == "Partido Oficial (Mesa Táctil)":
        contexto_jornada = st.selectbox("Selecciona la Jornada Oficial", [
            "J1 - Leones Anáhuac (Visita)", 
            "J2 - Burros Blancos (Local - EOU)", 
            "J3 - ITESM Puebla (Local - EOU)", 
            "J4 - ITESM Mty (Local)", 
            "J5 - ITESM CEM (Local - EOU)", 
            "J6 - Linces UVM (Visita)", 
            "J7 - Águilas Blancas (Local - EOU)", 
            "J8 - Aztecas UDLAP (Local)", 
            "J9 - Leones UAC (Local - EOU)"
        ], key="jornada_live_sel")

        tipo_seleccion_mesa = st.radio("Método de captura:", ["Lista del Roster", "Número de Jersey Exprés"], horizontal=True, key="tipo_mesa_sel")

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
                    jugador_seleccionado_roster = st.selectbox("Jugador", jugadores_live_list, format_func=format_live_player, key="live_jugador_box")
                else:
                    jugador_seleccionado_roster = None

            if st.button("Confirmar y Seleccionar Atleta"):
                if jugador_seleccionado_roster:
                    match_j = st.session_state.df[st.session_state.df['Jugador'] == jugador_seleccionado_roster]
                    if not match_j.empty:
                        st.session_state.active_idx = match_j.index[0]
                        st.session_state.active_jugador_nombre = match_j['Jugador'].values[0]
                        st.session_state.active_pos = match_j['Posición'].values[0]
                        st.success(f"Atleta seleccionado: **{st.session_state.active_jugador_nombre}** ({st.session_state.active_pos})")

        else:
            col_ex1, col_ex2 = st.columns(2)
            with col_ex1:
                jersey_exprs = st.number_input("Número de Jersey", min_value=0, max_value=99, value=87, key="num_jersey_exprs")
            with col_ex2:
                pos_exprs = st.selectbox("Posición", ["QB", "RB", "WR", "OL", "DL", "LB", "DB", "CB", "K"], key="pos_exprs_box")
                
            if st.button("Confirmar y Cargar por Jersey"):
                unidad_asignada = "Ofensiva" if pos_exprs in ["QB", "RB", "WR", "OL"] else ("Equipos Especiales" if pos_exprs == "K" else "Defensiva")
                match_jersey = st.session_state.df[st.session_state.df['Jersey'] == int(jersey_exprs)]
                
                if not match_jersey.empty:
                    idx_found = match_jersey.index[0]
                    st.session_state.df.at[idx_found, 'Posición'] = pos_exprs
                    st.session_state.df.at[idx_found, 'Unidad'] = unidad_asignada
                    
                    st.session_state.active_idx = idx_found
                    st.session_state.active_jugador_nombre = st.session_state.df.at[idx_found, 'Jugador']
                    st.session_state.active_pos = pos_exprs
                    st.success(f"Atleta cargado: **{st.session_state.active_jugador_nombre}** (#{jersey_exprs} - {pos_exprs})")
                else:
                    st.error("No se encontró ningún jugador con ese número de jersey en el roster.")

        if st.session_state.active_idx is not None and st.session_state.active_jugador_nombre is not None:
            idx_live = st.session_state.active_idx
            jugador_live = st.session_state.active_jugador_nombre
            pos_live = st.session_state.active_pos

            st.divider()
            st.subheader(f"Registrar Acciones de Partido para: {jugador_live} ({pos_live}) [{contexto_jornada}]")

            if st.session_state.df.at[idx_live, 'Partidos_Convocados'] == 0:
                st.session_state.df.at[idx_live, 'Partidos_Convocados'] = 1

            if pos_live == 'QB':
                col_q1, col_q2, col_q3 = st.columns(3)
                with col_q1:
                    yds_plus = st.number_input("Yardas en la Jugada", min_value=-15, max_value=99, value=5, step=1, key="qb_yds_live")
                    if st.button("Sumar Yardas"):
                        st.session_state.df.at[idx_live, 'Yardas_Producidas_Partidos'] += yds_plus
                        st.success(f"{yds_plus} yardas sumadas a {jugador_live}.")
                with col_q2:
                    if st.button("Pase Completado"):
                        st.session_state.df.at[idx_live, 'Pases_Intentados_Partidos'] += 1
                        st.session_state.df.at[idx_live, 'Pases_Completados_Partidos'] += 1
                        st.success("Pase completado registrado.")
                with col_q3:
                    if st.button("Pase Incompleto"):
                        st.session_state.df.at[idx_live, 'Pases_Intentados_Partidos'] += 1
                        st.success("Pase incompleto registrado.")

            elif pos_live in ['WR', 'RB']:
                col_w1 = st.columns(1)[0]
                with col_w1:
                    yds_plus = st.number_input("Yardas en la Jugada", min_value=-5, max_value=99, value=5, step=1, key="wr_yds_live")
                    if st.button("Sumar Yardas de Avance"):
                        st.session_state.df.at[idx_live, 'Yardas_Producidas_Partidos'] += yds_plus
                        st.success(f"{yds_plus} yardas sumadas a {jugador_live}.")

            elif pos_live == 'OL':
                col_ol1, col_ol2 = st.columns(2)
                with col_ol1:
                    if st.button("Bloqueo de Dominio (Pancake)"):
                        st.session_state.df.at[idx_live, 'Bloqueos_Dominio_Partidos'] += 1
                        st.success("Pancake registrado.")
                with col_ol2:
                    if st.button("Sack Permitido"):
                        st.session_state.df.at[idx_live, 'Capturas_Permitidas_Partidos'] += 1
                        st.success("Sack permitido registrado.")

            elif pos_live in ['DL', 'LB']:
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    if st.button("Tackleada Efectiva"):
                        st.session_state.df.at[idx_live, 'Tackleadas_Efectivas_Partidos'] += 1
                        st.success("Tackleada registrada.")
                with col_d2:
                    if st.button("Sack Defensivo"):
                        st.session_state.df.at[idx_live, 'Capturas_QB_Sacks_Partidos'] += 1.0
                        st.success("Sack registrado.")

            elif pos_live in ['DB', 'CB']:
                col_db1, col_db2 = st.columns(2)
                with col_db1:
                    if st.button("Tackleada Efectiva"):
                        st.session_state.df.at[idx_live, 'Tackleadas_Efectivas_Partidos'] += 1
                        st.success("Tackleada registrada.")
                with col_db2:
                    if st.button("Intercepción (INT)"):
                        st.session_state.df.at[idx_live, 'Intercepciones_Partidos'] += 1
                        st.success("Intercepción registrada.")

            elif pos_live == 'K':
                col_k1, col_k2 = st.columns(2)
                with col_k1:
                    if st.button("Gol de Campo (3 pts)"):
                        st.session_state.df.at[idx_live, 'Goles_Campo_Partidos'] += 1
                        st.success("Gol de campo registrado.")
                with col_k2:
                    if st.button("Punto Extra (PAT)"):
                        st.session_state.df.at[idx_live, 'Puntos_Extra_Partidos'] += 1
                        st.success("Punto extra registrado.")

    else:
        # Modo Entrenamiento con Calendario Editable y Métricas Técnicas
        st.subheader("Registro de Práctica: Carga Física y Técnica")
        
        col_cal1, col_cal2 = st.columns(2)
        with col_cal1:
            fecha_entreno = st.date_input("📅 Fecha de la Práctica", value=date.today(), key="calendar_entreno_date")
        with col_cal2:
            sesion_tipo = st.selectbox("Tipo de Sesión", ["Práctica Táctica / Fuerte", "Práctica Ligera / Recuperación", "Entrenamiento Pre-partido"], key="tipo_sesion_entreno")

        unidad_entreno_sel = st.selectbox("Selecciona la Unidad", st.session_state.df['Unidad'].unique(), key="entreno_unidad_live")
        jugadores_entreno_list = st.session_state.df[st.session_state.df['Unidad'] == unidad_entreno_sel]['Jugador'].tolist()

        def format_entreno_player(nombre):
            sub_df = st.session_state.df[st.session_state.df['Jugador'] == nombre]
            if not sub_df.empty:
                pos = sub_df['Posición'].values[0]
                jersey = sub_df['Jersey'].values[0]
                return f"#{jersey} - {nombre} ({pos})"
            return nombre

        jugador_entreno_sel = st.selectbox("Selecciona al Atleta", jugadores_entreno_list, format_func=format_entreno_player, key="entreno_atleta_live")

        if jugador_entreno_sel:
            idx_ent = st.session_state.df.index[st.session_state.df['Jugador'] == jugador_entreno_sel].tolist()[0]
            pos_ent = st.session_state.df.at[idx_ent, 'Posición']

            with st.form("form_registro_entreno_live"):
                st.markdown(f"**Registrando sesión para:** {jugador_entreno_sel} ({pos_ent}) — Fecha: `{fecha_entreno}`")
                
                st.markdown("---")
                st.markdown("##### 🏋️ Bienestar y Carga Física")
                fatiga_ent_val = st.slider("Fatiga Física Acumulada (1-10)", 1, 10, int(st.session_state.df.at[idx_ent, 'Fatiga_Entreno']))
                dolor_ent_val = st.slider("Dolor Muscular / Molestias (1-10)", 1, 10, int(st.session_state.df.at[idx_ent, 'Dolor_Muscular']))
                recup_ent_val = st.slider("Nivel de Recuperación / Frescura (1-10)", 1, 10, int(st.session_state.df.at[idx_ent, 'Recuperacion_Entreno']))
                
                asist_ent_val = st.selectbox("Asistencia a la Sesión", ["Asistió", "No Asistió"])
                estatus_med_val = st.selectbox("Estatus Médico", ["Activo", "Precaución Médica", "Lesionado / Inactivo"])

                st.markdown("---")
                st.markdown("##### 🏈 Rendimiento Técnico en Práctica")
                
                n_yds_ent, n_p_int_ent, n_p_comp_ent = 0, 0, 0
                n_pancakes_ent, n_sacks_perm_ent = 0, 0
                n_tack_ent, n_int_ent, n_sacks_def_ent = 0, 0, 0.0

                if pos_ent == 'QB':
                    n_yds_ent = st.number_input("Yardas Lanzadas / Acarreo en Práctica", min_value=-10, value=0)
                    col_ep1, col_ep2 = st.columns(2)
                    with col_ep1: n_p_comp_ent = st.number_input("Pases Completados en Práctica", min_value=0, value=0)
                    with col_ep2: n_p_int_ent = st.number_input("Pases Intentados en Práctica", min_value=0, value=0)
                elif pos_ent in ['WR', 'RB']:
                    n_yds_ent = st.number_input("Yardas Ganadas en Práctica", min_value=-5, value=0)
                elif pos_ent == 'OL':
                    n_pancakes_ent = st.number_input("Bloqueos de Dominio (Pancakes) en Práctica", min_value=0, value=0)
                    n_sacks_perm_ent = st.number_input("Sacks Permitidos en Práctica", min_value=0, value=0)
                elif pos_ent in ['DL', 'LB']:
                    n_tack_ent = st.number_input("Tackleadas Efectivas en Práctica", min_value=0, value=0)
                    n_sacks_def_ent = st.number_input("Sacks Defensivos en Práctica", min_value=0.0, value=0.0, step=0.5)
                elif pos_ent in ['DB', 'CB']:
                    n_tack_ent = st.number_input("Tackleadas Efectivas en Práctica", min_value=0, value=0)
                    n_int_ent = st.number_input("Intercepciones en Práctica", min_value=0, value=0)

                guardar_entreno_btn = st.form_submit_button("Guardar Registro Completo de Práctica")
                if guardar_entreno_btn:
                    st.session_state.df.at[idx_ent, 'Entrenos_Programados'] += 1
                    if asist_ent_val == "Asistió":
                        st.session_state.df.at[idx_ent, 'Entrenos_Asistidos'] += 1
                    
                    st.session_state.df.at[idx_ent, 'Fatiga_Entreno'] = fatiga_ent_val
                    st.session_state.df.at[idx_ent, 'Dolor_Muscular'] = dolor_ent_val
                    st.session_state.df.at[idx_ent, 'Recuperacion_Entreno'] = recup_ent_val
                    st.session_state.df.at[idx_ent, 'Estatus_Medico'] = estatus_med_val

                    # Acumular métricas técnicas de entreno
                    st.session_state.df.at[idx_ent, 'Yardas_Producidas_Entrenos'] += n_yds_ent
                    st.session_state.df.at[idx_ent, 'Pases_Intentados_Entrenos'] += n_p_int_ent
                    st.session_state.df.at[idx_ent, 'Pases_Completados_Entrenos'] += n_p_comp_ent
                    st.session_state.df.at[idx_ent, 'Bloqueos_Dominio_Entrenos'] += n_pancakes_ent
                    st.session_state.df.at[idx_ent, 'Capturas_Permitidas_Entrenos'] += n_sacks_perm_ent
                    st.session_state.df.at[idx_ent, 'Tackleadas_Efectivas_Entrenos'] += n_tack_ent
                    st.session_state.df.at[idx_ent, 'Intercepciones_Entrenos'] += n_int_ent
                    st.session_state.df.at[idx_ent, 'Capturas_QB_Sacks_Entrenos'] += n_sacks_def_ent

                    hist_f = st.session_state.df.at[idx_ent, 'Historial_Fatiga']
                    hist_f.append(fatiga_ent_val)
                    if len(hist_f) > 5: hist_f.pop(0)
                    st.session_state.df.at[idx_ent, 'Historial_Fatiga'] = hist_f

                    st.success(f"Práctica del {fecha_entreno} guardada exitosamente para {jugador_entreno_sel}.")

# --- PESTAÑA 5: EVALUACIÓN PSICODEPORTIVA ---
with tab5:
    st.header("🧠 Evaluación y Monitoreo Psicodeportivo")
    st.write("Registra las evaluaciones de mitad de semana (fatiga/dolor) o la activación pre-partido (ansiedad/sueño).")

    unidad_psi = st.selectbox("Selecciona la Unidad", st.session_state.df['Unidad'].unique(), key="psi_unidad_sel")
    jugadores_psi_list = st.session_state.df[st.session_state.df['Unidad'] == unidad_psi]['Jugador'].tolist()

    def format_psi_player(nombre):
        sub_df = st.session_state.df[st.session_state.df['Jugador'] == nombre]
        if not sub_df.empty:
            pos = sub_df['Posición'].values[0]
            jersey = sub_df['Jersey'].values[0]
            return f"#{jersey} - {nombre} ({pos})"
        return nombre

    jugador_psi_sel = st.selectbox("Selecciona al Atleta", jugadores_psi_list, format_func=format_psi_player, key="psi_jugador_sel")

    if jugador_psi_sel:
        idx_psi = st.session_state.df.index[st.session_state.df['Jugador'] == jugador_psi_sel].tolist()[0]
        
        tipo_encuesta = st.selectbox(
            "Selecciona el tipo de evaluación:", 
            ["Evaluación de Mitad de Semana (Entrenamiento)", "Evaluación Pre-partido (Matchday)"]
        )

        with st.form("form_psicodeportivo_ind"):
            if tipo_encuesta == "Evaluación de Mitad de Semana (Entrenamiento)":
                st.markdown("#### Factores de Carga y Fatiga en Entrenamientos")
                fatiga_val = st.slider("Fatiga Física Acumulada (1-10)", 1, 10, int(st.session_state.df.at[idx_psi, 'Fatiga_Entreno']))
                dolor_val = st.slider("Dolor Muscular / Molestias (1-10)", 1, 10, int(st.session_state.df.at[idx_psi, 'Dolor_Muscular']))
                recup_val = st.slider("Nivel de Recuperación (1-10)", 1, 10, int(st.session_state.df.at[idx_psi, 'Recuperacion_Entreno']))
                asist_ent = st.selectbox("Asistencia al Entrenamiento", ["Asistió", "No Asistió"])
            else:
                st.markdown("#### Factores Psicológicos y de Activación Pre-partido")
                ansiedad_val = st.slider("Nivel de Ansiedad / Activación (1-10)", 1, 10, int(st.session_state.df.at[idx_psi, 'Ansiedad_Competitiva']))
                confianza_val = st.slider("Confianza en el Plan de Juego (1-10)", 1, 10, int(st.session_state.df.at[idx_psi, 'Confianza_Tactica']))
                sueno_val = st.slider("Horas de Sueño Noche Previa", 1, 12, int(st.session_state.df.at[idx_psi, 'Sueno_Prepartido']))

            estatus_med = st.selectbox("Estatus Médico / Disponibilidad", ["Activo", "Precaución Médica", "Lesionado / Inactivo"])

            guardar_psi = st.form_submit_button("Guardar Evaluación Psicológica")
            if guardar_psi:
                st.session_state.df.at[idx_psi, 'Estatus_Medico'] = estatus_med
                if tipo_encuesta == "Evaluación de Mitad de Semana (Entrenamiento)":
                    st.session_state.df.at[idx_psi, 'Fatiga_Entreno'] = fatiga_val
                    st.session_state.df.at[idx_psi, 'Dolor_Muscular'] = dolor_val
                    st.session_state.df.at[idx_psi, 'Recuperacion_Entreno'] = recup_val
                    st.session_state.df.at[idx_psi, 'Entrenos_Programados'] += 1
                    if asist_ent == "Asistió":
                        st.session_state.df.at[idx_psi, 'Entrenos_Asistidos'] += 1
                    
                    hist_f = st.session_state.df.at[idx_psi, 'Historial_Fatiga']
                    hist_f.append(fatiga_val)
                    if len(hist_f) > 5: hist_f.pop(0)
                    st.session_state.df.at[idx_psi, 'Historial_Fatiga'] = hist_f
                else:
                    st.session_state.df.at[idx_psi, 'Ansiedad_Competitiva'] = ansiedad_val
                    st.session_state.df.at[idx_psi, 'Confianza_Tactica'] = confianza_val
                    st.session_state.df.at[idx_psi, 'Sueno_Prepartido'] = sueno_val

                st.success(f"Evaluación guardada exitosamente para {jugador_psi_sel}.")

# --- PESTAÑA 2: BASE DE DATOS Y GESTIÓN DE ROSTER ---
with tab2:
    st.header("Gestión del Roster y Base de Datos Analítica")
    st.write("Puedes editar directamente cualquier celda en las siguientes tablas (nombres, estatus, estadísticas, bienestar).")

    sub_psi, sub_of, sub_def, sub_st = st.tabs([
        "Bienestar y Estatus Médico", 
        "Unidad Ofensiva", 
        "Unidad Defensiva", 
        "Equipos Especiales"
    ])

    with sub_psi:
        st.subheader("Edición Directa: Bienestar Psicológico y Estatus Médico")
        cols_psi_all = [
            'Jersey', 'Jugador', 'Posición', 'Unidad', 'Estatus_Medico',
            'Fatiga_Entreno', 'Dolor_Muscular', 'Recuperacion_Entreno',
            'Ansiedad_Competitiva', 'Confianza_Tactica', 'Sueno_Prepartido'
        ]
        df_psi_edit = st.data_editor(st.session_state.df[cols_psi_all], use_container_width=True, hide_index=True, key="editor_psi_direct")
        if not df_psi_edit.equals(st.session_state.df[cols_psi_all]):
            st.session_state.df.update(df_psi_edit)
            st.success("Datos de bienestar actualizados.")

    with sub_of:
        st.subheader("Edición Directa: Rendimiento Ofensivo")
        df_of = st.session_state.df[st.session_state.df['Unidad'] == 'Ofensiva'].copy()
        cols_of_view = [
            'Jersey', 'Jugador', 'Posición', 'Partidos_Convocados', 
            'Yardas_Producidas_Partidos', 'Pases_Intentados_Partidos', 'Pases_Completados_Partidos',
            'Bloqueos_Dominio_Partidos', 'Capturas_Permitidas_Partidos'
        ]
        df_of_edited = st.data_editor(df_of[cols_of_view], use_container_width=True, hide_index=True, key="edit_of_direct")
        if not df_of_edited.equals(df_of[cols_of_view]):
            st.session_state.df.update(df_of_edited)
            st.success("Estadísticas ofensivas actualizadas.")

    with sub_def:
        st.subheader("Edición Directa: Rendimiento Defensivo")
        df_def = st.session_state.df[st.session_state.df['Unidad'] == 'Defensiva'].copy()
        cols_def_view = [
            'Jersey', 'Jugador', 'Posición', 'Partidos_Convocados',
            'Tackleadas_Efectivas_Partidos', 'Intercepciones_Partidos', 'Capturas_QB_Sacks_Partidos'
        ]
        df_def_edited = st.data_editor(df_def[cols_def_view], use_container_width=True, hide_index=True, key="edit_def_direct")
        if not df_def_edited.equals(df_def[cols_def_view]):
            st.session_state.df.update(df_def_edited)
            st.success("Estadísticas defensivas actualizadas.")

    with sub_st:
        st.subheader("Edición Directa: Equipos Especiales")
        df_st = st.session_state.df[st.session_state.df['Posición'] == 'K'].copy()
        cols_st_view = [
            'Jersey', 'Jugador', 'Posición', 'Partidos_Convocados',
            'Goles_Campo_Partidos', 'Puntos_Extra_Partidos'
        ]
        df_st_edited = st.data_editor(df_st[cols_st_view], use_container_width=True, hide_index=True, key="edit_st_direct")
        if not df_st_edited.equals(df_st[cols_st_view]):
            st.session_state.df.update(df_st_edited)
            st.success("Estadísticas de pateo actualizadas.")

# --- PESTAÑA 6: CALENDARIO ---
with tab6:
    st.header("Calendario Oficial ONEFA 2026 y Planificación Psicológica")
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
    st.header("Box Score Oficial y Estadísticas por Categoría")
    st.write("Puedes modificar cualquier número o nombre directamente sobre las tablas del Box Score.")
    
    df_global = st.session_state.df.copy()
    
    st.markdown("### OFENSIVA: PASSING & RUSHING (QB, WR, RB)")
    df_of = df_global[df_global['Unidad'] == 'Ofensiva'].copy()
    if not df_of.empty:
        df_of['Pases_C_ATT'] = df_of['Pases_Completados_Partidos'].astype(str) + "-" + df_of['Pases_Intentados_Partidos'].astype(str)
        box_passing = df_of[['Jersey', 'Jugador', 'Posición', 'Pases_C_ATT', 'Yardas_Producidas_Partidos']].rename(columns={
            'Jersey': 'NO.', 'Jugador': 'JUGADOR', 'Posición': 'POS', 'Pases_C_ATT': 'CP-ATT', 'Yardas_Producidas_Partidos': 'YDS'
        })
        box_passing_edit = st.data_editor(box_passing, use_container_width=True, hide_index=True, key="box_pass_edit")
        if not box_passing_edit.equals(box_passing):
            st.success("Box score de ofensiva actualizado.")

    st.markdown("### BLOQUEOS Y PROTECCIÓN (OFFENSIVE LINE - OL)")
    df_ol = df_global[df_global['Posición'] == 'OL'].copy()
    if not df_ol.empty:
        box_blocking = df_ol[['Jersey', 'Jugador', 'Posición', 'Bloqueos_Dominio_Partidos', 'Capturas_Permitidas_Partidos']].rename(columns={
            'Jersey': 'NO.', 'Jugador': 'JUGADOR', 'Posición': 'POS', 'Bloqueos_Dominio_Partidos': 'BLOQUEOS DOMINIO (PANCAKES)', 'Capturas_Permitidas_Partidos': 'SACKS PERMITIDOS'
        })
        box_blocking_edit = st.data_editor(box_blocking, use_container_width=True, hide_index=True, key="box_block_edit")
        if not box_blocking_edit.equals(box_blocking):
            st.success("Box score de línea ofensiva actualizado.")

    st.markdown("### DEFENSE (FRONT 7 & SECUNDARIA)")
    df_def = df_global[df_global['Unidad'] == 'Defensiva'].copy()
    if not df_def.empty:
        box_defense = df_def[['Jersey', 'Jugador', 'Posición', 'Tackleadas_Efectivas_Partidos', 'Capturas_QB_Sacks_Partidos', 'Intercepciones_Partidos']].rename(columns={
            'Jersey': 'NO.', 'Jugador': 'JUGADOR', 'Posición': 'POS', 'Tackleadas_Efectivas_Partidos': 'TACKLES', 'Capturas_QB_Sacks_Partidos': 'SACKS', 'Intercepciones_Partidos': 'INT'
        })
        box_def_edit = st.data_editor(box_defense, use_container_width=True, hide_index=True, key="box_def_edit")
        if not box_def_edit.equals(box_defense):
            st.success("Box score defensivo actualizado.")

    st.markdown("### KICKING & SPECIAL TEAMS")
    df_st = df_global[df_global['Posición'] == 'K'].copy()
    if not df_st.empty:
        box_st = df_st[['Jersey', 'Jugador', 'Posición', 'Goles_Campo_Partidos', 'Puntos_Extra_Partidos']].rename(columns={
            'Jersey': 'NO.', 'Jugador': 'JUGADOR', 'Posición': 'POS', 'Goles_Campo_Partidos': 'GOLES DE CAMPO (FG)', 'Puntos_Extra_Partidos': 'PUNTOS EXTRA (PAT)'
        })
        box_st_edit = st.data_editor(box_st, use_container_width=True, hide_index=True, key="box_st_edit")
        if not box_st_edit.equals(box_st):
            st.success("Box score de pateo actualizado.")

# --- PESTAÑA 1: ANÁLISIS INDIVIDUAL COMPLETO ---
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
                
                estatus = stats_jugador['Estatus_Medico']
                fatiga_entreno = stats_jugador['Fatiga_Entreno']
                ansiedad = stats_jugador['Ansiedad_Competitiva']
                sueno_pre = stats_jugador['Sueno_Prepartido']
                
                factor_sueno_inv = max(0, (10 - sueno_pre))
                indice_riesgo = (fatiga_entreno * 0.4) + (ansiedad * 0.4) + (factor_sueno_inv * 0.2)

                col_title, col_semaforo = st.columns([2, 1])
                with col_title:
                    st.header(f"Análisis: {jugador_filtro} - #{stats_jugador['Jersey']} ({pos})")
                
                with col_semaforo:
                    if estatus == "Lesionado / Inactivo" or indice_riesgo >= 7.0:
                        st.error(f"RIESGO ALTO (Índice: {indice_riesgo:.1f}/10)")
                    elif estatus == "Precaución Médica" or indice_riesgo >= 5.0:
                        st.warning(f"RIESGO MODERADO (Índice: {indice_riesgo:.1f}/10)")
                    else:
                        st.success(f"ÓPTIMO / DISPONIBLE (Índice: {indice_riesgo:.1f}/10)")

                entrenos_tot = max(int(stats_jugador['Entrenos_Programados']), 1)
                entrenos_asist = int(stats_jugador['Entrenos_Asistidos'])
                pct_entrenos = min(100.0, (entrenos_asist / entrenos_tot) * 100)

                partidos_tot = max(int(stats_jugador['Partidos_Programados']), 1)
                partidos_jugados = int(stats_jugador['Partidos_Convocados'])
                pct_partidos = min(100.0, (partidos_jugados / partidos_tot) * 100)

                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    st.markdown(f"Asistencia a Entrenamientos: `{pct_entrenos:.1f}%` ({entrenos_asist}/{entrenos_tot})")
                with col_p2:
                    st.markdown(f"Convocatoria en Partidos: `{pct_partidos:.1f}%` ({partidos_jugados}/{partidos_tot})")

                st.subheader("Métricas de Rendimiento (Partidos & Entrenamientos)")
                col1, col2, col3 = st.columns(3)
                
                pj = stats_jugador['PJ_Calc']
                pe = stats_jugador['PE_Calc']

                if pos == 'QB':
                    intentos_tot = stats_jugador['Pases_Intentados_Partidos']
                    completados_tot = stats_jugador['Pases_Completados_Partidos']
                    pct_comp = (completados_tot / intentos_tot * 100) if intentos_tot > 0 else 0.0
                    yardas_ppg = stats_jugador['Yardas_Producidas_Partidos'] / pj
                    yardas_ent = stats_jugador['Yardas_Producidas_Entrenos']
                    with col1: st.metric("PPG (Yardas / Partido)", f"{yardas_ppg:.1f} yds")
                    with col2: st.metric("AVG Pases (Comp / Int)", f"{pct_comp:.1f}%", f"{completados_tot}/{intentos_tot}")
                    with col3: st.metric("Yardas en Entrenos", int(yardas_ent))
                elif pos in ['WR', 'RB']:
                    yardas_ppg = stats_jugador['Yardas_Producidas_Partidos'] / pj
                    yardas_ent = stats_jugador['Yardas_Producidas_Entrenos']
                    with col1: st.metric("PPG (Yardas / Partido)", f"{yardas_ppg:.1f} yds")
                    with col2: st.metric("Yardas Acumuladas Prácticas", int(yardas_ent))
                    with col3: st.metric("Total Yardas Globales", int(stats_jugador['Yardas_Producidas_Partidos'] + yardas_ent))
                
                elif pos == 'OL':
                    pancakes_ppg = stats_jugador['Bloqueos_Dominio_Partidos'] / pj
                    pancakes_ent = stats_jugador['Bloqueos_Dominio_Entrenos']
                    with col1: st.metric("PPG (Pancakes / Partido)", f"{pancakes_ppg:.1f}")
                    with col2: st.metric("Pancakes en Prácticas", int(pancakes_ent))
                    with col3: st.metric("Sacks Permitidos (Total)", int(stats_jugador['Capturas_Permitidas_Partidos'] + stats_jugador['Capturas_Permitidas_Entrenos']))
                
                elif pos in ['DL', 'LB']:
                    tackleadas_ppg = stats_jugador['Tackleadas_Efectivas_Partidos'] / pj
                    tackleadas_ent = stats_jugador['Tackleadas_Efectivas_Entrenos']
                    with col1: st.metric("PPG (Tackleadas / Partido)", f"{tackleadas_ppg:.1f}")
                    with col2: st.metric("Tackleadas en Prácticas", int(tackleadas_ent))
                    with col3: st.metric("Total Sacks Defensivos", float(stats_jugador['Capturas_QB_Sacks_Partidos'] + stats_jugador['Capturas_QB_Sacks_Entrenos']))
                
                elif pos in ['DB', 'CB']:
                    intercepciones_ppg = stats_jugador['Intercepciones_Partidos'] / pj
                    tackleadas_ppg = stats_jugador['Tackleadas_Efectivas_Partidos'] / pj
                    with col1: st.metric("PPG (Intercepciones / P.)", f"{intercepciones_ppg:.2f}")
                    with col2: st.metric("AVG Tackleadas / Partido", f"{tackleadas_ppg:.1f}")
                    with col3: st.metric("Total Intercepciones", int(stats_jugador['Intercepciones_Partidos'] + stats_jugador['Intercepciones_Entrenos']))
                
                elif pos == 'K':
                    goles_campo = stats_jugador['Goles_Campo_Partidos']
                    puntos_extra = stats_jugador['Puntos_Extra_Partidos']
                    puntos_totales = (goles_campo * 3) + puntos_extra
                    ppg_puntos = puntos_totales / pj
                    with col1: st.metric("PPG (Puntos / Partido)", f"{ppg_puntos:.1f} pts")
                    with col2: st.metric("Goles de Campo (Total)", int(goles_campo))
                    with col3: st.metric("Puntos Extra (Total)", int(puntos_extra))

                st.divider()

                st.subheader("Perfil Psicodeportivo Especializado")
                
                col_psi1, col_psi2 = st.columns(2)
                with col_psi1:
                    st.markdown("#### Mitad de Semana (Entrenamientos)")
                    st.metric("Fatiga Física Acumulada", f"{stats_jugador['Fatiga_Entreno']}/10")
                    st.metric("Dolor / Molestias Físicas", f"{stats_jugador['Dolor_Muscular']}/10")
                    st.metric("Recuperación / Frescura", f"{stats_jugador['Recuperacion_Entreno']}/10")
                
                with col_psi2:
                    st.markdown("#### Pre-partido (Matchday)")
                    st.metric("Ansiedad / Activación", f"{stats_jugador['Ansiedad_Competitiva']}/10")
                    st.metric("Confianza Táctica", f"{stats_jugador['Confianza_Tactica']}/10")
                    st.metric("Sueño Noche Previa", f"{stats_jugador['Sueno_Prepartido']} hrs")

                st.divider()

                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    st.write("Tendencia de Fatiga en Entrenamientos:")
                    df_tendencia_fatiga = pd.DataFrame({'Fatiga': stats_jugador['Historial_Fatiga']})
                    st.line_chart(df_tendencia_fatiga)
                with col_g2:
                    st.write("Evolución de Rendimiento Juego a Juego:")
                    df_tendencia_juego = pd.DataFrame({'Impacto': stats_jugador['Historial_Rendimiento_Juego']})
                    st.line_chart(df_tendencia_juego)
