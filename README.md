# Student API

A simple REST API built with [FastAPI](https://fastapi.tiangolo.com/) to manage student records.

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn

## Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install fastapi
```

## Running the API

```bash
fastapi dev myapi.py
```

The API will be available at `http://127.0.0.1:8000`.  
Interactive docs (Swagger UI) at `http://127.0.0.1:8000/docs`.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check / welcome message |
| `GET` | `/get-student/{student_id}` | Get a student by ID |
| `GET` | `/get-by-name/student_id` | Search a student by name and age |
| `POST` | `/create-student/{student_id}` | Create a new student |
| `PUT` | `/update-student/{student_id}` | Update an existing student |
| `DELETE` | `/delete-student/{student_id}` | Delete a student |

## Student Schema

```json
{
  "name": "string",
  "age": 0,
  "year": "string"
}
```
