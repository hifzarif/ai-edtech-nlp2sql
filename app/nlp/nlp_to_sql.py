def generate_sql(question: str) -> str:
    question = question.lower()

    if "how many" in question and "python" in question:
        return """
        SELECT COUNT(*) as count
        FROM enrollments e
        JOIN courses c ON e.course_id = c.id
        WHERE c.name LIKE '%Python%'
        """

    elif "all students" in question:
        return "SELECT * FROM students"

    elif "all courses" in question:
        return "SELECT * FROM courses"

    elif "enrollments" in question:
        return "SELECT * FROM enrollments"

    return "SELECT * FROM students LIMIT 5"