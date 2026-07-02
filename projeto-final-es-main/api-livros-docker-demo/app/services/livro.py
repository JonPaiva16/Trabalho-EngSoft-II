"""
Service de livros com regras de negocio.
"""

from datetime import date

from app.clients.open_library import consultar_open_library
from app.models import Livro, LivroAtualizar, LivroCriar
from app.repository import RepositorioLivros


class ISBNDuplicadoError(ValueError):
    """Erro usado quando o ISBN ja esta cadastrado."""


class AnoFuturoError(ValueError):
    """Erro usado quando o ano informado esta no futuro."""


class ServicoLivros:
    """
    Regras de negocio para livros.

    Responsabilidades:
    - impedir ISBN duplicado;
    - impedir cadastro com ano futuro;
    - complementar dados usando Open Library quando possivel.
    """

    def __init__(self, repositorio: RepositorioLivros) -> None:
        self._repo = repositorio

    def listar(self) -> list[Livro]:
        return self._repo.listar()

    def buscar(self, livro_id: int) -> Livro | None:
        return self._repo.buscar_por_id(livro_id)

    def criar(self, dados: LivroCriar) -> Livro:
        if self._repo.get_by_isbn(dados.isbn):
            raise ISBNDuplicadoError("ISBN ja cadastrado")

        ano_atual = date.today().year
        if dados.ano > ano_atual:
            raise AnoFuturoError("Ano de publicacao nao pode ser futuro")

        dados_completos = dados
        if not dados.titulo or not dados.autor:
            dados_open_library = consultar_open_library(dados.isbn)
            if dados_open_library:
                dados_completos = LivroCriar(
                    titulo=dados.titulo or dados_open_library.get("titulo"),
                    autor=dados.autor or dados_open_library.get("autor"),
                    ano=dados.ano or dados_open_library.get("ano"),
                    isbn=dados.isbn,
                )

        return self._repo.adicionar(dados_completos)

    def atualizar(self, livro_id: int, dados: LivroAtualizar) -> Livro | None:
        ano_atual = date.today().year
        if dados.ano > ano_atual:
            raise AnoFuturoError("Ano de publicacao nao pode ser futuro")

        livro_com_mesmo_isbn = self._repo.get_by_isbn(dados.isbn)
        if livro_com_mesmo_isbn and livro_com_mesmo_isbn.id != livro_id:
            raise ISBNDuplicadoError("ISBN ja cadastrado")

        return self._repo.atualizar(livro_id, dados)

    def remover(self, livro_id: int) -> bool:
        return self._repo.remover(livro_id)
