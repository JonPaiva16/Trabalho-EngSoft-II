"""Testes unitarios do service de livros."""

from datetime import date
from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.models import LivroCriar
from app.repository import RepositorioEmMemoria
from app.services.livro import ServicoLivros


def criar_service() -> ServicoLivros:
    return ServicoLivros(RepositorioEmMemoria())


@patch("app.services.livro.consultar_open_library", return_value=None)
def test_cadastro_livro_com_sucesso_sem_open_library(mock_open_library):
    service = criar_service()
    dados = LivroCriar(titulo="Livro Teste", autor="Autor Teste", ano=2024, isbn="123")

    livro = service.criar(dados)

    assert livro.id == 1
    assert livro.titulo == "Livro Teste"
    assert livro.autor == "Autor Teste"
    assert livro.isbn == "123"
    mock_open_library.assert_called_once_with("123")


@patch("app.services.livro.consultar_open_library", return_value=None)
def test_isbn_duplicado_retorna_erro(mock_open_library):
    service = criar_service()
    dados = LivroCriar(titulo="Livro Teste", autor="Autor Teste", ano=2024, isbn="123")
    service.criar(dados)

    with pytest.raises(HTTPException) as erro:
        service.criar(dados)

    assert erro.value.status_code == 409
    assert erro.value.detail == "ISBN ja cadastrado"
    assert mock_open_library.call_count == 1


@patch("app.services.livro.consultar_open_library", return_value=None)
def test_ano_futuro_retorna_erro(mock_open_library):
    service = criar_service()
    dados = LivroCriar(
        titulo="Livro Futuro",
        autor="Autor Teste",
        ano=date.today().year + 1,
        isbn="999",
    )

    with pytest.raises(HTTPException) as erro:
        service.criar(dados)

    assert erro.value.status_code == 400
    assert erro.value.detail == "Ano de publicacao nao pode ser futuro"
    mock_open_library.assert_not_called()


@patch(
    "app.services.livro.consultar_open_library",
    return_value={"title": "Titulo Open Library", "authors": [{"name": "Autor Open Library"}]},
)
def test_open_library_retorna_dados(mock_open_library):
    service = criar_service()
    dados = LivroCriar(titulo="Titulo Manual", autor="Autor Manual", ano=2020, isbn="456")

    livro = service.criar(dados)

    assert livro.titulo == "Titulo Open Library"
    assert livro.autor == "Autor Open Library"
    mock_open_library.assert_called_once_with("456")


@patch("app.services.livro.consultar_open_library", return_value=None)
def test_open_library_retorna_none(mock_open_library):
    service = criar_service()
    dados = LivroCriar(titulo="Titulo Manual", autor="Autor Manual", ano=2020, isbn="789")

    livro = service.criar(dados)

    assert livro.titulo == "Titulo Manual"
    assert livro.autor == "Autor Manual"
    mock_open_library.assert_called_once_with("789")
