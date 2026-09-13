# Stack Notes

**Updated:** 2026-09-13 after scope reduction

| Need | Choice |
|---|---|
| Runtime | Python 3.13.3 available locally; existing `code/main.py` |
| Files and joins | Standard-library `csv`, `pathlib`, dictionaries |
| Financial arithmetic | `Decimal` parsed from strings |
| Dates | `datetime` and `calendar` |
| Agentic workflow and supplied evidence | One model client, bounded tool loop and validated evidence tools |
| Checks and packaging | Existing evaluation entry point, focused standard-library checks, `zipfile` |

No database, multi-agent framework, provider router, language-support layer, persistent extraction cache, or usage-ledger dependency. Choose and pin one model client when integrating it; do not install alternatives speculatively.

Primary references already checked: [CSV](https://docs.python.org/3/library/csv.html), [decimal](https://docs.python.org/3/library/decimal.html), [dates](https://docs.python.org/3/library/datetime.html). The existing research confirmed [vision](https://platform.claude.com/docs/en/build-with-claude/vision) and [structured extraction](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) as one provider option; no provider is mandated.
