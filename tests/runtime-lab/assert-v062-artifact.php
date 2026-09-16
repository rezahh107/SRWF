<?php

declare(strict_types=1);

if ($argc !== 2) {
    fwrite(STDERR, "Usage: php assert-v062-artifact.php <artifact.json>\n");
    exit(64);
}

$path = $argv[1];
if (!is_file($path)) {
    fwrite(STDERR, "Artifact not found: {$path}\n");
    exit(66);
}

$expectedSha = 'd371ece6587b956d693eed556b5d6d1aa6d0bb60e10c8d40c73f3750607d7ee8';
$expectedSize = 350906;
$expectedTitle = 'SRWF — ثبت‌نام دانش‌آموز [v0.6.2 PROVISIONAL — DO NOT PUBLISH]';
$expectedInventory = [
    1 => 'first_name', 2 => 'last_name', 3 => 'father_name', 4 => 'national_id',
    5 => 'dob_jalali', 6 => 'gender_code', 7 => 'student_mobile', 8 => 'home_phone',
    9 => 'contact1_mobile', 10 => 'contact2_mobile', 11 => 'contact1_relationship',
    12 => 'contact2_relationship', 13 => 'student_photo', 14 => 'education_level',
    15 => 'grade_group_selection', 16 => 'group_code', 17 => 'graduation_status',
    18 => 'registration_center_code', 19 => 'school_code', 20 => 'school_name_other',
    21 => 'school_name', 22 => 'report_card_file', 23 => 'finance_status',
    24 => 'hekmat_package', 25 => 'hekmat_tracking', 26 => 'bonyad_shahid_case_number',
    27 => 'bonyad_shahid_type_code', 28 => 'bonyad_shahid_type_name',
    29 => 'tuition_amount', 30 => 'discount_amount', 31 => 'discount_title',
    32 => 'net_payable_amount', 33 => 'discount_code', 34 => 'discount_name',
    35 => 'review_status', 36 => 'review_reason', 37 => 'registration_counter',
];
$financeReserved = [
    'finance_status', 'hekmat_package', 'hekmat_tracking', 'bonyad_shahid_case_number',
    'bonyad_shahid_type_code', 'bonyad_shahid_type_name', 'tuition_amount',
    'discount_amount', 'discount_title', 'net_payable_amount', 'discount_code', 'discount_name',
];

$failures = [];
$assert = static function (bool $condition, string $message) use (&$failures): void {
    if (!$condition) {
        $failures[] = $message;
    }
};

$raw = file_get_contents($path);
if ($raw === false) {
    fwrite(STDERR, "Unable to read artifact: {$path}\n");
    exit(74);
}
if (getenv('SRWF_V062_SKIP_BYTE_IDENTITY') !== '1') {
    $assert(strlen($raw) === $expectedSize, 'exact byte size mismatch');
    $assert(hash('sha256', $raw) === $expectedSha, 'exact SHA-256 mismatch');
}

try {
    $root = json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
} catch (JsonException $e) {
    fwrite(STDERR, 'Invalid JSON: ' . $e->getMessage() . "\n");
    exit(65);
}

$forms = array_filter($root, static fn($key): bool => $key !== 'version', ARRAY_FILTER_USE_KEY);
$assert(count($forms) === 1, 'artifact must contain exactly one form');
$form = reset($forms);
$assert(is_array($form), 'form payload missing');
if (!is_array($form)) {
    $form = [];
}
$assert(($form['title'] ?? null) === $expectedTitle, 'provisional form title mismatch');
$fields = $form['fields'] ?? [];
$assert(is_array($fields) && count($fields) === 37, 'field count must be exactly 37');

$byAdmin = [];
$seenIds = [];
foreach ($fields as $field) {
    if (!is_array($field)) {
        $failures[] = 'non-object field payload';
        continue;
    }
    $id = (int) ($field['id'] ?? 0);
    $admin = (string) ($field['adminLabel'] ?? '');
    if ($id > 0) {
        $seenIds[$id] = ($seenIds[$id] ?? 0) + 1;
    }
    if ($admin !== '') {
        $byAdmin[$admin] = $field;
    }
}
foreach ($expectedInventory as $id => $admin) {
    $assert(($seenIds[$id] ?? 0) === 1, "field id {$id} must occur exactly once");
    $assert(isset($byAdmin[$admin]), "missing adminLabel {$admin}");
    if (isset($byAdmin[$admin])) {
        $assert((int) ($byAdmin[$admin]['id'] ?? 0) === $id, "{$admin} id mismatch");
    }
}

$national = $byAdmin['national_id'] ?? [];
$assert(($national['type'] ?? null) === 'pgr_national_id', 'national_id must use current PersianGravity pgr_national_id');
$assert(($national['forceEnglish'] ?? null) === true, 'national_id forceEnglish must be true');
$assert((int) ($national['maxLength'] ?? 0) === 10, 'national_id maxLength must be 10');
$assert(($national['noDuplicates'] ?? null) === false, 'national_id duplicates must remain allowed');
$assert(($national['isRequired'] ?? null) === true, 'national_id must be required');
$assert(($national['visibility'] ?? null) === 'visible', 'national_id must be public-visible');
$assert(($national['type'] ?? null) !== 'ir_national_id', 'legacy ir_national_id is forbidden');

$dob = $byAdmin['dob_jalali'] ?? [];
$assert(($dob['type'] ?? null) === 'pgr_jalali_date', 'dob_jalali must use current PersianGravity pgr_jalali_date');
$assert(($dob['jalali_format'] ?? null) === 'ymd_slash', 'dob_jalali presentation format must be ymd_slash');
foreach (['check_jalali', 'dateType', 'dateFormat', 'dateFormatPlacement', 'calendarIconType', 'calendarIconUrl'] as $legacyKey) {
    $assert(!array_key_exists($legacyKey, $dob), "legacy dob property {$legacyKey} is forbidden");
}

