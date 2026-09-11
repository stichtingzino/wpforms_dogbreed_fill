<?php
/* 
 * 
 * @link        https://github.com/mjb021/wpforms_dogbreed_fill
 * @since       0.1.1
 * @package     WPF_Dog_Breed_Fill
 * 
 * @wordpress-plugin
 * Plugin Name: WPF Dog Breed Fill
 * Plugin URI: https://github.com/mjb021/wpforms_dogbreed_fill
 * Description: A plugin to fill dog breed options in WPForms.
 * Version: 0.1.4-rc1
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
define( 'wpf_dogbreed_fill_VERSION', '0.1.3' );

// Define the plugin directory path
define( 'WPFORMS_DOGBREED_FILL_DIR', plugin_dir_path( __FILE__ ) );
define( 'WPFORMS_DOGBREED_FILL_URL', plugin_dir_url( __FILE__ ) );

require_once WPFORMS_DOGBREED_FILL_DIR . 'includes/functions.php';

/**
 * This plugin is basically a filter which fills the selection options on
 * a WPForms form of a specific type.
 * The source file for the breeds file is searched for in uploads/wpf first, if it
 * does not exist there, it will be searched for in the plugin directory.
 */

function dynamic_fci_breeds_checkboxes( $properties, $field, $form_data ) {
    // This routine will check for the term "ras" or "breed" in the label of the field,
    // and if found, it will fill the options with FCI dog breeds for the groups selected in settings.
    // echo '<div style="background:#d4edda; border:2px solid #c3e6cb; color:#155724; padding:15px; margin:20px 0; font-family:monospace; border-radius:5px;">';
    // echo '<strong>[STEP 1: wpforms_field_properties triggered]</strong><br>';
    // echo 'Form ID: <pre>' . print_r( $form_data['ID'], true ) . '</pre>';
    // echo 'Field Label: <pre>' . print_r( $field['label'], true ) . '</pre>';
    // echo '<strong>field_type: ' . esc_html( $field['type'] ) . '</strong><br>';
    if ( ! array_key_exists( 'label', $field ) || (! str_contains( $field['label'], 'ras' ) && ! str_contains( $field['label'], 'breed' ) )) {
        // echo '</div>';
        return $properties;
    }

    $fci_breeds = wpf_dogbreed_fill_get_selected_group_breeds();

    if ( empty( $fci_breeds ) ) {
        // echo '</div>';
        return $properties;
    }

    // Wis eventuele handmatige backend-keuzes
    unset( $properties['inputs'] );

    // Bouw de nieuwe optielijst op
    $counter = 1;
    $form_id = $form_data['id'];
    $field_id = $field['id'];
    foreach ( $fci_breeds as $value => $label ) {
        $properties['inputs'][ $counter ] = [
            'container' => [
                'attr' => [],
                'class' => [
                    0 => 'choice-' . $counter,
                    1 => 'depth-1'
                ],
                'data' => [],
                'id' => '',
            ],
            'label' => [
				'attr' => [
					'for' => 'wpforms-' . $form_id . '-field_' . $field_id . '_' . $counter
				],
				'class' => [
					0 => 'wpforms-field-label-inline',
				],
				'data' => [],
				'id' => '',
				'text' => esc_html( $label )
			],
            'attr' => [
				'name' => 'wpforms[fields][' . $field_id . '][]',
				'value' => esc_attr( $value ),
            ],
			'class' => [],
			'data' => [],
			'id' => 'wpforms-' . $form_id . '-field_' . $field_id . '_' . $counter,
            'required' => '',
			'default' => false,
        ];
        $counter++;
    }

    // echo '</div>';
    return $properties;
}

if ( is_admin() ) {
    require_once plugin_dir_path( __FILE__ ) . 'admin/wpforms_dogbreed_fill_admin.php';
}

add_filter( 'wpforms_field_properties', 'dynamic_fci_breeds_checkboxes', 10, 3 );
?>
