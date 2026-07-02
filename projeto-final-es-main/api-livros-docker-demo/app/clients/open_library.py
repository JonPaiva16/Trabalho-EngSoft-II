"""
Cliente para consulta de livros na Open Library.
"""

import urllib.request
import json


def consultar_open_library(isbn: str) -> dict | None:
    """
    Consulta informacoes de um livro pelo ISBN na Open Library.

    Retorna um dicionario simples com titulo, autor e ano quando encontrar
    dados suficientes. Em caso de erro ou ausencia de dados, retorna None.
    """
    url = (
        "https://openlibrary.org/api/books"
        f"?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    )

    try:
        with urllib.request.urlopen(url, timeout=5) as resposta:
            conteudo = resposta.read().decode("utf-8")
    except (OSError, TimeoutError):
        return None

    dados = json.loads(conteudo)
    livro = dados.get(f"ISBN:{isbn}")
    if not livro:
        return None

    autores = livro.get("authors") or []
    autor = autores[0].get("name") if autores else None
    ano_publicacao = livro.get("publish_date")
    ano = None
    if ano_publicacao:
        numeros = "".join(caractere for caractere in ano_publicacao if caractere.isdigit())
        if len(numeros) >= 4:
            ano = int(numeros[:4])

    return {
        "titulo": livro.get("title"),
        "autor": autor,
        "ano": ano,
    }
