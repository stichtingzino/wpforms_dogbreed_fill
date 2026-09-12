<?php
/**
 * Contains all support functions for this plugin including pluging install and deinstall
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

function wpf_dogbreed_fill_get_language_code() {
    $selected_language = get_option( 'wpf_dogbreed_fill_language', 'Auto' );

    if ( $selected_language !== 'Auto' ) {
        return $selected_language;
    }

    // 1. Get the current user or site locale (e.g., 'nl_NL' or 'en_US')
    $locale = get_user_locale(); // Alternatively, use get_locale() for general site settings

    // 2. Extract the part before the underscore and convert to lowercase
    $locale_parts = explode('_', $locale);
    $language_code = strtolower($locale_parts[0]);

    // 3. Define the allowed language codes
    $allowed_languages = wpf_dogbreed_fill_get_available_languages();

    // 4. Verify if the language is allowed, otherwise fall back to 'nl'
    if (!in_array($language_code, $allowed_languages)) {
        $language_code = 'nl';
    }

    return $language_code;
}



// This function retrieves FCI dog breeds for a specific group number from the JSON file.
function get_fci_dog_breeds_by_group( $group_number ) {
    $dog_breeds_file = WPFORMS_DOGBREED_FILL_DIR . 'data/fci_dataset_' .  wpf_dogbreed_fill_get_language_code() . '.json';

    if ( ! file_exists( $dog_breeds_file ) ) {
        return [];
    }

    $json_data = file_get_contents( $dog_breeds_file );
    $breeds = json_decode( $json_data, true );

    if ( ! is_array( $breeds ) || empty( $breeds ) ) {
        return [];
    }

    $group_key = 'group_' . (string) $group_number;

    if ( isset( $breeds[ $group_key ] ) && is_array( $breeds[ $group_key ] ) && isset ($breeds[ $group_key ]['breeds'])) {
        return $breeds[ $group_key ]['breeds'];
    }

    return [];
}

function wpf_dogbreed_fill_get_available_languages() {
    $data_dir = WPFORMS_DOGBREED_FILL_DIR . 'data/';
    $files = glob( $data_dir . 'fci_dataset_*.json' );

    $languages = [];
    foreach ( $files as $file ) {
        $filename = basename( $file );
        if ( preg_match( '/fci_dataset_([a-z]{2})\.json/', $filename, $matches ) ) {
            $languages[] = $matches[1];
        }
    }

    return array_unique( $languages );
}

function wpf_dogbreed_fill_get_available_groups() {
    $dog_breeds_file = WPFORMS_DOGBREED_FILL_DIR . 'data/fci_dataset_' .  wpf_dogbreed_fill_get_language_code() . '.json';

    if ( ! file_exists( $dog_breeds_file ) ) {
        return [];
    }

    $json_data = file_get_contents( $dog_breeds_file );
    $breeds = json_decode( $json_data, true );

    if ( ! is_array( $breeds ) || empty( $breeds ) ) {
        return [];
    }

    $groups = [];
    foreach ( $breeds as $group_key => $group_data ) {
        if ( strpos( $group_key, 'group_' ) === 0 && isset( $group_data['fci_group'] ) ) {
            $group_number = substr( $group_key, 6 );
            $group_name = isset( $group_data['group_name'] ) ? $group_data['group_name'] : 'FCI Group ' . $group_number;
            $groups[ $group_number ] = $group_name;
        }
    }

    ksort( $groups );
    return $groups;
}

function wpf_dogbreed_fill_get_selected_groups() {
    $selected_groups = get_option( 'wpf_dogbreed_fill_selected_groups', array( 1 ) );

    if ( ! is_array( $selected_groups ) ) {
        $selected_groups = array( 1 );
    }

    $selected_groups = array_map( 'absint', $selected_groups );
    $selected_groups = array_values( array_unique( array_filter( $selected_groups, function( $group ) {
        return $group > 0;
    } ) ) );

    if ( empty( $selected_groups ) ) {
        $selected_groups = array( 1 );
    }

    sort( $selected_groups );
    return $selected_groups;
}

function wpf_dogbreed_fill_get_selected_group_breeds() {
    $selected_groups = wpf_dogbreed_fill_get_selected_groups();
    $fci_breeds = [];

    foreach ( $selected_groups as $group_number ) {
        $group_breeds = get_fci_dog_breeds_by_group( $group_number );
        if ( is_array( $group_breeds ) && ! empty( $group_breeds ) ) {
            $fci_breeds = array_merge( $fci_breeds, $group_breeds );
        }
    }

    return $fci_breeds;
}
