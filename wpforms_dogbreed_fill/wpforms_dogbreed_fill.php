/* 
 * 
 * @link        https://github.com/mjb021/wpforms_dogbreed_fill
 * @since       0.1.0
 * @package     WPF_Dog_Breed_Fill
 * 
 * @wordpress-plugin
 * Plugin Name: WPF Dog Breed Fill
 * Plugin URI: https://github.com/mjb021/wpforms_dogbreed_fill
 * Description: A plugin to fill dog breed options in WPForms.
 * Version: 0.1.0
 * Author: Mark Blom
 * License: <GPL-3></GPL-3>.0+
 * License URI: http://www.gnu.org/licenses/gpl-3.0.txt
 */

// If this file is called directly, abort.
if ( ! defined( 'WPINC' ) ) {
	die;
}
/**
 * Currently plugin version.
 * Start at version 1.0.0 and use SemVer - https://semver.org
 * Rename this for your plugin and update it as you release new versions.
 */
define( 'wpf_dogbreed_fill_VERSION', '0.1.0' );

/**
 * This plugin is basically a filter which fills the selection options on
 * a WPForms form of a specific type.
 * The source file for the breeds file is searched for in uploads/wpf first, if it
 * does not exist there, it will be searched for in the plugin directory.
 */
if ( ! file_exists( get_home_path() . 'uploads/wpf/dogbreeds.json' ) ) {
    $dog_breeds_file = plugin_dir_path( __FILE__ ) . 'dogbreeds.json';
} else {
    $dog_breeds_file = get_home_path() . 'uploads/wpf/dogbreeds.json';
}

// This function retrieves FCI dog breeds for a specific group number from the JSON file.
function get_fci_dog_breeds_by_group( $group_number ) {
    global $dog_breeds_file;

    if ( ! file_exists( $dog_breeds_file ) ) {
        return [];
    }

    $json_data = file_get_contents( $dog_breeds_file );
    $breeds = json_decode( $json_data, true );

    if ( ! is_array( $breeds ) || ! isset( $breeds['fci_groep'] ) || ! is_array( $breeds['fci_groep'] ) ) {
        return [];
    }

    $group_key = (string) $group_number;

    if ( isset( $breeds['fci_groep'][ $group_key ] ) ) {
        return $breeds['fci_groep'][ $group_key ];
    }

    if ( isset( $breeds['fci_groep'][ $group_number ] ) ) {
        return $breeds['fci_groep'][ $group_number ];
    }

    return [];
}

function wpf_dogbreed_fill_get_available_groups() {
    global $dog_breeds_file;

    if ( ! file_exists( $dog_breeds_file ) ) {
        return [];
    }

    $json_data = file_get_contents( $dog_breeds_file );
    $breeds = json_decode( $json_data, true );

    if ( ! is_array( $breeds ) || ! isset( $breeds['fci_groep'] ) || ! is_array( $breeds['fci_groep'] ) ) {
        return [];
    }

    $groups = [];
    foreach ( $breeds['fci_groep'] as $group_number => $group_breeds ) {
        $groups[ (string) $group_number ] = sprintf( 'FCI Group %s', $group_number );
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

function dynamic_fci_breeds_checkboxes( $properties, $field, $form_data ) {
    // This routine will check for the term "ras" or "breed" in the label of the field,
    // and if found, it will fill the options with FCI dog breeds for the groups selected in settings.
    if ( absint( $form_data['id'] ) !== 125 || absint( $field['id'] ) !== 4 ) {
        return $properties;
    }
    if ( ! str_contains( $field['label'], 'ras' ) && ! str_contains( $field['label'], 'breed' ) ) {
        return $properties;
    }

    $fci_breeds = wpf_dogbreed_fill_get_selected_group_breeds();

    if ( empty( $fci_breeds ) ) {
        return $properties;
    }

    // Wis eventuele handmatige backend-keuzes
    unset( $properties['inputs'] );

    // Bouw de nieuwe optielijst op
    $counter = 1;
    foreach ( $fci_breeds as $value => $label ) {
        $properties['inputs'][ $counter ] = [
            'label' => esc_html( $label ),
            'value' => esc_attr( $value ),
            'id'    => 'wpforms-' . $form_data['id'] . '-field_' . $field['id'] . '_' . $counter,
        ];
        $counter++;
    }

    return $properties;
}

if ( is_admin() ) {
    require_once plugin_dir_path( __FILE__ ) . 'admin/wpf_dogbreed_fill_admin.php';
}

add_filter( 'wpforms_field_properties', 'dynamic_fci_breeds_checkboxes', 10, 3 );
