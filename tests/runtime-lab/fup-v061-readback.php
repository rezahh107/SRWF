<?php
/**
 * Disposable runtime proof for the SRWF v0.6.1 Gravity Forms candidate.
 *
 * Executed under wp eval-file with authentic Gravity Forms / Gravity Perks /
 * GP File Upload Pro active. This is CI-only evidence and never writes staging IDs.
 */

if (!defined('ABSPATH')) {
    fwrite(STDERR, "WordPress bootstrap is required.\n");
    exit(2);
}

$candidate = getenv('SRWF_V061_PATH') ?: '';
$artifact_dir = getenv('SRWF_ARTIFACT_DIR') ?: '';
$expected_sha = getenv('SRWF_V061_SHA256') ?: '';
$expected_gf = getenv('SRWF_GF_VERSION') ?: '';
$expected_gp = getenv('SRWF_GP_VERSION') ?: '';
$expected_fup = getenv('SRWF_FUP_VERSION') ?: '';

function srwf_fail(string $message): never {
    throw new RuntimeException($message);
}

function srwf_empty_dimension(mixed $value): bool {
    return $value === null || $value === '';
}

function srwf_find_field(array $form, string $admin_label): ?GF_Field {
    foreach (rgar($form, 'fields', array()) as $field) {
        if ($field instanceof GF_Field && (string) $field->adminLabel === $admin_label) {
            return $field;
        }
    }
    return null;
}

if ($candidate === '' || !is_readable($candidate)) {
    srwf_fail('Candidate artifact is missing or unreadable.');
}
if ($artifact_dir === '' || !is_dir($artifact_dir)) {
    srwf_fail('Artifact directory is unavailable.');
}
$actual_sha = hash_file('sha256', $candidate);
if (!is_string($actual_sha) || $expected_sha === '' || !hash_equals($expected_sha, $actual_sha)) {
    srwf_fail('Candidate SHA-256 mismatch.');
}

if (!class_exists('GFForms') || !class_exists('GFAPI')) {
    srwf_fail('Gravity Forms is not active.');
}
if ($expected_gf === '' || GFForms::$version !== $expected_gf) {
    srwf_fail('Unexpected Gravity Forms version: ' . GFForms::$version);
}
if (!defined('GRAVITY_PERKS_VERSION') || GRAVITY_PERKS_VERSION !== $expected_gp) {
    srwf_fail('Unexpected Gravity Perks version.');
}
if (!defined('GPFUP_VERSION') || GPFUP_VERSION !== $expected_fup) {
    srwf_fail('Unexpected GP File Upload Pro version.');
}
if (!function_exists('gp_file_upload_pro')) {
    srwf_fail('GP File Upload Pro runtime accessor is unavailable.');
}

$perk = gp_file_upload_pro();
if (!$perk instanceof GP_File_Upload_Pro) {
    srwf_fail('GP File Upload Pro runtime instance is unavailable.');
}

$existing = GFAPI::get_forms(null, null, 'id', 'ASC');
if (!is_array($existing) || count($existing) !== 0) {
    srwf_fail('Disposable runtime was not empty before import.');
}

$export_file = WP_PLUGIN_DIR . '/gravityforms/export.php';
if (!class_exists('GFExport')) {
    if (!is_readable($export_file)) {
        srwf_fail('Gravity Forms import/export implementation is unavailable.');
    }
    require_once $export_file;
}

$legacy_imported_forms = null;
$import_result = GFExport::import_file($candidate, $legacy_imported_forms);
if (!is_array($import_result)) {
    srwf_fail('Gravity Forms import returned an unexpected result type.');
}
$form_ids = isset($import_result['form_ids']) && is_array($import_result['form_ids'])
    ? array_values($import_result['form_ids'])
    : array();
$failed_forms = isset($import_result['failed_forms']) && is_array($import_result['failed_forms'])
    ? $import_result['failed_forms']
    : array();
if (count($form_ids) !== 1 || count($failed_forms) !== 0) {
    srwf_fail('Expected exactly one successful form import with no failures.');
}

$form_id = (int) $form_ids[0];
if ($form_id < 1) {
    srwf_fail('Imported form ID is invalid.');
}
$inactive_result = GFAPI::update_form_property($form_id, 'is_active', false);
if (is_wp_error($inactive_result)) {
    srwf_fail('Failed to keep imported form inactive: ' . $inactive_result->get_error_message());
}

$form = GFAPI::get_form($form_id);
if (!is_array($form)) {
    srwf_fail('Imported form could not be read back through GFAPI.');
}
$fields = rgar($form, 'fields', array());
if (!is_array($fields) || count($fields) !== 37) {
    srwf_fail('Unexpected imported field count.');
}

$photo = srwf_find_field($form, 'student_photo');
if (!$photo instanceof GF_Field) {
    srwf_fail('student_photo field is missing after import.');
}

