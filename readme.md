

# API FastAPI - Configuración y Ejecución Local

Este documento describe cómo configurar, ejecutar y probar la API Librería desarrollada con **FastAPI** de manera local.

## **Requisitos Previos**
Asegúrate de tener instalados los siguientes componentes en tu entorno local:

- **Python 3.9+**  
- **Git**  
- **Virtualenv** (opcional, pero recomendado)
- **PostgreSQL/MySQL/SQLite** (según la base de datos que utilice tu proyecto)
- **Pip** (Administrador de paquetes de Python)


## **Configuración del Entorno**

### 1. Crear un entorno virtual (opcional pero recomendado)

```bash
py -m venv venv
```
o

```bash
python -m venv venv
```

Activa el entorno virtual:

- **Windows: (cmd)**  
  ```bash
  .\venv\Scripts\activate
  ```
  **(Git Bash)**
  ```bash
  source venv/Scripts/activate
  ```

- **macOS/Linux:**  
  ```bash
  source venv/bin/activate
  ```

### 2. Instalar dependencias
Ejecutar en la ruta al nivel de app/ y tests/ 

```bash
pip install -r requirements.txt
```

---

### 3. Configurar Variables de Entorno

Crea un archivo `.env` en el directorio raíz del proyecto a nivel de app/ con las siguientes variables de entorno. Asegúrate de reemplazar los valores con tu configuración:

```ini
# Archivo .env

# URL de la base de datos
DATABASE_URL=sqlite:///./library.db #default sqlite
#DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/nombre_base_datos #Ejemplo postgres

# Variables de seguridad
SECRET_KEY=tu_clave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## **Ejecución del Proyecto Localmente**

Ejecuta el servidor de desarrollo de FastAPI:

```bash
uvicorn app.main:app --reload
```

Esto iniciará el servidor en `http://127.0.0.1:8000`. La opción `--reload` permite recargar automáticamente el servidor cuando se realicen cambios en el código.

---

## **Pruebas**
Puedes ejecutar las pruebas con `pytest` en el directorio al nivel de app y tests:

```bash
pytest
```
**Con Información de covertura**
```bash
pytest --cov=app tests
```
---

---
## **Acceso a la Documentación Interactiva**

La documentación interactiva de la API está disponible en Swagger UI:

- [Swagger UI](http://127.0.0.1:8000/docs)
- [Redoc](http://127.0.0.1:8000/redoc)

Aquí podrás ver todos los endpoints de la API, las estructuras de datos esperadas y ejemplos de solicitudes y respuestas.

---

## **Guía para el Uso de la API**  
El flujo de uso de la API sigue un orden lógico para garantizar el correcto funcionamiento del sistema:  

1. **Crear Autores**  
   - Antes de registrar libros, se deben crear los autores.  
   - Consulta el endpoint de creación en Swagger para más detalles.  

2. **Registrar Libros**  
   - Una vez que existan autores, se pueden registrar libros asociados a ellos.  

3. **Registrar Usuarios**  
   - Crea un usuario proporcionando un correo y una contraseña.  

4. **Obtener Token de Autenticación**  
   - Usa el endpoint `users/token` con el correo y contraseña del usuario para obtener un `access_token`.  
   - El token es necesario para los siguientes pasos.  

5. **Prestar Libros**  
   - Para prestar un libro, deben existir autores, libros y un usuario válido.  
   - Se debe incluir el token en el encabezado `Authorization`.  

6. **Devolver Libros**  
   - Para devolver un libro, el usuario debe haberlo prestado previamente.  
   - También se requiere el token de autenticación en el encabezado.  

### **Importante:**  
El encabezado `Authorization` **no funciona desde Swagger UI**. Para probar los servicios protegidos (`/loans/borrow` y `/loans/return`), es necesario utilizar una herramienta externa como Postman o Curl.  

---  

## **Ejemplo de Solicitudes con Curl**  

### **Prestar un Libro**  
```bash  
curl --location --request POST 'http://127.0.0.1:8000/loans/borrow/1' \
--header 'Authorization: Bearer tokenGenerado' \
--header 'Content-Type: application/json'  
```  

### **Devolver un Libro**  
```bash  
curl --location --request POST 'http://127.0.0.1:8000/loans/return/1' \
--header 'Authorization: Bearer tokenGenerado' \
--header 'Content-Type: application/json'  
```  

Este flujo asegura que todas las acciones se realicen en el orden correcto y con las dependencias necesarias. Para más detalles sobre cada endpoint y sus parámetros, consulta la documentación interactiva en Swagger UI.  

---

## **Estructura del Proyecto**

La estructura básica del proyecto es la siguiente:

```
📂 app
 ┣ 📂 routers
 ┣ 📂 schemas
 ┣ 📜 __init__.py
 ┣ 📜 models.py
 ┣ 📜 main.py
 ┣ 📜 auth.py
 ┣ 📜 database.py
📜 .env
📜 alembic.ini
📜 requirements.txt
📂 tests

---
