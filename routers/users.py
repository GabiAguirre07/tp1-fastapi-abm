"""Endpoints HTTP de la entidad Usuario.

Traduce las peticiones HTTP a operaciones del repositorio de usuarios y
decide los códigos de respuesta. No contiene lógica de almacenamiento.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from models.users import User, UserCreate, UserUpdate
from repositories.users import RepositorioUsuarios, obtener_repositorio_usuarios

router = APIRouter(prefix="/users", tags=["Usuarios"])

# Repositorio inyectado por FastAPI en cada endpoint que lo declare.
RepoUsuarios = Annotated[RepositorioUsuarios, Depends(obtener_repositorio_usuarios)]


def _no_encontrado(user_id: int) -> HTTPException:
    """Construye el error 404 para un usuario inexistente."""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Usuario {user_id} no encontrado",
    )


@router.get("")
def listar_usuarios(repo: RepoUsuarios, is_active: bool | None = None) -> list[User]:
    """Lista los usuarios. Si se indica is_active, filtra por ese estado."""
    return repo.listar_por_estado(is_active)


@router.get("/{user_id}")
def obtener_usuario(user_id: int, repo: RepoUsuarios) -> User:
    """Devuelve un usuario por id. Responde 404 si no existe."""
    usuario = repo.obtener(user_id)
    if usuario is None:
        raise _no_encontrado(user_id)

    return usuario


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_usuario(datos: UserCreate, repo: RepoUsuarios) -> User:
    """Crea un usuario. El id lo asigna el servidor."""
    return repo.crear(datos)


@router.patch("/{user_id}")
def actualizar_usuario(user_id: int, cambios: UserUpdate, repo: RepoUsuarios) -> User:
    """Modifica solo los campos enviados. Responde 404 si no existe."""
    usuario = repo.actualizar(user_id, cambios)
    if usuario is None:
        raise _no_encontrado(user_id)

    return usuario


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(user_id: int, repo: RepoUsuarios) -> None:
    """Elimina un usuario. Responde 204 sin cuerpo, o 404 si no existe."""
    if not repo.eliminar(user_id):
        raise _no_encontrado(user_id)
