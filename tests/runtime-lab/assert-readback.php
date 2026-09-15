<?php
/**
 * Compare the exact pinned Gravity Forms export with disposable runtime read-back.
 *
 * The source artifact is content-addressed by its Owner-recorded SHA-256. This
 * verifier checks that source-defined form/field settings survive the real import path;
 * it does not turn disposable CI IDs into staging authority.
 */

declare(strict_types=1);

if ($argc !== 4) {
    fwrite(STDERR, "Usage: php assert-readback.php <source.json> <readback.json> <evidence.json>\n");
    exit(2);
}

[$script, $source_path, $readback_path, $evidence_path] = $argv;
$expected_sha = getenv('SRWF_SCAFFOLD_SHA256') ?: '445f146b6c6d9ecf7badecce23b19be9dee59b653ec7c78c4537decaa3b31c89';
$expected_gf_sha = getenv('SRWF_GF_SHA256') ?: '542f56ae0747f3661d1474996527298027db3fb8ed3e6469a6391aaabf61069b';
$expected_gf_version = getenv('SRWF_GF_VERSION') ?: '3.1.1.1';

$failures = array();

function load_json_file(string $path, array &$failures): ?array
{
    if (!is_readable($path)) {
        $failures[] = "unreadable_json:$path";
        return null;
    }
    try {
        $decoded = json_decode((string) file_get_contents($path), true, 512, JSON_THROW_ON_ERROR);
    } catch (JsonException $exception) {
        $failures[] = 'invalid_json:' . $exception->getMessage();
        return null;
    }
    if (!is_array($decoded)) {
        $failures[] = "json_root_not_object_or_array:$path";
        return null;
    }
    return $decoded;
}

function scalar_equivalent(mixed $expected, mixed $actual, string $path): bool
{
    if ($expected === null || $actual === null) {
        return $expected === $actual;
    }
    if (is_bool($expected) || is_bool($actual)) {
        return (bool) $expected === (bool) $actual;
    }
    if (is_string($expected) && is_string($actual) && str_ends_with($path, '.description')) {
        $flags = ENT_QUOTES | ENT_HTML5;
        return html_entity_decode($expected, $flags, 'UTF-8') === html_entity_decode($actual, $flags, 'UTF-8');
    }
    if (is_scalar($expected) && is_scalar($actual)) {
        return (string) $expected === (string) $actual;
    }
    return $expected === $actual;
}

function compare_source_subset(mixed $expected, mixed $actual, string $path, array &$failures): void
{
    if (!is_array($expected)) {
        if (!scalar_equivalent($expected, $actual, $path)) {
            $failures[] = sprintf('value_mismatch:%s expected=%s actual=%s', $path, json_encode($expected), json_encode($actual));
        }
        return;
    }
    if (!is_array($actual)) {
        $failures[] = "type_mismatch:$path";
        return;
    }

    $expected_is_list = array_is_list($expected);
    if ($expected_is_list) {
        if (!array_is_list($actual) || count($expected) !== count($actual)) {
            $failures[] = sprintf('list_shape_mismatch:%s expected_count=%d actual_count=%d', $path, count($expected), count($actual));
            return;
        }
        foreach ($expected as $index => $value) {
            compare_source_subset($value, $actual[$index], $path . '[' . $index . ']', $failures);
        }
        return;
    }

    foreach ($expected as $key => $value) {
        if (!array_key_exists($key, $actual)) {
            $failures[] = "missing_key:$path.$key";
            continue;
        }
        compare_source_subset($value, $actual[$key], $path . '.' . $key, $failures);
    }
}

function failures_for_path(array $failures, string $path_prefix): array
{
    return array_values(array_filter(
        $failures,
        static fn(string $failure): bool => str_contains($failure, $path_prefix)
    ));
}

$source = load_json_file($source_path, $failures);
$readback = load_json_file($readback_path, $failures);
$source_sha = is_readable($source_path) ? hash_file('sha256', $source_path) : false;
if (!is_string($source_sha) || !hash_equals($expected_sha, $source_sha)) {
    $failures[] = 'source_sha256_mismatch';
}

