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
        
        # Bienestar Actual
        'Carga_Mental_Actual': [5]*15,
        'Sueno_Actual': [7]*15,
        'Fatiga_Actual': [4]*15,
        
        'Historial_Fatiga': [[4, 5, 4]]*15,
        'Historial_Carga': [[5, 6, 5]]*15
    }
    st.session_state.df = pd.DataFrame(datos_iniciales)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Análisis Individual", "⚙️ Base de Datos", "📈 Rendimiento Equipo", "📝 Registro Diario"])

# --- PESTAÑA 4: REGISTRO DIARIO ---
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
        st.info(f"Registrando actividad tipo: **{tipo_evento}** para **{jugador_seleccionado}** ({pos_actual})")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.subheader("Estado Psicodeportivo Actual")
            carga_nueva = st.slider("Carga Mental / Estrés (1-10)", 1, 10, int(st.session_state.df.at[idx, 'Carga_Mental_Actual']))
            sueno_nuevo = st.slider("Horas de Sueño", 1, 12, int(st.session_state.df.at[idx, 'Sueno_Actual']))
            fatiga_nueva = st.slider("Nivel de Fatiga Física (1-10)", 1, 10, int(st.session_state.df.at[idx, 'Fatiga_Actual']))
            
            nuevo_estatus = st.selectbox("Estatus Médico / Disponibilidad", ["Activo", "Precaución Médica", "Lesionado / Inactivo"], index=["Activo", "Precaución Médica", "Lesionado / Inactivo"].index(st.session_state.df.at[idx, 'Estatus_Medico']) if st.session_state.df.at[idx, 'Estatus_Medico'] in ["Activo", "Precaución Médica", "Lesionado / Inactivo"] else 0)

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
            st.session_state.df.at[idx, 'Estatus_Medico'] = nuevo_estatus
            st.session_state.df.at[idx, 'Carga_Mental_Actual'] = carga_nueva
            st.session_state.df.at[idx, 'Sueno_Actual'] = sueno_nuevo
            st.session_state.df.at[idx, 'Fatiga_Actual'] = fatiga_nueva
            
            hist_fatiga = st.session_state.df.at[idx, 'Historial_Fatiga']
            hist_fatiga.append(fatiga_nueva)
            if len(hist_fatiga) > 5: hist_fatiga.pop(0)
            st.session_state.df.at[idx, 'Historial_Fatiga'] = hist_fatiga
            
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
            else:
                st.session_state.df.at[idx, 'Entrenamientos_Asistidos'] += 1
                st.session_state.df.at[idx, 'Yardas_Entrenamientos'] += n_yardas
                st.session_state.df.at[idx, 'Tackleadas_Entrenamientos'] += n_tackleadas
                st.session_state.df.at[idx, 'Intercepciones_Entrenamientos'] += n_intercepciones
                st.session_state.df.at[idx, 'Pancakes_Entrenamientos'] += n_pancakes
                st.session_state.df.at[idx, 'Sacks_Permitidos_Entrenamientos'] += n_sacks_perm
                st.session_state.df.at[idx, 'Sacks_QB_Entrenamientos'] += n_sacks_qb
            
            st.success(f"✅ ¡Registro guardado para {jugador_seleccionado}!")

# --- PESTAÑA 3: RENDIMIENTO DEL EQUIPO (ACTUALIZADO) ---
with tab3:
    st.header("📈 Rendimiento General por Unidades y Bienestar Colectivo")
    df_global = st.session_state.df.copy()
    
    col_of, col_def, col_st = st.columns(3)
    
    with col_of:
        st.subheader("🏈 Ofensiva")
        of_df = df_global[df_global['Unidad'] == 'Ofensiva']
        st.metric("Yardas Totales (Partidos)", int(of_df['Yardas_Partidos'].sum()))
        st.metric("Promedio Carga Mental", f"{of_df['Carga_Mental_Actual'].mean():.1f}/10")
        st.metric("Fatiga Física Promedio", f"{of_df['Fatiga_Actual'].mean():.1f}/10")
        
    with col_def:
        st.subheader("🛡️ Defensiva")
        def_df = df_global[df_global['Unidad'] == 'Defensiva']
        st.metric("Tackleadas Totales (Partidos)", int(def_df['Tackleadas_Partidos'].sum()))
        st.metric("Promedio Sacks (Partidos)", f"{def_df['Sacks_QB_Partidos'].sum() / max(def_df['Partidos_Jugados'].sum(), 1):.2f}")
        st.metric("Promedio Carga Mental", f"{def_df['Carga_Mental_Actual'].mean():.1f}/10")
        st.metric("Fatiga Física Promedio", f"{def_df['Fatiga_Actual'].mean():.1f}/10")
        
    with col_st:
        st.subheader("🦵 Equipos Especiales")
        st_df = df_global[df_global['Unidad'] == 'Equipos Especiales']
        st.metric("Puntos Totales (Partidos)", int((st_df['Goles_Campo_Partidos'].sum() * 3) + (st_df['Puntos_Extra_Partidos'].sum() * 1)))
        st.metric("Promedio Carga Mental", f"{st_df['Carga_Mental_Actual'].mean():.1f}/10")
        st.metric("Fatiga Física Promedio", f"{st_df['Fatiga_Actual'].mean():.1f}/10")

    st.divider()
    st.subheader("📥 Exportar Reporte Semanal para Head Coach")
    st.write("Descarga la base de datos completa con los estatus médicos y métricas de bienestar actualizadas para compartir por WhatsApp o correo.")
    
    csv_data = df_global.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Reporte en CSV",
        data=csv_data,
        file_name='reporte_semanal_pumas_cu.csv',
        mime='text/csv',
    )

