# Advanced Travel Bot: Market Intelligence & Dynamic Pricing Scanner

Un motor de inteligencia de mercado desarrollado en Python diseñado para auditar, monitorizar y demostrar la existencia de algoritmos de discriminación de precios (Dynamic Pricing) en la industria de las agencias de viajes (OTA).

Este proyecto no utiliza APIs públicas documentadas. Está basado enteramente en ingeniería inversa del tráfico de red (XHR/Fetch) para interceptar respuestas directas del servidor y evadir sistemas anti-bots modernos mediante falsificación de huellas TLS a nivel de socket.

El Problema: Perfilado de Dispositivos (Device Fingerprinting)

Durante el análisis del tráfico de red en plataformas líderes de viajes, se descubrió que el servidor no devuelve un precio estándar. En su lugar, el navegador del cliente envía silenciosamente un perfil de hardware y software a través de headers personalizados antes de procesar la cotización.

Ejemplo de Payload interceptado (esky-ab-tests-attributes):


JSON
{
  "mobileDevice": false,
  "screenResolutionHeight": 1080,
  "screenResolutionWidth": 1920,
  "browser": "Chrome"
}


En base a este JSON, el servidor aplica un Spread de precios (Ahorro/Penalización). El objetivo de este bot es automatizar el proceso de engañar a este algoritmo para extraer las anomalías de precio en tiempo real.

 
Arquitectura y Decisiones de Ingeniería (Under the Hood)
El desarrollo de este bot prioriza la eficiencia de memoria, la concurrencia y la evasión de firewalls (WAF) como Cloudflare o Akamai.

1. Evasión TLS / JA3 Fingerprint
El uso de la librería estándar requests resulta en bloqueos inmediatos (HTTP 403 Forbidden) debido a las discrepancias en el handshake TLS.

Solución: Implementación de curl_cffi (basado en Chrome/Safari nativo). El bot falsifica la huella JA3 a nivel de socket de red, engañando al WAF haciéndole creer que la petición emana de un iPhone real usando Safari.

2. Gestión de Memoria (Pass-through Pipe Architecture)
El procesamiento de respuestas JSON masivas (típicamente >80KB por vuelo) suele provocar picos de consumo de RAM.

Solución: El procesador actúa como una tubería de paso. Se lee el bloque de red en memoria volátil, se extrae únicamente el nodo del árbol JSON que contiene el precio, e inmediatamente se aplican los comandos del y la llamada manual al recolector de basura (gc.collect()).

Rendimiento: 0 MB de uso de disco duro. Consumo de RAM lineal y estancado en 20-50 MB independientemente de la carga de trabajo.

3. Inyección de Headers y Manipulación A/B
El cliente fantasma intercepta la petición originaria y genera un A/B/C test en milisegundos:

Sonda A: Emula Desktop Windows 10 + Chrome.

Sonda B: Emula iOS + Safari (Inyectando "mobileDevice": true).

Sonda C: Emula Android + Chrome.

4. Traffic Shaping y Auto-Curación
Para evitar saturar los endpoints no documentados, el motor cuenta con:

Traffic Shaping: Semáforos de velocidad con latencia inducida variable.

Decoradores de Fallo (@auto_heal): Si un servidor banea temporalmente el nodo, un decorador intercepta el código de error, rota dinámicamente la identidad digital de la sesión y reintenta el fetch de forma asíncrona sin bloquear el hilo principal.

⚙️ Tecnologías Utilizadas
Backend / Scraper: Python, curl_cffi, tls-client, concurrent.futures (Multithreading).

Frontend / UI: Streamlit.

Análisis de Datos: Pandas.

Seguridad: Criptografía básica (Hashlib) para generación de heurística y gestión estricta de variables vía .env.
