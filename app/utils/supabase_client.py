import os
import requests

class SupabaseAuth:
    def __init__(self, url, key):
        self.url = f"{url}/auth/v1"
        self.headers = {
            "apikey": key,
            "Content-Type": "application/json"
        }

    def sign_in_with_password(self, credentials):
        endpoint = f"{self.url}/token?grant_type=password"
        payload = {
            "email": credentials.get("email"),
            "password": credentials.get("password")
        }
        response = requests.post(endpoint, json=payload, headers=self.headers)
        if response.status_code != 200:
            raise Exception(response.json().get("error_description", "Login failed"))
        
        data = response.json()
        # Mocking the object structure expected by the app (response.user.id)
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
        endpoint = f"{self.url}/signup"
        payload = {
            "email": credentials.get("email"),
            "password": credentials.get("password")
        }
        response = requests.post(endpoint, json=payload, headers=self.headers)
        if response.status_code not in [200, 201]:
             raise Exception(response.json().get("msg", "Registration failed"))
        return True # Success

    def sign_out(self):
        # Client-side logout only needs to clear session usually
        pass

class SupabaseClient:
    def __init__(self, url, key):
        self.auth = SupabaseAuth(url, key)
        self.rest_url = f"{url}/rest/v1"
        self.headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }

# Singleton accessor
def get_supabase_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        # Fallback for when keys aren't set yet (prevents crash on run.py)
        return SupabaseClient("https://placeholder.supabase.co", "placeholder")
    return SupabaseClient(url, key)
