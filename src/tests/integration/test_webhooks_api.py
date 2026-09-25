from fastapi.testclient import TestClient
from main import app
from src.core.config import settings

client = TestClient(app)


def test_webhook_alert_without_api_key():
    """Garante que requisições sem o header X-API-Key recebam HTTP 401 Unauthorized."""
    response = client.post(
        "/api/v1/webhooks/alert",
        json={
            "service_name": "app-victim",
            "status": "CRITICAL",
            "error_message": "Service Down",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Header 'X-API-Key' ausente na requisição."


def test_webhook_alert_with_invalid_api_key():
    """Garante que chaves de API incorretas recebam HTTP 403 Forbidden."""
    response = client.post(
        "/api/v1/webhooks/alert",
        headers={"X-API-Key": "chave_totalmente_errada"},
        json={
            "service_name": "app-victim",
            "status": "CRITICAL",
            "error_message": "Service Down",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Chave de API inválida ou não autorizada."


def test_webhook_alert_success():
    """Garante que o envio com a chave de API correta retorne HTTP 202 Accepted."""
    response = client.post(
        "/api/v1/webhooks/alert",
        headers={"X-API-Key": settings.API_KEY},
        json={
            "service_name": "app-victim",
            "status": "CRITICAL",
            "error_message": "Service Down",
            "environment": "prod",
        },
    )

    assert response.status_code == 202
    data = response.json()
    assert data["status"] == "accepted"
    assert "app-victim" in data["message"]