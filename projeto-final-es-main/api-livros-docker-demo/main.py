"""
API REST de catalogo de livros (FastAPI).
"""

from fastapi import FastAPI, HTTPException, status

from app.models import Livro, LivroAtualizar, LivroCriar
from app.repository import RepositorioEmMemoria
from app.services.livro import AnoFuturoError, ISBNDuplicadoError, ServicoLivros


app = FastAPI(title="Catalogo de Livros", version="1.0.0")

servico = ServicoLivros(RepositorioEmMemoria())


@app.get("/livros", response_model=list[Livro])
def listar_livros():
    return servico.listar()


@app.get("/livros/{livro_id}", response_model=Livro)
def buscar_livro(livro_id: int):
    livro = servico.buscar(livro_id)
    if livro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro nao encontrado",
        )
    return livro


@app.post("/livros", response_model=Livro, status_code=status.HTTP_201_CREATED)
def criar_livro(dados: LivroCriar):
    try:
        return servico.criar(dados)
    except ISBNDuplicadoError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(erro),
        ) from erro
    except AnoFuturoError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        ) from erro


@app.put("/livros/{livro_id}", response_model=Livro)
def atualizar_livro(livro_id: int, dados: LivroAtualizar):
    try:
        livro = servico.atualizar(livro_id, dados)
    except ISBNDuplicadoError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(erro),
        ) from erro
    except AnoFuturoError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        ) from erro

    if livro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro nao encontrado",
        )
    return livro


@app.delete("/livros/{livro_id}", status_code=status.HTTP_200_OK)
def remover_livro(livro_id: int):
    removido = servico.remover(livro_id)
    if not removido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livro nao encontrado",
        )
    return {"mensagem": "Livro removido com sucesso"}
