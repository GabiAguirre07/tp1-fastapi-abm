"""Clases base compartidas por los esquemas Pydantic de todas las entidades.

Centralizan la configuración común para que cada entidad la obtenga por herencia.
"""

from pydantic import BaseModel, ConfigDict


class EsquemaBase(BaseModel):
    """Base de todos los esquemas: recorta espacios en los textos antes de validar."""

    model_config = ConfigDict(str_strip_whitespace=True)


class EsquemaEntrada(EsquemaBase):
    """Base de los esquemas de entrada: además rechaza campos no declarados."""

    model_config = ConfigDict(extra="forbid")
