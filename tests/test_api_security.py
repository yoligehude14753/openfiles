"""Ensure the API never leaks sensitive credentials."""

import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    from src.api.app import app
    return TestClient(app)


class TestSettingsEndpoint:
    def test_no_raw_api_key_in_response(self, client):
        resp = client.get("/api/v1/settings")
        assert resp.status_code == 200
        data = resp.json()

        assert "yunwu_api_key" not in data, "Raw API key must not be exposed"
        assert "openai_api_key" not in data
        assert "anthropic_api_key" not in data
        assert "kimi_api_key" not in data

    def test_masked_key_present(self, client):
        resp = client.get("/api/v1/settings")
        data = resp.json()

        assert "yunwu_api_key_masked" in data
        assert "yunwu_api_key_set" in data

    @patch("src.api.routes.system.settings")
    def test_mask_format_long_key(self, mock_settings, client):
        mock_settings.yunwu_api_key = "sk-abcdef1234567890"
        mock_settings.llm_provider = "yunwu"
        mock_settings.embedding_provider = "yunwu"
        mock_settings.yunwu_base_url = "https://yunwu.ai/v1"
        mock_settings.yunwu_model = "gpt-5.4-nano"
        mock_settings.ollama_host = "http://localhost:11434"
        mock_settings.ollama_model = "llama3.2"
        mock_settings.scan_dirs_list = []
        mock_settings.max_file_size_mb = 100
        mock_settings.daily_budget_usd = 10.0
        mock_settings.monthly_budget_usd = 100.0

        resp = client.get("/api/v1/settings")
        data = resp.json()

        masked = data["yunwu_api_key_masked"]
        assert masked.startswith("sk-a")
        assert "****" in masked
        assert masked.endswith("7890")
        assert data["yunwu_api_key_set"] is True

    @patch("src.api.routes.system.settings")
    def test_mask_format_empty_key(self, mock_settings, client):
        mock_settings.yunwu_api_key = ""
        mock_settings.llm_provider = "yunwu"
        mock_settings.embedding_provider = "yunwu"
        mock_settings.yunwu_base_url = "https://yunwu.ai/v1"
        mock_settings.yunwu_model = "gpt-5.4-nano"
        mock_settings.ollama_host = "http://localhost:11434"
        mock_settings.ollama_model = "llama3.2"
        mock_settings.scan_dirs_list = []
        mock_settings.max_file_size_mb = 100
        mock_settings.daily_budget_usd = 10.0
        mock_settings.monthly_budget_usd = 100.0

        resp = client.get("/api/v1/settings")
        data = resp.json()

        assert data["yunwu_api_key_masked"] == ""
        assert data["yunwu_api_key_set"] is False