$checks = array(
    'type_fileupload' => $photo->type === 'fileupload',
    'required' => (bool) $photo->isRequired === true,
    'extensions_jpg_jpeg' => (string) $photo->allowedExtensions === 'jpg,jpeg',
    'max_file_size_5mb' => (string) $photo->maxFileSize === '5',
    'single_file_limit' => (bool) $photo->multipleFiles === true && (string) $photo->maxFiles === '1',
    'fup_enabled' => (bool) rgar($photo, 'gpfupEnable') === true,
    'crop_enabled' => (bool) rgar($photo, 'gpfupEnableCrop') === true,
    'crop_required' => (bool) rgar($photo, 'gpfupCropRequired') === true,
    'ratio_antecedent_3' => (string) rgar($photo, 'gpfupAspectRatioAntecedent') === '3',
    'ratio_consequent_4' => (string) rgar($photo, 'gpfupAspectRatioConsequent') === '4',
    'max_width_1200' => (string) rgar($photo, 'gpfupMaxWidth') === '1200',
    'max_height_1600' => (string) rgar($photo, 'gpfupMaxHeight') === '1600',
    'no_min_width' => srwf_empty_dimension(rgar($photo, 'gpfupMinWidth')),
    'no_min_height' => srwf_empty_dimension(rgar($photo, 'gpfupMinHeight')),
    'no_exact_width' => srwf_empty_dimension(rgar($photo, 'gpfupExactWidth')),
    'no_exact_height' => srwf_empty_dimension(rgar($photo, 'gpfupExactHeight')),
);

$ratio = $perk->get_aspect_ratio_float($photo);
$checks['plugin_ratio_float_0_75'] = is_float($ratio) && abs($ratio - 0.75) < 0.0000001;
$checks['plugin_should_enqueue_frontend'] = $perk->should_enqueue_frontend($form) === true;

// Exercise File Upload Pro's own frontend localization path so evidence records
// the exact values the maintained Perk exposes to its browser runtime.
if (!wp_script_is('gp-file-upload-pro', 'registered')) {
    wp_register_script('gp-file-upload-pro', 'https://example.invalid/gp-file-upload-pro.js', array(), GPFUP_VERSION, true);
}
$perk->localize_frontend_scripts($form);
$localized_data = wp_scripts()->get_data('gp-file-upload-pro', 'data');
if (!is_string($localized_data) || $localized_data === '') {
    srwf_fail('GP File Upload Pro frontend localization was not produced.');
}
$var_name = 'GPFUP_FORM_INIT_' . $form_id;
$pattern = '/var\\s+' . preg_quote($var_name, '/') . '\\s*=\\s*(\\[[^;]+\\]);/s';
if (!preg_match($pattern, $localized_data, $matches)) {
    srwf_fail('Could not parse GP File Upload Pro frontend localization.');
}
$localized = json_decode($matches[1], true, 512, JSON_THROW_ON_ERROR);
$localized_photo = null;
foreach ($localized as $item) {
    if (is_array($item) && (int) ($item['fieldId'] ?? 0) === (int) $photo->id) {
        $localized_photo = $item;
        break;
    }
}
if (!is_array($localized_photo)) {
    srwf_fail('student_photo was not present in GP File Upload Pro frontend localization.');
}
$checks['localized_crop_required'] = (bool) ($localized_photo['cropRequired'] ?? false) === true;
$checks['localized_aspect_ratio_0_75'] = isset($localized_photo['aspectRatio'])
    && abs((float) $localized_photo['aspectRatio'] - 0.75) < 0.0000001;
$checks['localized_max_width_1200'] = (string) ($localized_photo['maxWidth'] ?? '') === '1200';
$checks['localized_max_height_1600'] = (string) ($localized_photo['maxHeight'] ?? '') === '1600';
$checks['localized_no_min_dimensions'] = empty($localized_photo['minWidth']) && empty($localized_photo['minHeight']);
$checks['localized_no_exact_dimensions'] = empty($localized_photo['exactWidth']) && empty($localized_photo['exactHeight']);

// Exercise Gravity Forms' authentic export preparation after the real import.
$runtime_forms = GFFormsModel::get_form_meta_by_id(array($form_id));
$exported = GFExport::prepare_forms_for_export($runtime_forms);
$exported_photo = null;
foreach (($exported[0]['fields'] ?? array()) as $field) {
    if (is_object($field) && (string) $field->adminLabel === 'student_photo') {
        $exported_photo = $field;
        break;
    }
}
if (!$exported_photo instanceof GF_Field) {
    srwf_fail('student_photo is missing from authentic Gravity Forms export preparation.');
}
$checks['export_preserves_ratio_3_4'] = (string) rgar($exported_photo, 'gpfupAspectRatioAntecedent') === '3'
    && (string) rgar($exported_photo, 'gpfupAspectRatioConsequent') === '4';
