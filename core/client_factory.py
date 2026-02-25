from curl_cffi import requests
from modules.identity import IdentityManager
from utils.exceptions import auto_heal_request

class GhostClient:
    def __init__(self):
        self.identity_manager = IdentityManager()
        # Si tienes la app 1.1.1.1 WARP corriendo en modo proxy local, suele estar en este puerto
        self.warp_proxy = "socks5://127.0.0.1:40000" 

    # Aplicamos el decorador. Si falla, reintenta 3 veces y permite usar URLs espejo.
    @auto_heal_request(max_retries=3, switch_to_mirror=True)
    def fetch(self, url, use_warp=False):
        profile, headers = self.identity_manager.get_random_profile()
        
        # Enrutamos por 1.1.1.1 si se solicita, para evadir bloqueos de IP de tu operadora
        proxies = {"http": self.warp_proxy, "https": self.warp_proxy} if use_warp else None
        
        # La petición base. Si esto falla, el @auto_heal_request lo captura arriba.
        response = requests.get(
            url, 
            headers=headers, 
            impersonate=profile["impersonate"],
            proxies=proxies,
            timeout=15
        )
        return response
