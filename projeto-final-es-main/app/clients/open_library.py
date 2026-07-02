"""Cliente externo da Open Library."""

from typing import Any

import requests


def consultar_open_library(isbn: str) -> dict[str, Any] | None:
    """Consulta dados de um livro na Open Library pelo ISBN."""
    url = f"https://openlibrary.org/isbn/{isbn}.json"
    try:
        resposta = requests.get(url, timeout=5)
    except requests.RequestException:
        return None

    if resposta.status_code != 200:
        return None
    return resposta.json()
