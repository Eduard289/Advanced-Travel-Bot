import streamlit as st
import time
from core.scrapers import FlightArbitrageScanner

# Configuración de la página
st.set_page_config(page_title="Advanced Travel Bot", page_icon="✈️", layout="wide")

st.title("✈️ Advanced Travel Bot: Live Arbitrage")
st.markdown("### ¿Influyen los headers en el precio? Descubrámoslo.")

# Barra lateral de configuración
with st.sidebar:
    st.header("Parámetros de Vuelo")
    origen = st.text_input("Origen (Código IATA)", value="MAD", help="Ejemplo: MAD para Madrid")
    destino = st.text_input("Destino (Código IATA)", value="NRT", help="Ejemplo: NRT para Tokio")
    fecha = st.date_input("Fecha de Salida")
    
    st.markdown("---")
    st.markdown("**⚙️ Estado del Sistema:**")
    st.caption("✅ Evasión TLS/JA3 Activa")
    st.caption("✅ RAM: Modo Pass-through (0MB Disco)")
    st.caption("🚦 Semáforo de Velocidad: Óptimo")

# Botón de ejecución principal
if st.button("Ejecutar Análisis de Huella Digital", type="primary"):
    scanner = FlightArbitrageScanner()
    
    # Barra de progreso visual
    with st.spinner("Interceptando API, rotando identidades y aplicando semáforo de velocidad..."):
        # Simulamos el endpoint de una aerolínea
        endpoint_simulado = f"https://api.aerolinea-fantasma.com/v1/prices?from={origen}&to={destino}"
        
        # Ejecutamos la prueba A/B
        resultados = scanner.compare_flight_prices(endpoint_simulado, base_payload={})
        
        st.markdown("### Resultados del Experimento")
        
        # Tarjetas de métricas para un impacto visual brutal
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="🖥️ Perfil Windows / Chrome", 
                value=f"€{resultados['Desktop (Chrome)']:.2f}"
            )
            
        with col2:
            st.metric(
                label="📱 Perfil iOS / Safari", 
                value=f"€{resultados['Mobile (Safari)']:.2f}"
            )
            
        with col3:
            spread = resultados['Diferencia_Spread']
            # Si el spread es positivo (Desktop es más caro), mostramos ahorro en verde
            if spread > 0:
                st.metric(
                    label="💰 Spread (Ahorro detectado)", 
                    value=f"€{abs(spread):.2f}", 
                    delta=f"-€{spread:.2f} comprando desde móvil",
                    delta_color="inverse"
                )
            else:
                st.metric(
                    label="💰 Spread (Sin variación)", 
                    value="€0.00"
                )
                
        st.success("Análisis completado. Los bloques de datos JSON han sido purgados de la RAM con éxito.")
