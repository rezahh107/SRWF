<?php
/**
 * Authentic runtime read-back for the SRWF v0.6.2 provisional candidate.
 *
 * Always exercises Gravity Forms + maintained PersianGravity. When
 * SRWF_V062_RUNTIME_MODE=FULL_STACK it additionally requires authentic
 * Gravity Perks, GP File Upload Pro and GP Advanced Select.
 */

if (!defined('ABSPATH')) {
    fwrite(STDERR, "WordPress bootstrap is required.\n");
    exit(2);
}

$candidate = getenv('SRWF_V062_PATH') ?: '';
$artifactDir = getenv('SRWF_ARTIFACT_DIR') ?: '';
$expectedSha = getenv('SRWF_V062_SHA256') ?: '';
$expectedGf = getenv('SRWF_GF_VERSION') ?: '';
$expectedPgr = getenv('SRWF_PGR_VERSION') ?: '';
$mode = getenv('SRWF_V062_RUNTIME_MODE') ?: 'MINIMAL_CURRENT_PG';
$fullStack = $mode === 'FULL_STACK';

function srwf_v062_fail(string $message): never {
    throw new RuntimeException($message);
}

function srwf_v062_find_field(array $form, string $adminLabel): ?GF_Field {
    foreach (rgar($form, 'fields', array()) as $field) {
        if ($field instanceof GF_Field && (string) $field->adminLabel === $adminLabel) {
            return $field;
        }
    }
    return null;
}

function srwf_v062_field_prop(GF_Field $field, string $name, mixed $default = null): mixed {
    return $field->{$name} ?? $default;
}

function srwf_v062_empty_dimension(mixed $value): bool {
    return $value === null || $value === '';
}

function srwf_v062_plugin_version_by_prefix(string $prefix): string {
    if (!function_exists('get_plugins')) {
        require_once ABSPATH . 'wp-admin/includes/plugin.php';
    }
    foreach (get_plugins() as $pluginFile => $data) {
        if (str_starts_with((string) $pluginFile, $prefix . '/')) {
            return (string) ($data['Version'] ?? '');
        }
    }
    return '';
}

if (!in_array($mode, array('MINIMAL_CURRENT_PG', 'FULL_STACK'), true)) {
    srwf_v062_fail('Unsupported SRWF_V062_RUNTIME_MODE.');
}
if ($candidate === '' || !is_readable($candidate)) {
    srwf_v062_fail('Candidate artifact is missing or unreadable.');
}
if ($artifactDir === '' || !is_dir($artifactDir)) {
    srwf_v062_fail('Artifact directory is unavailable.');
}

$actualSha = hash_file('sha256', $candidate);
if (!is_string($actualSha) || $expectedSha === '' || !hash_equals($expectedSha, $actualSha)) {
    srwf_v062_fail('Candidate SHA-256 mismatch.');
}
if (!class_exists('GFForms') || !class_exists('GFAPI')) {
    srwf_v062_fail('Gravity Forms is not active.');
}
if ($expectedGf === '' || GFForms::$version !== $expectedGf) {
    srwf_v062_fail('Unexpected Gravity Forms version: ' . GFForms::$version);
}
if (!defined('PGR_VERSION') || $expectedPgr === '' || PGR_VERSION !== $expectedPgr) {
    srwf_v062_fail('Unexpected PersianGravity version.');
}
if (!class_exists('PGR_GF_Field_National_ID') || !class_exists('PGR_GF_Field_Jalali_Date')) {
    srwf_v062_fail('Maintained PersianGravity field classes are unavailable.');
}

$existing = GFAPI::get_forms(null, null, 'id', 'ASC');
if (!is_array($existing) || count($existing) !== 0) {
    srwf_v062_fail('Disposable runtime was not empty before import.');
}

$exportFile = WP_PLUGIN_DIR . '/gravityforms/export.php';
if (!class_exists('GFExport')) {
    if (!is_readable($exportFile)) {
        srwf_v062_fail('Gravity Forms import/export implementation is unavailable.');
    }
    require_once $exportFile;
}

