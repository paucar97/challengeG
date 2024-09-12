import os
import json
import pandas as pd

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from io import StringIO
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

load_dotenv()

app = FastAPI()

RDS_ENDPOINT = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
USERNAME = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
DATABASE = os.getenv("DB_NAME")


DATABASE_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{RDS_ENDPOINT}:{PORT}/{DATABASE}"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    department = Column(String(100), nullable=True)

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    job = Column(String(100), nullable=True)

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    datetime = Column(String(100), nullable=True)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=True)

Base.metadata.create_all(engine)

@app.post("/upload_file/{file_type}")
async def upload_file(file_type: str,file: UploadFile = File(...)):
    try:

        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')),keep_default_na=False,skiprows=0,header=None)
        df.replace('',value=None,inplace=True)
        if file_type == "employee":
            df.columns = ['id','name','datetime','department_id','job_id']
            df['datetime'] = df['datetime'].apply(lambda x: datetime.strptime(x,'%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S') if x is not None else x)
            process_and_insert_data(df, Employee)
        elif file_type == "department":
            df.columns = ['id','department']
            process_and_insert_data(df, Department)
        elif file_type == "job":
            df.columns = ['id','job']
            process_and_insert_data(df, Job)
        else:
            raise HTTPException(status_code=400, detail="Tipo de archivo no válido")

        return {"message": "Archivo cargado y procesado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar el archivo: {str(e)}")

def process_and_insert_data(df: pd.DataFrame, model):
    batch_size = 1000
    data = df.to_dict(orient='records')
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        session.bulk_insert_mappings(model, batch)
        session.commit()

@app.get("/hired_by_quarter/")
async def hired_by_quarter():
    try:
        query = """
            SELECT d.department, j.job, 
                SUM(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 1 THEN 1 ELSE 0 END) AS Q1,
                SUM(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 2 THEN 1 ELSE 0 END) AS Q2,
                SUM(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 3 THEN 1 ELSE 0 END) AS Q3,
                SUM(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 4 THEN 1 ELSE 0 END) AS Q4
            FROM employees e
            JOIN departments d ON e.department_id = d.id
            JOIN jobs j ON e.job_id = j.id
            WHERE EXTRACT(YEAR FROM e.datetime) = 2021
            GROUP BY department, job
            ORDER BY department, job;
        """
        df = pd.read_sql_query(query,engine)
        return json.loads(df.to_json(orient="records"))
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/departments_above_average/")
async def departments_above_average():
    try:
        query = """
            WITH department_hires AS (
                SELECT department_id, COUNT(*) AS hires
                FROM employees
                WHERE EXTRACT(YEAR FROM datetime) = '2021'
                GROUP BY department_id
            ),
            avg_hires AS (
                SELECT AVG(hires) AS avg_hires FROM department_hires
            )
            SELECT d.id, d.department, dh.hires
            FROM department_hires dh
            JOIN departments d ON dh.department_id = d.id
            where dh.hires > (select avg_hires from avg_hires)
            ORDER BY dh.hires DESC;
        """
        df = pd.read_sql_query(query,engine)

        return json.loads(df.to_json(orient="records"))
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



# Ejecutar la app con Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)