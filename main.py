from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os

app = FastAPI()

# CORS: allow all origins (browser access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

DATA_FILE = "datao.json"

# Load data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
            if not isinstance(data, dict):
                data = {}
        except:
            data = {}
else:
    data = {}

# Pydantic model for Student
class Student(BaseModel):
    roll: str
    name: str
    fname: str
    clas: str
    age: str
    subjects: list = []
    marks: list = []

# Save data to file
def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# ---------- Add Student ----------
@app.post("/add_student")
def add_student(student: Student):
    if student.roll in data:
        raise HTTPException(status_code=400, detail="Roll already exists")
    data[student.roll] = {
        "name": student.name,
        "fname": student.fname,
        "classs": student.clas,
        "age": student.age,
        "siname": student.subjects,
        "simark": student.marks
    }
    save_data()
    return {"message": "Student added successfully"}

# ---------- Get All Students ----------
@app.get("/get_all")
def get_all():
    return data

# ---------- Search Student ----------
@app.get("/search/{roll}")
def search_student(roll: str):
    if roll not in data:
        raise HTTPException(status_code=404, detail="Roll not found")
    return data[roll]

# ---------- Update Student ----------
@app.put("/update_student/{roll}")
def update_student(roll: str, student: Student):
    if roll not in data:
        raise HTTPException(status_code=404, detail="Roll not found")
    info = data[roll]
    info["name"] = student.name
    info["fname"] = student.fname
    info["classs"] = student.clas
    info["age"] = student.age
    info["siname"] = student.subjects
    info["simark"] = student.marks
    save_data()
    return {"message": "Student updated successfully"}

# ---------- Delete Student ----------
@app.delete("/delete_student/{roll}")
def delete_student(roll: str):
    if roll not in data:
        raise HTTPException(status_code=404, detail="Roll not found")
    del data[roll]
    save_data()
    return {"message": "Student deleted successfully"}