$legacyImportedForms = null;
$importResult = GFExport::import_file($candidate, $legacyImportedForms);
if (!is_array($importResult)) {
    srwf_v062_fail('Gravity Forms import returned an unexpected result type.');
}
$formIds = isset($importResult['form_ids']) && is_array($importResult['form_ids'])
    ? array_values($importResult['form_ids'])
    : array();
$failedForms = isset($importResult['failed_forms']) && is_array($importResult['failed_forms'])
    ? $importResult['failed_forms']
    : array();
if (count($formIds) !== 1 || count($failedForms) !== 0) {
    srwf_v062_fail('Expected exactly one successful form import with no failures.');
}

$formId = (int) $formIds[0];
if ($formId < 1) {
    srwf_v062_fail('Imported form ID is invalid.');
}
$inactiveResult = GFAPI::update_form_property($formId, 'is_active', false);
if (is_wp_error($inactiveResult)) {
    srwf_v062_fail('Failed to keep imported form inactive: ' . $inactiveResult->get_error_message());
}
$form = GFAPI::get_form($formId);
if (!is_array($form)) {
    srwf_v062_fail('Imported form could not be read back through GFAPI.');
}
$fields = rgar($form, 'fields', array());
if (!is_array($fields) || count($fields) !== 37) {
    srwf_v062_fail('Unexpected imported field count.');
}

$national = srwf_v062_find_field($form, 'national_id');
$dob = srwf_v062_find_field($form, 'dob_jalali');
$photo = srwf_v062_find_field($form, 'student_photo');
$school = srwf_v062_find_field($form, 'school_code');
if (!$national instanceof PGR_GF_Field_National_ID) {
    srwf_v062_fail('national_id did not hydrate as the maintained PersianGravity field class.');
}
if (!$dob instanceof PGR_GF_Field_Jalali_Date) {
    srwf_v062_fail('dob_jalali did not hydrate as the maintained PersianGravity field class.');
}
if (!$photo instanceof GF_Field || !$school instanceof GF_Field) {
    srwf_v062_fail('student_photo or school_code is missing after import.');
}

$checks = array(
    'form_inactive' => (bool) rgar($form, 'is_active') === false,
    'field_count_37' => count($fields) === 37,
    'national_type_current' => $national->type === 'pgr_national_id',
    'national_required' => (bool) $national->isRequired === true,
    'national_duplicates_allowed' => (bool) $national->noDuplicates === false,
    'national_force_english' => (bool) srwf_v062_field_prop($national, 'forceEnglish') === true,
    'dob_type_current' => $dob->type === 'pgr_jalali_date',
    'dob_required' => (bool) $dob->isRequired === true,
    'dob_presentation_ymd_slash' => (string) srwf_v062_field_prop($dob, 'jalali_format') === 'ymd_slash',
    'school_gpadvs_enabled_metadata' => (bool) srwf_v062_field_prop($school, 'gpadvsEnable') === true,
    'school_gf_enhanced_ui_off' => empty($school->enableEnhancedUI),
    'school_choice_count_947' => is_array($school->choices) && count($school->choices) === 947,
    'photo_type_fileupload' => $photo->type === 'fileupload',
    'photo_required' => (bool) $photo->isRequired === true,
    'photo_extensions_jpg_jpeg' => (string) $photo->allowedExtensions === 'jpg,jpeg',
    'photo_max_file_size_5mb' => (string) $photo->maxFileSize === '5',
    'photo_single_file_limit' => (bool) $photo->multipleFiles === true && (string) $photo->maxFiles === '1',
    'photo_fup_enabled_metadata' => (bool) srwf_v062_field_prop($photo, 'gpfupEnable') === true,
    'photo_crop_enabled_metadata' => (bool) srwf_v062_field_prop($photo, 'gpfupEnableCrop') === true,
    'photo_crop_required_metadata' => (bool) srwf_v062_field_prop($photo, 'gpfupCropRequired') === true,
    'photo_ratio_3_4_metadata' => (string) srwf_v062_field_prop($photo, 'gpfupAspectRatioAntecedent') === '3'
        && (string) srwf_v062_field_prop($photo, 'gpfupAspectRatioConsequent') === '4',
    'photo_max_1200_1600_metadata' => (string) srwf_v062_field_prop($photo, 'gpfupMaxWidth') === '1200'
        && (string) srwf_v062_field_prop($photo, 'gpfupMaxHeight') === '1600',
    'photo_no_min_exact_metadata' => srwf_v062_empty_dimension(srwf_v062_field_prop($photo, 'gpfupMinWidth'))
        && srwf_v062_empty_dimension(srwf_v062_field_prop($photo, 'gpfupMinHeight'))
        && srwf_v062_empty_dimension(srwf_v062_field_prop($photo, 'gpfupExactWidth'))
        && srwf_v062_empty_dimension(srwf_v062_field_prop($photo, 'gpfupExactHeight')),
);

