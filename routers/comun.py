"""Utilidades HTTP compartidas por todos los routers."""

from fastapi import HTTPException, status


def no_encontrado(recurso: str, recurso_id: int) -> HTTPException:
    """Construye el error 404 para un recurso inexistente."""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{recurso} {recurso_id} no encontrado",
    )
