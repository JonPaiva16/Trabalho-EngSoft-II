"""Testes unitarios do cliente da Open Library.

Estes testes NAO fazem chamadas de rede reais: requests.get e sempre
mockado, conforme exigido pelo enunciado (Aula 9 - Mock da dependencia
externa).
"""

from unittest.mock import Mock, patch

import requests

from app.clients.open_library import consultar_open_library


@patch("app.clients.open_library.requests.get")
def test_consultar_open_library_sucesso(mock_get):
    resposta_mock = Mock()
    resposta_mock.status_code = 200
    resposta_mock.json.return_value = {"title": "Titulo Mockado", "authors": []}
    mock_get.return_value = resposta_mock

    resultado = consultar_open_library("123")

    assert resultado == {"title": "Titulo Mockado", "authors": []}
    mock_get.assert_called_once_with(
        "https://openlibrary.org/isbn/123.json", timeout=5
    )


@patch("app.clients.open_library.requests.get")
def test_consultar_open_library_status_diferente_de_200(mock_get):
    resposta_mock = Mock()
    resposta_mock.status_code = 404
    mock_get.return_value = resposta_mock

    resultado = consultar_open_library("isbn-inexistente")

    assert resultado is None


@patch("app.clients.open_library.requests.get")
def test_consultar_open_library_erro_de_rede(mock_get):
    mock_get.side_effect = requests.RequestException("timeout")

    resultado = consultar_open_library("999")

    assert resultado is None
