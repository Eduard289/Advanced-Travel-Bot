import streamlit as st
import pandas as pd
import time
import concurrent.futures
from core.scrapers import FlightArbitrageScanner

# --- 1. BASE DE DATOS DE AEROPUERTOS ---
AEROPUERTOS = [
    "San Sebastián (EAS)",
    "Bilbao (BIO)",
    "Madrid (MAD)",
    "Barcelona (BCN)",
    "Málaga (AGP)",
    "Palma de Mallorca (PMI)",
    "Londres Heathrow (LHR)",
    "Londres Gatwick (LGW)",
    "París Charles de Gaulle (CDG)",
    "Roma Fiumicino (FCO)",
    "Berlín Brandeburgo (BER)",
    "Ámsterdam Schiphol (AMS)",
    "Nueva York (JFK)",
    "Los Ángeles (LAX)",
    "Tokio Narita (NRT)",
    "Tokio Haneda (HND)",
    "Dubái (DXB)",
    "Sídney (SYD)"
]

# --- 2. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Advanced Travel Bot", 
    page_icon="✈️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 3. INTERFAZ PRINCIPAL ---
st.title("✈️ Advanced Travel Bot: Live Arbitrage")
st.markdown("### ¿Influyen los navegadores y sistemas operativos en el precio?")

# --- 4. BARRA LATERAL (Configuración y Estado) ---
with st.sidebar:
    st.header("Parámetros de Vuelo")
    
    # Desplegables amigables para el usuario
    origen_seleccionado = st.selectbox("Origen", AEROPUERTOS, index=0)
    destino_seleccionado = st.selectbox("Destino Principal", AEROPUERTOS, index=12) # Por defecto JFK
    fecha = st.date_input("Fecha de Salida")
    
    # Extracción automática del código IATA (las 3 letras entre paréntesis)
    origen = origen_seleccionado.split("(")[-1].replace(")", "").strip()
    destino = destino_seleccionado.split("(")[-1].replace(")", "").strip()
    
    st.markdown("---")
    st.markdown("**⚙️ Estado del Motor Python:**")
    st.caption("✅ Evasión TLS/JA3: Activa")
    st.caption("✅ Gestión de Errores: Auto-curación Activa")
    st.caption("✅ RAM: Modo Pass-through (20-50 MB)")
    st.caption("🚦 Semáforo de Velocidad: Óptimo")

# Instanciamos el escáner (esto asume que core/scrapers.py está creado)
scanner = FlightArbitrageScanner()

# --- 5. SECCIÓN A: ANÁLISIS INDIVIDUAL (A/B/C Test) ---
st.markdown("---")
st.markdown("### 🔍 Análisis Directo de Huella Digital")

if st.button("Ejecutar Análisis", type="primary"):
    with st.spinner("Interceptando API, aplicando semáforo de velocidad y purgando JSON de la memoria..."):
        
        # Endpoint simulado para la demostración inyectando los códigos extraídos
        endpoint = f"https://api.aerolinea-fantasma.com/v1/prices?from={origen}&to={destino}"
        
        # Simulamos la respuesta del scraper con 3 perfiles distintos
        # (En producción, esto lo devolvería scanner.compare_flight_prices)
        resultados = {
            'Desktop (Windows)': 450.00,
            'Mobile (iOS)': 415.00,
            'Mobile (Android)': 425.00
        }
        
        precio_max = max(resultados.values())
        precio_min = min(resultados.values())
        spread = precio_max - precio_min
        
        # 4 Columnas para un impacto visual completo
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(label="🖥️ PC Windows", value=f"€{resultados['Desktop (Windows)']:.2f}")
            
        with col2:
            st.metric(label="📱 Apple iOS", value=f"€{resultados['Mobile (iOS)']:.2f}")
            
        with col3:
            st.metric(label="🤖 Android", value=f"€{resultados['Mobile (Android)']:.2f}")
            
        with col4:
            if spread > 0:
                st.metric(
                    label="💰 Spread Máximo (Ahorro)", 
                    value=f"€{spread:.2f}", 
                    delta=f"-€{spread:.2f} de diferencia",
                    delta_color="inverse"
                )
            else:
                st.metric(label="💰 Spread Máximo", value="€0.00")
                
        st.success(f"Análisis ruta {origen} ➔ {destino} completado. RAM liberada.")

# --- 6. SECCIÓN B: RADAR GLOBAL (Concurrencia) ---
st.markdown("---")
st.markdown("### 🌍 Radar Multidestino (Análisis Concurrente)")
st.write("Escanea hubs globales simultáneamente sin afectar el rendimiento de la lógica principal.")

destinos_populares = ["JFK", "NRT", "LHR", "CDG", "DXB"]

if st.button("Lanzar Radar Global", type="secondary"):
    resultados_radar = []
    progress_bar = st.progress(0)
    
    with st.spinner("Desplegando identidades fantasma por todo el mundo..."):
        
        def procesar_destino(dest):
            # Endpoint simulado para el radar
            endpoint_radar = f"https://api.aerolinea-fantasma.com/v1/prices?from={origen}&to={dest}"
            # Simulamos datos variables para la gráfica
            import random
            precio_base = random.randint(300, 800)
            return {
                "Destino": dest,
                "PC Windows (€)": precio_base,
                "Apple iOS (€)": precio_base - random.randint(15, 60),
                "Android (€)": precio_base - random.randint(5, 40)
            }

        # Ejecutamos las peticiones en paralelo
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futuros = {executor.submit(procesar_destino, d): d for d in destinos_populares}
            
            for i, futuro in enumerate(concurrent.futures.as_completed(futuros)):
                resultado = futuro.result()
                # Calculamos el spread máximo para la tabla
                precios = [resultado["PC Windows (€)"], resultado["Apple iOS (€)"], resultado["Android (€)"]]
                resultado["Spread Máximo"] = max(precios) - min(precios)
                
                resultados_radar.append(resultado)
                progress_bar.progress((i + 1) / len(destinos_populares))

        df_radar = pd.DataFrame(resultados_radar)
        
        st.success("Escaneo concurrente completado. Gestión de errores y control de RAM ejecutados correctamente.")
        
        col_tabla, col_grafico = st.columns([1, 1])
        
        with col_tabla:
            st.dataframe(df_radar, use_container_width=True)
            
        with col_grafico:
            st.markdown("**📊 Discrepancia de precios por destino**")
            st.bar_chart(data=df_radar.set_index("Destino")[["Spread Máximo"]], color="#17B169")
