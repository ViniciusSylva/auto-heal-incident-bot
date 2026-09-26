from fastapi import Header, HTTPException, status
from src.core.config import settings


async def verify_api_key(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> str:
    """
    Inspeciona o cabeçalho HTTP 'X-API-Key' e valida se bate com a chave configurada em settings.
    """
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Header 'X-API-Key' ausente na requisição.",
        )

    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chave de API inválida ou não autorizada.",
        )

    return x_api_key