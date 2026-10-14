"""Run TPL-Bench on a local model and emit preds JSONL for src/evaluate.py.

Backends (all optional, stdlib-first):
  dummy          — no model, writes empty predictions (pipeline smoke test)
  hf             — HuggingFace transformers (pip install transformers torch --upgrade)
  ollama         — local Ollama server (stdlib urllib, no extra deps)
  openai-compat  — any OpenAI-compatible server: vLLM, LM Studio, Ollama, llama.cpp server

Examples (PowerShell):
  python src/run_local.py --gold data/dev/tpl_dev.jsonl --out preds_dummy.jsonl --backend dummy
  python src/run_local.py --gold data/dev/tpl_dev.jsonl --out preds_ollama.jsonl --backend ollama --model gemma3:4b
  python src/run_local.py --gold data/dev/tpl_dev.jsonl --out preds_hf.jsonl --backend hf --model google/gemma-2-2b-it --max-new-tokens 256
  python src/run_local.py --gold data/dev/tpl_dev.jsonl --out preds_vllm.jsonl --backend openai-compat --model google/gemma-2-2b-it --base-url http://localhost:8000/v1

Then score:
  python src/evaluate.py --gold data/dev/tpl_dev.jsonl --preds preds_ollama.jsonl
"""
import argparse
import json
import sys
import urllib.error
import urllib.request


def build_prompt(item: dict) -> str:
    passage = str(item.get("passage_ta", "") or "").strip()
    prompt = str(item.get("prompt_ta", "") or "").strip()
    track = item.get("track", "")
    choices = item.get("choices") if isinstance(item.get("choices"), list) else None

    if track == "grounded":
        base = ("அறிவுறுத்தல் — பதில் கொடுத்த பகுதிகளிலிருந்து மட்டும் தருக, "
                "மூலம் [பகுதி 1]/[பகுதி 2] காட்டி எழுதுக. "
                "பகுதிகளில் பதில் இல்லையெனில் எழுதுக: தகவல் இல்லை.\n")
        if passage:
            base += f"பகுதிகள்: {passage}\n"
        base += f"கேள்வி: {prompt}\n"
        if choices:
            base += "விருப்பங்கள்:\n" + "\n".join(f"{i+1}. {c}" for i, c in enumerate(choices)) + "\n"
        return base + "பதில்:"
    if choices:
        ch_txt = "\n".join(f"{i+1}. {c}" for i, c in enumerate(choices))
        base = "அறிவுறுத்தல் — சரியான பதில் மட்டும் எழுதுக, விளக்கம் தர வேண்டாம்.\n"
        if passage:
            base += f"பத்தி: {passage}\n"
        base += f"கேள்வி: {prompt}\nவிருப்பங்கள்:\n{ch_txt}\nபதில்:"
        return base
    if track == "ilakkanam":
        return ("அறிவுறுத்தல் — தவறான வாக்கியத்தை திருத்தி சரியான வாக்கியம் மட்டும் எழுதுக.\n"
                f"தவறு: {prompt}\nசரி:")
    if track == "surukkam":
        return ("அறிவுறுத்தல் — கீழே உள்ள பத்தியை சுருக்கி எழுதுக. "
                "பெயர், எண், உண்மை மாறக் கூடாது, புது செய்தி சேர்க்கக் கூடாது.\n"
                f"பத்தி: {passage or prompt}\nசுருக்கம்:")
    if track == "eluthu":
        return f"அறிவுறுத்தல்: {prompt}\nசொல் வரம்பை பின்பற்றுக. சரியான தெளிவான ஒழுங்கான தமிழில் எழுதுக.\n"
    base = "அறிவுறுத்தல் — சரியான பதில் மட்டும் எழுதுக, விளக்கம் தர வேண்டாம்.\n"
    if passage:
        base += f"பத்தி: {passage}\n"
    base += f"கேள்வி: {prompt}\nபதில்:"
    return base


def load_gold(path, limit=None):
    try:
        fh = open(path, encoding="utf-8")
    except FileNotFoundError:
        print(f"ERROR: gold file not found: {path}", file=sys.stderr)
        raise SystemExit(1)
    items = []
    with fh:
        for i, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"ERROR: gold line {i}: invalid JSON: {e}", file=sys.stderr)
                raise SystemExit(1)
    items.sort(key=lambda o: o.get("id", ""))
    if limit is None:
        return items
    if limit <= 0:
        return []
    return items[:limit]


