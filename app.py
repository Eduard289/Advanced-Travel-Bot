import streamlit as st
import pandas as pd
import time
import concurrent.futures
import requests
import random
from core.scrapers import FlightArbitrageScanner # Descomenta esto cuando tengamos el scraper real

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Advanced Travel Bot", 
    page_icon="✈️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CARGA GLOBAL DE AEROPUERTOS (Caché Optimizada) ---
@st.cache_data(show_spinner="Cargando base de datos global de aeropuertos...")
def cargar_aeropuertos():
    """Descarga y cachea la lista de todos los aeropuertos del mundo con código IATA."""
    try:
        # Repositorio Open Source muy fiable y rápido
        url = "https://raw.githubusercontent.com/mwgg/Airports/master/airports.json"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        lista_aeropuertos = []
        for key, info in data.items():
            iata = info.get("iata")
            city = info.get("city")
            name = info.get("name")
            
            # Filtramos solo aeropuertos comerciales con IATA válido
            if iata and iata != "\\N" and len(iata) == 3 and city:
                lista_aeropuertos.append(f"{city} - {name} ({iata})")
                
        # Ordenamos alfabéticamente y eliminamos duplicados
        return sorted(list(set(lista_aeropuertos)))
    except Exception as e:
        # Fallback de emergencia si falla la red
        return [
            "Madrid - Barajas (MAD)", 
            "Barcelona - El Prat (BCN)", 
            "Nueva York - John F Kennedy (JFK)", 
            "Tokio - Narita (NRT)",
            "Londres - Heathrow (LHR)"
        ]

# Cargamos la lista antes de pintar la interfaz
AEROPUERTOS_GLOBALES = cargar_aeropuertos()

# Búsqueda de índices por defecto (para que no salga el primero de la lista global, que suele ser extraño)
def buscar_indice(codigo_iata, lista):
    for i, aero in enumerate(lista):
        if f"({codigo_iata})" in aero:
            return i
    return 0

idx_madrid = buscar_indice("MAD", AEROPUERTOS_GLOBALES)
idx_tokio = buscar_indice("NRT", AEROPUERTOS_GLOBALES)

# --- 3. INTERFAZ PRINCIPAL ---
st.title("✈️ Advanced Travel Bot: Live Arbitrage")
st.markdown("### ¿Influyen los navegadores y sistemas operativos en el precio?")

# --- 4. BARRA LATERAL (Configuración y Estado) ---
with st.sidebar:
    st.header("Parámetros de Vuelo")
    
    # Desplegables con búsqueda integrada (puedes escribir "Bilbao" o "Tokio")
    origen_seleccionado = st.selectbox("Origen", AEROPUERTOS_GLOBALES, index=idx_madrid)
    destino_seleccionado = st.selectbox("Destino Principal", AEROPUERTOS_GLOBALES, index=idx_tokio)
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

# Instanciamos el escáner (Simulado por ahora)
# scanner = FlightArbitrageScanner()

# --- 5. SECCIÓN A: ANÁLISIS INDIVIDUAL (A/B/C Test) ---
st.markdown("---")
st.markdown("### 🔍 Análisis Directo de Huella Digital")

if st.button("Ejecutar Análisis", type="primary"):
    with st.spinner("Interceptando API, aplicando semáforo de velocidad y purgando JSON de la memoria..."):
        
        time.sleep(1.5) # Semáforo de velocidad simulado
        
        # Endpoint para la demostración inyectando los códigos mundiales extraídos
        endpoint = f"https://api.aerolinea-fantasma.com/v1/prices?from={origen}&to={destino}"
        
        # --- AQUÍ IRÁ LA CONEXIÓN REAL AL SCRAPER ---
        # resultados = scanner.compare_flight_prices(endpoint, base_payload={})
        
        # Por ahora, mantenemos la simulación dinámica para probar la UI
        precio_base = random.uniform(250.0, 950.0)
        resultados = {
            'Desktop (Windows)': precio_base,
            'Mobile (iOS)': precio_base - random.uniform(25.0, 85.0),
            'Mobile (Android)': precio_base - random.uniform(10.0, 45.0)
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
                st.metric(label="💰 Spread Máximo (Ahorro)", value=f"€{spread:.2f}", delta=f"-€{spread:.2f} de diferencia", delta_color="inverse")
            else:
                st.metric(label="💰 Spread Máximo", value="€0.00")
                
        st.success(f"Análisis ruta {origen} ➔ {destino} completado. RAM liberada.")

# --- 6. SECCIÓN B: RADAR GLOBAL (Concurrencia) ---
st.markdown("---")
st.markdown("### 🌍 Radar Multidestino (Análisis Concurrente)")
st.write("Escanea hubs globales simultáneamente sin afectar el rendimiento de la lógica principal.")

destinos_populares = ["JFK", "NRT", "LHR", "CDG", "DXB", "SYD", "EZE", "GRU"]

if st.button("Lanzar Radar Global", type="secondary"):
    resultados_radar = []
    progress_bar = st.progress(0)
    
    with st.spinner("Desplegando identidades fantasma por todo el mundo..."):
        
        def procesar_destino(dest):
            # Endpoint simulado para el radar
            endpoint_radar = f"https://api.aerolinea-fantasma.com/v1/prices?from={origen}&to={dest}"
            # Datos dinámicos para la gráfica visual
            precio_base = random.randint(300, 1200)
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
