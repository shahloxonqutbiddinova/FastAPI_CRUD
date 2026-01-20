from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Date, ForeignKey, DECIMAL, INTEGER
from datetime import datetime, date
from typing import List

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key = True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique = True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    birth_date: Mapped[date] = mapped_column(Date, nullable = True)
    password: Mapped[str] = mapped_column(String(200))


    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(primary_key = True)
    bio: Mapped[str] = mapped_column(String(500))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique = True)

    user: Mapped["User"] = relationship(back_populates="prodiles", uselist=False)
    books: Mapped[List["Book"]] = relationship(back_populates="author")

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(100))
    author_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"))

    author: Mapped["Profile"] = relationship(back_populates = "books")

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    bith_date: Mapped[date] = mapped_column(DateTime, nullable = True)

    course: Mapped["StudenyCourse"] = relationship(back_populates = "Student")

class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(DECIMAL(10,2))
    duration: Mapped[int] = mapped_column(INTEGER)

    students: Mapped["StudentCourse"] = relationship(back_populates = "course")

class StudentCourse(Base):
    __tablename__ = "student_courses"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), primary_key = True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), primary_key=True)

    student: Mapped["Student"] = relationship(back_populates = "courses")
    course: Mapped["Course"] = relationship(back_populates="students")