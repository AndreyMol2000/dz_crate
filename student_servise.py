import asyncio
from scheme import Student
from sqlalchemy import select , func , delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

class StudetService(): 
    def __init__(self , db_url):
        self.db_url = db_url

    def get_async_session(self):
        engine = create_async_engine(self.db_url)

        return  sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False
    )

    async def add_students(self):
        Session = self.get_async_session()
        with open("students.csv", "r", encoding="utf-8") as file:
        # Пропускаем заголовок, если он есть
            lines = file.readlines()
        if len(lines) > 0:
            first_line = lines[0].strip()
            # Более надежная проверка на заголовок
            if not first_line.replace(',', '').strip().isdigit():
                print("Пропускаем строку заголовков")
                lines = lines[1:]  # Удаляем заголовок из дальнейшей обработки
            
            async with Session() as db:
                for line in lines:
                    line = line.strip().split(',')
                    student = Student(
                            last_name=line[0].strip(),
                            name=line[1].strip(),
                            faculty=line[2].strip(),  # Используем faculty вместо faq
                            kours=line[3].strip(),
                            score=int(line[4].strip())
                    )
                    db.add(student)
                await db.commit()
                print(f"Данные успешно добавлены. Обработано {len(lines)} строк")

    async def get_students(self):
        session = self.get_async_session()
        
        async with session() as db:
            result = await db.execute(select(Student))  
            students = result.scalars().all()
            
            print("\nСписок студентов:")
            for student in students: 
                print(f"{student.id}: {student.last_name} {student.name}, {student.faculty}, {student.kours} - {student.score}")
            
            return students
    
    async def get_student(self , id):

        session = self.get_async_session()
        
        async with session() as db:
            result = await db.execute(select(Student).where(Student.id == id))  
            students = result.scalars().all()
            for student in students: 
                print(f"{student.id}: {student.last_name} {student.name}, {student.faculty}, {student.kours} - {student.score}")
            
            return students

    async def get_student_by_faculty(self , faculty):

        session = self.get_async_session()
        
        async with session() as db:
            result = await db.execute(select(Student).where(Student.kours == faculty))  
            students = result.scalars().all()
            for student in students: 
                print(f"{student.id}: {student.last_name} {student.name}, {student.faculty}, {student.kours} - {student.score}")
            
            return students

    async def get_kours(self):
        async with self.get_async_session()() as db:
            result = await db.execute(
            select(Student.kours)
            .distinct()
            .order_by(Student.kours)
        )
        kours_list = result.scalars().all()
        
        print("Уникальные курсы:", *{kours for kours in kours_list}, sep="\n- ")
        return kours_list

    async def get_avg_facult(self, faculty):
        async with self.get_async_session() as db:  # Предполагаем, что `get_async_session` возвращает AsyncSession
        # Запрос среднего балла (AVG) для указанного факультета
            avg_score = await db.execute(
            select(func.avg(Student.score))
            .where(Student.faculty == faculty)  # Фильтр по факультету
        )
        avg_result = avg_score.scalar()  # Получаем одно значение (средний балл)  
        
        # Возвращаем средний балл и список студентов (или только avg_result, если не нужен список)
        return {"avg_score": avg_result}

    async def del_student(self , id):

        session = self.get_async_session()
        
        async with session() as db:
            result = await db.execute(delete(Student).where(Student.id == id))  
            return result


async def runner():
    PG_URL = "postgresql+asyncpg://postgres:132@localhost:5432/postgres"

    student_service = StudetService(PG_URL)
    res = await student_service.del_student(2)
    print(res)

if __name__ == "__main__":
    asyncio.run(runner())