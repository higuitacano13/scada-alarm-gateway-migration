# SCADA Alarm Gateway & Migrator

## 📌 Descripción General

Este repositorio contiene la solución desarrollada para la prueba técnica **“The SCADA Alarm Gateway & Migrator”**, cuyo objetivo es diseñar y construir un sistema completo que permita:

- Generar datasets representativos de alarmas SCADA con problemas típicos de calidad de datos.
- Ingerir, limpiar y normalizar dicha información.
- Persistir los datos normalizados en una base de datos relacional (SQL Server).
- Exponer una API REST en Python (FastAPI) para la consulta de alarmas y métricas agregadas.

La solución fue diseñada poniendo especial énfasis en **criterio técnico, buenas prácticas, separación de responsabilidades, escalabilidad y testabilidad**, tal como se solicita en el documento de la prueba.

---

## 🏗️ Arquitectura de la Solución

La aplicación sigue una arquitectura en capas, inspirada en principios de *Clean Architecture*:

```
API (FastAPI)
 ├── Routers (alarms, metrics, ingestion)
 ├── Schemas (Pydantic)
 └── Dependencias

Application Layer
 ├── Services

Data Access Layer
 ├── Repositories (SQLAlchemy)
 └── DB Session

Ingestion Layer (ETL)
 ├── Generator
 ├── Cleaner
 └── Loader

Database
 └── SQL Server
```

---

## 📁 Estructura del Proyecto

```
app/
├── api/
│   ├── alarms.py
│   ├── metrics.py
│   ├── ingestion.py
├── core/
│   └── config.py
├── db/
│   ├── base.py
│   └── session.py
├── dependencies/
│   └── alarm_dependencies.py
├── ingestion/
│   ├── generator.py
│   ├── cleaner.py
│   └── loader.py
├── models/
│   ├── alarm_event_model.py
│   ├── alarm_severity_model.py
│   ├── schemas.py
│   └── source_system_model.py
├── repositories/
│   └── alarm_repository.py
├── services/
│   └── alarm_service.py
├── tests/
│   ├── test_alarm_repository.py
│   ├── test_alarm_service.py
│   ├── test_alarm.py
│   ├── test_cleaner.py
│   ├── test_generator.py
│   ├── test_ingestion.py
│   ├── test_loader.py
│   └── test_metrics-py
├── main.py
├── pytest.ini
├── requirements.txt
└── README.md
```

## ✅ Requisitos Previos

Para ejecutar el proyecto localmente se requiere:

- Python **3.10 o superior**
- SQL Server (local o remoto)
- Driver **ODBC Driver 18 for SQL Server**
- Git

Opcional:
- Postman (para pruebas manuales)
- Docker (para la siguiente sección del proyecto)

``
## ▶️ Ejecución Local (sin Docker)

### 1. Clonar el repositorio
```bash
git clone https://github.com/higuitacano13/scada-alarm-gateway-migration.git
cd scada-alarm-gateway
```

### 2. Crear y activar entorno virtual
```bash
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\\Scripts\\activate    # Windows
```
### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
DB_SERVER=localhost
DB_NAME=scada
DB_USER=sa
DB_PASSWORD=your_password
DB_DRIVER=ODBC Driver 18 for SQL Server

DATASET_RAW_PATH=./datasets/raw
DATASET_PROCESSED_PATH=./datasets/processed
```

### 5. Ejecutar la API
```bash
uvicorn app.main:app --reload
```

---

## 🧪 Dataset de Prueba

El sistema incluye un **generador de datasets SCADA** que crea archivos JSON y CSV con características realistas y problemas intencionales de calidad de datos:

- Valores nulos.
- Formatos de fecha heterogéneos.
- Severidades inconsistentes (strings, números, valores inválidos).
- Campos opcionales ausentes.

---

## 🔄 Pipeline de Ingestión (ETL)

### 1. Generación
Se generan archivos JSON y CSV que representan un histórico de alarmas industriales.

### 2. Limpieza y Normalización
- Parseo de fechas desde múltiples formatos.
- Normalización de severidad.
- Descarte de registros inválidos.

### 3. Carga
- Inserción masiva en SQL Server.
- Almacenamiento del `raw_payload_path` para trazabilidad.

---

## 🚀 API REST (FastAPI)
A continuación se presenta una guía práctica para consumir los principales endpoints del sistema, incluyendo ejemplos en `curl`.
**Nota:** Para ejecutar los ejemplos, la API debe estar corriendo localmente en `http://localhost:8000`.