$checks['national_canonical_ascii'] = $national->get_value_save_entry('۰۰۰۰۰۰۰۰۱۹', $form, '', 0, array()) === '0000000019';
$nationalValid = clone $national;
$nationalValid->failed_validation = false;
$nationalValid->validate('۰۰۰۰۰۰۰۰۱۹', $form);
$checks['national_valid_checksum_accepted'] = $nationalValid->failed_validation === false;
$nationalInvalid = clone $national;
$nationalInvalid->failed_validation = false;
$nationalInvalid->validate('1111111111', $form);
$checks['national_invalid_checksum_rejected'] = $nationalInvalid->failed_validation === true;

$checks['dob_canonical_ascii_dash'] = $dob->get_value_save_entry('۱۴۰۰/۰۱/۰۲', $form, '', 0, array()) === '1400-01-02';
$dobValid = clone $dob;
$dobValid->failed_validation = false;
$dobValid->validate('۱۴۰۰/۰۱/۰۲', $form);
$checks['dob_valid_jalali_accepted'] = $dobValid->failed_validation === false;
$dobInvalid = clone $dob;
$dobInvalid->failed_validation = false;
$dobInvalid->validate('۱۴۰۰/۱۳/۴۰', $form);
$checks['dob_invalid_jalali_rejected'] = $dobInvalid->failed_validation === true;

$observed = array(
    'form_id' => $formId,
    'form_inactive' => true,
    'field_count' => count($fields),
    'national_field_class' => get_class($national),
    'national_type' => $national->type,
    'national_canonical_sample' => $national->get_value_save_entry('۰۰۰۰۰۰۰۰۱۹', $form, '', 0, array()),
    'dob_field_class' => get_class($dob),
    'dob_type' => $dob->type,
    'dob_jalali_format' => srwf_v062_field_prop($dob, 'jalali_format'),
    'dob_canonical_sample' => $dob->get_value_save_entry('۱۴۰۰/۰۱/۰۲', $form, '', 0, array()),
    'school_field_id' => (int) $school->id,
    'photo_field_id' => (int) $photo->id,
);

