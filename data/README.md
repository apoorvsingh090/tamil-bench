# `data/` layout

* `data/dev/tpl_dev.jsonl` — public dev set (v0.1: 50 seed items).
* `data/canary.txt` — contamination canary, keep out of training.
* `data/test_hidden/` — **not in git** (see `.gitignore`). Reserved for hidden test.

Each line is one item, UTF-8, `\n`-terminated JSON matching `schema/tpl_schema.json`.
