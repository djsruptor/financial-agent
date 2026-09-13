# Buy or Wait?

Run offline checks without a model call:

```sh
python3 evaluation/main.py --checks agent
python3 evaluation/main.py --checks phase1
python3 evaluation/main.py --samples request_01,request_02,request_03 --live
```

The live runner uses the official Python `openai` SDK with `gpt-4.1-2025-04-14` and reads `OPENAI_API_KEY` from the environment. Install with `python3 -m pip install -r requirements.txt`; never put the key in a file or log. The model can select only `inspect_records`, `resolve_evidence`, `forecast_baseline`, and `finish`; host code validates evidence and computes every financial amount. Live output reports actual response token totals and exits as `credential_blocked` when no key is configured.
