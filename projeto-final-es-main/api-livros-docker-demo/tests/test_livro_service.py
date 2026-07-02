"""
Testes unitarios do service de livros.
"""

from datetime import date
from unittest.mock import patch

import pytest

from app.models import LivroCriar
from app.services.livro import AnoFuturoError, ISBNDuplicadoError


def test_criar_livro_com_sucesso(servico):
    dados = LivroCriar(
        titulo="Clean Code",
        autor="Robert Martin",
        ano=2008,
        isbn="9780132350884",
    )

    livro = servico.criar(dados)

    assert livro.id == 1
    assert livro.titulo == "Clean Code"
    assert livro.autor == "Robert Martin"
    assert livro.ano == 2008
    assert livro.isbn == "9780132350884"


def test_criar_livro_com_isbn_duplicado_deve_gerar_erro(servico):
    dados = LivroCriar(
        titulo="Livro 1",
        autor="Autor",
        ano=2020,
        isbn="123",
    )
    servico.criar(dados)

    with pytest.raises(ISBNDuplicadoError):
        servico.criar(dados)


def test_criar_livro_com_ano_futuro_deve_gerar_erro(servico):
    dados = LivroCriar(
        titulo="Livro Futuro",
        autor="Autor",
        ano=date.today().year + 1,
        isbn="456",
    )

    with pytest.raises(AnoFuturoError):
        servico.criar(dados)


@patch("app.services.livro.consultar_open_library")
def test_criar_livro_usando_dados_da_open_library(mock_open_library, servico):
    mock_open_library.return_value = {
        "titulo": "Domain-Driven Design",
        "autor": "Eric Evans",
        "ano": 2003,
    }
    dados = LivroCriar(titulo=None, autor=None, ano=2003, isbn="9780321125217")

    livro = servico.criar(dados)

    mock_open_library.assert_called_once_with("9780321125217")
    assert livro.titulo == "Domain-Driven Design"
    assert livro.autor == "Eric Evans"


@patch("app.services.livro.consultar_open_library")
def test_criar_livro_quando_open_library_retorna_none(mock_open_library, servico):
    mock_open_library.return_value = None
    dados = LivroCriar(titulo=None, autor=None, ano=2020, isbn="999")

    livro = servico.criar(dados)

    mock_open_library.assert_called_once_with("999")
    assert livro.titulo == ""
    assert livro.autor == ""
    assert livro.ano == 2020
