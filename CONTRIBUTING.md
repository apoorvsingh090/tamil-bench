# Contributing to TPL-Bench

TPL-Bench measures Tamil **reading (வாசிப்பு)** and **writing (எழுத்து)**.

## What we accept

* Correct written Tamil items (செந்தமிழ், no raw MT). Sources (NCERT Tamil
  textbooks, public tales) must be noted in `source` with license.
* One item = one JSON line matching `schema/tpl_schema.json`.
* Every item needs: `id`, `track`, `level`, `prompt_ta`, `answer` or `rubric`, `source`.
* Keep seed Tamil in standard written register; mark spoken/dialect items
  `nadai` track explicitly.

## Levels

* `A1/A2` — primary literacy, simple sentences
* `B1/B2` — secondary (NCERT Tamil 8-12)
* `C1` — advanced (essay, classical touch, multi-doc reasoning)

## Tracks

| track | meaning |
|---|---|
| `vasippu` | passage comprehension (கதை, கட்டுரை) |
| `anumanam` | inference, NLI, coref (அவள்/அவர்கள்), pazhamozhi |
| `ilakkanam` | cases (வேற்றுமை), number, tense, person agreement, ன/ண/ந spelling |
| `surukkam` | summarization with grounding |
| `eluthu` | katturai, kaditham, uraiyadal, arivippu (rubric-scored) |
| `nadai` | senthamizh/pechchu, dialects, Tanglish, Roman→Tamil script |
| `grounded` | multi-doc QA with citation, anti-hallucination |

## Quality bar

1. `python src/validate.py --data data/dev/tpl_dev.jsonl` must pass.
2. No duplicate prompts. MCQ distractors plausible, single correct answer.
3. Writing prompts must include a 1-5 rubric (`sari, thelivu, amaippu, porutham`).
4. Every case/tense/agreement answer double-checked (verb agrees with subject
   in Tamil; mixed-gender coordination takes masculine plural).

```powershell
python src/validate.py --data data/dev/tpl_dev.jsonl
python src/evaluate.py --gold data/dev/tpl_dev.jsonl --preds examples/sample_preds.jsonl
```

Hidden test (`data/test_hidden/`) is maintained by maintainers only.

## Pull requests

- **Branch naming:** `feature/<short-description>` or `fix/<short-description>`
  from `master`.
- **Commit messages:** conventional style already used in this repo
  (`feat:` / `fix:` / `docs:`, one logical change per commit).
- **Before opening a PR:** run the quality-bar commands above; CI runs the
  same validator + scorer smoke test on every push and pull request.
- **Item PRs:** keep the diff to one track or one fix theme; reviewers check
  language accuracy, provenance, and schema match. Hidden-test items are
  maintained by maintainers only — never open PRs containing them.
- **Scorer/validator changes:** include a note in the PR describing the
  scoring behaviour before vs after.

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).
