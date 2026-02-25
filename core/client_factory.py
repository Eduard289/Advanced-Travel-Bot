from curl_cffi import requests
from modules.identity import IdentityManager

class GhostClient:
    """Cliente que mimetiza navegadores reales para evitar bloqueos"""
    
    def __init__(self):
        self.identity_manager = IdentityManager()

    def fetch(self, url, proxy=None):
        profile, headers = self.identity_manager.get_random_profile()
        
        proxies = {"http": proxy, "https": proxy} if proxy else None
        
        try:
            # La clave es 'impersonate'. Esto configura el TLS y HTTP2 para que coincida con el UA.
            response = requests.get(
                url, 
                headers=headers, 
                impersonate=profile["impersonate"],
                proxies=proxies,
                timeout=30
            )
            return response
        except Exception as e:
            return f"Error en la petición: {str(e)}"
