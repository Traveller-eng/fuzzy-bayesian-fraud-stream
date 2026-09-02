from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Tuple

from .transaction import GeoPoint


@dataclass(frozen=True)
class HistoricalTransaction:
    amount: float
    event_time: datetime
    location: Optional[GeoPoint] = None


@dataclass(frozen=True)
class PopulationStats:
    amount_median: float
    amount_mad: float
    daily_spend_baseline: float


@dataclass(frozen=True)
class UserHistory:
    user_id: str
    prior_transactions: Tuple[HistoricalTransaction, ...]
    population_stats: Optional[PopulationStats]
    last_location: Optional[GeoPoint] = None
    last_location_time: Optional[datetime] = None
    state_available: bool = True
