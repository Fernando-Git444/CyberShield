import os
import requests

class SupabaseAuth:
    """Cliente de autenticación REST para Supabase."""
    
    def __init__(self, url, key):
        self.url = f"{url}/auth/v1"
        self.headers = {
            "apikey": key,
            "Content-Type": "application/json"
        }

    def sign_in_with_password(self, credentials):
        """Inicia sesión con correo y contraseña."""
        endpoint = f"{self.url}/token?grant_type=password"
        payload = {
            "email": credentials.get("email"),
            "password": credentials.get("password")
        }
        response = requests.post(endpoint, json=payload, headers=self.headers)
        if response.status_code != 200:
            raise Exception(response.json().get("error_description", "Error de inicio de sesión"))
        
        data = response.json()
        # Simular la estructura de objeto esperada por la app (response.user.id)
        class User:
            def __init__(self, uid, email):
                self.id = uid
                self.email = email
        
        class AuthResponse:
            def __init__(self, user_data):
                self.user = User(user_data['user']['id'], user_data['user']['email'])
                self.access_token = user_data.get('access_token')

        return AuthResponse(data)

    def sign_up(self, credentials):
        """Registra un nuevo usuario con correo y contraseña."""
        endpoint = f"{self.url}/signup"
        payload = {
            "email": credentials.get("email"),
            "password": credentials.get("password")
        }
        response = requests.post(endpoint, json=payload, headers=self.headers)
        if response.status_code not in [200, 201]:
             raise Exception(response.json().get("msg", "Error de registro"))
        return True # Registro exitoso

    def sign_out(self):
        """Cierra la sesión del usuario (solo limpia la sesión del lado del cliente)."""
        pass

class SupabaseClient:
    """Cliente principal de Supabase que expone autenticación y acceso REST."""
    
    def __init__(self, url, key):
        self.auth = SupabaseAuth(url, key)
        self.rest_url = f"{url}/rest/v1"
        self.headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }

# Función de acceso singleton para obtener el cliente de Supabase
def get_supabase_client():
    """Retorna una instancia del cliente de Supabase configurado con las variables de entorno."""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        # Respaldo para cuando las claves aún no están configuradas (previene error al ejecutar run.py)
        return SupabaseClient("https://placeholder.supabase.co", "placeholder")
    return SupabaseClient(url, key)
