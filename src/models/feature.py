from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class FeatureStatus(str, Enum):
    VALID = "VALID"
    UNKNOWN = "UNKNOWN"
    INVALID = "INVALID"


@dataclass(frozen=True)
class FeatureValue:
    name: str
    status: FeatureStatus
    confidence: float
    value: Optional[float] = None
    reason: str = ""

    def __post_init__(self) -> None:
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(
                f"Feature '{self.name}' confidence must be in [0, 1], "
                f"got {self.confidence}"
            )

        if self.status == FeatureStatus.VALID:
            if self.value is None or not math.isfinite(self.value):
                raise ValueError(
                    f"Feature '{self.name}' is VALID but value is missing or non-finite."
                )
        else:
            if self.value is not None:
                raise ValueError(
                    f"Feature '{self.name}' has status {self.status}, "
                    f"so value must be None."
                )
