"""Repositorio genérico en memoria reutilizable por todas las entidades.

Centraliza las operaciones de almacenamiento (alta, baja, modificación y
consulta) para que cada entidad solo agregue sus búsquedas propias.
"""

from pydantic import BaseModel


class RepositorioEnMemoria[ModeloT: BaseModel]:
    """Almacena entidades en un diccionario indexado por id.

    El id lo asigna el repositorio con un contador incremental que nunca
    reutiliza valores. No conoce HTTP: cuando algo no existe devuelve None o
    False y deja que la capa superior decida cómo informarlo.
    """

    def __init__(self, tipo: type[ModeloT]) -> None:
        """Inicializa el repositorio vacío para el modelo de salida indicado."""
        self._tipo = tipo
        self._datos: dict[int, ModeloT] = {}
        self._proximo_id: int = 1

    def listar(self) -> list[ModeloT]:
        """Devuelve todas las entidades almacenadas."""
        return list(self._datos.values())

    def obtener(self, entidad_id: int) -> ModeloT | None:
        """Devuelve la entidad con ese id, o None si no existe."""
        return self._datos.get(entidad_id)

    def crear(self, datos: BaseModel) -> ModeloT:
        """Crea una entidad con los datos recibidos y un id nuevo, y la devuelve."""
        entidad = self._tipo(id=self._proximo_id, **datos.model_dump())
        self._datos[self._proximo_id] = entidad
        self._proximo_id += 1
        return entidad

    def actualizar(self, entidad_id: int, cambios: BaseModel) -> ModeloT | None:
        """Aplica solo los campos enviados y devuelve la entidad actualizada.

        Ignora los campos no enviados y los enviados en nulo.
        Devuelve None si la entidad no existe.
        """
        actual = self._datos.get(entidad_id)
        if actual is None:
            return None
        nuevo = actual.model_copy(
            update=cambios.model_dump(exclude_unset=True, exclude_none=True)
        )
        self._datos[entidad_id] = nuevo
        return nuevo

    def eliminar(self, entidad_id: int) -> bool:
        """Elimina la entidad y devuelve True, o False si no existía."""
        return self._datos.pop(entidad_id, None) is not None
