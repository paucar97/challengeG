# Data Engineering Coding Challenge

## Project Description

This project is part of Globant's Data Engineering challenge, aiming to develop an API that handles data migration from CSV files to an SQL database, and exposes endpoints to perform SQL queries on the loaded data.

### Main Features:

1. **CSV File Upload**: The API allows uploading CSV files with historical data of employees, departments, and jobs, which are inserted into the database.

2. **Batch Insertion**: Data can be uploaded in batches of up to 1000 rows per request.

3. **SQL Queries**: The API exposes endpoints that allow querying metrics like hires per quarter and departments that hired more employees than the average.

4. **Environment Variables**: The project uses a .env file for configuring sensitive variables such as database credentials.

## Requirements

- **Python 3.12** or higher
- **Docker** (optional, if you wish to run the application in a container)
- **MySQL** or any other SQL database of your choice

## Local Installation

### 1. Clone the Repository

Clone this repository on your local machine:

```bash
git clone https://github.com/paucar97/challengeG.git
cd challengeG
```

### 2. Create and Activate a Virtual Environment

Create a virtual environment in Python 3.12 and activate it:

```bash
python3.12 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install the dependencies from the `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory with the necessary environment variables for the database:

```bash
DB_HOST=your_database_host
DB_PORT=3306
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

### 5. Run the Application Locally

To run the application locally using Uvicorn:

```bash
uvicorn app:app --reload
```

The application will be available at: `http://127.0.0.1:8000`.

You can access the automatically generated API documentation at:

Swagger UI: `http://127.0.0.1:8000/docs`
ReDoc: `http://127.0.0.1:8000/redoc`

## Using Docker

### 1. Build the Docker Image

```bash
docker build -t my-app-g .
```

### 2. Ejecutar el contenedor

```bash
docker run -d -p 8080:8000 --env-file .env my-app-g
```

Esto ejecutará la aplicación en `http://localhost:8080`.

## Main Endpoints

### 1. Upload CSV Files:

- POST `/upload/{file_type}`

- `file_type` parameter: Can be `employee`, `department`, or `job`.

### 2. Query Employees Hired by Quarter:

- GET `/hired_by_quarter/`

### 3. Query Departments that Hired More than Average:

- GET `/departments_above_average/`
