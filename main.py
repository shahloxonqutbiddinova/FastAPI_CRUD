from fastapi import FastAPI, Path, Depends
from typing import Annotated
from database import Base, engine, SessionLocal, get_db
import models
from schemas import StudentSchema, CourseSchema
from sqlalchemy.orm import Session



app = FastAPI(title = "My First API")
Base.metadata.create_all(bind=engine)

@app.get(path='/users/{user_id}/')
async def first_view(user_id: Annotated[int, Path(ge=0)]):
    return {"message": "My first api", "user_id": user_id}

@app.post(path="/create-student/")
async def create_student(student:StudentSchema):
    with SessionLocal() as session:
        student_db = models.Student()
        student_db.name = student.name
        student_db.bith_date = student.birth_date

        session.add(student_db)
        session.commit()
        session.refresh(student_db)
    return {"student": student_db}


@app.get(path ="/students")
async def get_all_student(db: Session = Depends(get_db)):
    students = db.query(models.Student).filter(models.Student.id == 2).first()

    return students

@app.put(path="/update-student/{student_id}")
async def update_student(student_id: int, student: StudentSchema, db: Session = Depends(get_db)):
    student_db = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student_db is not None:
        student_db.name = student.name
        student_db.birth_date = student.birth_date
        db.commit()
        db.refresh(student_db)
        return student_db
    return {"message": "Student not found."}

@app.delete(path="/delete-student/{student_id}")
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    student_db = db.query(models.Student).filter(models.Student.id == student_id).first()
    if student_db is not None:
        db.delete(student_db)
        db.commit()
        return {"message": "Student deleted."}
    return {"message": "Student not found."}


@app.post(path="/create_course/")
async def create_course(course: CourseSchema):
    with SessionLocal() as session:
        course_db = models.Course()
        course_db.name = course.name
        course_db.price = course.price
        course_db.duration = course.duration

        session.add(course_db)
        session.commit()
        session.refresh(course_db)
    return {"course": course_db}


@app.get(path="/courses")
async def get_all_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).all()
    return courses


@app.put(path="/update-course/{course_id}")
async def update_course(course_id: int, course: CourseSchema, db: Session = Depends(get_db)):
    course_db = db.query(models.Course).filter(models.Course.id == course_id).first()
    if course_db is not None:
        course_db.name = course.name
        course_db.price = course.price
        course_db.duration = course.duration
        db.commit()
        db.refresh(course_db)
        return course_db
    return {"message": "Course not found."}


@app.delete(path="/delete-course/{course_id}")
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    course_db = db.query(models.Course).filter(models.Course.id == course_id).first()
    if course_db is not None:
        db.delete(course_db)
        db.commit()
        return {"message": "Course deleted."}
    return {"message": "Course not found."}