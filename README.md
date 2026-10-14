# TPL-Bench — Tamil Reading-Writing Bench

**Tamil reading + writing comprehension for AI models.**

MIT-licensed, open, Tamil-first for scored content (prompts, passages,
answers). Sister bench to [HPL-Bench](https://github.com/apoorvsingh090/hpl-bench)
(Hindi) and [SPL-Bench](https://github.com/apoorvsingh090/sanskrit-bench)
(Sanskrit) — same harness design, rebuilt for Tamil: வேற்றுமை (cases),
verb agreement, tense, ன/ண/ந spelling, செந்தமிழ்/பேச்சு registers, Tanglish,
Roman→Tamil script.
(Meta-docs — schema notes, judge settings, explanations — may use English.)

TPL-Bench tests whether a model can **read Tamil stories/articles and write
correct Tamil** — from primary `A1` to advanced `C1`.

## Tracks (v0.1 seed: 50 items, target: 3000)

| track | what it tests | scoring |
|---|---|---|
| `vasippu` | story/article comprehension (seed: short passages; target 150–800 words) | MCQ accuracy + short-answer F1 |
| `anumanam` | NLI, coref (அவள்), pazhamozhi, niti | accuracy |
| `ilakkanam` | cases, number/tense/person agreement, ன/ண/ந spelling (seed: 1 exemplar each; target: paradigms) | exact + token-F1 |
| `surukkam` | summarization, no hallucination (seed passages distinct from vasippu) | LLM-judge + token-F1 informative |
| `eluthu` | katturai, kaditham, uraiyadal, arivippu (60–200 words) | rubric 1–5 LLM-judge + human audit |
| `nadai` | senthamizh/pechchu, dialects, Tanglish, Roman→Tamil (classical: zero in seed, target) | accuracy + style-appropriateness |
| `grounded` | 2-snippet toys in seed (target: multi-doc), cite `[பகுதி 1]`, abstain `தகவல் இல்லை` / deny with citation | accuracy + abstention rate; long-form via judge |

Levels in seed v0.1.0: `A1:6 / A2:4 / B1:18 / B2:16 / C1:6`. Target adds classical/sangam C1 + long-doc.

## Quickstart

```powershell
# validate schema
python src/validate.py --data data/dev/tpl_dev.jsonl

# score your model (preds: {"id":..., "prediction":...} per line)
python src/evaluate.py --gold data/dev/tpl_dev.jsonl --preds examples/sample_preds.jsonl
```

## Run it without a local GPU (Hugging Face cloud)

```powershell
# https://huggingface.co/join → https://huggingface.co/settings/tokens
$env:HF_TOKEN = "hf_..."

python src/run_hf_api.py --gold data/dev/tpl_dev.jsonl --out preds.jsonl --model google/gemma-2-2b-it --limit 5
python src/run_hf_api.py --gold data/dev/tpl_dev.jsonl --out preds.jsonl --model google/gemma-2-2b-it
python src/evaluate.py --gold data/dev/tpl_dev.jsonl --preds preds.jsonl
```

Or locally via Ollama / transformers / vLLM — see `src/run_local.py --help`.
Free-tier note: HF free accounts get ~$0.10/month Inference Providers credit —
enough for the 50-item seed on small models; then pay-as-you-go.

Prompts are fixed Tamil templates — see `examples/prompts_ta.md`.
Contributing: `CONTRIBUTING.md`. Hidden test: `data/README.md`.

## Repo layout

```
tamil-bench/
  LICENSE  MIT
  README.md
  CITATION.cff
  CONTRIBUTING.md
  requirements.txt
  .gitignore
  schema/tpl_schema.json
  data/dev/tpl_dev.jsonl        # public dev (50 seed v0.1.0)
  data/canary.txt               # contamination canary, keep out of training
  data/README.md
  data/test_hidden/             # git-ignored, leaderboard only
  src/validate.py               # stdlib schema check
  src/evaluate.py               # stdlib scorer (auto part + aggregates)
  src/run_local.py              # run Ollama / HF-transformers / vLLM locally
  src/run_hf_api.py             # run on HF Inference Providers (no local GPU)
  examples/prompts_ta.md
  examples/judge_rubric_ta.md   # LLM-judge spec + bias controls
  examples/sample_preds.jsonl
```

## Scoring policy

* Auto (deterministic): MCQ/ilakkanam accuracy (exact match). Short-answer token-F1 informative only.
* Judge (semantic): `surukkam/eluthu/grounded-long` use `examples/judge_rubric_ta.md`
  with LLM-judge + 5% human audit (10% for C1/eluthu suggested).
* Report per-track + `VASIPPU` (vasippu+anumanam+grounded) vs `ELUTHU`
  (ilakkanam+surukkam+eluthu) + `NADAI` robustness.
* `dev-public / test-hidden` (target 30/70). Canary in `data/canary.txt`.

## Limitations (seed)

* Passages are short toys (≤60 words), not 150–800; classical/sangam coverage zero.
* n=50 → per-track CIs ±15–30%. Don't leaderboard on seed alone.
* Seed Tamil kept to standard written register; dialectal/pechchu depth is future work.

## License

MIT — see `LICENSE`. Data seeds are original examples (`seed:v0.1.0`).
If you contribute textbook-derived items, note source + license in `source`.
