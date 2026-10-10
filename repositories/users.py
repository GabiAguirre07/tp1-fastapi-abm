"""Repositorio en memoria de la entidad Usuario.

Define el repositorio con las búsquedas propias de usuarios, crea la única
instancia que comparte toda la aplicación y expone la función que la provee
a los endpoints mediante Depends.
"""

from models.users import User, UserCreate
from repositories.base import RepositorioEnMemoria


class RepositorioUsuarios(RepositorioEnMemoria[User]):
    """Repositorio de usuarios: agrega el filtro por estado al repositorio genérico."""

    def __init__(self) -> None:
        """Inicializa el repositorio para trabajar con el modelo User."""
        super().__init__(User)

    def listar_por_estado(self, is_active: bool | None = None) -> list[User]:
        """Devuelve los usuarios con el estado indicado, o todos si es None."""
        if is_active is None:
            return self.listar()
        return [user for user in self.listar() if user.is_active == is_active]


# Instancia única: los datos viven en memoria y deben compartirse entre requests.
_repositorio = RepositorioUsuarios()
for nombre in ("Juan Perez", "Pepe Sanchez"):
    _repositorio.crear(UserCreate(name=nombre))


def obtener_repositorio_usuarios() -> RepositorioUsuarios:
    """Provee el repositorio de usuarios a los endpoints (usar con Depends)."""
    return _repositorio
