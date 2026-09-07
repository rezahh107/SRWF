---
document_id: SRWF-OWNER-COMPREHENSION-PROTOCOL
title: "SRWF Owner Comprehension Protocol"
version: 1.0.1
status: SUPPORTING_COMMUNICATION_PROTOCOL
language: fa-IR
applies_to: SRWF owner-facing explanations and implementation guidance
source_model: adaptive_owner_comprehension
---

# SRWF Owner Comprehension Protocol

## 1. Purpose

هدف این سند این است که وضعیت‌ها، مشکلات، تصمیم‌ها و Gateهای فنی SRWF برای Owner به شکلی توضیح داده شوند که **درک درست و تصمیم درست** را آسان کند؛ بدون اینکه دقت فنی، blocker، ریسک، عدم‌قطعیت یا evidence gap پنهان شود.

این پروتکل از الگوی `adaptive_owner_comprehension` اقتباس شده است: توضیح مستقیم و ساده در اولویت است و mental model / analogy / contrast / concrete scenario فقط وقتی استفاده می‌شود که واقعاً فهم موضوع را بهتر کند.

## 2. Authority boundary

این سند فقط نحوه‌ی **توضیح و ارائه‌ی وضعیت/تصمیم به Owner** را تنظیم می‌کند.

- هیچ business semantic، معماری، Gate، Lock یا Decision در SRWF را تغییر نمی‌دهد.
- `docs/authority/MASTER.md` همچنان authority معماری و تصمیم‌های `D-01..D-17` است.
- `docs/operations/EXECUTION_PLAYBOOK.md` همچنان ترتیب اجرایی و Gateها را تعیین می‌کند.
- این سند حق ندارد یک `NOT_PROVEN` را ساده‌سازی کرده و به `CONFIRMED` تبدیل کند یا blocker/uncertainty را حذف کند.
- اختلاف فنی مستقیم با Lockهای پروژه همچنان طبق قاعده‌ی `CONTRADICTION → STOP → OWNER RE-ADJUDICATION` مدیریت می‌شود.

## 3. Core invariant

`COMPREHENSION != ANALOGY`

تصویرسازی ذهنی هدف نیست؛ **فهم درست هدف است**.

بنابراین:

1. اگر توضیح مستقیم و ساده کافی است، همان را استفاده کن.
2. اگر مفهوم هنوز انتزاعی، چندلایه یا مستعد سوءبرداشت است، یک mental model، analogy، contrast یا concrete scenario اضافه کن.
3. اگر یک تصویر ذهنی قبلی هنوز مفید است، فقط بخش مرتبط آن را طبیعی ادامه بده.
4. اگر دیگر مفید نیست، آن را بدون نگرانی از یکدستی قالب کنار بگذار.
5. هیچ analogy را فقط برای زیبایی، تکرار یا حفظ یک قالب ثابت بازسازی نکن.

## 4. Owner-facing explanation sequence

### Step A — Simple meaning first
اول معنای انسانی و عملی وضعیت را بگو؛ سپس فقط در صورت نیاز شناسه یا اصطلاح فنی را اضافه کن.

### Step B — Find the dangerous misunderstanding
سوءبرداشتی را که تصمیم بعدی Owner را عوض می‌کند روشن کن. نمونه‌های SRWF:

- `SELECTED` با `IMPLEMENTED` یکی نیست.
- `DOCUMENTED` با `OBSERVED_IN_STAGING` یکی نیست.
- `NOT_PROVEN` به معنی `PROVEN_ABSENT` نیست.
- آماده بودن scaffold به معنی موفق بودن import نیست.
- PASS شدن یک candidate فقط همان requirement را می‌بندد؛ شکست آن معماری را خودکار باز نمی‌کند.

### Step C — Add a mental model only if useful
اگر توضیح مستقیم کافی نیست، یک mental model کوتاه و غیرمتناقض اضافه کن؛ اگر دیگر مفید نیست کنار بگذار.

### Step D — Deepen only decision-critical consequences
فقط تفاوت‌ها، پیامدها، ریسک‌ها یا irreversibilityهای تصمیم‌ساز را عمیق کن. گزینه‌ی بسته‌شده را دوباره به‌عنوان انتخاب مطرح نکن.

