import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Centraliza as configuracoes carregadas por variaveis de ambiente."""

    openai_api_key: str | None
    openai_model: str
    chunk_size: int


def get_settings() -> Settings:
    """Retorna as configuracoes da aplicacao com valores padrao seguros."""

    chunk_size = os.getenv("CHUNK_SIZE", "4000")

    try:
        parsed_chunk_size = int(chunk_size)
    except ValueError:
        parsed_chunk_size = 4000

    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        chunk_size=parsed_chunk_size,
    )
