"""質問スクリプトのテスト（Gemini APIは呼び出さない）。"""

from types import SimpleNamespace

import pytest

from app import ask


@pytest.mark.parametrize("temperature", [None, 0.7])
def test_ask_passes_temperature_and_displays_response_time(
    monkeypatch, capsys, temperature
):
    request = {}

    class FakeModels:
        def generate_content(self, **kwargs):
            request.update(kwargs)
            return SimpleNamespace(text="answer", usage_metadata=None)

    class FakeClient:
        models = FakeModels()

    monkeypatch.setattr(ask.genai, "Client", lambda api_key: FakeClient())
    monkeypatch.setattr(ask, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask, "get_temperature", lambda: temperature)

    assert ask.ask("question") == "answer"
    assert request["contents"] == "question"
    if temperature is None:
        assert request["config"] is None
    else:
        assert request["config"].temperature == temperature
    assert "[応答時間]" in capsys.readouterr().out
