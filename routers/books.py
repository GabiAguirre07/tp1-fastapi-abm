"""Endpoints HTTP de la entidad Libro.

Traduce las peticiones HTTP a operaciones del repositorio de libros y
decide los códigos de respuesta. No contiene lógica de almacenamiento.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from models.books import Book, BookCreate, BookUpdate
from repositories.books import RepositorioLibros, obtener_repositorio_libros
from routers.comun import no_encontrado

router = APIRouter(prefix="/books", tags=["Libros"])

# Repositorio inyectado por FastAPI en cada endpoint que lo declare.
RepoLibros = Annotated[RepositorioLibros, Depends(obtener_repositorio_libros)]


@router.get("")
def listar_libros(
    repo: RepoLibros, autor: str | None = None, anio: int | None = None
) -> list[Book]:
    """Lista los libros. Filtra por autor (parcial) y/o año si se indican."""
    return repo.buscar(autor, anio)


@router.get("/{libro_id}")
def obtener_libro(libro_id: int, repo: RepoLibros) -> Book:
    """Devuelve un libro por id. Responde 404 si no existe."""
    libro = repo.obtener(libro_id)
    if libro is None:
        raise no_encontrado("Libro", libro_id)

    return libro


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_libro(datos: BookCreate, repo: RepoLibros) -> Book:
    """Crea un libro. El id lo asigna el servidor."""
    return repo.crear(datos)


@router.patch("/{libro_id}")
def actualizar_libro(libro_id: int, cambios: BookUpdate, repo: RepoLibros) -> Book:
    """Modifica solo los campos enviados. Responde 404 si no existe."""
    libro = repo.actualizar(libro_id, cambios)
    if libro is None:
        raise no_encontrado("Libro", libro_id)

    return libro


@router.delete("/{libro_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_libro(libro_id: int, repo: RepoLibros) -> None:
    """Elimina un libro. Responde 204 sin cuerpo, o 404 si no existe."""
    if not repo.eliminar(libro_id):
        raise no_encontrado("Libro", libro_id)
