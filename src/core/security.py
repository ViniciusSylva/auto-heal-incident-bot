from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from src.core.config import settings

# Define de onde o FastAPI deve extrair o token nos headers HTTP
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key_header: str = Security(API_KEY_HEADER)) -> str:
    """
    Dependência que valida se o header X-API-Key bate com a chave configurada.
    """
    if not api_key_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Header 'X-API-Key' ausente na requisição.",
        )

    if api_key_header != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chave de API inválida ou não autorizada.",
        )

    return api_key_header