# DEM\_API: CRUD de SampleData con FastAPI y PostgreSQL

Este proyecto ofrece una API REST para gestionar registros de muestra (`SampleData`) utilizando **FastAPI**, **SQLAlchemy** y **PostgreSQL**.

## 📋 Requisitos Previos

* **Docker** y **Docker Compose** (versión 3.8+).
* **Python 3.11** (si deseas ejecutar localmente sin Docker).

## 🗂️ Estructura del proyecto

```
DEM_api/
├── Dockerfile_api             # Imagen Docker para la API
├── docker-compose.yml         # Orquestación de servicios (API + PostgreSQL)
├── db/
│   └── initdb/
│       └── init.sql           # Script de inicialización de la base de datos
├── data/
│   └── sample.csv             # Datos de ejemplo para carga inicial
├── ingest/
│   └── load_sample.py         # Script para cargar `sample.csv` en la BD
└── api/
    ├── main.py                # Definición de la API y endpoints
    ├── crud.py                # Operaciones CRUD con SQLAlchemy
    ├── models.py              # Modelos ORM (SQLAlchemy)
    ├── schemas.py             # Esquemas Pydantic para validación
    ├── requirements.txt       # Dependencias Python
    ├── test_crud.py           # Pruebas unitarias para CRUD
    └── test_api.py            # Pruebas de integración de la API
```

## 🚀 Configuración y despliegue con Docker

1. Clona este repositorio:`git clone https://github.com/tu_usuario/DEM_api.git`
2. Levanta los contenedores:
```bash
docker-compose up -d --build
```
Se crearán dos servicios:
 * **db**: Base de datos PostgreSQL (puerto 5432).
```
POSTGRES_USER: postgres
POSTGRES_PASSWORD: postgres
POSTGRES_DB: postgres
```
 * **PgAdmin**: Para verificacion de la base de datos. [http://localhost:5050/](http://localhost:5050/)

```
PGADMIN_DEFAULT_EMAIL: admin@example.com
PGADMIN_DEFAULT_PASSWORD: postgres
```
 * **api**: Servicio FastAPI (puerto 8000).
4. Verifica que ambos servicios estén corriendo:<br>
```bash
docker-compose ps
```
5. La API estará disponible en [http://localhost:8000](http://localhost:8000).

---
## :dependabot: Endpoints disponibles

Puedes consultarlos tambien en [http://localhost:8000/docs](http://localhost:8000/docs)

| Método | Ruta          | Descripción                               |
| ------ | ------------- | ----------------------------------------- |
| POST   | `/items/`     | Crea un nuevo registro.                   |
| GET    | `/items/`     | Lista todos los registros (filtros). |
| GET    | `/items/{id}` | Obtiene un registro por su `id`.          |
| PUT    | `/items/{id}` | Actualiza un registro existente.          |
| DELETE | `/items/{id}` | Elimina un registro existente.            |

**Parámetros de filtrado en GET `/items/`:**

* `skip` (int): registros a omitir.
* `limit` (int): límite de resultados.
* `first_name`, `last_name`, `department`, `city`: coincidencia parcial.
* `state`: código de estado (2 letras).

---

## 📋 Pruebas

Se incluyen dos conjuntos de pruebas automatizadas para garantizar la calidad y el correcto funcionamiento de la capa de acceso a datos (CRUD) y de la API REST.

**1. Pruebas unitarias para CRUD (api/test_crud.py)**

Objetivo: Verificar que las operaciones básicas de creación, lectura, actualización y eliminación funcionan correctamente a nivel de modelo y base de datos.
Herramientas: pytest, sesión de prueba de SQLAlchemy con base de datos en memoria o contenedor dedicado.

Casos testeados:
* **Create:** Inserta un SampleData nuevo y comprueba que se devuelve un objeto con sus atributos correctamente asignados.
* **Read (get_by_id, get_all, get_by_email):** Recupera los registros recién creados y valida que los datos coinciden con los esperados.
* **Update:** Modifica campos de un registro existente y verifica que los cambios se persisten.
* **Delete:** Elimina un registro y comprueba que ya no aparece en la base de datos (get_by_id retorna None).
  
**2. Pruebas de integración de la API (api/test_api.py)**

Objetivo: Asegurar que los endpoints HTTP exponen correctamente los recursos y respetan los contratos.
Herramientas: pytest, httpx.AsyncClient (o TestClient de FastAPI).

Escenario de prueba:
* **POST /items/:** Envía un JSON con datos válidos y comprueba que responde 201 Created con el registro insertado.
* **GET /items/:** Solicita la lista completa y valida la presencia del elemento creado.
* **GET /items/{id}:** Accede a un registro concreto y compara la respuesta con los datos esperados.
* **PUT /items/{id}:** Envía un JSON con cambios de campos y verifica 200 OK y contenido actualizado.
* **DELETE /items/{id}:** Elimina un registro existente y comprueba 204 No Content; un GET posterior retorna 404 Not Found.

```bash
# Ejecutar todas las pruebas
docker-compose exec app bash
pytest
```

---

## 💻 Acceso al contenedor de PostgreSQL

Para conectarte al contenedor y ejecutar consultas manuales:

```bash
docker-compose exec db psql -U postgres -d postgres
```

---

## Estructura de la base de datos

La tabla `sample_data` se crea con el script `db/initdb/init.sql`:

```sql
CREATE TABLE sample_data (
  id          SERIAL,
  first_name  VARCHAR(100) NOT NULL,
  last_name   VARCHAR(100) NOT NULL,
  company_name VARCHAR(255),
  address     TEXT,
  city        VARCHAR(100),
  state       CHAR(2) CHECK (state ~ '^[A-Za-z]{2}$'),
  zip         VARCHAR(10),
  phone1      VARCHAR(20),
  phone2      VARCHAR(20),
  email       VARCHAR(255) NOT NULL,
  department  VARCHAR(100),
  PRIMARY KEY (first_name, last_name, email)
);
```

---

## 
Alan Alexis Zavala Mendoza
