"""
Configuracoes compartilhadas dos testes.
"""

import pytest
from fastapi.testclient import TestClient

import main
from app.repository import RepositorioEmMemoria
from app.services.livro import ServicoLivros


@pytest.fixture
def repositorio():
    return RepositorioEmMemoria()


@pytest.fixture
def servico(repositorio):
    return ServicoLivros(repositorio)


@pytest.fixture
def client():
    main.servico = ServicoLivros(RepositorioEmMemoria())
    return TestClient(main.app)
