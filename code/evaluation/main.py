"""Small independent checks for the deterministic financial tools."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from main import ZERO, build_request_context, check_schedule, forecast_baseline, load_dataset, project_flows, reconstruct_cash_state


def context(events, *, balance="500", floor="200", currency="EUR", day="2026-01-01", rates=()):
    return {"request": {"request_id": "r", "user_id": "u", "request_date": day, "requested_amount": "500"},
            "profile": {"user_id": "u", "home_currency": currency}, "user_id": "u", "request_date": date.fromisoformat(day),
            "home_currency": currency, "balance": Decimal(balance), "floor": Decimal(floor), "requested_amount": Decimal("500"),
            "events": events, "rates": list(rates), "unresolved_evidence": []}


def event(identifier, amount, *, direction="debit", status="settled", when="2026-01-02", currency="EUR", linked="", kind="expense"):
    return {"event_id": identifier, "amount": amount, "direction": direction, "status": status,
            "settlement_date": when, "event_date": when, "currency": currency, "linked_event_id": linked,
            "event_type": kind, "category": "rent"}


def input_checks() -> None:
    assert not reconstruct_cash_state(context([event("old", "50", when="2025-12-31")]))["flows"]
    state = reconstruct_cash_state(context([event("debit", "20", status="pending"), event("credit", "30", direction="credit", status="pending")]))
    assert state["pending_reserve"] == Decimal("20") and not state["flows"]
    assert not reconstruct_cash_state(context([event("x", "20", status="cancelled"), event("y", "20", status="unrealized")]))["flows"]
    refund = reconstruct_cash_state(context([event("sale", "20"), event("refund", "20", direction="credit", linked="sale")]))
    assert len(refund["flows"]) == 2
    assert reconstruct_cash_state(context([event("bad", "NaN")]))["unresolved_evidence"] == ["bad"]
    fx = reconstruct_cash_state(context([event("usd", "100", currency="USD")], rates=[{"rate_date": "2026-01-02", "from_currency": "USD", "to_currency": "EUR", "rate": "0.9"}]))
    assert fx["flows"][0]["amount"] == Decimal("90")
    assert reconstruct_cash_state(context([event("missing-fx", "10", currency="USD")]))["unresolved_evidence"] == ["missing-fx"]


def forecast_checks() -> None:
    later = context([event("debit", "500", when="2026-01-11"), event("salary", "700", direction="credit", when="2026-01-21")], balance="1000", floor="200", day="2026-01-01")
    result = forecast_baseline(later)
    assert result["safe_amount"] == Decimal("300") and result["earliest_date"] == date(2026, 1, 21)
    breach = context([event("debit", "40", when="2026-01-02"), event("salary", "100", direction="credit", when="2026-01-03")], balance="120", floor="100")
    assert forecast_baseline(breach)["baseline_feasible"] is False
    floor_case = context([], balance="500", floor="200")
    floor_case["requested_amount"] = Decimal("300")
    exact = forecast_baseline(floor_case)
    assert exact["safe_amount"] == Decimal("300") and exact["earliest_date"] == date(2026, 1, 1)
    same_day = context([event("debit", "100", when="2026-01-02"), event("credit", "200", direction="credit", when="2026-01-02")], balance="250", floor="200")
    assert forecast_baseline(same_day)["baseline_feasible"] is False
    boundary = forecast_baseline(context([event("edge", "100", when="2026-03-31")], balance="500", floor="200"))
    assert boundary["safe_amount"] == Decimal("200")
    assert not check_schedule(result["normalized_context"], [{"date": "2026-01-21", "amount": "1001"}])["safe"]
    weekly = context([event("a", "20", when="2025-12-11"), event("b", "30", when="2025-12-18"), event("c", "25", when="2025-12-25")])
    projected = [flow for flow in project_flows(weekly) if flow["synthetic"]]
    assert [flow["amount"] for flow in projected[:3]] == [Decimal("30")] * 3


def sample_check(request_id: str) -> dict:
    dataset = load_dataset()
    sample = next((row for row in dataset["sample_requests"] if row["request_id"] == request_id), None)
    if not sample:
        raise ValueError(f"unknown public sample: {request_id}")
    fields = ("request_id", "user_id", "request_date", "request_type", "requested_amount", "desired_completion_date", "allows_partial_payment", "request_text")
    result = forecast_baseline(reconstruct_cash_state(build_request_context(dataset, request_id, {field: sample[field] for field in fields})))
    if request_id == "request_01":
        assert result["safe_amount"] == Decimal("25256")
        assert result["earliest_date"] == date(2024, 3, 3)
    return {"request_id": request_id, "baseline_feasible": result["baseline_feasible"],
            "safe_amount": str(result["safe_amount"]), "earliest_date": str(result["earliest_date"] or "")}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checks", choices=("input", "forecast", "core"))
    parser.add_argument("--samples")
    parser.add_argument("--structured-only", action="store_true")
    args = parser.parse_args()
    if args.checks in {"input", "core"}:
        input_checks()
    if args.checks in {"forecast", "core"}:
        forecast_checks()
    if args.samples:
        print(json.dumps(sample_check(args.samples), sort_keys=True))
        return
    print("checks passed")


if __name__ == "__main__":
    main()