def gen_hf(prompts, model, max_new_tokens=256, temperature=0.0):
    try:
        from transformers import pipeline
    except ImportError:
        print("ERROR: pip install transformers torch --upgrade", file=sys.stderr)
        raise SystemExit(1)
    do_sample = temperature > 0
    pipe = pipeline(
        "text-generation", model=model, trust_remote_code=True,
        do_sample=do_sample, temperature=temperature or None,
        max_new_tokens=max_new_tokens,
    )
    out = []
    for p in prompts:
        r = pipe(p, return_full_text=False)[0]["generated_text"]
        out.append(str(r).strip())
    return out


def ollama_generate(prompt: str, model: str, host="http://localhost:11434", options=None) -> str:
    host = (host or "").rstrip("/")
    body = json.dumps({
        "model": model, "prompt": prompt, "stream": False,
        "options": options or {},
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{host}/api/generate", data=body,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return str(json.loads(r.read().decode("utf-8")).get("response", "") or "").strip()
    except urllib.error.HTTPError as e:
        print(f"ERROR: Ollama HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}", file=sys.stderr)
        raise SystemExit(1)
    except urllib.error.URLError as e:
        print(f"ERROR: cannot reach Ollama at {host} ({e}). Is `ollama serve` running?", file=sys.stderr)
        raise SystemExit(1)
    except (ValueError, KeyError) as e:
        print(f"ERROR: bad Ollama response: {e}", file=sys.stderr)
        raise SystemExit(1)


def openai_compat_generate(prompt: str, model: str, base_url: str, api_key="sk-no-key", temperature=0.0, max_tokens=512) -> str:
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature, "max_tokens": max_tokens,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions", data=body,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"ERROR: server HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:300]}", file=sys.stderr)
        raise SystemExit(1)
    except urllib.error.URLError as e:
        print(f"ERROR: cannot reach server at {base_url} ({e})", file=sys.stderr)
        raise SystemExit(1)
    try:
        content = data["choices"][0]["message"].get("content") or ""
    except (KeyError, IndexError, AttributeError) as e:
        print(f"ERROR: unexpected server response shape: {e}; body={str(data)[:300]}", file=sys.stderr)
        raise SystemExit(1)
    return str(content).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--backend", default="dummy", choices=["dummy", "hf", "ollama", "openai-compat"])
    ap.add_argument("--model", default="")
    ap.add_argument("--base-url", default="http://localhost:8000/v1")
    ap.add_argument("--ollama-host", default="http://localhost:11434")
    ap.add_argument("--api-key", default="sk-no-key")
    ap.add_argument("--max-new-tokens", type=int, default=256)
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--limit", type=int, default=None, help="score first N items (quick smoke test)")
    args = ap.parse_args()

    items = load_gold(args.gold, args.limit)
    print(f"loaded {len(items)} items from {args.gold}", file=sys.stderr)

    if args.backend == "dummy":
        preds = ["" for _ in items]
    elif args.backend == "hf":
        if not args.model:
            print("ERROR: --model required for hf backend", file=sys.stderr)
            raise SystemExit(2)
        preds = gen_hf([build_prompt(it) for it in items], args.model,
                       args.max_new_tokens, args.temperature)
    elif args.backend == "ollama":
        if not args.model:
            print("ERROR: --model required, e.g. --model gemma3:4b", file=sys.stderr)
            raise SystemExit(2)
        preds = [ollama_generate(build_prompt(it), args.model, args.ollama_host,
                                 {"temperature": args.temperature,
                                  "num_predict": args.max_new_tokens}) for it in items]
    else:
        if not args.model:
            print("ERROR: --model required", file=sys.stderr)
            raise SystemExit(2)
        preds = [openai_compat_generate(build_prompt(it), args.model, args.base_url,
                                        args.api_key, args.temperature, args.max_new_tokens)
                 for it in items]

    with open(args.out, "w", encoding="utf-8") as f:
        for it, p in zip(items, preds):
            f.write(json.dumps({"id": it.get("id"), "prediction": p}, ensure_ascii=False) + "\n")
    print(f"wrote {args.out} ({len(items)} preds, backend={args.backend})")


if __name__ == "__main__":
    main()
