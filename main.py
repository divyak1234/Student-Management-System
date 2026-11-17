
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from fastapi.responses import RedirectResponse

import sqlite3

def get_conn():
    connection = sqlite3.connect("students0.db")
    return connection

def create_tb():
    connection = get_conn()
    cursor = connection.cursor()

    q = """
    CREATE TABLE IF NOT EXISTS students0 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        marks INTEGER,
        course TEXT,
        image TEXT,
        status INTEGER
    )
    """

    cursor.execute(q)
    connection.commit()
    connection.close()

create_tb()


templates = Jinja2Templates(
    directory="templates"
)

app = FastAPI()


class Student(BaseModel):
    name: str = Field(max_length=20, min_length=4)
    age: int = Field(ge=20, le=60)
    gender: str
    marks: int = Field(ge=21, le=100)
    course: str
    image: str
    status: int = Field(ge=0, le=1)


@app.get("/")
def home(req: Request):

    connection = get_conn()
    cursor = connection.cursor()

    q = "SELECT * FROM students0"

    cursor.execute(q)
    students0 = cursor.fetchall()

    connection.close()

    return templates.TemplateResponse(
        request=req,
        name="home.html",
        context={"stds": students0}
    )


@app.get("/students/add")
def send_std_form(req: Request):

    return templates.TemplateResponse(
        request=req,
        name="add-std.html",
        context={}
    )


@app.get("/students/{std_id}")
def get_student(req: Request, std_id: int):

    connection = get_conn()
    cursor = connection.cursor()

    q = "SELECT * FROM students0 WHERE id = ?"

    cursor.execute(q, (std_id,))
    students0 = cursor.fetchone()

    connection.close()

    if students0 is None:
        return {"msg": "Student not found"}

    return templates.TemplateResponse(
        request=req,
        name="single-std.html",
        context={"std": students0}
    )

@app.post("/std/delete/{std_id}")
def delete_std(std_id: int):

    connection = get_conn()
    cursor = connection.cursor()

    q = "DELETE FROM students0 WHERE id = ?"

    cursor.execute(q, (std_id,))

    connection.commit()
    connection.close()

    return RedirectResponse(
        url="/",
        status_code=303
    )


@app.post("/students/add")
def create_std(
    name: str = Form(),
    age: int = Form(),
    gender: str = Form(),
    marks: int = Form(),
    course: str = Form(),
    image: str = Form(),
    status: int = Form()
):

    Student_obj = Student(
        name=name,
        age=age,
        gender=gender,
        marks=marks,
        course=course,
        image=image,
        status=status
    )

    values = (
        Student_obj.name,
        Student_obj.age,
        Student_obj.gender,
        Student_obj.marks,
        Student_obj.course,
        Student_obj.image,
        Student_obj.status
    )

    connection = get_conn()
    cursor = connection.cursor()

    q = """
    INSERT INTO students0
    (name, age, gender, marks, course, image, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    cursor.execute(q, values)

    connection.commit()
    connection.close()

    return RedirectResponse(
        url="/",
        status_code=303
    )


@app.get("/students/edit/{std_id}")
def edit_std(req: Request, std_id: int):

    connection = get_conn()
    cursor = connection.cursor()

    q = "SELECT * FROM students0 WHERE id = ?"

    cursor.execute(q, (std_id,))

    student = cursor.fetchone()

    connection.close()

    if student is None:
        return {"msg": "Student not found"}

    return templates.TemplateResponse(
        request=req,
        name="edit-std.html",
        context={"std": student}
    )


@app.post("/students/edit/{std_id}")
def update_std(
    std_id : int,
    name: str = Form(),
    age: int = Form(),
    gender: str = Form(),
    marks: int = Form(),
    course: str = Form(),
    image: str = Form(),
    status: int = Form()
):

    Student_obj = Student(
        name=name,
        age=age,
        gender=gender,
        marks=marks,
        course=course,
        image=image,
        status=status
    )


    connection = get_conn()
    cursor = connection.cursor()

    q = """
    UPDATE students0
    SET name = ?,
    age =?,
    gender = ?,
    marks = ?,
    course = ?,
    image = ?,
    status = ? where id = ?
    """
    cursor.execute(q, (std_id,Student_obj.name,Student_obj.age,Student_obj.gender,Student_obj.marks,Student_obj.course,Student_obj.image,Student_obj.status))
    
    
    connection.commit()
    connection.close()

    return RedirectResponse(
        url="/",
        status_code=303
    )