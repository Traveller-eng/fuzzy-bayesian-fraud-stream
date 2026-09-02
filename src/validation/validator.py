from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Tuple, Optional

from src.models.transaction import Transaction, GeoPoint


@dataclass(frozen=True)
class ValidationConfig:
    max_amount: float = 1_000_000.0
    future_tolerance_seconds: float = 60.0
    require_currency: bool = True


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    errors: Tuple[str, ...]
    warnings: Tuple[str, ...]
    transaction: Optional[Transaction]


def validate_transaction(
    tx: Transaction,
    config: ValidationConfig,
    now: datetime,
) -> ValidationResult:
    errors = []
    warnings = []

    # Transaction ID
    if not tx.transaction_id or not isinstance(tx.transaction_id, str):
        errors.append("transaction_id_missing_or_invalid")

    # User ID
    if not tx.user_id or not isinstance(tx.user_id, str):
        errors.append("user_id_missing_or_invalid")

    # Amount
    if not math.isfinite(tx.amount):
        errors.append("amount_not_finite")
    elif tx.amount <= 0:
        errors.append("amount_not_positive")
    elif tx.amount > config.max_amount:
        errors.append("amount_above_max_allowed")

    # Currency
    if config.require_currency:
        if not tx.currency or len(tx.currency) != 3:
            warnings.append("currency_missing_or_not_3_letters")

    # Timestamp
    if tx.event_time.tzinfo is None:
        errors.append("event_time_naive_timezone")
    else:
        event_time_utc = tx.event_time.astimezone(timezone.utc)
        max_allowed = now + timedelta(seconds=config.future_tolerance_seconds)

        if event_time_utc > max_allowed:
            errors.append("event_time_too_far_in_future")

    # Location
    if tx.location is not None:
        lat = tx.location.latitude
        lon = tx.location.longitude

        if not math.isfinite(lat) or not math.isfinite(lon):
            errors.append("location_coordinates_not_finite")
        elif not (-90.0 <= lat <= 90.0):
            errors.append("latitude_out_of_range")
        elif not (-180.0 <= lon <= 180.0):
            errors.append("longitude_out_of_range")

    ok = len(errors) == 0

    return ValidationResult(
        ok=ok,
        errors=tuple(errors),
        warnings=tuple(warnings),
        transaction=tx if ok else None,
    )