$checks['export_preserves_max_1200_1600'] = (string) rgar($exported_photo, 'gpfupMaxWidth') === '1200'
    && (string) rgar($exported_photo, 'gpfupMaxHeight') === '1600';
$checks['export_preserves_no_min_exact'] = srwf_empty_dimension(rgar($exported_photo, 'gpfupMinWidth'))
    && srwf_empty_dimension(rgar($exported_photo, 'gpfupMinHeight'))
    && srwf_empty_dimension(rgar($exported_photo, 'gpfupExactWidth'))
    && srwf_empty_dimension(rgar($exported_photo, 'gpfupExactHeight'));

$failures = array_keys(array_filter($checks, static fn(bool $ok): bool => !$ok));
$status = empty($failures) ? 'LAB_PASS' : 'LAB_FAIL';

$evidence = array(
    'schema_version' => '1.0.0',
    'lab_status' => $status,
    'scenario' => 'GF_V061_FUP_AUTHENTIC_RUNTIME_READBACK',
    'boundary' => 'DISPOSABLE_CI_NOT_STAGING',
    'source_artifact' => array(
        'name' => basename($candidate),
        'sha256' => $actual_sha,
        'expected_sha256' => $expected_sha,
    ),
    'runtime' => array(
        'wordpress' => get_bloginfo('version'),
        'php' => PHP_VERSION,
        'gravity_forms' => GFForms::$version,
        'gravity_forms_package_sha256' => getenv('SRWF_GF_SHA256') ?: '',
        'gravity_perks' => GRAVITY_PERKS_VERSION,
        'gravity_perks_package_sha256' => getenv('SRWF_GP_SHA256') ?: '',
        'gp_file_upload_pro' => GPFUP_VERSION,
        'gp_file_upload_pro_package_sha256' => getenv('SRWF_FUP_SHA256') ?: '',
    ),
    'observed' => array(
        'form_id' => $form_id,
        'form_inactive' => true,
        'field_count' => count($fields),
        'student_photo_field_id' => (int) $photo->id,
        'student_photo_metadata' => array(
            'gpfupEnable' => rgar($photo, 'gpfupEnable'),
            'gpfupEnableCrop' => rgar($photo, 'gpfupEnableCrop'),
            'gpfupCropRequired' => rgar($photo, 'gpfupCropRequired'),
            'gpfupAspectRatioAntecedent' => rgar($photo, 'gpfupAspectRatioAntecedent'),
            'gpfupAspectRatioConsequent' => rgar($photo, 'gpfupAspectRatioConsequent'),
            'gpfupMaxWidth' => rgar($photo, 'gpfupMaxWidth'),
            'gpfupMaxHeight' => rgar($photo, 'gpfupMaxHeight'),
            'gpfupMinWidth' => rgar($photo, 'gpfupMinWidth'),
            'gpfupMinHeight' => rgar($photo, 'gpfupMinHeight'),
            'gpfupExactWidth' => rgar($photo, 'gpfupExactWidth'),
            'gpfupExactHeight' => rgar($photo, 'gpfupExactHeight'),
        ),
        'plugin_derived_aspect_ratio' => $ratio,
        'frontend_localization' => $localized_photo,
    ),
    'assertions' => $checks,
    'failures' => $failures,
    'evidence_semantics' => array(
        'ci_form_field_ids_are_disposable' => true,
        'write_ids_to_implementation_mapping' => false,
        'staging_exercised' => false,
        'staging_pass' => false,
        'production_ready_claim' => false,
        'synthetic_entry_data_created' => false,
    ),
);

$evidence_json = wp_json_encode($evidence, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
$export_json = wp_json_encode($exported, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
if (!is_string($evidence_json) || !is_string($export_json)) {
    srwf_fail('Could not serialize runtime evidence.');
}
file_put_contents(trailingslashit($artifact_dir) . 'v061-fup-runtime-evidence.json', $evidence_json . PHP_EOL);
file_put_contents(trailingslashit($artifact_dir) . 'v061-authentic-gf-roundtrip-export.json', $export_json . PHP_EOL);

if ($status !== 'LAB_PASS') {
    fwrite(STDERR, "SRWF v0.6.1 FUP runtime assertion failure(s):\n- " . implode("\n- ", $failures) . "\n");
    exit(1);
}

printf(
    "SRWF_V061_FUP_RUNTIME LAB_PASS form_id=%d field_id=%d aspect_ratio=%.2f max=%sx%s inactive=true\n",
    $form_id,
    (int) $photo->id,
    $ratio,
    (string) rgar($photo, 'gpfupMaxWidth'),
    (string) rgar($photo, 'gpfupMaxHeight')
);
