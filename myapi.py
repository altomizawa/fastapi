from typing import Optional
from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {
        "name": "John", 
        "age": 17,
        "year": "year 12"
    },
    2: {
        "name": "Jane", 
        "age": 16,
        "year": "year 11"
    },
    3: {
        "name": "Jack", 
        "age": 18,
        "year": "year 13"
    }
}

class Student(BaseModel):
    name: str
    age: int
    year: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

@app.get("/")
def index():
    return {"name": "First Data API"}

@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(..., description="The ID of the student you want to get", gt=0)):
   if student_id not in students:
        return {"error": "Student not found"}
   return students[student_id]

@app.get("/get-by-name/student_id")
def get_student(*, name: Optional[str] = Path(..., description="The name of the student you want to get"), age: int = Path(..., description="The age of the student you want to get", gt=0), student_id: int = Path(..., description="The ID of the student you want to get", gt=0)):
    for student_id in students:
        if students[student_id]["name"].lower() == name.lower():
          return students[student_id]
    return {"error": "Student not found"}

@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student exists"}
    
    students[student_id] = student
    return students[student_id]

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students or student_id <= 0:
        return {"error": "Student not found"}
    if student.name != None:
        students[student_id]["name"] = student.name
    if student.age != None:
        students[student_id]["age"] = student.age
    if student.year != None:
        students[student_id]["year"] = student.year
    return students[student_id]

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"error": "Student not found"}
    del students[student_id]
    return {"message": "Student deleted successfully"}