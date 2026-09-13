"""Deterministic, request-scoped financial tools for Buy or Wait?."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import date, timedelta
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


def _month_after(day: date) -> date:
    month = day.month + 1
    year = day.year + (month == 13)
    month = 1 if month == 13 else month
    import calendar
    return date(year, month, min(day.day, calendar.monthrange(year, month)[1]))


def _recurs_monthly(events: list[dict], start: date, end: date) -> list[dict]:
    """Project only three-observation monthly obligations, preserving source IDs."""
    grouped: dict[tuple, list[dict]] = {}
    for event in events:
        if event.get("status") != "settled" or event.get("direction") not in {"debit", "credit"}:
            continue
        try:
            settled, amount = as_date(event.get("settlement_date") or event["event_date"]), money(event.get("amount"))
        except (ValueError, KeyError):
            continue
        if amount is None or settled >= start or settled < start - timedelta(days=180):
            continue
        key = (event.get("description", "").strip().lower(), event.get("category", ""), event.get("currency", ""), event["direction"])
        grouped.setdefault(key, []).append(event)
    result = []
    for records in grouped.values():
        records.sort(key=lambda row: as_date(row.get("settlement_date") or row["event_date"]))
        if len(records) < 3:
            continue
        last_three = records[-3:]
        dates = [as_date(row.get("settlement_date") or row["event_date"]) for row in last_three]
        if len({(d.year, d.month) for d in dates}) != 3:
            continue
        # Same calendar day or month-end supports a monthly inference.
        import calendar
        anchors = [d.day == calendar.monthrange(d.year, d.month)[1] for d in dates]
        if not (len({d.day for d in dates}) == 1 or all(anchors)):
            continue
        sample = last_three[-1]
        amount = money(sample["amount"])
        if amount is None:
            continue
        next_day = _month_after(dates[-1])
        while next_day <= end:
            result.append({"source_id": sample["event_id"], "date": next_day, "amount": amount,
                           "direction": sample["direction"], "category": sample.get("category", ""), "synthetic": True})
            next_day = _month_after(next_day)
    return result


def _recurs_interval(events: list[dict], start: date, end: date) -> list[dict]:
    """Project only a stable 7/14/21-day debit cadence using its conservative amount."""
    grouped: dict[tuple, list[dict]] = {}
    for event in events:
        if event.get("status") != "settled" or event.get("direction") != "debit":
            continue
        try:
            settled, amount = as_date(event.get("settlement_date") or event["event_date"]), money(event.get("amount"))
        except (ValueError, KeyError):
            continue
        if amount is None or settled >= start or settled < start - timedelta(days=180):
            continue
        # Description changes are expected for variable essentials; category is stable evidence.
        grouped.setdefault((event.get("category", ""), event.get("currency", "")), []).append(event)
    result = []
    for records in grouped.values():
        records.sort(key=lambda row: as_date(row.get("settlement_date") or row["event_date"]))
        if len(records) < 3:
            continue
        recent = records[-3:]
        days = [as_date(row.get("settlement_date") or row["event_date"]) for row in recent]
        gap = (days[-1] - days[-2]).days
        if gap not in {7, 14, 21} or (days[-2] - days[-3]).days != gap:
            continue
        amounts = [money(row["amount"]) for row in recent]
        if any(value is None for value in amounts):
            continue
        next_day = days[-1] + timedelta(days=gap)
        while next_day <= end:
            result.append({"source_id": recent[-1]["event_id"], "date": next_day, "amount": max(amounts),
                           "direction": "debit", "category": recent[-1].get("category", ""), "synthetic": True})
            next_day += timedelta(days=gap)
    return result


def project_flows(context: dict) -> list[dict]:
    """Combine explicit normalized cash with supported, non-duplicated recurrences."""
    start, end = context["request_date"], context["request_date"] + timedelta(days=89)
    explicit = list(context.get("flows", []))
    used = {(flow["date"], flow["category"], flow["direction"]) for flow in explicit}
    inferred = [flow for flow in _recurs_monthly(context["events"], start, end) + _recurs_interval(context["events"], start, end)
                if (flow["date"], flow["category"], flow["direction"]) not in used]
    return sorted(explicit + inferred, key=lambda flow: (flow["date"], flow["direction"] != "debit", flow["source_id"]))


def check_schedule(context: dict, payments: list[dict]) -> dict:
    """Single whole-horizon safety authority; debits, credits, then payments each date."""
    start, end = context["request_date"], context["request_date"] + timedelta(days=89)
    balance = context["balance"] - context.get("pending_reserve", ZERO)
    floor = context["floor"]
    if balance < floor:
        return {"safe": False, "balance_path": [{"date": start, "balance": balance}], "first_breach": start}
    due: dict[date, list[dict]] = {}
    for payment in payments:
        when, amount = as_date(payment["date"]), money(payment["amount"])
        if amount is None or amount < ZERO or not start <= when <= end:
            return {"safe": False, "balance_path": [], "first_breach": when if start <= when <= end else start}
        due.setdefault(when, []).append({"amount": amount, "source_id": payment.get("source_id", "payment")})
    flows = project_flows(context)
    path = [{"date": start, "balance": balance}]
    for offset in range(90):
        current = start + timedelta(days=offset)
        todays = [flow for flow in flows if flow["date"] == current]
        for direction in ("debit", "credit"):
            for flow in (item for item in todays if item["direction"] == direction):
                balance += -flow["amount"] if direction == "debit" else flow["amount"]
                path.append({"date": current, "balance": balance, "source_id": flow["source_id"]})
                if balance < floor:
                    return {"safe": False, "balance_path": path, "first_breach": current}
        for payment in due.get(current, []):
            balance -= payment["amount"]
            path.append({"date": current, "balance": balance, "source_id": payment["source_id"]})
            if balance < floor:
                return {"safe": False, "balance_path": path, "first_breach": current}
    return {"safe": True, "balance_path": path, "first_breach": None}


def forecast_baseline(context: dict) -> dict:
    context = reconstruct_cash_state(context) if "flows" not in context else context
    if context["unresolved_evidence"]:
        return {"status": "analysis_error", "baseline_feasible": None, "safe_amount": None,
                "earliest_date": None, "normalized_context": context}
    baseline = check_schedule(context, [])
    if not baseline["safe"]:
        return {"status": "ok", "baseline_feasible": False, "safe_amount": ZERO, "earliest_date": None,
                "first_breach": baseline["first_breach"], "normalized_context": context}
    minimum = min(item["balance"] for item in baseline["balance_path"])
    safe_amount = min(context["requested_amount"], minimum - context["floor"])
    earliest = None
    for offset in range(90):
        candidate = context["request_date"] + timedelta(days=offset)
        if check_schedule(context, [{"date": candidate, "amount": context["requested_amount"]}])["safe"]:
            earliest = candidate
            break
    return {"status": "ok", "baseline_feasible": True, "safe_amount": safe_amount, "earliest_date": earliest,
            "first_breach": None, "normalized_context": context}


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
    result = forecast_baseline(context) if args.baseline else {"request_id": args.request_id,
              "analysis_error": bool(context["unresolved_evidence"]), "unresolved_evidence": context["unresolved_evidence"],
              "flow_count": len(context["flows"])}
    result["request_id"] = args.request_id
    print(json.dumps(result, default=_json, sort_keys=True))


if __name__ == "__main__":
    main()
