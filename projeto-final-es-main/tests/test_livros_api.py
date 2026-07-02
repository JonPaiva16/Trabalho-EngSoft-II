"""Testes de integracao das rotas de livros."""

from datetime import date
from unittest.mock import patch

import app.main as main_module
from app.repository import RepositorioEmMemoria
from app.services.livro import ServicoLivros
from fastapi.testclient import TestClient

client = TestClient(main_module.app)


def setup_function():
    main_module.servico = ServicoLivros(RepositorioEmMemoria())


@patch("app.services.livro.consultar_open_library", return_value=None)
def test_post_livros_sucesso(mock_open_library):
    resposta = client.post(
        "/livros",
        json={"titulo": "Clean Code", "autor": "Robert Martin", "ano": 2008, "isbn": "111"},
    )

    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["id"] == 1
    assert corpo["isbn"] == "111"
    mock_open_library.assert_called_once_with("111")


@patch("app.services.livro.consultar_open_library", return_value=None)
def test_post_livros_isbn_duplicado(_mock_open_library):
    payload = {"titulo": "Livro", "autor": "Autor", "ano": 2022, "isbn": "222"}
    primeira = client.post("/livros", json=payload)
    segunda = client.post("/livros", json=payload)

    assert primeira.status_code == 201
    assert segunda.status_code == 409
    assert segunda.json()["detail"] == "ISBN ja cadastrado"


@patch("app.services.livro.consultar_open_library", return_value=None)
def test_post_livros_ano_futuro(_mock_open_library):
    resposta = client.post(
        "/livros",
        json={
            "titulo": "Livro Futuro",
            "autor": "Autor",
            "ano": date.today().year + 1,
            "isbn": "333",
        },
    )

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == "Ano de publicacao nao pode ser futuro"


@patch("app.services.livro.consultar_open_library", return_value=None)
def test_get_livros(_mock_open_library):
    client.post(
        "/livros",
        json={"titulo": "Livro 1", "autor": "Autor 1", "ano": 2020, "isbn": "444"},
    )

    resposta = client.get("/livros")

    assert resposta.status_code == 200
    assert resposta.json()[0]["titulo"] == "Livro 1"


def test_get_livro_nao_encontrado():
    resposta = client.get("/livros/999")

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Livro nao encontrado"


def test_post_livros_payload_invalido():
    resposta = client.post("/livros", json={"titulo": "", "autor": "Autor"})

    assert resposta.status_code == 422


@patch("app.services.livro.consultar_open_library", return_value=None)
def test_put_livro_sucesso(_mock_open_library):
    criado = client.post(
        "/livros",
        json={"titulo": "Livro Original", "autor": "Autor Original", "ano": 2019, "isbn": "555"},
    )
    livro_id = criado.json()["id"]

    resposta = client.put(
        f"/livros/{livro_id}",
        json={"titulo": "Livro Editado", "autor": "Autor Editado", "ano": 2021, "isbn": "555"},
    )

    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["id"] == livro_id
    assert corpo["titulo"] == "Livro Editado"
    assert corpo["autor"] == "Autor Editado"
    assert corpo["ano"] == 2021


def test_put_livro_nao_encontrado():
    resposta = client.put(
        "/livros/999",
        json={"titulo": "Qualquer", "autor": "Qualquer", "ano": 2021, "isbn": "666"},
    )

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Livro nao encontrado"


def test_put_livros_payload_invalido():
    resposta = client.put("/livros/1", json={"titulo": "", "autor": "Autor"})

    assert resposta.status_code == 422


@patch("app.services.livro.consultar_open_library", return_value=None)
def test_delete_livro_sucesso(_mock_open_library):
    criado = client.post(
        "/livros",
        json={"titulo": "Livro Para Remover", "autor": "Autor", "ano": 2015, "isbn": "777"},
    )
    livro_id = criado.json()["id"]

    resposta = client.delete(f"/livros/{livro_id}")

    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "Livro removido com sucesso"

    verificacao = client.get(f"/livros/{livro_id}")
    assert verificacao.status_code == 404


def test_delete_livro_nao_encontrado():
    resposta = client.delete("/livros/999")

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Livro nao encontrado"
