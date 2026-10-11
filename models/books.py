"""Esquemas Pydantic de la entidad Libro.

Define los modelos de entrada (alta y modificación) y de salida de la API,
junto con las reglas de validación compartidas entre ellos.
"""

from datetime import date
from typing import Annotated

from pydantic import Field

from models.base import EsquemaBase, EsquemaEntrada

# Año actual, calculado al iniciar la app, como límite de anio_publicacion.
ANIO_ACTUAL = date.today().year

# Tipos reutilizables: cada campo del libro con sus reglas de validación.
Titulo = Annotated[
    str,
    Field(
        min_length=1,
        max_length=200,
        description="Título del libro",
        examples=["Ficciones", "Don Quijote de la Mancha", "Crimen y castigo"],
    ),
]

Autor = Annotated[
    str,
    Field(
        min_length=2,
        max_length=200,
        description="Autor del libro",
        examples=["Jorge Luis Borges", "William Shakespeare", "Miguel de Cervantes"],
    ),
]

Isbn = Annotated[
    str,
    Field(
        pattern=r"^(\d{10}|\d{13})$",
        description="ISBN de 10 o 13 dígitos, sin guiones",
        examples=["9789875666474", "9482815567"],
    ),
]

AnioPublicacion = Annotated[
    int,
    Field(
        ge=1450,
        le=ANIO_ACTUAL,
        description="Año de publicación del libro",
        examples=[1450, 2026, 1967],
    ),
]


class BookBase(EsquemaBase):
    """Campos comunes a la entrada y la salida de un libro."""

    titulo: Titulo
    autor: Autor
    isbn: Isbn
    anio_publicacion: AnioPublicacion


class BookCreate(BookBase, EsquemaEntrada):
    """Datos para dar de alta un libro (cuerpo del POST). El id lo genera el servidor."""


class BookUpdate(EsquemaEntrada):
    """Datos para modificar parcialmente un libro (cuerpo del PATCH).

    Todos los campos son opcionales: solo se actualizan los que el cliente envía.
    """

    titulo: Titulo | None = None
    autor: Autor | None = None
    isbn: Isbn | None = None
    anio_publicacion: AnioPublicacion | None = None


class Book(BookBase):
    """Libro tal como lo devuelve la API, incluyendo el id generado por el servidor."""

    id: int = Field(description="Identificador generado por el servidor", gt=0)
