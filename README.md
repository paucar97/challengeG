# Data Engineering Coding Challenge

## Descripción del Proyecto

Este proyecto es parte del reto de **Data Engineering** de **Globant**, cuyo objetivo es desarrollar una API que maneje la migración de datos desde archivos CSV hacia una base de datos SQL, así como exponer algunos endpoints para realizar consultas SQL sobre los datos cargados.

### Funcionalidades principales:

1. **Subida de archivos CSV**: La API permite subir archivos CSV con datos históricos de empleados, departamentos y trabajos, que se insertan en la base de datos.
2. **Inserción por lotes**: Los datos pueden ser cargados en lotes de hasta 1000 filas por solicitud.
3. **Consultas SQL**: La API expone endpoints que permiten consultar métricas como las contrataciones por trimestre y los departamentos que contrataron más empleados que el promedio.
4. **Variables de Entorno**: El proyecto utiliza un archivo `.env` para la configuración de variables sensibles como las credenciales de la base de datos.

## Requisitos

- **Python 3.12** o superior
- **Docker** (opcional, si deseas levantar la aplicación en un contenedor)
- **MySQL** o cualquier otra base de datos SQL que prefieras

## Instalación Local

### 1. Clonar el repositorio

Clona este repositorio en tu máquina local:

```bash
git clone https://github.com/usuario/proyecto.git
cd proyecto
```

### 2. Crear y activar un entorno virtual

Crea un entorno virtual en Python 3.12 y actívalo:

```bash
python3.12 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

Instala las dependencias desde el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en el directorio raíz con las variables de entorno necesarias para la base de datos:

```bash
DB_HOST=your_database_host
DB_PORT=3306
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

### 5. Ejecutar la aplicación localmente

Para ejecutar la aplicación localmente utilizando Uvicorn:

```bash
uvicorn app:app --reload
```

La aplicación estará disponible en: `http://127.0.0.1:8000`.

Puedes acceder a la documentación de la API generada automáticamente en:

Swagger UI: `http://127.0.0.1:8000/docs`
ReDoc: `http://127.0.0.1:8000/redoc`

## Uso con Docker

### 1. Construir la imagen Docker

Si prefieres levantar la aplicación con Docker, primero asegúrate de tener Docker instalado y luego construye la imagen:

```bash
docker build -t data-engineering-app .
```

### 2. Ejecutar el contenedor

Ejecuta el contenedor de Docker mapeando el puerto 8000:

```bash
docker run -d -p 8000:8000 --env-file .env data-engineering-app
```

Esto ejecutará la aplicación en `http://localhost:8000`.

## Endpoints Principales

### 1. Subida de archivos CSV:

POST `/upload/{file_type}`
Parámetro `file_type`: Puede ser `employee`, `department`, o `job`.
Envío del archivo CSV en el cuerpo de la solicitud usando `multipart/form-data`.

### 2. Consultar empleados contratados por trimestre:

GET `/hired_by_quarter/`

### 3. Consultar departamentos que contrataron más que la media:

GET `/departments_above_average/`