# --- PESTAÑA 2: BASE DE DATOS Y EDICIÓN ---
with tab2:
    st.subheader("Gestión del Roster y Estatus Médico")
    df_editado = st.data_editor(st.session_state.df, num_rows="dynamic", use_container_width=True, hide_index=True)
    if st.button("Guardar Cambios Globales"):
        st.session_state.df = df_editado
        st.success("¡Base de datos actualizada correctamente!")

# --- PESTAÑA 1: ANÁLISIS INDIVIDUAL ---
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
                
                estatus = stats_jugador['Estatus_Medico']
                fatiga = stats_jugador['Fatiga_Actual']
                carga = stats_jugador['Carga_Mental_Actual']
                
                col_title, col_semaforo = st.columns([2, 1])
                with col_title:
                    st.header(f"Análisis: {jugador_filtro} - #{stats_jugador['Jersey']} ({pos})")
                
                with col_semaforo:
                    if estatus == "Lesionado / Inactivo" or fatiga >= 8 or carga >= 8:
                        st.error("🔴 **ESTATUS: ALTO RIESGO / DESCANSO**")
                    elif estatus == "Precaución Médica" or fatiga >= 6 or carga >= 6:
                        st.warning("🟡 **ESTATUS: PRECAUCIÓN / MODERADO**")
                    else:
                        st.success("🟢 **ESTATUS: DISPONIBLE / ÓPTIMO**")

                st.subheader("📊 Rendimiento Promedio: Partidos vs Entrenamientos")
                col1, col2, col3 = st.columns(3)
                
                pj = stats_jugador['PJ_Calc']
                pe = stats_jugador['PE_Calc']

                if pos in ['QB', 'WR', 'RB']:
                    with col1: st.metric("Promedio Yardas / Partido", f"{stats_jugador['Yardas_Partidos'] / pj:.1f} yds")
                    with col2: st.metric("Promedio Yardas / Entreno", f"{stats_jugador['Yardas_Entrenamientos'] / pe:.1f} yds")
                    with col3: st.metric("Total Yardas Acumuladas", int(stats_jugador['Yardas_Partidos'] + stats_jugador['Yardas_Entrenamientos']))
                
                elif pos == 'OL':
                    with col1: st.metric("Promedio Pancakes / Partido", f"{stats_jugador['Pancakes_Partidos'] / pj:.1f}")
                    with col2: st.metric("Promedio Pancakes / Entreno", f"{stats_jugador['Pancakes_Entrenamientos'] / pe:.1f}")
                    with col3: st.metric("Sacks Permitidos (Partidos)", int(stats_jugador['Sacks_Permitidos_Partidos']))
                
                elif pos in ['DL', 'LB']:
                    with col1: st.metric("Promedio Tackleadas / Partido", f"{stats_jugador['Tackleadas_Partidos'] / pj:.1f}")
                    with col2: st.metric("Promedio Sacks / Partido", f"{stats_jugador['Sacks_QB_Partidos'] / pj:.2f}")
                    with col3: st.metric("Total Sacks (Partidos)", int(stats_jugador['Sacks_QB_Partidos']))
                
                elif pos == 'DB':
                    with col1: st.metric("Promedio Intercepciones / Partido", f"{stats_jugador['Intercepciones_Partidos'] / pj:.2f}")
                    with col2: st.metric("Promedio Tackleadas / Partido", f"{stats_jugador['Tackleadas_Partidos'] / pj:.1f}")
                    with col3: st.metric("Total Intercepciones", int(stats_jugador['Intercepciones_Partidos']))
                
                elif pos in ['K', 'P']:
                    with col1: st.metric("Goles de Campo (Partidos)", int(stats_jugador['Goles_Campo_Partidos']))
                    with col2: st.metric("Puntos Extra (Partidos)", int(stats_jugador['Puntos_Extra_Partidos']))
                    with col3: st.metric("Total Puntos (Partidos)", int((stats_jugador['Goles_Campo_Partidos'] * 3) + stats_jugador['Puntos_Extra_Partidos']))

                st.divider()

                st.subheader("🧠 Monitoreo Psicodeportivo y Tendencias Históricas")
                col4, col5, col6 = st.columns(3)
                with col4: st.metric("Carga Mental Actual", f"{carga}/10")
                with col5: st.metric("Horas de Sueño", f"{stats_jugador['Sueno_Actual']} hrs")
                with col6: st.metric("Fatiga Física Actual", f"{fatiga}/10")

                st.write("📈 **Tendencia de Fatiga Reciente (Últimos registros):**")
                df_tendencia_fatiga = pd.DataFrame({'Fatiga': stats_jugador['Historial_Fatiga']})
                st.line_chart(df_tendencia_fatiga)