$source_form = null;
if (is_array($source)) {
    $source_forms = $source;
    unset($source_forms['version']);
    $source_forms = array_values(array_filter($source_forms, 'is_array'));
    if (count($source_forms) !== 1) {
        $failures[] = 'source_must_contain_exactly_one_form';
    } else {
        $source_form = $source_forms[0];
    }
}

$actual_form = is_array($readback) ? ($readback['import']['form'] ?? null) : null;
if (!is_array($actual_form)) {
    $failures[] = 'runtime_form_readback_missing';
}

$expected_title = is_array($source_form) ? (string) ($source_form['title'] ?? '') : '';
$title_override = getenv('SRWF_LAB_EXPECT_TITLE_OVERRIDE');
if (is_string($title_override) && $title_override !== '') {
    $expected_title = $title_override;
}
$actual_title = is_array($readback) ? (string) ($readback['import']['title'] ?? '') : '';
if ($expected_title === '' || $actual_title !== $expected_title) {
    $failures[] = 'form_title_mismatch';
}

if (is_array($readback)) {
    if (($readback['import']['count'] ?? null) !== 1) {
        $failures[] = 'import_count_not_one';
    }
    if (($readback['import']['is_active'] ?? null) !== false) {
        $failures[] = 'imported_form_not_inactive';
    }
    if (($readback['runtime']['gravity_forms'] ?? '') !== $expected_gf_version) {
        $failures[] = 'gravity_forms_version_mismatch';
    }
    if (($readback['runtime']['gravity_forms_package_sha256'] ?? '') !== $expected_gf_sha) {
        $failures[] = 'gravity_forms_package_sha256_mismatch';
    }
    if (($readback['source']['sha256'] ?? '') !== $expected_sha) {
        $failures[] = 'readback_source_sha256_mismatch';
    }
}

$source_fields = is_array($source_form) && isset($source_form['fields']) && is_array($source_form['fields'])
    ? $source_form['fields']
    : array();
$actual_fields = is_array($actual_form) && isset($actual_form['fields']) && is_array($actual_form['fields'])
    ? $actual_form['fields']
    : array();

$field_failure_start = count($failures);
if (count($source_fields) === 0) {
    $failures[] = 'source_field_structure_empty';
}
if (count($source_fields) !== count($actual_fields)) {
    $failures[] = sprintf('field_count_mismatch expected=%d actual=%d', count($source_fields), count($actual_fields));
}

$actual_by_id = array();
foreach ($actual_fields as $field) {
    if (is_array($field) && array_key_exists('id', $field)) {
        $actual_by_id[(string) $field['id']] = $field;
    }
}

$field_inventory = array();
foreach ($source_fields as $source_field) {
    if (!is_array($source_field) || !array_key_exists('id', $source_field)) {
        $failures[] = 'source_field_without_id';
        continue;
    }
    $source_id = (string) $source_field['id'];
    if (!isset($actual_by_id[$source_id])) {
        $failures[] = 'missing_runtime_field_id:' . $source_id;
        continue;
    }
    $expected_field = $source_field;
    unset($expected_field['formId']);
    compare_source_subset($expected_field, $actual_by_id[$source_id], 'field[' . $source_id . ']', $failures);
    $field_inventory[] = array(
        'field_id' => $actual_by_id[$source_id]['id'] ?? null,
        'type' => $actual_by_id[$source_id]['type'] ?? null,
    );
}
$field_failures = array_slice($failures, $field_failure_start);

$form_setting_failure_start = count($failures);
if (is_array($source_form) && is_array($actual_form)) {
    $expected_settings = $source_form;
    // Only runtime identity/state properties and fields (verified separately above) are
    // outside form-setting equivalence. Source-defined notifications and confirmations
    // deliberately remain in this projection and therefore fail closed on drift.
    foreach (array('id', 'fields', 'is_active', 'date_created', 'version') as $runtime_owned_key) {
        unset($expected_settings[$runtime_owned_key]);
    }
    compare_source_subset($expected_settings, $actual_form, 'form', $failures);
}
$form_setting_failures = array_slice($failures, $form_setting_failure_start);
$confirmation_failures = failures_for_path($form_setting_failures, 'form.confirmations');
$notification_failures = failures_for_path($form_setting_failures, 'form.notifications');

