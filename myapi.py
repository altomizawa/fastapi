from typing import Optional
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from bson import ObjectId
from bson.errors import InvalidId
from db import users_collection

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
    country: str

class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    country: Optional[str] = None

@app.get("/")
def get_all_students():
    user = users_collection.find()
    if not user:
        return {"message": "User not found"}
    res = []
    for user in users_collection.find():
        res.append({"name": user["name"], "age": user["age"], "country": user["country"], "id": str(user["_id"])})
    return {"success":"true", "data": res}

@app.get("/get-student/{student_id}")
def get_student(student_id: str = Path(..., description="MongoDB ObjectId of the student")):
    try:
        object_id = ObjectId(student_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid student_id format")

    student = users_collection.find_one({"_id": object_id})
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return {
        "name": student.get("name"),
        "age": student.get("age"),
        "country": student.get("country"),
        "id": str(student["_id"]),
    }

@app.get("/get-by-name/student_id")
def get_student(*, name: Optional[str] = Path(..., description="The name of the student you want to get"), age: int = Path(..., description="The age of the student you want to get", gt=0), student_id: int = Path(..., description="The ID of the student you want to get", gt=0)):
    for student_id in students:
        if students[student_id]["name"].lower() == name.lower():
          return students[student_id]
    return {"error": "Student not found"}

@app.post("/create-student")
def create_student(student: Student):
    try:
        users_collection.insert_one(student.dict())
        return {"message": "Student created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/update-student/{student_id}")
def update_student(student_id: str, student: UpdateStudent):
    try:
        object_id = ObjectId(student_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid student_id format")
    try:
        existing_student = users_collection.find_one({"_id": object_id})
        if existing_student is None:
            raise HTTPException(status_code=404, detail="Student not found")  
        update_data = {k: v for k, v in student.dict().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        users_collection.update_one({"_id": object_id}, {"$set": update_data})
        updated_student = users_collection.find_one({"_id": object_id})
        return {"status": "success", "data": {
            "name": updated_student.get("name"),
            "age": updated_student.get("age"),
            "country": updated_student.get("country"),
            "id": str(updated_student["_id"])}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/delete-student/{student_id}")
def delete_student(student_id: str):
    try:
        object_id = ObjectId(student_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid student_id format")
    result = users_collection.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}