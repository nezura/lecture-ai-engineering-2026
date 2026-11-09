"""共通設定のテスト。"""

import pytest

from app.config import get_temperature


def test_get_temperature_defaults_to_none(monkeypatch):
    monkeypatch.delenv("AIE_TEMPERATURE", raising=False)

    assert get_temperature() is None


@pytest.mark.parametrize("value", ["0", "0.7", "2", "2.1", "100"])
def test_get_temperature_reads_valid_value(monkeypatch, value):
    monkeypatch.setenv("AIE_TEMPERATURE", value)

    assert get_temperature() == float(value)


@pytest.mark.parametrize("value", ["high", "-0.1", "nan", "inf", "-inf"])
def test_get_temperature_rejects_invalid_value(monkeypatch, value):
    monkeypatch.setenv("AIE_TEMPERATURE", value)

    with pytest.raises(SystemExit, match="AIE_TEMPERATURE"):
        get_temperature()
