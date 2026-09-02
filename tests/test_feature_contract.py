import math
import pytest

from src.models.feature import FeatureStatus, FeatureValue


def test_valid_feature_requires_finite_value():
    feature = FeatureValue(
        name="z_plus",
        status=FeatureStatus.VALID,
        confidence=0.9,
        value=3.2,
    )

    assert feature.value == 3.2


def test_unknown_feature_must_not_have_value():
    with pytest.raises(ValueError):
        FeatureValue(
            name="geo_speed",
            status=FeatureStatus.UNKNOWN,
            confidence=0.0,
            value=100.0,
        )


def test_invalid_feature_must_not_have_value():
    with pytest.raises(ValueError):
        FeatureValue(
            name="drift",
            status=FeatureStatus.INVALID,
            confidence=0.0,
            value=0.0,
        )


def test_confidence_must_be_bounded():
    with pytest.raises(ValueError):
        FeatureValue(
            name="v_10m",
            status=FeatureStatus.VALID,
            confidence=1.2,
            value=3.0,
        )


def test_confidence_must_be_non_negative():
    with pytest.raises(ValueError):
        FeatureValue(
            name="v_10m",
            status=FeatureStatus.VALID,
            confidence=-0.1,
            value=3.0,
        )


def test_valid_feature_with_nan_value_raises():
    with pytest.raises(ValueError):
        FeatureValue(
            name="z_plus",
            status=FeatureStatus.VALID,
            confidence=0.9,
            value=float("nan"),
        )


def test_valid_feature_with_inf_value_raises():
    with pytest.raises(ValueError):
        FeatureValue(
            name="z_plus",
            status=FeatureStatus.VALID,
            confidence=0.9,
            value=float("inf"),
        )


def test_valid_feature_with_none_value_raises():
    with pytest.raises(ValueError):
        FeatureValue(
            name="z_plus",
            status=FeatureStatus.VALID,
            confidence=0.9,
            value=None,
        )


def test_unknown_feature_with_none_value_ok():
    feature = FeatureValue(
        name="geo_speed",
        status=FeatureStatus.UNKNOWN,
        confidence=0.0,
        value=None,
        reason="previous_location_missing",
    )

    assert feature.status == FeatureStatus.UNKNOWN
    assert feature.value is None
    assert feature.reason == "previous_location_missing"


def test_invalid_feature_with_none_value_ok():
    feature = FeatureValue(
        name="drift",
        status=FeatureStatus.INVALID,
        confidence=0.0,
        value=None,
        reason="underlying_data_invalid",
    )

    assert feature.status == FeatureStatus.INVALID
    assert feature.value is None


def test_feature_reason_is_optional():
    feature = FeatureValue(
        name="v_10m",
        status=FeatureStatus.VALID,
        confidence=0.95,
        value=5.0,
    )

    assert feature.reason == ""


def test_confidence_boundary_values():
    # confidence = 0.0 should be valid for UNKNOWN/INVALID
    feature_zero = FeatureValue(
        name="test",
        status=FeatureStatus.UNKNOWN,
        confidence=0.0,
    )
    assert feature_zero.confidence == 0.0

    # confidence = 1.0 should be valid for VALID
    feature_one = FeatureValue(
        name="test",
        status=FeatureStatus.VALID,
        confidence=1.0,
        value=1.0,
    )
    assert feature_one.confidence == 1.0
