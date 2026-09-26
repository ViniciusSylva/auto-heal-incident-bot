from fastapi import Header, HTTPException, status
from fastapi.testclient import TestClient
from src.core.security import verify_api_key
from src.main import app

client = TestClient(app)

TEST_API_KEY = "chave_de_teste_segura_123"


async def mock_verify_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> str:
    """Mock da dependência que recebe corretamente o header da requisição."""
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Header 'X-API-Key' ausente na requisição.",
        )

    if x_api_key != TEST_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chave de API inválida ou não autorizada.",
        )

    return x_api_key


def test_webhook_alert_without_api_key():
    """Garante que requisições sem o header X-API-Key recebam HTTP 401 Unauthorized."""
    app.dependency_overrides[verify_api_key] = mock_verify_api_key
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
    app.dependency_overrides.clear()


def test_webhook_alert_with_invalid_api_key():
    """Garante que chaves de API incorretas recebam HTTP 403 Forbidden."""
    app.dependency_overrides[verify_api_key] = mock_verify_api_key
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
    app.dependency_overrides.clear()


def test_webhook_alert_success():
    """Garante que o envio com a chave de API correta retorne HTTP 202 Accepted."""
    app.dependency_overrides[verify_api_key] = mock_verify_api_key
    response = client.post(
        "/api/v1/webhooks/alert",
        headers={"X-API-Key": TEST_API_KEY},
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
    app.dependency_overrides.clear()