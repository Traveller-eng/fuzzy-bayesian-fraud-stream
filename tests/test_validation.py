from datetime import datetime, timezone

import pytest

from src.models.transaction import Transaction
from src.validation.validator import (
    ValidationConfig,
    validate_transaction,
)


def make_tx(**kwargs):
    defaults = dict(
        transaction_id="tx_1",
        user_id="user_1",
        amount=100.0,
        currency="USD",
        event_time=datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
    )
    defaults.update(kwargs)
    return Transaction(**defaults)


def test_valid_transaction_passes():
    now = datetime(2026, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
    tx = make_tx()
    result = validate_transaction(tx, ValidationConfig(), now)

    assert result.ok
    assert result.errors == ()


def test_negative_amount_is_invalid():
    now = datetime(2026, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
    tx = make_tx(amount=-10.0)
    result = validate_transaction(tx, ValidationConfig(), now)

    assert not result.ok
    assert "amount_not_positive" in result.errors


def test_future_timestamp_is_invalid():
    now = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    tx = make_tx(event_time=datetime(2026, 1, 1, 12, 5, 0, tzinfo=timezone.utc))
    result = validate_transaction(tx, ValidationConfig(), now)

    assert not result.ok
    assert "event_time_too_far_in_future" in result.errors


def test_nan_amount_is_invalid():
    now = datetime(2026, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
    tx = make_tx(amount=float("nan"))
    result = validate_transaction(tx, ValidationConfig(), now)

    assert not result.ok
    assert "amount_not_finite" in result.errors


def test_zero_amount_is_invalid():
    now = datetime(2026, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
    tx = make_tx(amount=0.0)
    result = validate_transaction(tx, ValidationConfig(), now)

    assert not result.ok
    assert "amount_not_positive" in result.errors


def test_amount_above_max_is_invalid():
    now = datetime(2026, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
    config = ValidationConfig(max_amount=1000.0)
    tx = make_tx(amount=2000.0)
    result = validate_transaction(tx, config, now)

    assert not result.ok
    assert "amount_above_max_allowed" in result.errors


def test_missing_transaction_id_is_invalid():
    now = datetime(2026, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
    tx = make_tx(transaction_id="")
    result = validate_transaction(tx, ValidationConfig(), now)

    assert not result.ok
    assert "transaction_id_missing_or_invalid" in result.errors


def test_missing_user_id_is_invalid():
    now = datetime(2026, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
    tx = make_tx(user_id="")
    result = validate_transaction(tx, ValidationConfig(), now)

    assert not result.ok
    assert "user_id_missing_or_invalid" in result.errors


def test_naive_timestamp_is_invalid():
    now = datetime(2026, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
    tx = make_tx(event_time=datetime(2026, 1, 1, 12, 0, 0))
    result = validate_transaction(tx, ValidationConfig(), now)

    assert not result.ok
    assert "event_time_naive_timezone" in result.errors


def test_latitude_out_of_range_is_invalid():
    now = datetime(2026, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
    from src.models.transaction import GeoPoint
    
    tx = make_tx(location=GeoPoint(latitude=95.0, longitude=0.0))
    result = validate_transaction(tx, ValidationConfig(), now)

    assert not result.ok
    assert "latitude_out_of_range" in result.errors


def test_longitude_out_of_range_is_invalid():
    now = datetime(2026, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
    from src.models.transaction import GeoPoint
    
    tx = make_tx(location=GeoPoint(latitude=45.0, longitude=200.0))
    result = validate_transaction(tx, ValidationConfig(), now)

    assert not result.ok
    assert "longitude_out_of_range" in result.errors


def test_valid_location_passes():
    now = datetime(2026, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
    from src.models.transaction import GeoPoint
    
    tx = make_tx(location=GeoPoint(latitude=45.0, longitude=-75.0))
    result = validate_transaction(tx, ValidationConfig(), now)

    assert result.ok
    assert result.errors == ()


def test_missing_location_is_valid():
    now = datetime(2026, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
    tx = make_tx(location=None)
    result = validate_transaction(tx, ValidationConfig(), now)

    assert result.ok
    assert result.errors == ()


def test_currency_warning_when_invalid():
    now = datetime(2026, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
    tx = make_tx(currency="US")
    result = validate_transaction(tx, ValidationConfig(), now)

    assert result.ok
    assert "currency_missing_or_not_3_letters" in result.warnings


def test_valid_currency_no_warning():
    now = datetime(2026, 1, 1, 12, 0, 30, tzinfo=timezone.utc)
    tx = make_tx(currency="USD")
    result = validate_transaction(tx, ValidationConfig(), now)

    assert result.ok
    assert "currency_missing_or_not_3_letters" not in result.warnings