if ($fullStack) {
    $expectedGp = getenv('SRWF_GP_VERSION') ?: '';
    $expectedFup = getenv('SRWF_FUP_VERSION') ?: '';
    $expectedAdvs = getenv('SRWF_ADVS_VERSION') ?: '';
    if (!defined('GRAVITY_PERKS_VERSION') || GRAVITY_PERKS_VERSION !== $expectedGp) {
        srwf_v062_fail('Unexpected or unavailable Gravity Perks runtime.');
    }
    if (!defined('GPFUP_VERSION') || GPFUP_VERSION !== $expectedFup || !function_exists('gp_file_upload_pro')) {
        srwf_v062_fail('Unexpected or unavailable GP File Upload Pro runtime.');
    }
    if (!function_exists('gp_advanced_select')) {
        srwf_v062_fail('GP Advanced Select runtime accessor is unavailable.');
    }

    $advsVersion = srwf_v062_plugin_version_by_prefix('gp-advanced-select');
    if ($expectedAdvs === '' || $advsVersion !== $expectedAdvs) {
        srwf_v062_fail('Unexpected GP Advanced Select version: ' . $advsVersion);
    }

    $fup = gp_file_upload_pro();
    if (!$fup instanceof GP_File_Upload_Pro) {
        srwf_v062_fail('GP File Upload Pro runtime instance is unavailable.');
    }
    $advs = gp_advanced_select();
    if (!is_object($advs) || !method_exists($advs, 'is_advanced_select_field')) {
        srwf_v062_fail('GP Advanced Select runtime instance is unavailable.');
    }

    $checks['fup_runtime_ratio_0_75'] = abs((float) $fup->get_aspect_ratio_float($photo) - 0.75) < 0.0000001;
    $checks['fup_runtime_should_enqueue'] = $fup->should_enqueue_frontend($form) === true;
    $checks['advs_runtime_recognizes_school'] = $advs->is_advanced_select_field($school) === true;

    if (!wp_script_is('gp-file-upload-pro', 'registered')) {
        wp_register_script('gp-file-upload-pro', 'https://example.invalid/gp-file-upload-pro.js', array(), GPFUP_VERSION, true);
    }
    $fup->localize_frontend_scripts($form);
    $localizedData = wp_scripts()->get_data('gp-file-upload-pro', 'data');
    if (!is_string($localizedData) || $localizedData === '') {
        srwf_v062_fail('GP File Upload Pro frontend localization was not produced.');
    }
    $varName = 'GPFUP_FORM_INIT_' . $formId;
    $pattern = '/var\\s+' . preg_quote($varName, '/') . '\\s*=\\s*(\\[[^;]+\\]);/s';
    if (!preg_match($pattern, $localizedData, $matches)) {
        srwf_v062_fail('Could not parse GP File Upload Pro frontend localization.');
    }
    $localized = json_decode($matches[1], true, 512, JSON_THROW_ON_ERROR);
    $localizedPhoto = null;
    foreach ($localized as $item) {
        if (is_array($item) && (int) ($item['fieldId'] ?? 0) === (int) $photo->id) {
            $localizedPhoto = $item;
            break;
        }
    }
    if (!is_array($localizedPhoto)) {
        srwf_v062_fail('student_photo was not present in GP File Upload Pro frontend localization.');
    }
    $checks['fup_localized_crop_required'] = (bool) ($localizedPhoto['cropRequired'] ?? false) === true;
    $checks['fup_localized_aspect_ratio_0_75'] = isset($localizedPhoto['aspectRatio'])
        && abs((float) $localizedPhoto['aspectRatio'] - 0.75) < 0.0000001;
    $checks['fup_localized_max_1200_1600'] = (string) ($localizedPhoto['maxWidth'] ?? '') === '1200'
        && (string) ($localizedPhoto['maxHeight'] ?? '') === '1600';
    $checks['fup_localized_no_min_exact'] = empty($localizedPhoto['minWidth']) && empty($localizedPhoto['minHeight'])
        && empty($localizedPhoto['exactWidth']) && empty($localizedPhoto['exactHeight']);
    $observed['fup_frontend_localization'] = $localizedPhoto;
    $observed['gp_advanced_select_field_recognized'] = true;
}

// Gravity Forms 3.1.1.1 returns one numeric form payload plus a top-level
// "version" metadata entry. Historical v0.6.1 authentic round-trip evidence
// has this exact shape; count($exported) is therefore expected to be 2.
$runtimeForms = GFFormsModel::get_form_meta_by_id(array($formId));
$exported = GFExport::prepare_forms_for_export($runtimeForms);
if (!is_array($exported) || !array_key_exists('version', $exported)) {
    srwf_v062_fail('Authentic Gravity Forms round-trip export metadata is missing.');
}
$roundtripForms = array_filter(
    $exported,
    static fn($key): bool => $key !== 'version',
    ARRAY_FILTER_USE_KEY
);
if (count($roundtripForms) !== 1 || !isset($roundtripForms[0]) || !is_array($roundtripForms[0])) {
    srwf_v062_fail('Authentic Gravity Forms round-trip must contain exactly one form payload.');
}
$roundtripNational = null;
$roundtripDob = null;
foreach (($roundtripForms[0]['fields'] ?? array()) as $field) {
    if (is_object($field) && (string) $field->adminLabel === 'national_id') {
        $roundtripNational = $field;
    }
    if (is_object($field) && (string) $field->adminLabel === 'dob_jalali') {
        $roundtripDob = $field;
    }
}
$checks['gf_roundtrip_national_current_type'] = $roundtripNational instanceof GF_Field
    && (string) $roundtripNational->type === 'pgr_national_id';
