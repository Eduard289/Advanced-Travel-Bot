import time
from core.client_factory import GhostClient

class FlightArbitrageScanner:
    """Ejecuta pruebas A/B de precios modificando la huella de red"""
    
    def __init__(self):
        self.client = GhostClient()

    def compare_flight_prices(self, api_endpoint, base_payload):
        resultados = {}

        # --- Prueba 1: Perfil "Estándar" (Ej: PC Windows, Chrome) ---
        # Aquí forzaríamos a IdentityManager a darnos un perfil de escritorio
        print("Obteniendo precio con perfil: Windows Desktop / Chrome...")
        resp_desktop = self.client.fetch(api_endpoint)
        
        # Simulamos la extracción del JSON (dependerá de la web exacta)
        # precio_desktop = resp_desktop.json().get('price')
        precio_desktop = 450.00 # Dato simulado para el ejemplo
        resultados['Desktop (Chrome)'] = precio_desktop
        
        # Semáforo de velocidad: Pausa humana para no saturar ni alertar (Rate Limiting)
        time.sleep(2.5)

        # --- Prueba 2: Perfil "Premium" (Ej: iPhone, Safari) ---
        # Aquí forzaríamos a IdentityManager a darnos un perfil iOS
        print("Obteniendo precio con perfil: iOS Mobile / Safari...")
        resp_mobile = self.client.fetch(api_endpoint)
        
        # precio_mobile = resp_mobile.json().get('price')
        precio_mobile = 415.00 # Dato simulado para el ejemplo
        resultados['Mobile (Safari)'] = precio_mobile

        # --- Análisis ---
        spread = precio_desktop - precio_mobile
        resultados['Diferencia_Spread'] = round(spread, 2)
        
        return resultados
