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

# 1. Base de datos inicial con terminología profesional
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
        
        # Rendimiento en campo (Terminología Profesional)
        'Yardas_Producidas_Partidos': [0]*15,
        'Tackleadas_Efectivas_Partidos': [0]*15,
        'Intercepciones_Partidos': [0]*15,
        'Bloqueos_Dominio_Partidos': [0]*15, # Nombre profesional para pancakes
        'Capturas_Permitidas_Partidos': [0]*15,
        'Capturas_QB_Sacks_Partidos': [0]*15,
        'Goles_Campo_Partidos': [0]*15,
        'Puntos_Extra_Partidos': [0]*15,
        
        'Yardas_Producidas_Entrenos': [0]*15,
        'Tackleadas_Efectivas_Entrenos': [0]*15,
        'Intercepciones_Entrenos': [0]*15,
        'Bloqueos_Dominio_Entrenos': [0]*15,
        'Capturas_Permitidas_Entrenos': [0]*15,
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

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Análisis Individual", "⚙️ Base de Datos", "📈 Rendimiento Equipo", "📝 Registro Diario", "📅 Calendario y Planificación"])

# --- PESTAÑA 2: BASE DE DATOS MODULARIZADA Y PROFESIONAL ---
with tab2:
    st.header("⚙️ Gestión y Consulta de la Base de Datos")
    st.write("Datos organizados por área bajo estándares de analítica deportiva profesional.")

    sub_psi, sub_of, sub_def, sub_st = st.tabs([
        "🧠 Psicodeportivo y Bienestar", 
        "🏈 Unidad Ofensiva", 
        "🛡️ Unidad Defensiva", 
        "🦵 Equipos Especiales"
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
        st.subheader("Rendimiento Técnico: Unidad Ofensiva")
        cols_of = [
            'Jersey', 'Jugador', 'Posición', 'Partidos_Convocados',
            'Yardas_Producidas_Partidos', 'Bloqueos_Dominio_Partidos', 'Capturas_Permitidas_Partidos',
            'Yardas_Producidas_Entrenos', 'Bloqueos_Dominio_Entrenos', 'Capturas_Permitidas_Entrenos'
        ]
        indices_of = st.session_state.df[st.session_state.df['Unidad'] == 'Ofensiva'].index
        df_of_edit = st.data_editor(st.session_state.df.loc[indices_of, cols_of], use_container_width=True, hide_index=True, key="editor_of")
        if st.button("Guardar Cambios Ofensiva"):
            st.session_state.df.update(df_of_edit)
            st.success("¡Estadísticas ofensivas actualizadas correctamente!")

    with sub_def:
        st.subheader("Rendimiento Técnico: Unidad Defensiva (Front 7 y Secundaria)")
        cols_def = [
            'Jersey', 'Jugador', 'Posición', 'Partidos_Convocados',
            'Tackleadas_Efectivas_Partidos', 'Intercepciones_Partidos', 'Capturas_QB_Sacks_Partidos',
            'Tackleadas_Efectivas_Entrenos', 'Intercepciones_Entrenos', 'Capturas_QB_Sacks_Entrenos'
        ]
        indices_def = st.session_state.df[st.session_state.df['Unidad'] == 'Defensiva'].index
        df_def_edit = st.data_editor(st.session_state.df.loc[indices_def, cols_def], use_container_width=True, hide_index=True, key="editor_def")
        if st.button("Guardar Cambios Defensiva"):
            st.session_state.df.update(df_def_edit)
            st.success("¡Estadísticas defensivas actualizadas correctamente!")

    with sub_st:
        st.subheader("Rendimiento Técnico: Equipos Especiales")
        cols_st = [
            'Jersey', 'Jugador', 'Posición', 'Partidos_Convocados',
            'Goles_Campo_Partidos', 'Puntos_Extra_Partidos'
        ]
        indices_st = st.session_state.df[st.session_state.df['Unidad'] == 'Equipos Especiales'].index
        df_st_edit = st.data_editor(st.session_state.df.loc[indices_st, cols_st], use_container_width=True, hide_index=True, key="editor_st")
        if st.button("Guardar Cambios Equipos Especiales"):
            st.session_state.df.update(df_st_edit)
            st.success("¡Estadísticas de equipos especiales actualizadas correctamente!")

# --- PESTAÑA 4: REGISTRO DIARIO ---
with tab4:
    st.header("Captura de Datos Operativos por Jornada")
    
    col_filtro1, col_filtro2, col_filtro3, col_filtro4 = st.columns(4)
    with col_filtro1:
        tipo_registro_principal = st.selectbox("¿Qué deseas registrar?", ["Estadísticas de Partido", "Monitoreo Psicodeportivo y Bienestar"])
    with col_filtro2:
        jornada_seleccionada = st.selectbox("Selecciona la Jornada", [
            "J1 - Leones Anáhuac (Visita)", 
            "J2 - Burros Blancos (Local)", 
            "J3 - ITESM Puebla (Visita)", 
            "J4 - ITESM Mty (Local)", 
            "J5 - ITESM CEM (Visita)", 
            "J6 - Linces UVM (Visita)", 
            "J7 - Águilas Blancas (Local)", 
            "J8 - Aztecas UDLAP (Local)", 
            "J9 - Leones UAC (Local)", 
            "Entrenamiento Semanal Regular"
        ])
    with col_filtro3:
        unidad_registro = st.selectbox("Unidad", st.session_state.df['Unidad'].unique(), key="unidad_reg")
    
    jugadores_filtrados = st.session_state.df[st.session_state.df['Unidad'] == unidad_registro]['Jugador'].tolist()
    
    def mostrar_nombre_con_posicion(nombre_jugador):
        pos = st.session_state.df[st.session_state.df['Jugador'] == nombre_jugador]['Posición'].values[0]
        return f"{nombre_jugador} ({pos})"
    
    with col_filtro4:
        jugador_seleccionado = st.selectbox("Jugador", jugadores_filtrados, format_func=mostrar_nombre_con_posicion, key="jugador_reg")
    
    idx = st.session_state.df.index[st.session_state.df['Jugador'] == jugador_seleccionado].tolist()[0]
    pos_actual = st.session_state.df.at[idx, 'Posición']
    
    st.divider()

    if tipo_registro_principal == "Estadísticas de Partido":
        st.subheader(f"🏟️ Registro de Partido ({jornada_seleccionada}) para: {jugador_seleccionado} ({pos_actual})")
        
        with st.form("form_partido"):
            convocatoria_partido = st.selectbox("Estatus de Convocatoria / Participación", ["Jugó (Convocado con acción)", "Inactivo / No Convocado"])
            
            st.write("---")
            st.subheader("Métricas de Rendimiento en el Emparrillado")
            
            n_yardas, n_tackleadas, n_intercepciones = 0, 0, 0
            n_bloqueos_dom, n_sacks_perm, n_sacks_qb = 0, 0, 0
            n_gc, n_pe = 0, 0
            
            if pos_actual in ['QB', 'WR', 'RB']:
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
                
                st.success(f"✅ ¡Estadísticas de {jornada_seleccionada} guardadas para {jugador_seleccionado}!")

    else:
        st.subheader(f"🧠 Monitoreo Psicodeportivo ({jornada_seleccionada}) para: {jugador_seleccionado} ({pos_actual})")
        
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
                    
                    hist_fatiga = st.session_state.df.at[idx, 'Historial_Fatiga']
                    hist_fatiga.append(fatiga_entreno_nueva)
                    if len(hist_fatiga) > 5: hist_fatiga.pop(0)
                    st.session_state.df.at[idx, 'Historial_Fatiga'] = hist_fatiga
                else:
                    st.session_state.df.at[idx, 'Ansiedad_Competitiva'] = ansiedad_nueva
                    st.session_state.df.at[idx, 'Confianza_Tactica'] = confianza_nueva
                    st.session_state.df.at[idx, 'Sueno_Prepartido'] = sueno_previo_nuevo
                
                st.success(f"✅ ¡{tipo_encuesta} guardada para {jugador_seleccionado}!")

# --- PESTAÑA 5: CALENDARIO Y PLANIFICACIÓN SEMANAL ---
with tab5:
    st.header("📅 Calendario Oficial ONEFA 2026 y Planificación Psicológica")
    st.write("Consulta las fechas de la temporada y el programa estratégico para la aplicación de encuestas de bienestar.")
    
    df_calendario = pd.DataFrame({
        'Jornada': ['J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10'],
        'Fecha': ['4 Sep', '12 Sep', '18 Sep', '25 Sep', '3 Oct', '9 Oct', '17 Oct', '24 Oct', '30 Oct', 'Noviembre'],
        'Rival': ['Leones Anáhuac', 'Burros Blancos', 'ITESM Puebla', 'ITESM Mty', 'ITESM CEM', 'Linces UVM', 'Águilas Blancas', 'Aztecas UDLAP', 'Leones UAC', 'BYE (Descanso)'],
        'Sede / Condición': ['Visita (Cueva del León)', 'Local (EFO)', 'Visita (EFO)', 'Local (Borregos)', 'Visita (EFO)', 'Visita (JOM)', 'Local (EFO)', 'Local (Templo del Dolor)', 'Local (UAC)', 'Descanso'],
        'Evaluaciones Clave': [
            'Mié (Fatiga/Dolor) & Vie (Ansiedad/Confianza)', 
            'Mié & Vie', 'Mié & Vie', 'Mié & Vie', 'Mié & Vie', 
            'Mié & Vie', 'Mié & Vie', 'Mié & Vie', 'Mié & Vie', 'Descanso'
        ]
    })
    
    st.dataframe(df_calendario, use_container_width=True, hide_index=True)
    st.info("💡 **Enfoque Psicodeportivo:** Los **Miércoles** medimos sobrecarga física y dolor muscular; los **Viernes** medimos la activación, confianza táctica y descanso previo al juego.")

# --- PESTAÑA 3: RENDIMIENTO DEL EQUIPO Y REPORTES ---
with tab3:
    st.header("📈 Rendimiento General y Comparativa de Unidades")
    df_global = st.session_state.df.copy()
    
    col_of, col_def, col_st = st.columns(3)
    
    with col_of:
        st.subheader("🏈 Ofensiva")
        of_df = df_global[df_global['Unidad'] == 'Ofensiva']
        st.metric("Yardas Totales (Partidos)", int(of_df['Yardas_Producidas_Partidos'].sum()))
        st.metric("Fatiga Entrenos Promedio", f"{of_df['Fatiga_Entreno'].mean():.1f}/10")
        st.metric("Confianza Táctica Promedio", f"{of_df['Confianza_Tactica'].mean():.1f}/10")
        
    with col_def:
        st.subheader("🛡️ Defensiva")
        def_df = df_global[df_global['Unidad'] == 'Defensiva']
        st.metric("Tackleadas Totales", int(def_df['Tackleadas_Efectivas_Partidos'].sum()))
        total_partidos_convocados = max(int(def_df['Partidos_Convocados'].sum()), 1)
        st.metric("Promedio Sacks / J", f"{def_df['Capturas_QB_Sacks_Partidos'].sum() / total_partidos_convocados:.2f}")
        st.metric("Fatiga Entrenos Promedio", f"{def_df['Fatiga_Entreno'].mean():.1f}/10")
        st.metric("Confianza Táctica Promedio", f"{def_df['Confianza_Tactica'].mean():.1f}/10")
        
    with col_st:
        st.subheader("🦵 Equipos Especiales")
        st_df = df_global[df_global['Unidad'] == 'Equipos Especiales']
        st.metric("Puntos Totales", int((st_df['Goles_Campo_Partidos'].sum() * 3) + (st_df['Puntos_Extra_Partidos'].sum() * 1)))
        st.metric("Fatiga Entrenos Promedio", f"{st_df['Fatiga_Entreno'].mean():.1f}/10")
        st.metric("Confianza Táctica Promedio", f"{st_df['Confianza_Tactica'].mean():.1f}/10")

    st.divider()
    st.subheader("📊 Gráfica Comparativa de Fatiga en Entrenamientos por Unidad")
    df_fatiga_unidad = df_global.groupby('Unidad')['Fatiga_Entreno'].mean().reset_index()
    st.bar_chart(df_fatiga_unidad.set_index('Unidad'))

    st.divider()
    st.subheader("📥 Exportar Reportes Especializados para Head Coach")
    st.write("Descarga bases de datos limpias y segmentadas por área para compartir con los entrenadores de posición.")
    
    col_dl1, col_dl2, col_dl3 = st.columns(3)
    
    with col_dl1:
        cols_psi_exp = ['Jersey', 'Jugador', 'Posición', 'Unidad', 'Estatus_Medico', 'Fatiga_Entreno', 'Dolor_Muscular', 'Recuperacion_Entreno', 'Ansiedad_Competitiva', 'Confianza_Tactica', 'Sueno_Prepartido']
        csv_psi = df_global[cols_psi_exp].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Reporte Psicodeportivo",
            data=csv_psi,
            file_name='reporte_psicodeportivo_pumas_cu.csv',
            mime='text/csv',
        )
        
    with col_dl2:
        cols_of_exp = ['Jersey', 'Jugador', 'Posición', 'Yardas_Producidas_Partidos', 'Bloqueos_Dominio_Partidos', 'Capturas_Permitidas_Partidos', 'Yardas_Producidas_Entrenos']
        csv_of = df_global[df_global['Unidad'] == 'Ofensiva'][cols_of_exp].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Reporte Ofensiva",
            data=csv_of,
            file_name='reporte_ofensiva_pumas_cu.csv',
            mime='text/csv',
        )
        
    with col_dl3:
        cols_def_exp = ['Jersey', 'Jugador', 'Posición', 'Tackleadas_Efectivas_Partidos', 'Intercepciones_Partidos', 'Capturas_QB_Sacks_Partidos']
        csv_def = df_global[df_global['Unidad'] != 'Ofensiva'][cols_def_exp].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Reporte Defensiva / ST",
            data=csv_def,
            file_name='reporte_defensiva_pumas_cu.csv',
            mime='text/csv',
        )

