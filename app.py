import streamlit as st
from core.client_factory import GhostClient

st.set_page_config(page_title="Ghost Arbitrage Bot", page_icon="✈️")

st.title("✈️ Global Price Arbitrage")
st.markdown("### Detectando variaciones de precio por huella digital")

with st.sidebar:
    st.header("Configuración de Red")
    proxy_input = st.text_input("Proxy (opcional)", placeholder="http://user:pass@host:port")
    test_url = st.text_input("URL de Prueba", value="https://www.google.com")

if st.button("Ejecutar Escaneo Fantasma"):
    client = GhostClient()
    
    with st.spinner("Simulando huella digital y saltando protecciones..."):
        resp = client.fetch(test_url, proxy=proxy_input)
        
        if hasattr(resp, 'status_code'):
            st.success(f"Petición Exitosa: Código {resp.status_code}")
            with st.expander("Ver Headers Enviados"):
                st.json(resp.request.headers)
        else:
            st.error(resp)

#
