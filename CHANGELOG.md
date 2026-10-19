# Changelog

All notable changes to TPL-Bench will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Git tags `v0.1.0` / `v0.1.1` mark the releases below.

## [Unreleased]

### Added

- GitHub Actions CI: schema validation + sample-pred scoring smoke test (stdlib)
- CodeQL code scanning (Python)
- Community files: `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md`
- Issue forms (bug report, feature request) and pull request template
- `dependabot.yml` (weekly grouped GitHub Actions updates)

## [0.1.1] - 2026-10-14

### Fixed

- v0.1.1 audit fixes: distinct grounded stories, Tamil nits, out artifact,
  honest nadai row

## [0.1.0] - 2026-10-14

### Added

- Initial TPL-Bench: Tamil Reading-Writing Bench, 50 seed dev items
- Tracks: vasippu, anumanam, ilakkanam, surukkam, eluthu, nadai, grounded
- Stdlib validator (`src/validate.py`) and scorer (`src/evaluate.py`)
- Local runner (`src/run_local.py`: Ollama / HF-transformers / vLLM) and
  HF Inference Providers runner (`src/run_hf_api.py`)
- Schema (`schema/tpl_schema.json`), judge rubric, prompts, sample preds,
  contamination canary, CITATION.cff, MIT license
