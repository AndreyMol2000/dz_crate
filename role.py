from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from student_servise import StudetService

role_router = APIRouter()
PG_URL = "postgresql+asyncpg://postgres:132@localhost:5432/postgres"
student_service = StudetService(PG_URL)

@role_router.get("/students/{id}", status_code=HTTPStatus.OK)
async def get_student(id: int):
    student = await student_service.get_student(id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@role_router.get("/students", status_code=HTTPStatus.OK)
async def get_all_students():
    return await student_service.get_students()

@role_router.get("/faculties/{faculty}/students", status_code=HTTPStatus.OK)
async def get_students_by_faculty(faculty: str):
    return await student_service.get_student_by_faculty(faculty)

@role_router.get("/courses", status_code=HTTPStatus.OK)
async def get_courses():
    return await student_service.get_kours()

@role_router.get("/faculties/{faculty}/average", status_code=HTTPStatus.OK)
async def get_faculty_average(faculty: str):
    return await student_service.get_avg_facult(faculty)

@role_router.delete("/students/{id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_student(id: int):
    await student_service.del_student(id)
    return {"message": "Student deleted"}