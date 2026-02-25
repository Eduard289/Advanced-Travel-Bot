import functools
import time

def auto_heal_request(max_retries=3, switch_to_mirror=False):
    """
    Decorador que gestiona errores automáticamente sin bloquear el hilo principal.
    Rota la identidad o cambia a URL espejo si hay bloqueos.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, url, *args, **kwargs):
            current_url = url
            
            for attempt in range(max_retries):
                try:
                    # Intenta ejecutar la petición normal
                    response = func(self, current_url, *args, **kwargs)
                    
                    # Si el servidor nos devuelve un 403 (Prohibido) o 429 (Demasiadas peticiones)
                    if hasattr(response, 'status_code') and response.status_code in [403, 429]:
                        raise ValueError(f"Bloqueo detectado: Status {response.status_code}")
                        
                    return response # Si todo va bien, sale y no consume más recursos
                    
                except Exception as e:
                    if attempt == max_retries - 1:
                        return f"Fallo definitivo tras {max_retries} intentos: {str(e)}"
                    
                    print(f"⚠️ Error detectado: {str(e)}. Auto-curando (Intento {attempt + 1})...")
                    
                    # Lógica de evasión: Rotar identidad
                    self.identity_manager.get_random_profile()
                    
                    # Lógica de evasión IP: Si está activo, saltar a URL espejo
                    if switch_to_mirror and "mirror" not in current_url:
                        print("🔄 Pivotando a URL espejo (ej. de .com a .es)...")
                        # Aquí reemplazarías el dominio base por el espejo
                        current_url = current_url.replace(".com", ".es")
                    
                    time.sleep(1.5) # Breve pausa para no saturar
                    
        return wrapper
    return decorator