### Step E — Preserve evidence truth
ساده‌سازی هرگز blocker واقعی، `NOT_PROVEN`، evidence gap، risk، dependency/Gate یا نتیجهٔ واقعی PASS/FAIL را حذف نکند.

### Step F — End with the smallest next action
پاسخ اجرایی با کوچک‌ترین اقدام بعدی واقعی تمام شود؛ نه roadmap طولانی.

## 5. Technical-to-owner translation patterns

| Technical state | Owner-facing meaning |
|---|---|
| `SELECTED` | راه انتخاب شده است، ولی موفقیت اجرایی هنوز از این واژه نتیجه نمی‌شود. |
| `NOT_PROVEN` | هنوز evidence یا تست واقعی کافی نداریم. |
| `UNEXECUTED` | این تست هنوز اجرا نشده است. |
| `PASS` | معیار مشاهده‌پذیر همان probe در محیط هدف پاس شده است. |
| `FAIL` | همان candidate/probe معیار لازم را پاس نکرده؛ نتیجه را به کل معماری تعمیم نده. |
| `BLOCKER` | این مورد جلوی ادامه‌ی همان مسیر/مرحله‌ی وابسته را می‌گیرد. |
| `DEFERRED` | عمداً برای بعد گذاشته شده و الان شرط ادامه‌ی مسیر جاری نیست. |
| `CONTRADICTION` | evidence مستقیم با یک Lock تعارض دارد؛ ادامه‌ی همان تصمیم باید متوقف و به Owner ارجاع شود. |

## 6. Mental-model selection guidance

- Building/construction: Stage، prerequisite، scaffold، Gate.
- Assembly line/پرونده در مسیر: Gravity Flow workflow/assignment/Approval.
- Single source of truth/دفتر اصلی: data authority در برابر workflow authority.
- Key and lock: permission/capability/access control، فقط وقتی مفید است.
- Map vs actual terrain: documentation/design در برابر runtime validation.

## 7. SRWF examples

### Runtime inventory
`current_gate = STAGE_0_ENVIRONMENT_INVENTORY`: «قبل از ساخت باید نسخه‌ها و ابزارهای واقعی سایت را بدانیم؛ تا آن زمان compatibility کامل اثبات نشده است.»

### Scaffold import
`GF_IMPORT_SCAFFOLD_V0.4_GFNATIVEFORMAT = NOT_PROVEN`: «فایل فرم آمادهٔ امتحان است ولی پذیرش بدون خطا در سایت واقعی هنوز ثابت نشده.»

### V-01
`V-01 = UNEXECUTED`: «مسیر Inbox → Entry Details → edit → Approve انتخاب شده، ولی هنوز end-to-end در staging اجرا نشده.»

## 8. Anti-patterns

- شروع با انبوه ID/Gate بدون معنای انسانی؛
- analogy اجباری در هر پاسخ؛
- analogy به‌عنوان architecture claim؛
- حذف uncertainty برای ساده‌تر شدن؛
- roadmap طولانی وقتی فقط یک next action لازم است؛
- بازکردن تصمیم قفل‌شده صرفاً برای comparison؛
- technical detail بی‌اثر بر تصمیم/اقدام.

## 9. Response quality check

1. معنای ساده اول روشن است؟
2. مهم‌ترین سوءبرداشت برطرف شده؟
3. mental model واقعاً مفید است؟
4. blocker/risk/uncertainty/evidence gap دست‌نخورده مانده؟
5. فقط گزینه‌های واقعاً باز مقایسه شده‌اند؟
6. اقدام بعدی کوچک و قابل اجراست؟

## 10. Provenance

این پروتکل از الگوی `adaptive_owner_comprehension` در `LLM_Project_Orchestrator_GPT_Project_Package_v1.0.0-alpha13` اقتباس شده است. این provenance فقط منشأ الگوی ارتباطی را ثبت می‌کند و به پکیج مبدأ هیچ authority در business semantics یا معماری SRWF نمی‌دهد.

## 11. Changelog

### v1.0.1 — 2026-09-06
- authority pointers به stable repository paths normalize شدند؛ semantics ارتباطی تغییر نکرد.
