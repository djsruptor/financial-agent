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


def _supported_salary_schedule(events: list[dict], start: date, end: date) -> list[dict]:
    """A named next salary plus a settled salary is evidence of ongoing employment."""
    settled_salary = any(
        event.get("status") == "settled" and event.get("direction") == "credit" and event.get("category") == "salary"
        and as_date(event.get("settlement_date") or event["event_date"]) < start for event in events
    )
    if not settled_salary:
        return []
    result = []
    for event in events:
        if event.get("status") not in {"scheduled", "confirmed"} or event.get("direction") != "credit" or event.get("category") != "salary":
            continue
        amount = money(event.get("amount"))
        if amount is None:
            continue
        next_day = as_date(event.get("settlement_date") or event["event_date"])
        while next_day <= end:
            if next_day >= start:
                result.append({"source_id": event["event_id"], "date": next_day, "amount": amount,
                               "direction": "credit", "category": "salary", "synthetic": next_day != as_date(event.get("settlement_date") or event["event_date"])})
            next_day = _month_after(next_day)
    return result


def project_flows(context: dict) -> list[dict]:
    """Combine explicit normalized cash with supported, non-duplicated recurrences."""
    start, end = context["request_date"], context["request_date"] + timedelta(days=89)
    explicit = list(context.get("flows", []))
    used = {(flow["date"], flow["category"], flow["direction"]) for flow in explicit}
    inferred = [flow for flow in _recurs_monthly(context["events"], start, end) + _recurs_interval(context["events"], start, end) + _supported_salary_schedule(context["events"], start, end)
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


MODEL_ID = "gpt-4.1-2025-04-14"
MAX_TURNS, MAX_ATTEMPTS, MAX_EVIDENCE_ATTEMPTS = 12, 24, 2


def _source_index(dataset: dict, context: dict) -> dict[str, dict]:
    """Return only supplied, request-scoped evidence available on the request date."""
    cutoff = context["request_date"].isoformat() + "T23:59:59Z"
    sources = {}
    for row in dataset["messages"]:
        if row["user_id"] == context["user_id"] and row.get("sent_at", "") <= cutoff and row.get("request_id") in {"", context["request"]["request_id"]}:
            sources[row["message_id"]] = {"kind": "message", **dict(row)}
    for row in dataset["images"]:
        if row["user_id"] == context["user_id"] and row.get("request_id") in {"", context["request"]["request_id"]}:
            sources[row["image_id"]] = {"kind": "image", **dict(row)}
    return sources


def _usage(total: dict, response: dict) -> None:
    total["attempts"] += 1
    usage = response.get("usage", {}) if isinstance(response, dict) else {}
    for key in ("input_tokens", "output_tokens", "total_tokens"):
        value = usage.get(key)
        if isinstance(value, int) and value >= 0:
            total[key] = total.get(key, 0) + value
        elif value is not None:
            total["unavailable"] = True


def _observation_error(code: str) -> dict:
    return {"ok": False, "error": code}


def _host_result(forecast: dict, revision: int, usage: dict, tools: list[dict]) -> dict:
    return {
        "status": forecast["status"], "request_id": forecast["normalized_context"]["request"]["request_id"],
        "baseline_feasible": forecast["baseline_feasible"], "safe_amount": forecast["safe_amount"],
        "earliest_date": forecast["earliest_date"], "first_breach": forecast.get("first_breach"),
        "evidence_revision": revision, "usage": usage, "tool_sequence": tools,
    }


def _apply_evidence(context: dict, source: dict, facts: object) -> tuple[bool, str]:
    """Validate source-scoped facts before they change normalized financial state."""
    if not isinstance(facts, list) or not facts:
        return False, "missing_or_ambiguous_facts"
    if source["kind"] == "image":
        media = Path("dataset/media/images").resolve()
        image = (media / f"{source['image_id']}.png").resolve()
        if media not in image.parents or not image.is_file():
            return False, "missing_or_unauthorized_image"
    applied = False
    for fact in facts:
        if not isinstance(fact, dict) or fact.get("source_id") != (source.get("message_id") or source.get("image_id")):
            return False, "invalid_fact_source"
        try:
            amount, effective = money(fact.get("amount")), as_date(fact.get("effective_date"))
        except ValueError:
            return False, "invalid_fact_value"
        if amount is None or amount < ZERO or fact.get("currency") != context["home_currency"]:
            return False, "invalid_fact_value"
        effect, target_id = fact.get("effect"), fact.get("target_event_id", "")
        if source["kind"] == "image":
            if effect != "net_amount" or fact.get("field") != "net" or target_id != source.get("related_event_id"):
                return False, "invalid_image_fact"
        if effect == "salary_amendment":
            targets = [event for event in context["events"] if event.get("category") == "salary" and event.get("direction") == "credit"
                       and as_date(event.get("settlement_date") or event["event_date"]) >= effective]
            if target_id:
                targets = [event for event in targets if event["event_id"] == target_id]
            if not targets:
                return False, "ambiguous_or_missing_target"
        elif effect == "net_amount":
            targets = [event for event in context["events"] if event["event_id"] == target_id]
            if len(targets) != 1:
                return False, "ambiguous_or_missing_target"
        else:
            return False, "unsupported_evidence_effect"
        for event in targets:
            if event.get("currency") != fact["currency"]:
                return False, "currency_mismatch"
            if event.get("amount") != format(amount, "f"):
                event["amount"] = format(amount, "f")
                applied = True
    return applied, "ok"


def _dispatch(action: dict, context: dict, dataset: dict, sources: dict, revision: int,
              forecast: dict | None) -> tuple[dict, int, dict | None]:
    """Literal host allowlist; no model field crosses the financial result boundary."""
    name, args = action.get("tool"), action.get("arguments", {})
    if not isinstance(args, dict):
        return _observation_error("malformed_arguments"), revision, forecast
    if name == "inspect_records":
        return {"ok": True, "request_id": context["request"]["request_id"], "user_id": context["user_id"],
                "evidence_ids": sorted(sources), "unresolved_evidence": sorted(context["unresolved_evidence"])}, revision, forecast
    if name == "resolve_evidence":
        source_id = args.get("source_id")
        source = sources.get(source_id)
        if not source:
            return _observation_error("unknown_or_unauthorized_evidence"), revision, forecast
        applied, reason = _apply_evidence(context, source, args.get("facts"))
        if reason != "ok":
            return _observation_error(reason), revision, forecast
        sources.pop(source_id)
        context["unresolved_evidence"] = [item for item in context["unresolved_evidence"] if item != source_id]
        if applied:
            refreshed = reconstruct_cash_state(context)
            refreshed["unresolved_evidence"] = sorted(set(refreshed["unresolved_evidence"] + context["unresolved_evidence"]))
            context.clear()
            context.update(refreshed)
            revision += 1
            forecast = None
        return {"ok": True, "source_id": source_id, "changed": applied, "evidence_revision": revision}, revision, forecast
    if name == "forecast_baseline":
        if context["unresolved_evidence"]:
            return _observation_error("unresolved_evidence"), revision, forecast
        forecast = forecast_baseline(context)
        forecast["evidence_revision"] = revision
        return {"ok": True, "status": forecast["status"], "baseline_feasible": forecast["baseline_feasible"],
                "safe_amount": forecast["safe_amount"], "earliest_date": forecast["earliest_date"],
                "evidence_revision": revision}, revision, forecast
    if name == "finish":
        if context["unresolved_evidence"]:
            return _observation_error("unresolved_evidence"), revision, forecast
        if not forecast or forecast.get("evidence_revision") != revision:
            return _observation_error("stale_or_missing_forecast"), revision, forecast
        return {"ok": True, "finished": True}, revision, forecast
    return _observation_error("unknown_tool"), revision, forecast


def run_request(request: dict, dataset: dict, client) -> dict:
    """Run a bounded, model-selected workflow against host-owned financial tools."""
    context = reconstruct_cash_state(build_request_context(dataset, request["request_id"], request))
    sources, tools, usage = _source_index(dataset, context), [], {"attempts": 0, "unavailable": False}
    context["unresolved_evidence"] = sorted(sources)
    revision, forecast, evidence_attempts, failures = 0, None, {}, set()
    observation = {"ok": True, "request_id": context["request"]["request_id"], "next": "inspect_records"}
    for turn in range(MAX_TURNS):
        if usage["attempts"] >= MAX_ATTEMPTS:
            break
        try:
            response = client({"model": MODEL_ID, "turn": turn + 1, "observation": observation,
                               "allowed_tools": ["inspect_records", "resolve_evidence", "forecast_baseline", "finish"],
                               "timeout_seconds": 60})
        except Exception as exc:
            usage["attempts"] += 1
            observation = _observation_error("provider_error")
            if str(exc) in failures:
                break
            failures.add(str(exc))
            continue
        if not isinstance(response, dict):
            usage["attempts"] += 1
            observation = _observation_error("malformed_provider_response")
            continue
        _usage(usage, response)
        action = response.get("action")
        if not isinstance(action, dict):
            observation = _observation_error("malformed_action")
            continue
        if action.get("tool") == "resolve_evidence":
            source_id = action.get("arguments", {}).get("source_id") if isinstance(action.get("arguments"), dict) else None
            if source_id in sources:
                evidence_attempts[source_id] = evidence_attempts.get(source_id, 0) + 1
                if evidence_attempts[source_id] > MAX_EVIDENCE_ATTEMPTS:
                    observation = _observation_error("evidence_attempt_budget")
                    tools.append({"tool": "resolve_evidence", "source_id": source_id, "ok": False})
                    continue
        observation, revision, forecast = _dispatch(action, context, dataset, sources, revision, forecast)
        tools.append({"tool": action.get("tool"), "source_id": action.get("arguments", {}).get("source_id"), "ok": observation["ok"]})
        if observation.get("finished"):
            return _host_result(forecast, revision, usage, tools)
        fingerprint = json.dumps(action, sort_keys=True, default=str)
        if not observation["ok"] and fingerprint in failures:
            break
        if not observation["ok"]:
            failures.add(fingerprint)
    return {"status": "analysis_error", "request_id": context["request"]["request_id"], "reason": "workflow_budget_or_validation",
            "evidence_revision": revision, "usage": usage, "tool_sequence": tools}


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
    if args.baseline:
        result.pop("normalized_context", None)
    result["request_id"] = args.request_id
    print(json.dumps(result, default=_json, sort_keys=True))


if __name__ == "__main__":
    main()
