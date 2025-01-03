<?php
/**
 * Plugin Name: CKBA Plugin
 * Description: Verbindt WordPress met je FastAPI-backend.
 * Version: 1.0
 * Author: YininAI by YininIT
 */

 // Blokkeer directe toegang tot het bestand
if (!defined('ABSPATH')) {
    exit;
}

add_shortcode('test_shortcode', 'test_shortcode_function');

function test_shortcode_function() {
    return '<p>Dit is een werkende test-shortcode!</p>';
}


// Voeg een shortcode toe om gegevens op te halen
add_shortcode('ckba_data', 'ckba_get_data');

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


add_shortcode('ckba_test_db', 'ckba_test_db');

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


?>
