from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class FeatureEngineConfig:
    epsilon: float = 1e-9
    cold_start_min_n: int = 20
    history_confidence_k: int = 5
    geo_min_delta_seconds: float = 1.0
    velocity_windows_seconds: Tuple[int, int, int] = (
        600,     # 10 minutes
        3600,    # 1 hour
        86400,   # 24 hours
    )
