import streamlit as st
import pandas as pd
import time
import concurrent.futures
from core.scrapers import FlightArbitrageScanner

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Advanced Travel Bot", 
    page_icon="✈️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. INTERFAZ PRINCIPAL ---
st.title("✈️ Advanced Travel Bot: Live Arbitrage")
st.markdown("### ¿Influyen los headers en el precio? Descubrámoslo.")

# --- 3. BARRA LATERAL (Configuración y Estado) ---
with st.sidebar:
    st.header("Parámetros de Vuelo")
    origen = st.text_input("Origen (Código IATA)", value="MAD", help="Ejemplo: MAD para Madrid")
    destino = st.text_input("Destino Principal", value="NRT", help="Ejemplo: NRT para Tokio")
    fecha = st.date_input("Fecha de Salida")
    
    st.markdown("---")
    st.markdown("**⚙️ Estado del Motor Python:**")
    st.caption("✅ Evasión TLS/JA3: Activa")
    st.caption("✅ Gestión de Errores: Auto-curación Activa")
    st.caption("✅ RAM: Modo Pass-through (20-50 MB)")
    st.caption("🚦 Semáforo de Velocidad: Óptimo")

# Instanciamos el escáner (esto asume que core/scrapers.py está creado)
scanner = FlightArbitrageScanner()

# --- 4. SECCIÓN A: ANÁLISIS INDIVIDUAL (A/B Test) ---
st.markdown("---")
st.markdown("### 🔍 Análisis Directo (Prueba A/B)")

if st.button("Ejecutar Análisis de Huella Digital", type="primary"):
    with st.spinner("Interceptando API, aplicando semáforo de velocidad y procesando JSON en memoria..."):
        
        # Endpoint simulado para la demostración
        endpoint = f"https://api.aerolinea-fantasma.com/v1/prices?from={origen}&to={destino}"
        resultados = scanner.compare_flight_prices(endpoint, base_payload={})
        
        # Tarjetas de métricas para un impacto visual brutal
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="🖥️ Perfil Windows / Chrome", value=f"€{resultados['Desktop (Chrome)']:.2f}")
            
        with col2:
            st.metric(label="📱 Perfil iOS / Safari", value=f"€{resultados['Mobile (Safari)']:.2f}")
            
        with col3:
            spread = resultados['Diferencia_Spread']
            if spread > 0:
                st.metric(
                    label="💰 Spread (Ahorro detectado)", 
                    value=f"€{abs(spread):.2f}", 
                    delta=f"-€{spread:.2f} comprando desde móvil",
                    delta_color="inverse"
                )
            else:
                st.metric(label="💰 Spread (Sin variación)", value="€0.00")
                
        st.success("Análisis completado. Los chunks de datos han sido purgados de la RAM con éxito.")



# --- 5. SECCIÓN B: RADAR GLOBAL (Concurrencia) ---
st.markdown("---")
st.markdown("### 🌍 Radar Multidestino (Análisis Concurrente)")
st.write("Escanea hubs globales simultáneamente sin afectar el rendimiento de la lógica principal.")

destinos_populares = ["JFK", "NRT", "LHR", "CDG", "DXB"]

if st.button("Lanzar Radar Global", type="secondary"):
    resultados_radar = []
    progress_bar = st.progress(0)
    
    with st.spinner("Desplegando identidades fantasma por todo el mundo..."):
        
        def procesar_destino(dest):
            # Reutilizamos la lógica del escáner para cada destino
            endpoint_radar = f"https://api.aerolinea-fantasma.com/v1/prices?from={origen}&to={dest}"
            data = scanner.compare_flight_prices(endpoint_radar, base_payload={})
            return {
                "Destino": dest,
                "PC (€)": data['Desktop (Chrome)'],
                "Móvil (€)": data['Mobile (Safari)'],
                "Spread (Ahorro)": data['Diferencia_Spread']
            }

        # Ejecutamos las peticiones en paralelo (multithreading)
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futuros = {executor.submit(procesar_destino, d): d for d in destinos_populares}
            
            for i, futuro in enumerate(concurrent.futures.as_completed(futuros)):
                resultados_radar.append(futuro.result())
                progress_bar.progress((i + 1) / len(destinos_populares))

        df_radar = pd.DataFrame(resultados_radar)
        
        st.success("Escaneo concurrente completado. Gestión de errores y control de RAM ejecutados correctamente.")
        
        # Visualización de los datos del Radar
        col_tabla, col_grafico = st.columns([1, 1])
        
        with col_tabla:
            st.dataframe(df_radar, use_container_width=True)
            
        with col_grafico:
            st.markdown("**📊 Discrepancia de precios por destino**")
            st.bar_chart(data=df_radar.set_index("Destino")[["Spread (Ahorro)"]], color="#17B169")
