from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class GeoPoint:
    latitude: float
    longitude: float
    accuracy_meters: Optional[float] = None
    source: Optional[str] = None


@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    user_id: str
    amount: float
    currency: str
    event_time: datetime
    location: Optional[GeoPoint] = None
    device_id: Optional[str] = None
    ip_address: Optional[str] = None
    merchant_category: Optional[str] = None
