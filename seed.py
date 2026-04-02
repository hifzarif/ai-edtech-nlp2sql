from app.database import Base, engine, SessionLocal
from app.models import Student, Course, Enrollment
from datetime import datetime
import random

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear old data (optional but useful)
    db.query(Enrollment).delete()
    db.query(Student).delete()
    db.query(Course).delete()
    db.commit()

    # Students
    students = [
        Student(name=f"Student{i}", grade=random.choice(["A", "B", "C"]), created_at=datetime.now())
        for i in range(10)
    ]
    db.add_all(students)

    # Courses
    courses = [
        Course(name="Python Basics", category="Programming"),
        Course(name="Advanced Python", category="Programming"),
        Course(name="Math", category="Academic"),
        Course(name="AI", category="Tech"),
        Course(name="Data Science", category="Tech"),
    ]
    db.add_all(courses)

    db.commit()

    # Enrollments
    enrollments = []
    for i in range(20):
        enrollments.append(
            Enrollment(
                student_id=random.randint(1, 10),
                course_id=random.randint(1, 5),
                enrolled_at=datetime.now()
            )
        )

    db.add_all(enrollments)
    db.commit()

    db.close()

    print("✅ Database seeded successfully!")

if __name__ == "__main__":
    seed_data()