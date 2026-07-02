"""Service de livros: regras de negocio da funcionalidade principal."""

from datetime import date

from fastapi import HTTPException, status

from app.clients.open_library import consultar_open_library
from app.models import Livro, LivroAtualizar, LivroCriar
from app.repository import RepositorioLivros


class ServicoLivros:
    """Service responsavel pelas regras de negocio dos livros."""

    def __init__(self, repositorio: RepositorioLivros) -> None:
        self._repo = repositorio

    def listar(self) -> list[Livro]:
        return self._repo.listar()

    def buscar(self, livro_id: int) -> Livro | None:
        return self._repo.buscar_por_id(livro_id)

    def criar(self, dados: LivroCriar) -> Livro:
        if self._repo.get_by_isbn(dados.isbn) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="ISBN ja cadastrado",
            )

        if dados.ano > date.today().year:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ano de publicacao nao pode ser futuro",
            )

        dados_open_library = consultar_open_library(dados.isbn)
        if dados_open_library:
            dados = self._enriquecer_dados(dados, dados_open_library)

        return self._repo.adicionar(dados)

    def atualizar(self, livro_id: int, dados: LivroAtualizar) -> Livro | None:
        return self._repo.atualizar(livro_id, dados)

    def remover(self, livro_id: int) -> bool:
        return self._repo.remover(livro_id)

    @staticmethod
    def _enriquecer_dados(dados: LivroCriar, dados_open_library: dict) -> LivroCriar:
        titulo = dados_open_library.get("title") or dados.titulo
        autores = dados_open_library.get("authors") or []
        autor = dados.autor
        if autores and isinstance(autores[0], dict):
            autor = autores[0].get("name") or autores[0].get("key") or dados.autor

        return LivroCriar(
            titulo=titulo,
            autor=autor,
            ano=dados.ano,
            isbn=dados.isbn,
        )
