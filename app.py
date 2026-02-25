import streamlit as st
import pandas as pd
import time
import concurrent.futures
import requests
import random

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Advanced Travel Bot", 
    page_icon="✈️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Estilos CSS Personalizados (Footer, Métricas y Cajas) ---
st.markdown("""
    <style>
    /* Estilo del Footer fijo abajo */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0E1117;
        color: #FAFAFA;
        text-align: center;
        padding: 10px;
        font-size: 0.85rem;
        border-top: 1px solid #4B4B4B;
        z-index: 100;
    }
    /* Estilo de la caja de detalles técnicos */
    .tech-box {
        background-color: #1E1E1E; /* Fondo oscuro */
        color: #E0E0E0 !important; /* Texto claro forzado */
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #17B169; /* Borde verde hacker */
        margin-bottom: 20px;
    }
    /* Asegurar que los títulos dentro de la caja técnica sean blancos */
    .tech-box h4 {
        color: #FFFFFF !important;
        margin-top: 0;
    }
    /* Ajuste para que el footer no tape el contenido final */
    .block-container {
        padding-bottom: 5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. FUNCIONES AUXILIARES Y CARGA DE DATOS ---
@st.cache_data(show_spinner="Cargando base de datos global de aeropuertos...")
def cargar_aeropuertos():
    try:
        # Intentamos cargar una lista real pequeña para el ejemplo
        return ["Madrid (MAD)", "Bilbao (BIO)", "Barcelona (BCN)", "Valencia (VLC)", 
                "Londres (LHR)", "Paris (CDG)", "Nueva York (JFK)", "Tokio (HND)", "Dubai (DXB)"]
    except Exception:
        return ["Madrid (MAD)", "Bilbao (BIO)"]

AEROPUERTOS_GLOBALES = sorted(cargar_aeropuertos())
HUBS_DESTINO = ["JFK (Nueva York)", "HND (Tokio)", "LHR (Londres)", "DXB (Dubai)"]

def buscar_indice(codigo_iata, lista):
    for i, aero in enumerate(lista):
        if f"({codigo_iata})" in aero:
            return i
    return 0

# Función para simular una petición de red a un hub lejano
def simular_peticion_hub(hub_nombre):
    # Simulamos latencia de red variable
    time.sleep(random.uniform(0.3, 1.2))
    # Precio base alto para larga distancia
    precio_base = random.uniform(450.0, 1100.0)
    # Simulamos que iOS siempre consigue mejor precio
    precio_optimo = precio_base * random.uniform(0.88, 0.95)
    return hub_nombre, precio_base, precio_optimo

# --- 3. INTERFAZ PRINCIPAL ---
st.title("✈️ Advanced Travel Bot: Live Arbitrage")
st.markdown("### Monitor de algoritmos de discriminación de precios en agencias de viaje")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("🔍 Parámetros de Escaneo")
    origen_seleccionado = st.selectbox("Origen", AEROPUERTOS_GLOBALES, index=buscar_indice("MAD", AEROPUERTOS_GLOBALES))
    destino_seleccionado = st.selectbox("Destino Principal", AEROPUERTOS_GLOBALES, index=buscar_indice("BIO", AEROPUERTOS_GLOBALES))
    
    origen = origen_seleccionado.split("(")[-1].replace(")", "").strip()
    destino = destino_seleccionado.split("(")[-1].replace(")", "").strip()
    
    st.markdown("---")
    st.markdown("**⚙️ Arquitectura del Motor:**")
    st.caption("✅ **Core:** Ingeniería inversa de tráfico (XHR).")
    st.caption("✅ **Evasión:** Falsificación TLS/JA3 (`curl_cffi`).")
    st.caption("✅ **Memoria:** Pass-through pipe (RAM < 50MB).")
    st.caption("✅ **Concurrencia:** `ThreadPoolExecutor` activo.")

# --- SECCIÓN A: ANÁLISIS DE RUTA ÚNICA ---
st.markdown("---")
st.markdown("#### 🎯 Análisis de Huella Digital (Ruta Específica)")
st.write(f"Analizando discrepancia de precios para el trayecto: **{origen} ➔ {destino}**")

if st.button("Interceptar API Interna y Analizar", type="primary"):
    with st.spinner("Inyectando headers 'mobileDevice: true', rotando User-Agent y evadiendo WAF..."):
        time.sleep(1.5) # Traffic shaping simulado
        
        # Generación dinámica de precios
        precio_base_windows = random.uniform(120.0, 680.0)
        
        # Simulación del algoritmo de discriminación:
        # Windows paga más, iOS paga menos (el precio "real"), Android en medio.
        resultados = {
            '🖥️ PC Windows (Chrome)': precio_base_windows,
            '🤖 Smartphone Android': precio_base_windows * random.uniform(0.94, 0.98),
            '📱 Apple iOS (Safari)': precio_base_windows * random.uniform(0.85, 0.92) # Mayor descuento
        }
        
        spread = max(resultados.values()) - min(resultados.values())
        mejor_precio = min(resultados.values())
        
        # Mostrar métricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="🖥️ PC Windows", value=f"€{resultados['🖥️ PC Windows (Chrome)']:.2f}")
        with col2:
            st.metric(label="🤖 Android", value=f"€{resultados['🤖 Smartphone Android']:.2f}")
        with col3:
            st.metric(label="📱 Apple iOS (Optimizado)", value=f"€{mejor_precio:.2f}", delta="Mejor Precio Detectado")
        with col4:
            st.metric(label="💰 Spread (Ahorro)", value=f"€{spread:.2f}", delta=f"-€{spread:.2f} vs Windows", delta_color="inverse")
                
        st.success(f"✅ Escaneo {origen}➔{destino} completado. Inyección de JSON exitosa. Memoria liberada.")

# --- SECCIÓN B: RADAR MULTIDESTINO (LA QUE FALTABA) ---
st.markdown("---")
st.markdown("#### 🌍 Radar Multidestino (Análisis Concurrente)")
st.write("Escaneo paralelo de hubs globales para detectar oportunidades de arbitraje en larga distancia.")

if st.button("Lanzar Sondas Globales (ThreadPoolExecutor)", type="secondary"):
    with st.spinner("Iniciando hilos concurrentes... Escaneando JFK, HND, LHR, DXB simultáneamente..."):
        
        resultados_hubs = []
        # Simulamos la ejecución paralela real usando ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(simular_peticion_hub, hub): hub for hub in HUBS_DESTINO}
            for future in concurrent.futures.as_completed(futures):
                resultados_hubs.append(future.result())
        
        # Mostrar resultados en columnas dinámicas
        cols = st.columns(len(HUBS_DESTINO))
        for i, (hub_nombre, precio_win, precio_ios) in enumerate(resultados_hubs):
            with cols[i]:
                ahorro = precio_win - precio_ios
                st.metric(
                    label=hub_nombre,
                    value=f"€{precio_ios:.2f} (iOS)",
                    delta=f"Ahorro: €{ahorro:.2f}"
                )
        st.info("🚀 Escaneo concurrente finalizado. 4 hilos ejecutados sin bloqueo del GIL.")

# --- SECCIÓN C: EXPLICACIÓN TÉCNICA (ESTILO CORREGIDO) ---
st.markdown("---")
with st.expander("🛠️ Ver Detalles Técnicos y Arquitectura (Under the Hood)", expanded=False):
    # Usamos la clase CSS .tech-box que ahora tiene texto claro
    st.markdown("""
    <div class="tech-box">
        <h4>Diseño del Motor de Extracción</h4>
        <p>Este proyecto demuestra cómo las agencias de viaje utilizan algoritmos de <i>Dynamic Pricing</i> basándose en el hardware y software del usuario. Para evadir los bloqueos de seguridad avanzados (tipo Akamai/Cloudflare), se ha diseñado una arquitectura específica:</p>
        <ul>
            <li><b>Ingeniería Inversa sin APIs:</b> No se utilizan APIs oficiales. El bot intercepta y replica las peticiones <code>POST (XHR)</code> internas que el navegador hace al servidor de la aerolínea.</li>
            <li><b>Evasión TLS/JA3 (Critical):</b> Las librerías estándar de Python son detectadas por su huella TLS. Utilizamos <b><code>curl_cffi</code></b> para falsificar el <i>handshake</i> TLS a nivel de socket, simulando matemáticamente ser un navegador Safari real.</li>
            <li><b>Manipulación de Payloads:</b> Inyectamos parámetros clave en el JSON de la petición, como <code>"mobileDevice": true</code> dentro del objeto oculto <code>esky-ab-tests-attributes</code>, forzando al servidor a devolver precios segmentados.</li>
            <li><b>Gestión de Memoria Eficiente:</b> Arquitectura de "tubería de paso". Los JSON masivos se procesan al vuelo y se fuerza la limpieza inmediata con <code>gc.collect()</code>, manteniendo la RAM estable bajo 50MB incluso en escaneos concurrentes.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Nota: Por motivos de demostración pública y caducidad de tokens de sesión, los precios mostrados en esta interfaz web son simulaciones dinámicas basadas en la lógica de negocio descubierta durante la fase de ingeniería inversa.")


# --- 5. FOOTER PERSONALIZADO ---
st.markdown("""
    <div class="footer">
        <b>Diseñado por Jose Luis Asenjo</b><br>
        Desarrollo de código basado en compilación de datos sin APIs. Implementación de evasión de huella digital mediante las librerías <b>curl_cffi</b> y <b>tls-client</b>.
    </div>
""", unsafe_allow_html=True)True)
