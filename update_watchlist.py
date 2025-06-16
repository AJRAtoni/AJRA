import os
import time
import json
import webbrowser
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# --- CONFIGURACIÓN ---
# Tu Client ID de la API de Trakt.
CLIENT_ID = "421ffeb2db44f26a8a2b6b8a5c3e7c946a333c33ff2b7789bab3fdec2f674472"
# Tu nombre de usuario de Trakt.
TRAKT_USERNAME = "AJRA"
# Nombre del archivo HTML de tu watchlist.
HTML_FILE = "watchlist.html"
# Archivo donde se guardarán las credenciales de Trakt para no pedirlas cada vez.
TOKEN_FILE = "trakt_token.json"
# --- FIN DE LA CONFIGURACIÓN ---

# Cargamos las variables de entorno (el CLIENT_SECRET) del archivo .env
load_dotenv()
CLIENT_SECRET = os.getenv("TRAKT_CLIENT_SECRET")

API_URL = "https://api.trakt.tv"

def get_device_codes():
    """
    Paso 1 de la autenticación: Obtiene los códigos del dispositivo para que autorices la aplicación.
    """
    print("Conectando con Trakt.tv para obtener los códigos de autorización...")
    response = requests.post(
        f"{API_URL}/oauth/device/code", json={"client_id": CLIENT_ID}
    )
    if response.status_code != 200:
        print("Error al obtener los códigos del dispositivo de Trakt.tv.")
        print(f"Respuesta: {response.text}")
        exit()

    codes = response.json()
    print("-" * 50)
    print(f"Para autorizar el script, ve a: {codes['verification_url']}")
    print(f"E introduce este código: {codes['user_code']}")
    print("-" * 50)
    
    # Abrimos el navegador automáticamente para el usuario.
    webbrowser.open(codes["verification_url"])
    
    return codes


def get_token(device_code):
    """
    Paso 2 de la autenticación: Espera a que autorices la app y obtiene el token de acceso.
    """
    print("Esperando autorización en el navegador...")
    payload = {
        "code": device_code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    
    response = requests.post(f"{API_URL}/oauth/device/token", json=payload)
    
    # Esperamos a que el usuario introduzca el código en la web de Trakt
    while response.status_code != 200:
        time.sleep(5)
        response = requests.post(f"{API_URL}/oauth/device/token", json=payload)
        
        # Si el usuario es demasiado lento, el código expira.
        if response.status_code == 410:
            print("El código ha expirado. Por favor, ejecuta el script de nuevo.")
            exit()

    print("¡Autorización recibida!")
    return response.json()


def save_token(token_data):
    """Guarda el token en un archivo JSON."""
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)
    print(f"Token guardado en '{TOKEN_FILE}'.")


def load_token():
    """Carga el token desde el archivo JSON."""
    if not Path(TOKEN_FILE).exists():
        return None
    with open(TOKEN_FILE, "r") as f:
        return json.load(f)

def refresh_token(current_token):
    """Refresca un token de acceso que ha expirado."""
    print("El token de acceso ha expirado. Refrescando...")
    payload = {
        "refresh_token": current_token["refresh_token"],
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "grant_type": "refresh_token",
    }
    response = requests.post(f"{API_URL}/oauth/token", json=payload)
    if response.status_code == 200:
        new_token = response.json()
        save_token(new_token)
        print("Token refrescado con éxito.")
        return new_token
    else:
        print("Error al refrescar el token. Se necesitará autenticación manual.")
        return None


