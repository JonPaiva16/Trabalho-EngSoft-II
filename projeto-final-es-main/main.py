"""Arquivo de entrada mantido para compatibilidade com uvicorn main:app."""

from app.main import app

__all__ = ["app"]
