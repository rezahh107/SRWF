<?php
/**
 * Import the exact SRWF Gravity Forms export into disposable WordPress and emit raw read-back evidence.
 *
 * Executed with `wp eval-file`; production/staging state is never touched.
 */

if (!defined('ABSPATH')) {
    fwrite(STDERR, "WordPress bootstrap is required.\n");
    exit(2);
}

$scaffold = getenv('SRWF_SCAFFOLD_PATH') ?: '';
$artifact_dir = getenv('SRWF_ARTIFACT_DIR') ?: '';
$expected_sha = getenv('SRWF_SCAFFOLD_SHA256') ?: '';
$expected_gf_version = getenv('SRWF_GF_VERSION') ?: '';

if ($scaffold === '' || !is_readable($scaffold)) {
    throw new RuntimeException('Exact scaffold input is missing or unreadable.');
}
if ($artifact_dir === '' || !is_dir($artifact_dir)) {
    throw new RuntimeException('Artifact directory is unavailable.');
}
if (!class_exists('GFForms') || !class_exists('GFAPI')) {
    throw new RuntimeException('Gravity Forms is not active.');
}
if ($expected_gf_version === '' || GFForms::$version !== $expected_gf_version) {
    throw new RuntimeException(sprintf('Unexpected Gravity Forms version: %s', GFForms::$version));
}

$actual_sha = hash_file('sha256', $scaffold);
if (!is_string($actual_sha) || !hash_equals($expected_sha, $actual_sha)) {
    throw new RuntimeException('Scaffold SHA-256 does not match the pinned candidate.');
}

$existing = GFAPI::get_forms(null, null, 'id', 'ASC');
if (!is_array($existing) || count($existing) !== 0) {
    throw new RuntimeException('Disposable runtime was not empty before import.');
}

$export_file = WP_PLUGIN_DIR . '/gravityforms/export.php';
if (!class_exists('GFExport')) {
    if (!is_readable($export_file)) {
        throw new RuntimeException('Gravity Forms import implementation is unavailable.');
    }
    require_once $export_file;
}

$legacy_imported_forms = null;
$import_result = GFExport::import_file($scaffold, $legacy_imported_forms);
if (!is_array($import_result)) {
    throw new RuntimeException(sprintf(
        'Gravity Forms import returned unexpected result type: %s.',
        get_debug_type($import_result)
    ));
}

$form_ids = isset($import_result['form_ids']) && is_array($import_result['form_ids'])
    ? array_values($import_result['form_ids'])
    : array();
$failed_forms = isset($import_result['failed_forms']) && is_array($import_result['failed_forms'])
    ? $import_result['failed_forms']
    : array();

if (count($form_ids) !== 1 || count($failed_forms) !== 0) {
    throw new RuntimeException(sprintf(
        'Expected one successful imported form and no failures; observed form_ids=%s failed_forms=%s.',
        wp_json_encode($form_ids),
        wp_json_encode($failed_forms)
    ));
}

$count = count($form_ids);
$form_id = (int) $form_ids[0];
if ($form_id < 1) {
    throw new RuntimeException('Imported form did not expose a runtime Form ID.');
}

$inactive_result = GFAPI::update_form_property($form_id, 'is_active', false);
if (is_wp_error($inactive_result)) {
    throw new RuntimeException('Failed to keep imported form inactive: ' . $inactive_result->get_error_message());
}

$form = GFAPI::get_form($form_id);
if (!is_array($form)) {
    throw new RuntimeException('Imported form could not be read back through GFAPI.');
}

$forms = GFAPI::get_forms(null, false, 'id', 'ASC');
$listing = null;
foreach ($forms as $candidate) {
    if ((int) rgar($candidate, 'id') === $form_id) {
        $listing = $candidate;
        break;
    }
}
if (!is_array($listing)) {
    throw new RuntimeException('Imported form was not observable in the inactive form listing.');
}
if ((string) rgar($listing, 'is_active') !== '0') {
    throw new RuntimeException('Imported form is not inactive after explicit fail-safe deactivation.');
}

$field_ids = array();
$field_types = array();
foreach (rgar($form, 'fields', array()) as $field) {
    if (!is_object($field)) {
        throw new RuntimeException('Gravity Forms returned a non-object field during read-back.');
    }
    $field_ids[] = $field->id;
    $field_types[] = $field->type;
}

$readback = array(
    'schema_version' => '1.0.0',
    'lab_boundary' => 'DISPOSABLE_CI_NOT_STAGING',
    'source' => array(
        'file_name' => basename($scaffold),
        'sha256' => $actual_sha,
        'source_class' => getenv('SRWF_SCAFFOLD_SOURCE_CLASS') ?: 'UNKNOWN',
        'source_locator' => getenv('SRWF_SCAFFOLD_SOURCE_LOCATOR') ?: 'UNKNOWN',
    ),
    'runtime' => array(
        'wordpress' => get_bloginfo('version'),
        'php' => PHP_VERSION,
        'gravity_forms' => GFForms::$version,
        'gravity_forms_package_sha256' => getenv('SRWF_GF_SHA256') ?: '',
        'wp_cli' => getenv('SRWF_WP_CLI_VERSION') ?: '',
        'wp_cli_sha256' => getenv('SRWF_WP_CLI_SHA256') ?: '',
    ),
    'import' => array(
        'count' => $count,
        'form_id' => $form_id,
        'title' => (string) rgar($form, 'title'),
        'is_active' => false,
        'field_count' => count($field_ids),
        'field_ids' => $field_ids,
        'field_types' => $field_types,
        'form' => $form,
    ),
    'evidence_semantics' => array(
        'ci_form_field_ids_are_disposable' => true,
        'authoritative_implementation_mapping' => false,
        'staging_exercised' => false,
        'finance_manual_cheque_behavior_tested' => false,
    ),
);

$encoded = wp_json_encode($readback, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
if (!is_string($encoded)) {
    throw new RuntimeException('Could not serialize read-back evidence.');
}

$path = trailingslashit($artifact_dir) . 'lab-readback.json';
if (file_put_contents($path, $encoded . PHP_EOL) === false) {
    throw new RuntimeException('Could not write read-back evidence.');
}

printf(
    "SRWF_LAB_IMPORT_READBACK form_id=%d title=%s field_count=%d inactive=true\n",
    $form_id,
    (string) rgar($form, 'title'),
    count($field_ids)
);