def get_access_token():
    """
    Obtiene el token de acceso, ya sea cargándolo, refrescándolo o pidiendo uno nuevo.
    """
    if not CLIENT_SECRET:
        print("Error: La variable TRAKT_CLIENT_SECRET no está definida.")
        print("Por favor, crea un archivo .env y añade la línea: TRAKT_CLIENT_SECRET='tu_client_secret'")
        exit()

    token_data = load_token()

    if not token_data:
        print("No se encontró un token. Iniciando autenticación por primera vez.")
        device_codes = get_device_codes()
        token_data = get_token(device_codes["device_code"])
        save_token(token_data)
        return token_data["access_token"]
    
    # Comprobamos si el token ha expirado.
    # El tiempo está en segundos (timestamp).
    if time.time() > token_data.get("created_at", 0) + token_data.get("expires_in", 0):
        refreshed = refresh_token(token_data)
        if refreshed:
            return refreshed["access_token"]
        else: # Si el refresh falla, empezamos de nuevo.
             if Path(TOKEN_FILE).exists():
                Path(TOKEN_FILE).unlink() # Borramos el token viejo
             return get_access_token()

    return token_data["access_token"]


def get_watched_movies(access_token):
    """
    Obtiene la lista de películas vistas por el usuario desde la API de Trakt.
    """
    print("Obteniendo la lista de películas vistas desde Trakt.tv...")
    headers = {
        "Content-Type": "application/json",
        "trakt-api-version": "2",
        "trakt-api-key": CLIENT_ID,
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(
        f"{API_URL}/users/{TRAKT_USERNAME}/watched/movies", headers=headers
    )

    if response.status_code != 200:
        print(f"Error al obtener las películas vistas. Código: {response.status_code}")
        print(f"Respuesta: {response.text}")
        return set()

    watched_data = response.json()
    
    # Usamos un "set" para una búsqueda más rápida y normalizamos los títulos.
    watched_titles = {item["movie"]["title"].lower().strip() for item in watched_data}
    
    print(f"Encontradas {len(watched_titles)} películas vistas en tu perfil de Trakt.")
    return watched_titles


def update_watchlist_html(watched_titles):
    """
    Actualiza el archivo HTML, añadiendo o quitando la clase 'tachado'.
    """
    print(f"Leyendo el archivo '{HTML_FILE}'...")
    try:
        with open(HTML_FILE, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{HTML_FILE}'. Asegúrate de que está en la misma carpeta que el script.")
        return

    watchlist_div = soup.find("div", class_="watchlist")
    if not watchlist_div:
        print("Error: No se encontró el div con la clase 'watchlist' en tu HTML.")
        return

    movie_spans = watchlist_div.find_all("span")
    movies_updated = 0
    
    print("Comparando y actualizando la lista...")
    for span in movie_spans:
        movie_title = span.text.lower().strip()
        is_watched = movie_title in watched_titles
        has_tachado = "tachado" in span.get("class", [])

        # Si está vista en Trakt pero no tiene la clase, la añadimos.
        if is_watched and not has_tachado:
            span["class"] = span.get("class", []) + ["tachado"]
            print(f"  - Marcando como vista: '{span.text}'")
            movies_updated += 1
        
        # Si no está vista en Trakt pero sí tiene la clase, la quitamos.
        elif not is_watched and has_tachado:
            current_classes = span.get("class", [])
            current_classes.remove("tachado")
            # Si no quedan más clases, eliminamos el atributo para limpiar el HTML.
            if not current_classes:
                 del span['class']
            else:
                span['class'] = current_classes

            print(f"  - Desmarcando como vista: '{span.text}'")
            movies_updated += 1

    if movies_updated > 0:
        print(f"\nSe actualizaron {movies_updated} películas.")
        # Usamos prettify para mantener el formato del HTML lo más limpio posible.
        with open(HTML_FILE, "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        print(f"¡El archivo '{HTML_FILE}' ha sido actualizado con éxito!")
    else:
        print("\nTu watchlist ya estaba sincronizada. No se realizaron cambios.")


def main():
    """
    Función principal que orquesta todo el proceso.
    """
    print("--- Iniciando Sincronizador de Watchlist con Trakt.tv ---")
    access_token = get_access_token()
    watched_movies = get_watched_movies(access_token)
    if watched_movies:
        update_watchlist_html(watched_movies)
    print("--- Proceso finalizado ---")


if __name__ == "__main__":
    main() 