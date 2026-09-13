"""Deterministic, request-scoped financial tools for Buy or Wait?."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

ZERO = Decimal("0")


def money(value: str | Decimal | None) -> Decimal | None:
    """Parse finite money; blank values deliberately remain unresolved."""
    if value is None or str(value).strip() == "":
        return None
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"invalid money: {value!r}") from exc
    if not result.is_finite():
        raise ValueError(f"non-finite money: {value!r}")
    return result


def as_date(value: str | date) -> date:
    return value if isinstance(value, date) else date.fromisoformat(value)


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_dataset(root: str | Path = "dataset") -> dict[str, list[dict[str, str]]]:
    """Load supplied participant CSVs only; callers never mutate these rows."""
    root = Path(root)
    names = (
        "financial_profiles", "financial_events", "exchange_rates", "requests",
        "sample_requests", "request_payment_options", "messages", "images",
    )
    return {name: _rows(root / f"{name}.csv") for name in names}


def _request(dataset: dict, request_id: str, request: dict | None = None) -> dict:
    source = request or next((r for r in dataset["requests"] if r["request_id"] == request_id), None)
    if not source or source.get("request_id") != request_id:
        raise ValueError("unknown or unauthorized request")
    required = ("user_id", "request_date", "requested_amount")
    if any(not source.get(key) for key in required):
        raise ValueError("request lacks required fields")
    money(source["requested_amount"])
    return {key: value for key, value in source.items() if key not in {
        "amount_safe_to_pay", "affordability_status", "recommended_payment_method",
        "payment_plan", "earliest_date_for_full_payment", "spending_changes_needed",
        "decision_explanation",
    }}


def build_request_context(dataset: dict, request_id: str, request: dict | None = None) -> dict:
    request = _request(dataset, request_id, request)
    profile = next((p for p in dataset["financial_profiles"] if p["user_id"] == request["user_id"]), None)
    if not profile:
        raise ValueError("request user has no profile")
    balance, floor = money(profile["current_available_balance"]), money(profile["minimum_balance_to_keep"])
    if balance is None or floor is None or balance < ZERO or floor < ZERO:
        raise ValueError("invalid profile balance or floor")
    user_id, request_day = request["user_id"], as_date(request["request_date"])
    return {
        "request": request, "profile": dict(profile), "user_id": user_id,
        "request_date": request_day, "home_currency": profile["home_currency"],
        "balance": balance, "floor": floor, "requested_amount": money(request["requested_amount"]),
        "events": [dict(e) for e in dataset["financial_events"] if e["user_id"] == user_id],
        "rates": [dict(rate) for rate in dataset["exchange_rates"]],
        "unresolved_evidence": [],
    }


def _converted_amount(event: dict, context: dict) -> Decimal | None:
    amount = money(event.get("amount"))
    if amount is None:
        return None
    if event["currency"] == context["home_currency"]:
        return amount
    settle = event.get("settlement_date") or event.get("event_date")
    rate = next((r for r in context["rates"] if r["rate_date"] == settle and r["from_currency"] == event["currency"] and r["to_currency"] == context["home_currency"]), None)
    if not rate:
        raise ValueError(f"missing FX for {event['event_id']}")
    return amount * money(rate["rate"])


def reconstruct_cash_state(context: dict) -> dict:
    """Normalize known future cash, while treating the profile as today's snapshot."""
    day = context["request_date"]
    flows, unresolved, pending_reserve = [], [], ZERO
    linked = {e["linked_event_id"] for e in context["events"] if e.get("linked_event_id")}
    for event in context["events"]:
        status = event.get("status", "").lower()
        if status in {"failed", "cancelled", "unrealized"}:
            continue
        try:
            amount = _converted_amount(event, context)
        except ValueError:
            unresolved.append(event["event_id"])
            continue
        if amount is None:
            unresolved.append(event["event_id"])
            continue
        settlement = as_date(event.get("settlement_date") or event["event_date"])
        direction = event["direction"]
        # A cancelled authorization with a separately settled replacement is not cash twice.
        if event["event_id"] in linked and status == "cancelled":
            continue
        if status == "pending":
            if direction == "debit":
                pending_reserve += amount
            continue
        if settlement <= day:
            continue  # Current profile already contains settled snapshot history.
        if status not in {"settled", "scheduled", "confirmed"}:
            continue
        if direction == "credit" and event.get("event_type") in {"bonus", "refund", "investment_gain"} and status != "settled":
            continue
        flows.append({"source_id": event["event_id"], "date": settlement, "amount": amount,
                      "direction": direction, "category": event.get("category", ""), "synthetic": False})
    context = dict(context)
    context["flows"] = flows
    context["pending_reserve"] = pending_reserve
    context["unresolved_evidence"] = sorted(set(unresolved))
    return context


def _json(value):
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, date):
        return value.isoformat()
    raise TypeError(type(value).__name__)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request-id", required=True)
    parser.add_argument("--baseline", action="store_true")
    parser.add_argument("--structured-only", action="store_true")
    args = parser.parse_args()
    context = reconstruct_cash_state(build_request_context(load_dataset(), args.request_id))
    result = {"request_id": args.request_id, "analysis_error": bool(context["unresolved_evidence"]),
              "unresolved_evidence": context["unresolved_evidence"], "flow_count": len(context["flows"])}
    print(json.dumps(result, default=_json, sort_keys=True))


if __name__ == "__main__":
    main()