$checks['gf_roundtrip_dob_current_type'] = $roundtripDob instanceof GF_Field
    && (string) $roundtripDob->type === 'pgr_jalali_date'
    && (string) srwf_v062_field_prop($roundtripDob, 'jalali_format') === 'ymd_slash';

$failures = array_keys(array_filter($checks, static fn(bool $ok): bool => !$ok));
$status = empty($failures) ? 'LAB_PASS' : 'LAB_FAIL';
$runtime = array(
    'wordpress' => get_bloginfo('version'),
    'php' => PHP_VERSION,
    'gravity_forms' => GFForms::$version,
    'gravity_forms_package_sha256' => getenv('SRWF_GF_SHA256') ?: '',
    'persian_gravity' => PGR_VERSION,
    'persian_gravity_package_sha256' => getenv('SRWF_PGR_SHA256') ?: '',
);
if ($fullStack) {
    $runtime['gravity_perks'] = defined('GRAVITY_PERKS_VERSION') ? GRAVITY_PERKS_VERSION : '';
    $runtime['gravity_perks_package_sha256'] = getenv('SRWF_GP_SHA256') ?: '';
    $runtime['gp_file_upload_pro'] = defined('GPFUP_VERSION') ? GPFUP_VERSION : '';
    $runtime['gp_file_upload_pro_package_sha256'] = getenv('SRWF_FUP_SHA256') ?: '';
    $runtime['gp_advanced_select'] = srwf_v062_plugin_version_by_prefix('gp-advanced-select');
    $runtime['gp_advanced_select_package_sha256'] = getenv('SRWF_ADVS_SHA256') ?: '';
}

$evidence = array(
    'schema_version' => '1.0.0',
    'lab_status' => $status,
    'scenario' => $fullStack ? 'GF_V062_CURRENT_PG_FULL_STACK_READBACK' : 'GF_V062_CURRENT_PG_MINIMAL_READBACK',
    'boundary' => 'DISPOSABLE_CI_NOT_STAGING',
    'runtime_mode' => $mode,
    'source_artifact' => array(
        'name' => basename($candidate),
        'sha256' => $actualSha,
        'expected_sha256' => $expectedSha,
    ),
    'runtime' => $runtime,
    'observed' => $observed,
    'assertions' => $checks,
    'failures' => $failures,
    'evidence_semantics' => array(
        'ci_form_field_ids_are_disposable' => true,
        'write_ids_to_implementation_mapping' => false,
        'staging_exercised' => false,
        'staging_pass' => false,
        'production_ready_claim' => false,
        'synthetic_values_only' => true,
        'full_paid_stack_exercised' => $fullStack,
    ),
);
$evidenceJson = wp_json_encode($evidence, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
$exportJson = wp_json_encode($exported, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
if (!is_string($evidenceJson) || !is_string($exportJson)) {
    srwf_v062_fail('Could not serialize runtime evidence.');
}
file_put_contents(trailingslashit($artifactDir) . 'v062-runtime-evidence.json', $evidenceJson . PHP_EOL);
file_put_contents(trailingslashit($artifactDir) . 'lab-evidence.json', $evidenceJson . PHP_EOL);
file_put_contents(trailingslashit($artifactDir) . 'v062-authentic-gf-roundtrip-export.json', $exportJson . PHP_EOL);

if ($status !== 'LAB_PASS') {
    fwrite(STDERR, "SRWF v0.6.2 runtime assertion failure(s):\n- " . implode("\n- ", $failures) . "\n");
    exit(1);
}

printf(
    "SRWF_V062_RUNTIME LAB_PASS mode=%s form_id=%d fields=%d national=%s dob=%s inactive=true\n",
    $mode,
    $formId,
    count($fields),
    $national->type,
    $dob->type
);