$photo = $byAdmin['student_photo'] ?? [];
$assert(($photo['type'] ?? null) === 'fileupload', 'student_photo must remain fileupload');
$assert(($photo['isRequired'] ?? null) === true, 'student_photo must remain required');
$assert(($photo['allowedExtensions'] ?? null) === 'jpg,jpeg', 'student_photo extensions mismatch');
$assert((int) ($photo['maxFileSize'] ?? 0) === 5, 'student_photo max size must be 5 MB');
$assert(($photo['multipleFiles'] ?? null) === true, 'student_photo must use GF multi-file mode required by FUP');
$assert((string) ($photo['maxFiles'] ?? '') === '1', 'student_photo maxFiles must be 1');
foreach (['gpfupEnable', 'gpfupEnableCrop', 'gpfupCropRequired'] as $key) {
    $assert(($photo[$key] ?? null) === true, "student_photo {$key} must be true");
}
$assert((string) ($photo['gpfupAspectRatioAntecedent'] ?? '') === '3', 'student_photo crop antecedent must be 3');
$assert((string) ($photo['gpfupAspectRatioConsequent'] ?? '') === '4', 'student_photo crop consequent must be 4');
$assert((string) ($photo['gpfupMaxWidth'] ?? '') === '1200', 'student_photo max width must be 1200');
$assert((string) ($photo['gpfupMaxHeight'] ?? '') === '1600', 'student_photo max height must be 1600');
foreach (['gpfupMinWidth', 'gpfupMinHeight', 'gpfupExactWidth', 'gpfupExactHeight'] as $forbidden) {
    $assert(!array_key_exists($forbidden, $photo) || $photo[$forbidden] === '' || $photo[$forbidden] === null, "student_photo {$forbidden} must stay unset");
}

$groups = $byAdmin['grade_group_selection']['choices'] ?? [];
$assert(is_array($groups) && count($groups) === 33, 'grade group catalog must contain exactly 33 choices');
$dual = $byAdmin['graduation_status']['conditionalLogic']['rules'] ?? [];
$assert(is_array($dual) && count($dual) === 11, 'graduation dual-status matrix must contain exactly 11 rules');
$expectedDual = ['1','3','5','7','8','9','11','12','14','17','18'];
$observedDual = array_map(static fn(array $rule): string => (string) ($rule['value'] ?? ''), is_array($dual) ? $dual : []);
$assert($observedDual === $expectedDual, 'graduation dual-status codes mismatch');

$school = $byAdmin['school_code'] ?? [];
$schoolChoices = $school['choices'] ?? [];
$assert(($school['type'] ?? null) === 'select', 'school_code must remain select');
$assert(($school['isRequired'] ?? null) === true, 'school_code must remain required');
$assert(($school['gpadvsEnable'] ?? null) === true, 'school_code must enable GP Advanced Select');
$assert(($school['enableEnhancedUI'] ?? null) === false, 'school_code must keep GF Enhanced UI disabled');
$assert(is_array($schoolChoices) && count($schoolChoices) === 947, 'school catalog must contain 946 named choices + Other');
$other = array_values(array_filter(is_array($schoolChoices) ? $schoolChoices : [], static fn(array $choice): bool => (string) ($choice['value'] ?? '') === '0'));
$assert(count($other) === 1 && ($other[0]['text'] ?? null) === 'سایر / در فهرست نیست', 'school Other=0 choice mismatch');
$schoolValues = array_map(static fn(array $choice): string => (string) ($choice['value'] ?? ''), is_array($schoolChoices) ? $schoolChoices : []);
foreach (['1296','1314','1316','1319'] as $excluded) {
    $assert(!in_array($excluded, $schoolValues, true), "excluded school {$excluded} must not be present");
}

$report = $byAdmin['report_card_file'] ?? [];
$assert(($report['allowedExtensions'] ?? null) === 'jpg,jpeg,pdf', 'report_card_file extensions mismatch');
$assert((int) ($report['maxFileSize'] ?? 0) === 5, 'report_card_file max size must be 5 MB');
$assert(($report['isRequired'] ?? null) === false, 'report_card_file must remain conditionally required, not globally required');
$assert((string) ($report['maxFiles'] ?? '') === '1', 'report_card_file maxFiles must be 1');

foreach ($financeReserved as $admin) {
    $field = $byAdmin[$admin] ?? [];
    $assert(($field['visibility'] ?? null) !== 'visible', "reserved finance field {$admin} must not become public-visible");
    $assert(($field['isRequired'] ?? null) === false, "reserved finance field {$admin} must remain optional while finance implementation is suspended");
}

$assert(($byAdmin['review_status']['visibility'] ?? null) === 'administrative', 'review_status must remain administrative');
$assert(($byAdmin['review_reason']['visibility'] ?? null) === 'administrative', 'review_reason must remain administrative');
$assert(($byAdmin['registration_counter']['visibility'] ?? null) === 'administrative', 'registration_counter must remain administrative');
$assert(($byAdmin['registration_counter']['isRequired'] ?? null) === false, 'registration_counter must remain optional');

if ($failures !== []) {
    foreach ($failures as $failure) {
        fwrite(STDERR, "FAIL: {$failure}\n");
    }
    exit(1);
}

printf(
    "V062_ARTIFACT_CONTRACT_PASS sha256=%s size=%d fields=37 groups=33 schools=947\n",
    $expectedSha,
    $expectedSize
);
