# TP N°1 Python — ABM con FastAPI

API REST desarrollada con **FastAPI** y **Pydantic** para el Trabajo Práctico N°1.

- **Parte 1:** ABM completo de **Usuarios**: alta, baja, modificación, consulta por id y listado con filtro por estado.
- **Parte 2:** ABM completo de una entidad propia, **Libros**: alta, baja, modificación, consulta por id y búsqueda por autor y/o año.

Los datos se guardan **en memoria**: se pierden al reiniciar la aplicación y al iniciar se cargan datos de ejemplo.

## Requisitos

- **Python 3.12 o superior** (el proyecto usa la sintaxis de clases genéricas de Python 3.12).
- Git.

## Instalación

1. Clonar el repositorio y entrar a la carpeta:

   ```bash
   git clone https://github.com/GabiAguirre07/tp1-fastapi-abm.git
   cd tp1-fastapi-abm
   ```

2. Crear el entorno virtual:

   ```bash
   # Windows
   python -m venv .venv

   # macOS / Linux
   python3 -m venv .venv
   ```

3. Activarlo:

   ```bash
   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1

   # macOS / Linux
   source .venv/bin/activate
   ```

   > En Windows, si PowerShell indica que la ejecución de scripts está deshabilitada, ejecutar una vez
   > `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y volver a activar.

4. Instalar las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Ejecutar la aplicación

```bash
fastapi dev main.py
```

La API queda disponible en `http://127.0.0.1:8000`.

## Documentación interactiva (Swagger)

Con la aplicación levantada, abrir **http://127.0.0.1:8000/docs**.

Desde ahí se pueden probar todos los endpoints con **Try it out → Execute**. Los endpoints están agrupados en **Usuarios** y **Libros**.

También está disponible la documentación alternativa en `http://127.0.0.1:8000/redoc`.

## Endpoints

### Usuarios (`/users`)

| Método | Ruta               | Descripción                                                                                                            | Respuesta       |
| ------ | ------------------ | ---------------------------------------------------------------------------------------------------------------------- | --------------- |
| GET    | `/users`           | Lista los usuarios. Query param opcional `is_active` (`true` / `false`) para filtrar por estado; sin él devuelve todos | 200             |
| GET    | `/users/{user_id}` | Obtiene un usuario por id                                                                                              | 200 / 404       |
| POST   | `/users`           | Crea un usuario. El id lo genera el servidor                                                                           | 201 / 422       |
| PATCH  | `/users/{user_id}` | Modifica solo los campos enviados                                                                                      | 200 / 404 / 422 |
| DELETE | `/users/{user_id}` | Elimina un usuario                                                                                                     | 204 / 404       |

Campos: `name` (texto, 2 a 100 caracteres) e `is_active` (booleano, por defecto `true`).

### Libros (`/books`)

| Método | Ruta                | Descripción                                                                                                                              | Respuesta       |
| ------ | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | --------------- |
| GET    | `/books`            | Lista los libros. Query params opcionales y combinables: `autor` (coincidencia parcial, sin distinguir mayúsculas) y `anio` (año exacto) | 200             |
| GET    | `/books/{libro_id}` | Obtiene un libro por id                                                                                                                  | 200 / 404       |
| POST   | `/books`            | Crea un libro. El id lo genera el servidor                                                                                               | 201 / 422       |
| PATCH  | `/books/{libro_id}` | Modifica solo los campos enviados                                                                                                        | 200 / 404 / 422 |
| DELETE | `/books/{libro_id}` | Elimina un libro                                                                                                                         | 204 / 404       |

Campos (5): `id` (generado por el servidor), `titulo`, `autor`, `isbn` (10 o 13 dígitos, sin guiones) y `anio_publicacion` (entre 1450 y el año actual).

## Ejemplos para probar

Crear un usuario (`POST /users`):

```json
{ "name": "Ana Gómez" }
```

Desactivar un usuario (`PATCH /users/3`):

```json
{ "is_active": false }
```

Crear un libro (`POST /books`):

```json
{
  "titulo": "Martín Fierro",
  "autor": "José Hernández",
  "isbn": "9789500391788",
  "anio_publicacion": 1872
}
```

Buscar libros: `GET /books?autor=borges` o `GET /books?autor=borges&anio=1949`.

## Estructura del proyecto

```
├── main.py                 # Crea la app y registra los routers
├── models/                 # Esquemas Pydantic (validación de entrada y salida)
│   ├── base.py             # Configuración común a todos los esquemas
│   ├── users.py
│   └── books.py
├── repositories/           # Almacenamiento en memoria
│   ├── base.py             # Repositorio genérico reutilizable (alta, baja, modificación, consulta)
│   ├── users.py
│   └── books.py
└── routers/                # Endpoints HTTP
    ├── comun.py            # Utilidades compartidas (error 404)
    ├── users.py
    └── books.py
```

Cada capa tiene una única responsabilidad: los **routers** atienden HTTP, los **repositorios** guardan los datos y los **modelos** los validan. El repositorio genérico permite que cada entidad nueva solo agregue sus búsquedas propias.

## Lint y chequeo de tipos

Con el entorno virtual activado:

```bash
pyright
pip install pycodestyle
python -m pycodestyle .
```