# --- PESTAÑA 1: ANÁLISIS INDIVIDUAL ---
with tab1:
    df = st.session_state.df.copy()
    
    df['PJ_Calc'] = df['Partidos_Convocados'].replace(0, 1)
    df['PE_Calc'] = df['Entrenos_Asistidos'].replace(0, 1)

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
                        st.error(f"🔴 **RIESGO ALTO** (Índice: {indice_riesgo:.1f}/10)")
                    elif estatus == "Precaución Médica" or indice_riesgo >= 5.0:
                        st.warning(f"🟡 **RIESGO MODERADO** (Índice: {indice_riesgo:.1f}/10)")
                    else:
                        st.success(f"🟢 **ÓPTIMO / DISPONIBLE** (Índice: {indice_riesgo:.1f}/10)")

                entrenos_tot = max(int(stats_jugador['Entrenos_Programados']), 1)
                entrenos_asist = int(stats_jugador['Entrenos_Asistidos'])
                pct_entrenos = min(100.0, (entrenos_asist / entrenos_tot) * 100)

                partidos_tot = max(int(stats_jugador['Partidos_Programados']), 1)
                partidos_jugados = int(stats_jugador['Partidos_Convocados'])
                pct_partidos = min(100.0, (partidos_jugados / partidos_tot) * 100)

                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    st.markdown(f"🏋️ **Asistencia a Entrenamientos:** `{pct_entrenos:.1f}%` ({entrenos_asist}/{entrenos_tot})")
                with col_p2:
                    st.markdown(f"🏟️ **Convocatoria en Partidos:** `{pct_partidos:.1f}%` ({partidos_jugados}/{partidos_tot})")

                st.subheader("📊 Rendimiento Promedio: Partidos vs Entrenamientos")
                col1, col2, col3 = st.columns(3)
                
                pj = stats_jugador['PJ_Calc']
                pe = stats_jugador['PE_Calc']

                if pos in ['QB', 'WR', 'RB']:
                    with col1: st.metric("Promedio Yardas / Partido", f"{stats_jugador['Yardas_Producidas_Partidos'] / pj:.1f} yds")
                    with col2: st.metric("Promedio Yardas / Entreno", f"{stats_jugador['Yardas_Producidas_Entrenos'] / pe:.1f} yds")
                    with col3: st.metric("Total Yardas Acumuladas", int(stats_jugador['Yardas_Producidas_Partidos'] + stats_jugador['Yardas_Producidas_Entrenos']))
                
                elif pos == 'OL':
                    with col1: st.metric("Promedio Bloqueos Dominio / P.", f"{stats_jugador['Bloqueos_Dominio_Partidos'] / pj:.1f}")
                    with col2: st.metric("Promedio Bloqueos Dominio / E.", f"{stats_jugador['Bloqueos_Dominio_Entrenos'] / pe:.1f}")
                    with col3: st.metric("Capturas Permitidas (Sacks)", int(stats_jugador['Capturas_Permitidas_Partidos']))
                
                elif pos in ['DL', 'LB']:
                    with col1: st.metric("Promedio Tackleadas / Partido", f"{stats_jugador['Tackleadas_Efectivas_Partidos'] / pj:.1f}")
                    with col2: st.metric("Promedio Sacks / Partido", f"{stats_jugador['Capturas_QB_Sacks_Partidos'] / pj:.2f}")
                    with col3: st.metric("Total Sacks (Partidos)", int(stats_jugador['Capturas_QB_Sacks_Partidos']))
                
                elif pos == 'DB':
                    with col1: st.metric("Promedio Intercepciones / Partido", f"{stats_jugador['Intercepciones_Partidos'] / pj:.2f}")
                    with col2: st.metric("Promedio Tackleadas / Partido", f"{stats_jugador['Tackleadas_Efectivas_Partidos'] / pj:.1f}")
                    with col3: st.metric("Total Intercepciones", int(stats_jugador['Intercepciones_Partidos']))
                
                elif pos in ['K', 'P']:
                    with col1: st.metric("Goles de Campo (Partidos)", int(stats_jugador['Goles_Campo_Partidos']))
                    with col2: st.metric("Puntos Extra (Partidos)", int(stats_jugador['Puntos_Extra_Partidos']))
                    with col3: st.metric("Total Puntos (Partidos)", int((stats_jugador['Goles_Campo_Partidos'] * 3) + stats_jugador['Puntos_Extra_Partidos']))

                st.divider()

                st.subheader("🧠 Perfil Psicodeportivo Especializado")
                
                col_psi1, col_psi2 = st.columns(2)
                with col_psi1:
                    st.markdown("### 🏋️ Mitad de Semana (Entrenamientos)")
                    st.metric("Fatiga Física Acumulada", f"{stats_jugador['Fatiga_Entreno']}/10")
                    st.metric("Dolor / Molestias Físicas", f"{stats_jugador['Dolor_Muscular']}/10")
                    st.metric("Recuperación / Frescura", f"{stats_jugador['Recuperacion_Entreno']}/10")
                
                with col_psi2:
                    st.markdown("### 🏟️ Pre-partido (Matchday)")
                    st.metric("Ansiedad / Activación", f"{stats_jugador['Ansiedad_Competitiva']}/10")
                    st.metric("Confianza Táctica", f"{stats_jugador['Confianza_Tactica']}/10")
                    st.metric("Sueño Noche Previa", f"{stats_jugador['Sueno_Prepartido']} hrs")

                st.divider()

                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    st.write("📈 **Tendencia de Fatiga en Entrenamientos:**")
                    df_tendencia_fatiga = pd.DataFrame({'Fatiga': stats_jugador['Historial_Fatiga']})
                    st.line_chart(df_tendencia_fatiga)
                with col_g2:
                    st.write("🏈 **Evolución de Rendimiento Juego a Juego:**")
                    df_tendencia_juego = pd.DataFrame({'Impacto': stats_jugador['Historial_Rendimiento_Juego']})
                    st.line_chart(df_tendencia_juego)
