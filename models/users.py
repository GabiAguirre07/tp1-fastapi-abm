"""Esquemas Pydantic de la entidad Usuario.

Define los modelos de entrada (alta y modificación) y de salida de la API,
junto con las reglas de validación compartidas entre ellos.
"""

from typing import Annotated

from pydantic import Field

from models.base import EsquemaBase, EsquemaEntrada

# Tipo reutilizable: nombre de usuario con sus reglas de validación.
NombreUsuario = Annotated[
    str,
    Field(
        min_length=2,
        max_length=100,
        description="Nombre completo del usuario",
        examples=["Juan Perez", "Pía", "Lu"],
    ),
]


class UserBase(EsquemaBase):
    """Campos comunes a la entrada y la salida de un usuario.

    No se usa directamente en los endpoints: es la base de UserCreate y User.
    """

    name: NombreUsuario
    is_active: bool = Field(
        default=True, description="Indica si el usuario está activo"
    )


class UserCreate(UserBase, EsquemaEntrada):
    """Datos para dar de alta un usuario (cuerpo del POST).

    No incluye el id porque lo genera el servidor.
    Rechaza campos no declarados para que el cliente no pueda enviar datos inesperados.
    """


class UserUpdate(EsquemaEntrada):
    """Datos para modificar parcialmente un usuario (cuerpo del PATCH).

    Todos los campos son opcionales: solo se actualizan los que el cliente envía.
    No hereda de UserBase para no arrastrar la obligatoriedad de name ni el valor por defecto de is_active.
    """

    name: NombreUsuario | None = None
    is_active: bool | None = None


class User(UserBase):
    """Usuario tal como lo devuelve la API, incluyendo el id generado por el servidor."""

    id: int = Field(description="Identificador generado por el servidor", gt=0)
