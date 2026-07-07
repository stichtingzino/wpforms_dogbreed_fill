<?php
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

function wpf_dogbreed_fill_register_settings() {
    register_setting(
        'wpf_dogbreed_fill_settings',
        'wpf_dogbreed_fill_selected_groups',
        array(
            'type' => 'array',
            'sanitize_callback' => 'wpf_dogbreed_fill_sanitize_selected_groups',
            'default' => array( 1 ),
        )
    );

    add_settings_section(
        'wpf_dogbreed_fill_main_section',
        'FCI group selection',
        '__return_false',
        'wpf_dogbreed_fill_settings'
    );

    add_settings_field(
        'wpf_dogbreed_fill_selected_groups',
        'Select FCI groups',
        'wpf_dogbreed_fill_render_group_field',
        'wpf_dogbreed_fill_settings',
        'wpf_dogbreed_fill_main_section'
    );
}
add_action( 'admin_init', 'wpf_dogbreed_fill_register_settings' );

function wpf_dogbreed_fill_sanitize_selected_groups( $input ) {
    if ( ! is_array( $input ) ) {
        return array( 1 );
    }

    $selected_groups = array_map( 'absint', $input );
    $selected_groups = array_values( array_unique( array_filter( $selected_groups, function( $group ) {
        return $group > 0;
    } ) ) );

    if ( empty( $selected_groups ) ) {
        return array( 1 );
    }

    sort( $selected_groups );
    return $selected_groups;
}

function wpf_dogbreed_fill_render_group_field() {
    $available_groups = wpf_dogbreed_fill_get_available_groups();
    $selected_groups = get_option( 'wpf_dogbreed_fill_selected_groups', array( 1 ) );

    if ( ! is_array( $selected_groups ) ) {
        $selected_groups = array( 1 );
    }

    if ( empty( $available_groups ) ) {
        echo '<p>No FCI group data is available yet.</p>';
        return;
    }

    foreach ( $available_groups as $group_number => $group_label ) {
        $is_checked = in_array( (int) $group_number, $selected_groups, true );
        echo '<label style="display:block;margin-bottom:6px;">';
        echo '<input type="checkbox" name="wpf_dogbreed_fill_selected_groups[]" value="' . esc_attr( $group_number ) . '" ' . checked( $is_checked, true, false ) . ' /> ';
        echo esc_html( $group_label );
        echo '</label>';
    }
}

function wpf_dogbreed_fill_add_settings_page() {
    add_options_page(
        'FCI Dog Breed Fill',
        'FCI Dog Breed Fill',
        'manage_options',
        'wpf_dogbreed_fill_settings',
        'wpf_dogbreed_fill_settings_page'
    );
}
add_action( 'admin_menu', 'wpf_dogbreed_fill_add_settings_page' );

function wpf_dogbreed_fill_settings_page() {
    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }
    ?>
    <div class="wrap">
        <h1>FCI Dog Breed Fill settings</h1>
        <p>Select which FCI groups should be included in the breed dropdown.</p>
        <form method="post" action="options.php">
            <?php settings_fields( 'wpf_dogbreed_fill_settings' ); ?>
            <?php do_settings_sections( 'wpf_dogbreed_fill_settings' ); ?>
            <?php submit_button(); ?>
        </form>
    </div>
    <?php
}
?>
