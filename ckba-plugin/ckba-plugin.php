<?php
/**
 * Plugin Name: CKBA Plugin
 * Description: Verbindt WordPress met je FastAPI-backend.
 * Version: 1.0
 * Author: YininAI & YininIT
 */

// Blokkeer directe toegang
if (!defined('ABSPATH')) {
    exit;
}

// Upload functie
function ckba_upload_shortcode() {
    ob_start(); ?>
    <form id="ckba-upload-form" enctype="multipart/form-data">
        <input type="file" id="file" name="file" required>
        <button type="submit">Upload Document</button>
    </form>
    <div id="ckba-upload-response"></div>
    <script>
        document.getElementById("ckba-upload-form").addEventListener("submit", async function (e) {
            e.preventDefault();
            const formData = new FormData();
            formData.append("file", document.getElementById("file").files[0]);

            const responseDiv = document.getElementById("ckba-upload-response");
            responseDiv.innerHTML = "Even geduld, bestand wordt geupload...";

            try {
                const response = await fetch("https://ckba-main-fastapi-production.up.railway.app/upload", {
                    method: "POST",
                    body: formData,
                });

                const result = await response.json();
                if (response.ok) {
                    responseDiv.innerHTML = `<strong>Succes:</strong> ${result.message} (${result.filename})`;
                } else {
                    responseDiv.innerHTML = `<strong>Fout:</strong> ${result.detail}`;
                }
            } catch (error) {
                responseDiv.innerHTML = `<strong>Fout:</strong> Kan geen verbinding maken met de server.`;
            }
        });
    </script>
    <?php
    return ob_get_clean();
}

add_shortcode('ckba_upload', 'ckba_upload_shortcode');


// Stel een vraag en geef antwoord
function ckba_shortcode() {
    ob_start(); ?>
    <form id="ckba-form">
        <input type="text" id="question" name="question" placeholder="Stel een vraag" required>
        <button type="submit">Stel vraag</button>
    </form>
    <div id="ckba-response"></div>
    <script>
        document.getElementById("ckba-form").addEventListener("submit", async function (e) {
            e.preventDefault();
            const question = document.getElementById("question").value;
            const responseDiv = document.getElementById("ckba-response");
            responseDiv.innerHTML = "Even geduld, vraag wordt verwerkt...";

            const response = await fetch("https://ckba-main-fastapi-production.up.railway.app/answer", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: question })
            });

            const result = await response.json();
            if (response.ok) {
                responseDiv.innerHTML = `<strong>Antwoord:</strong> ${result.answer}`;
            } else {
                responseDiv.innerHTML = `<strong>Fout:</strong> ${result.detail}`;
            }
        });
    </script>
    <?php
    return ob_get_clean();
}

add_shortcode('ckba', 'ckba_shortcode');



// Shortcode: Database test
function ckba_test_db_shortcode() {
    $response = ckba_api_request('https://ckba-main-fastapi-production.up.railway.app/test-db');
    if (isset($response['database_url'])) {
        return "Verbonden met database: {$response['database_url']}";
    } elseif (isset($response['error'])) {
        return "Fout: {$response['error']}";
    }
    return 'Geen geldige database-informatie ontvangen.';
}

add_shortcode('ckba_test_db_shortcode', 'ckba_test_db_shortcode');



// Enkel de shortcode te testen
function test_shortcode_function() {
    return '<p>Dit is een werkende test-shortcode!</p>';
}

add_shortcode('test_shortcode', 'test_shortcode_function');


// Voeg een shortcode toe om servergegevens op te halen
function ckba_get_data() {
    $response = wp_remote_get('https://ckba-main-fastapi-production.up.railway.app/');

    if (is_wp_error($response)) {
        return 'Er is een fout opgetreden: ' . $response->get_error_message();
    }

    $body = wp_remote_retrieve_body($response);
    $data = json_decode($body, true);

    // Controleer of de data correct is
    if (isset($data['greeting']) && isset($data['message'])) {
        return '<p>' . esc_html($data['greeting']) . '</p><p>' . esc_html($data['message']) . '</p>';
    } else {
        return 'Geen geldige data ontvangen van de server.';
    }
}

add_shortcode('ckba_data', 'ckba_get_data');


// Voeg een shortcode toe om databasegegevens op te halen
function ckba_test_db() {
    $response = wp_remote_get('https://ckba-main-fastapi-production.up.railway.app/test-db');

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

add_shortcode('ckba_test_db', 'ckba_test_db');


?>
