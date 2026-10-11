"""Punto de entrada de la API: crea la aplicación y registra los routers."""

from fastapi import FastAPI

from routers import books, users

# Create the application instance
app = FastAPI()

# Routers de cada entidad
app.include_router(users.router)
app.include_router(books.router)


# Define a GET route for the root URL
@app.get("/")
def read_root():
    mensaje = "Primer clase de FastAPI"
    return {"message": mensaje}
