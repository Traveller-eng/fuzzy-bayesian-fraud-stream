from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .feature import FeatureValue


@dataclass(frozen=True)
class FeatureVector:
    z_plus: FeatureValue
    z_minus: FeatureValue
    v_10m: FeatureValue
    v_1h: FeatureValue
    v_24h: FeatureValue
    vol_ratio_24h: FeatureValue
    geo_speed: FeatureValue
    drift: FeatureValue
    schema_version: str = "feature_vector.v1"

    def all_features(self) -> List[FeatureValue]:
        return [
            self.z_plus,
            self.z_minus,
            self.v_10m,
            self.v_1h,
            self.v_24h,
            self.vol_ratio_24h,
            self.geo_speed,
            self.drift,
        ]

    def status_summary(self) -> Dict[str, str]:
        return {
            feature.name: feature.status.value
            for feature in self.all_features()
        }

    def confidence_summary(self) -> Dict[str, float]:
        return {
            feature.name: feature.confidence
            for feature in self.all_features()
        }
