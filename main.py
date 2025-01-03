from fastapi import FastAPI
import os
from dotenv import load_dotenv

# Laad het .env-bestand
load_dotenv()

# Haal DATABASE_URL op
DATABASE_URL = os.getenv("DATABASE_URL")

# Definieer de FastAPI-app
app = FastAPI()

@app.get("/")
async def root():
    return {"greeting": "Hello, World!", "message": "Welcome to FastAPI!"}

@app.get("/test-db")
def test_db():
    # Controleer of DATABASE_URL correct is geladen
    if not DATABASE_URL:
        return {"error": "DATABASE_URL niet gevonden"}
    return {"database_url": DATABASE_URL}

add_shortcode('ckba_test_db', 'ckba_test_db');

function ckba_test_db() {
    $response = wp_remote_get('https://your-fastapi-server-url.com/test-db');

    if (is_wp_error($response)) {
        return 'Fout bij verbinding met de database: ' . $response->get_error_message();
    }

    $body = wp_remote_retrieve_body($response);
    $data = json_decode($body, true);

    if (isset($data['database_url'])) {
        return '<p>Database verbonden: ' . esc_html($data['database_url']) . '</p>';
    } else if (isset($data['error'])) {
        return '<p>Fout: ' . esc_html($data['error']) . '</p>';
    } else {
        return 'Onverwachte response van de server.';
    }
}


