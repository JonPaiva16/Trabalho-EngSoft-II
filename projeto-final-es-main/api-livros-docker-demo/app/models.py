"""
Modelos Pydantic da API de catalogo de livros.
"""

from pydantic import BaseModel, Field


class LivroCriar(BaseModel):
    """Dados que o cliente envia para criar um livro."""
    titulo: str | None = Field(default=None, description="Titulo do livro")
    autor: str | None = Field(default=None, description="Nome do autor")
    ano: int = Field(..., ge=0, description="Ano de publicacao")
    isbn: str = Field(..., min_length=1, description="Codigo ISBN")


class LivroAtualizar(BaseModel):
    """Dados que o cliente envia para atualizar um livro."""
    titulo: str = Field(..., min_length=1)
    autor: str = Field(..., min_length=1)
    ano: int = Field(..., ge=0)
    isbn: str = Field(..., min_length=1)


class Livro(BaseModel):
    """Livro completo, como a API devolve."""
    id: int
    titulo: str
    autor: str
    ano: int
    isbn: str
