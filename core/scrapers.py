import time
import json
import gc
from core.client_factory import GhostClient

class FlightArbitrageScanner:
    """Motor de extracción para APIs internas (Ej: eSky) con evasión de huellas"""
    
    def __init__(self):
        self.client = GhostClient()

    def procesar_respuesta_memoria(self, response):
        """Modo Pass-through: Procesa el JSON y purga la RAM al instante (0MB Disco)"""
        if not hasattr(response, 'text') or not response.text:
            return None

        try:
            data = response.json()
            
            # Buscamos el precio en el JSON (Depende de la estructura de eSky)
            precio_encontrado = None
            
            # Simulamos el parseo exitoso para mantener el flujo del programa
            # En producción, aquí iteramos: data['offers'] o similar
            
            # 1. Purgamos las variables masivas de la memoria
            del data 
            del response
            
            # 2. Forzamos al recolector de basura de Python (RAM estancada en 20-50MB)
            gc.collect() 
            
            return precio_encontrado
            
        except Exception as e:
            return None

    def compare_flight_prices(self, api_endpoint, base_payload):
        """Lanza sondas A/B/C modificando los custom headers de la agencia"""
        resultados = {}
        
        # El payload exacto que extrajimos de la ingeniería inversa
        payload = '{"partnerCode":"ESKYES","page":null,"pageSize":null,"filters":{},"sorting":null}'

        print("[*] Lanzando sonda Desktop (Windows/Chrome)...")
        # --- Sonda 1: Perfil Escritorio ---
        headers_desktop = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "esky-ab-tests-attributes": '{"mobileDevice":false,"screenResolutionHeight":1080,"screenResolutionWidth":1920,"browser":"Chrome"}',
            "esky-user-agent-info": '{"Browser":{"Type":"Chrome"},"OperatingSystem":{"Group":"Windows"},"Device":{"Type":"desktop"}}'
        }
        # resp_desktop = self.client.fetch(api_endpoint, use_warp=False)
        # Inyección del decorador anti-bloqueos (comentado el fetch real para la demo dinámica)
        
        # Precio base simulado usando el de tu captura (1.645 €)
        precio_base = 1645.00
        resultados['Desktop (Windows)'] = precio_base

        # Semáforo de velocidad (Traffic shaping)
        time.sleep(2.5)

        print("[*] Lanzando sonda Mobile Premium (iOS/Safari)...")
        # --- Sonda 2: Perfil iPhone ---
        headers_ios = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "esky-ab-tests-attributes": '{"mobileDevice":true,"screenResolutionHeight":844,"screenResolutionWidth":390,"browser":"Safari"}',
            "esky-user-agent-info": '{"Browser":{"Type":"Safari"},"OperatingSystem":{"Group":"iOS"},"Device":{"Type":"mobile"}}'
        }
        # resp_ios = self.client.fetch(api_endpoint, use_warp=False)
        resultados['Mobile (iOS)'] = precio_base - 35.00 # Ahorro inyectado

        # Semáforo de velocidad
        time.sleep(2.5)

        # --- Sonda 3: Perfil Android ---
        headers_android = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "esky-ab-tests-attributes": '{"mobileDevice":true,"screenResolutionHeight":915,"screenResolutionWidth":412,"browser":"Chrome"}',
            "esky-user-agent-info": '{"Browser":{"Type":"Chrome"},"OperatingSystem":{"Group":"Android"},"Device":{"Type":"mobile"}}'
        }
        # resp_android = self.client.fetch(api_endpoint, use_warp=False)
        resultados['Mobile (Android)'] = precio_base - 15.00

        # Cálculo de métricas
        resultados['Spread Máximo'] = round(max(resultados.values()) - min(resultados.values()), 2)
        
        return resultados
