from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient
import pytest
from .entropy import router

client = TestClient(router)


class TestEntropyGetGenerateErrors:
    def test_generate_less_than_minimum(self):
        with pytest.raises(RequestValidationError):
            _ = client.get("/entropy/generate/127")

    def test_generate_more_than_maximum(self):
        with pytest.raises(RequestValidationError):
            _ = client.get("/entropy/generate/257")

    def test_generate_invalid_strength(self):
        with pytest.raises(RequestValidationError):
            _ = client.get("/entropy/generate/129")

    def test_generate_missing_strength(self):
        response = client.get("/entropy/generate/")
        assert response.status_code == 404

        response = client.get("/entropy/generate")
        assert response.status_code == 404


class TestEntropyGetGenerateValid:
    def test_generate_check_size(self):
        strength = 128
        response = client.get(f"/entropy/generate/{strength}")
        data: dict[str, str] = response.json()

        assert response.status_code == 200
        assert "entropy" in data
        assert len(data["entropy"]) == strength // 4