$generated_form_id = is_array($readback) ? ($readback['import']['form_id'] ?? null) : null;
if (!is_int($generated_form_id) && !ctype_digit((string) $generated_form_id)) {
    $failures[] = 'generated_form_id_missing';
}

$status = empty($failures) ? 'LAB_PASS' : 'LAB_FAIL';
$evidence = array(
    'schema_version' => '1.0.0',
    'lab_status' => $status,
    'scenario' => 'GF_V060_IMPORT_READBACK',
    'source_artifact' => array(
        'name' => basename($source_path),
        'sha256' => is_string($source_sha) ? $source_sha : null,
        'expected_sha256' => $expected_sha,
    ),
    'runtime' => is_array($readback) ? ($readback['runtime'] ?? array()) : array(),
    'observed' => array(
        'form_created' => $generated_form_id !== null,
        'generated_form_id' => $generated_form_id,
        'title' => $actual_title,
        'inactive' => is_array($readback) ? ($readback['import']['is_active'] ?? null) : null,
        'field_count' => count($actual_fields),
        'generated_field_ids' => array_values(array_map(static fn(array $field): mixed => $field['field_id'], $field_inventory)),
        'field_inventory' => $field_inventory,
        'source_defined_form_settings_preserved' => empty($form_setting_failures),
        'source_defined_field_settings_preserved' => empty($field_failures),
        'source_defined_confirmations_preserved' => empty($confirmation_failures),
        'source_defined_notifications_preserved' => empty($notification_failures),
    ),
    'assertions' => array(
        'exact_scaffold_hash' => !in_array('source_sha256_mismatch', $failures, true),
        'single_form_import' => !in_array('import_count_not_one', $failures, true),
        'form_inactive' => !in_array('imported_form_not_inactive', $failures, true),
        'title_readback' => !in_array('form_title_mismatch', $failures, true),
        'field_structure_readback' => !array_filter($field_failures, static fn(string $failure): bool =>
            str_starts_with($failure, 'source_field_structure_empty')
            || str_starts_with($failure, 'field_count_mismatch')
            || str_starts_with($failure, 'source_field_without_id')
            || str_starts_with($failure, 'missing_runtime_field_id:')
        ),
        'source_defined_confirmations_readback' => empty($confirmation_failures),
        'source_defined_notifications_readback' => empty($notification_failures),
        'source_defined_settings_readback' => empty($field_failures) && empty($form_setting_failures),
    ),
    'failures' => $failures,
    'evidence_semantics' => array(
        'ci_form_field_ids_are_disposable' => true,
        'write_ids_to_implementation_mapping' => false,
        'staging_exercised' => false,
        'staging_pass' => false,
        'production_ready_claim' => false,
        'finance_manual_cheque_behavior' => 'NOT_TESTED_SUSPENDED',
        'synthetic_entry_data_created' => false,
        'runtime_owned_form_identity_state_excluded_from_source_setting_equivalence' => array(
            'id', 'is_active', 'date_created', 'version'
        ),
        'description_html_entities_compared_by_decoded_text' => true,
    ),
);

$encoded = json_encode($evidence, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE | JSON_THROW_ON_ERROR);
if (file_put_contents($evidence_path, $encoded . PHP_EOL) === false) {
    fwrite(STDERR, "Could not write evidence.\n");
    exit(2);
}

if ($status !== 'LAB_PASS') {
    fwrite(STDERR, "SRWF Runtime Lab assertion failure(s):\n- " . implode("\n- ", $failures) . "\n");
    exit(1);
}

printf("SRWF_RUNTIME_LAB LAB_PASS form_id=%s field_count=%d\n", (string) $generated_form_id, count($actual_fields));
