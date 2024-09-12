# challengeG

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