🔄 **Ingestion**

Estos endpoints permiten generar y cargar datasets SCADA como parte de la prueba técnica y las pruebas end‑to‑end.

1️⃣ Generar dataset de alarmas
### Ejemplo
```bash
curl -X POST "http://localhost:8000/api/v1/ingestion/generate-dataset?size=5000&file_format=json"
```

### Parámetros (query)
<img width="750" height="154" alt="image" src="https://github.com/user-attachments/assets/19821475-fd3a-411f-848f-88f55edae7b0" />

### Respuesta Esperada
```bash
{
  "message": "Dataset generado correctamente",
  "records": 5000,
  "format": "json",
  "path": "datasets/generated/alarms_generated_20240417_120000.json"
}
```
  
2️⃣ Cargar dataset en la base de datos

### Ejemplo
```bash
curl -X POST http://localhost:8000/api/v1/ingestion/load-dataset \
  -F "file=@alarms_generated_20240417_120000.json"
```

### Parámetros (query)
<img width="662" height="131" alt="image" src="https://github.com/user-attachments/assets/4808f242-7438-447c-9926-c5cd37fe044f" />

### Respuesta Esperada
```bash
{
  "message": "Dataset procesado",
  "file": "alarms_generated_20260419_034004.csv",
  "inserted": 276,
  "failed_db": 0,
  "invalid": 724,
  "total": 1000
}
```

🚨 **Alarms**

Endpoints para consultar alarmas normalizadas con filtros y paginación.

3️⃣ Consultar alarmas
  
### Ejemplo
```bash
curl "http://localhost:8000:8000/api/v1/alarms/?from_date=2026-01-01%2000%3A00%3A00.000&to_date=2026-04-19%2000%3A00%3A00.000&severity=1&tag=VALVE_02&limit=2&offset=0"
```

### Parámetros (query)
<img width="657" height="326" alt="image" src="https://github.com/user-attachments/assets/ea9bae6b-62ec-487a-9502-57136b1e5289" />

### Respuesta Esperada
```bash
{
  "data": [
    {
      "tag": "VALVE_02",
      "description": "Alarm triggered",
      "severity": 1,
      "status": "ACTIVE",
      "event_time": "2026-04-18T23:24:47",
      "id": 350,
      "source_system": "SCADA_A",
      "created_at": "2026-04-19T00:38:04.291000"
    },
    {
      "tag": "VALVE_02",
      "description": "Alarm triggered",
      "severity": 1,
      "status": "ACTIVE",
      "event_time": "2026-04-18T23:24:47",
      "id": 401,
      "source_system": "SCADA_A",
      "created_at": "2026-04-19T00:38:04.407000"
    }
  ],
  "total": 157,
  "limit": 2,
  "offset": 0
}
```
 
📊 **Metrics**

Endpoints para métricas agregadas sobre el histórico de alarmas.
4️⃣ Top tags con mayor número de alarmas

### Ejemplo
```bash
curl -X POST "http://localhost:8000/api/v1/metrics/top-tags?from_date=2026-01-01%2000%3A00%3A00.000&to_date=2026-04-19%2000%3A00%3A00.000&limit=10"
```

### Parámetros (query)
<img width="633" height="189" alt="image" src="https://github.com/user-attachments/assets/487ab80f-e706-4cb0-b6ec-5888c2b3c62b" />

### Respuesta Esperada
```bash
{
  "data": [
    {
      "tag": "PUMP_01",
      "total_events": 530
    },
    {
      "tag": "VALVE_02",
      "total_events": 502
    },
    {
      "tag": "TEMP_03",
      "total_events": 494
    }
  ]
}

```
---

## ✅ Pruebas

La solución incluye pruebas automatizadas usando **pytest**:

```bash
pytest
```

---

---

