"""
Testes de integracao das rotas de livros.
"""

from datetime import date
from unittest.mock import patch


def test_post_livros_sucesso(client):
    resposta = client.post(
        "/livros",
        json={
            "titulo": "Refactoring",
            "autor": "Martin Fowler",
            "ano": 1999,
            "isbn": "9780201485677",
        },
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["id"] == 1
    assert corpo["titulo"] == "Refactoring"


def test_post_livros_isbn_duplicado(client):
    payload = {
        "titulo": "Livro",
        "autor": "Autor",
        "ano": 2021,
        "isbn": "111",
    }
    assert client.post("/livros", json=payload).status_code == 201

    resposta = client.post("/livros", json=payload)

    assert resposta.status_code == 409
    assert resposta.json()["detail"] == "ISBN ja cadastrado"


def test_post_livros_ano_futuro(client):
    resposta = client.post(
        "/livros",
        json={
            "titulo": "Livro Futuro",
            "autor": "Autor",
            "ano": date.today().year + 1,
            "isbn": "222",
        },
    )

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == "Ano de publicacao nao pode ser futuro"


def test_get_livros(client):
    client.post(
        "/livros",
        json={
            "titulo": "Livro API",
            "autor": "Autor API",
            "ano": 2020,
            "isbn": "333",
        },
    )

    resposta = client.get("/livros")

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1


def test_get_livro_inexistente_retorna_404(client):
    resposta = client.get("/livros/999")

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Livro nao encontrado"


def test_put_livro_inexistente_retorna_404(client):
    resposta = client.put(
        "/livros/999",
        json={
            "titulo": "Livro",
            "autor": "Autor",
            "ano": 2020,
            "isbn": "444",
        },
    )

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Livro nao encontrado"


def test_delete_livro_inexistente_retorna_404(client):
    resposta = client.delete("/livros/999")

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Livro nao encontrado"


@patch("app.services.livro.consultar_open_library")
def test_post_livros_com_open_library_mockada(mock_open_library, client):
    mock_open_library.return_value = {
        "titulo": "Livro Mockado",
        "autor": "Autor Mockado",
        "ano": 2010,
    }

    resposta = client.post(
        "/livros",
        json={
            "titulo": None,
            "autor": None,
            "ano": 2010,
            "isbn": "555",
        },
    )

    assert resposta.status_code == 201
    assert resposta.json()["titulo"] == "Livro Mockado"
    mock_open_library.assert_called_once_with("555")
