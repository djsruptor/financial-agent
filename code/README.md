# Buy or Wait?

Run offline checks without a model call:

```sh
python3 evaluation/main.py --checks agent
```

The live runner uses the official Python `openai` SDK with `gpt-4.1-2025-04-14` and reads `OPENAI_API_KEY` from the environment. Install with `python3 -m pip install -r requirements.txt`; never put the key in a file or log. The model can select only `inspect_records`, `resolve_evidence`, `forecast_baseline`, and `finish`; host code validates evidence and computes every financial amount.
