from pyodbc import Cursor
from pyodbc import Row

def insert_lesson(
        cursor: Cursor,
        course_code: str,
        title: str,
        academic_year: str,
        lesson_number: str,
        lesson_author: str,
        naucno_polje: str
) -> int:
    cursor.execute("""
        INSERT INTO lesson (course_code, title, academic_year, lesson_number, lesson_author, naucno_polje)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?, ?, ?)
    """, course_code, title, academic_year, lesson_number, lesson_author, naucno_polje)

    return cursor.fetchone()[0]

def search_lessons(
        cursor: Cursor,
        course_code: str = "",
        title: str = "",
        lesson_number: str = "",
        academic_year: str = ""
) -> list[Row]:
    if not course_code:
        course_code = ""
    if not title:
        title = ""
    if not lesson_number:
        lesson_number = ""
    if not academic_year:
        academic_year = ""

    cursor.execute("""
        SELECT TOP (500)
            id,
            course_code,
            title,
            academic_year,
            lesson_number,
            pdf_generated,
            lesson_author,
            naucno_polje
        FROM lesson
        WHERE
            course_code LIKE ? AND
            title LIKE ? AND
            lesson_number LIKE ? AND
            academic_year LIKE ?
        ORDER BY course_code ASC, lesson_number ASC
    """,
        f"%{course_code}%",
        f"%{title}%",
        f"%{lesson_number}%",
        f"%{academic_year}%"
    )

    return cursor.fetchall()
