"""Camada de repository da API de livros."""

from abc import ABC, abstractmethod

from app.models import Livro, LivroAtualizar, LivroCriar


class RepositorioLivros(ABC):
    """Interface que qualquer repositorio de livros deve implementar."""

    @abstractmethod
    def listar(self) -> list[Livro]:
        """Lista todos os livros."""

    @abstractmethod
    def buscar_por_id(self, livro_id: int) -> Livro | None:
        """Busca um livro pelo id."""

    @abstractmethod
    def get_by_isbn(self, isbn: str) -> Livro | None:
        """Busca um livro pelo ISBN."""

    @abstractmethod
    def adicionar(self, dados: LivroCriar) -> Livro:
        """Adiciona um livro."""

    @abstractmethod
    def atualizar(self, livro_id: int, dados: LivroAtualizar) -> Livro | None:
        """Atualiza um livro."""

    @abstractmethod
    def remover(self, livro_id: int) -> bool:
        """Remove um livro."""


class RepositorioEmMemoria(RepositorioLivros):
    """Repositorio em memoria usado pela API e pelos testes."""

    def __init__(self) -> None:
        self._livros: dict[int, Livro] = {}
        self._proximo_id = 1

    def listar(self) -> list[Livro]:
        return list(self._livros.values())

    def buscar_por_id(self, livro_id: int) -> Livro | None:
        return self._livros.get(livro_id)

    def get_by_isbn(self, isbn: str) -> Livro | None:
        for livro in self._livros.values():
            if livro.isbn == isbn:
                return livro
        return None

    def adicionar(self, dados: LivroCriar) -> Livro:
        novo = Livro(
            id=self._proximo_id,
            titulo=dados.titulo,
            autor=dados.autor,
            ano=dados.ano,
            isbn=dados.isbn,
        )
        self._livros[novo.id] = novo
        self._proximo_id += 1
        return novo

    def atualizar(self, livro_id: int, dados: LivroAtualizar) -> Livro | None:
        if livro_id not in self._livros:
            return None
        atualizado = Livro(id=livro_id, **dados.model_dump())
        self._livros[livro_id] = atualizado
        return atualizado

    def remover(self, livro_id: int) -> bool:
        if livro_id not in self._livros:
            return False
        del self._livros[livro_id]
        return True
