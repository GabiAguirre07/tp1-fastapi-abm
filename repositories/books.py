"""Repositorio en memoria de la entidad Libro.

Define el repositorio con las búsquedas propias de libros, crea la única
instancia que comparte toda la aplicación y expone la función que la provee
a los endpoints mediante Depends.
"""

from models.books import Book, BookCreate
from repositories.base import RepositorioEnMemoria


class RepositorioLibros(RepositorioEnMemoria[Book]):
    """Repositorio de libros: agrega la búsqueda por autor y año al repositorio genérico."""

    def __init__(self) -> None:
        """Inicializa el repositorio para trabajar con el modelo Book."""
        super().__init__(Book)

    def buscar(self, autor: str | None = None, anio: int | None = None) -> list[Book]:
        """Devuelve los libros que cumplen todos los filtros indicados.

        autor: coincidencia parcial sin distinguir mayúsculas.
        anio: año de publicación exacto.
        Sin filtros, devuelve todos los libros.
        """
        resultados = self.listar()
        if autor is not None:
            texto = autor.casefold()
            resultados = [
                libro for libro in resultados if texto in libro.autor.casefold()
            ]

        if anio is not None:
            resultados = [
                libro for libro in resultados if libro.anio_publicacion == anio
            ]

        return resultados


# Instancia única: los datos viven en memoria y deben compartirse entre requests.
_repositorio = RepositorioLibros()
for libro in (
    BookCreate(
        titulo="Ficciones",
        autor="Jorge Luis Borges",
        isbn="9789875666474",
        anio_publicacion=1944,
    ),
    BookCreate(
        titulo="El Aleph",
        autor="Jorge Luis Borges",
        isbn="9789875666481",
        anio_publicacion=1949,
    ),
    BookCreate(
        titulo="Rayuela",
        autor="Julio Cortázar",
        isbn="9788437604572",
        anio_publicacion=1963,
    ),
):
    _repositorio.crear(libro)


def obtener_repositorio_libros() -> RepositorioLibros:
    """Provee el repositorio de libros a los endpoints (usar con Depends)."""
    return _repositorio
