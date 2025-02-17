from fastapi import FastAPI
from .database import engine, Base
from .routers import users, authors, books, loans

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
# Configura el middleware de CORS
app.add_middleware(
     CORSMiddleware,
    allow_origins=["*"],  # Cambiar "*" por los dominios específicos en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
)


# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Incluir routers
app.include_router(users.router)
app.include_router(authors.router)
app.include_router(books.router)
app.include_router(loans.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library API!"}