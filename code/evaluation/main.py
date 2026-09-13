"""Small independent checks for the deterministic financial tools."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from main import ZERO, build_request_context, reconstruct_cash_state


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checks", choices=("input", "forecast", "core"))
    parser.add_argument("--samples")
    parser.add_argument("--structured-only", action="store_true")
    args = parser.parse_args()
    if args.checks in {"input", "core"}:
        input_checks()
    if args.checks in {"forecast", "core"}:
        from main import forecast_checks_placeholder  # added by task 2
        forecast_checks_placeholder()
    print("checks passed")


if __name__ == "__main__":
    main()
