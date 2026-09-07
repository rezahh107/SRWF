# Installation and Boot

## Preferred mode — repository connected

1. Add/upload this ZIP to the ChatGPT Project knowledge area if a portable snapshot is useful.
2. Connect/enable access to GitHub repository `rezahh107/SRWF` when available.
3. Use `02_PROJECT_INSTRUCTIONS.md` as Project Instructions.
4. On a new session, say `ادامه`.
5. The agent must read live `main` state before recommending the next implementation action.

In this mode the ZIP is reference/cache only; repository `main` is authoritative for current project/runtime state.

## Offline/fallback mode — repository temporarily unavailable

1. Read `02_PROJECT_INSTRUCTIONS.md`.
2. Read `01_PACKAGE_MANIFEST.json` to identify build commit/state.
3. Read `PROJECT_SOURCES/24_CURRENT_STATE.yaml` and `25_DECISION_HISTORY.jsonl`.
4. Continue only from the packaged snapshot and clearly mark it as build-time state.
5. Do not claim persistence of new material decisions/results; use `STATE_NOT_PERSISTED` until repository access returns.

## Updating the package

Do not manually edit an old ZIP. Build the next version from the accepted repository using `scripts/build_project_bundle.py` / the project-bundle GitHub Actions workflow. Package versioning belongs in `bundle/VERSION`; live project state remains in `runtime/`.
