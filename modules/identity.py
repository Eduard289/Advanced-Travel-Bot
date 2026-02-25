import random

class IdentityManager:
    """Genera identidades consistentes: UA + Headers + TLS Fingerprint"""
    
    @staticmethod
    def get_random_profile():
        profiles = [
            {
                "browser": "chrome",
                "platform": "windows",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "impersonate": "chrome120"
            },
            {
                "browser": "safari",
                "platform": "macos",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                "impersonate": "safari15_5"
            }
        ]
        
        profile = random.choice(profiles)
        
        # Headers base que respetan el estándar moderno (Sec-CH-UA)
        headers = {
            "User-Agent": profile["user_agent"],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
        }
        
        return profile, headers
