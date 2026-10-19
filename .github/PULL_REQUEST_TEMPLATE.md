## What does this PR change?

<!-- New items, scorer/validator fix, docs, runner, etc. -->

Related issue: fixes #

## Checklist

- [ ] `python src/validate.py --data data/dev/tpl_dev.jsonl` passes
- [ ] `python src/evaluate.py --gold data/dev/tpl_dev.jsonl --preds examples/sample_preds.jsonl` passes
      (only needed if `src/` or scoring changed)
- [ ] New items match `schema/tpl_schema.json`; no duplicate prompts; single
      correct MCQ answer with plausible distractors
- [ ] Item sources noted in `source` with license (original or textbook-derived)
- [ ] No hidden-test items (`data/test_hidden/`) or canary leakage
- [ ] Tamil follows standard written register, or is explicitly tagged `nadai`
