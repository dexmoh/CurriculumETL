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
        academic_year: str = "",
        author: str = ""
) -> list[Row]:
    if (not isinstance(course_code, str)) or (course_code is None):
        course_code = ""
    if (not isinstance(title, str)) or (title is None):
        title = ""
    if (not isinstance(lesson_number, str)) or (lesson_number is None):
        lesson_number = ""
    if (not isinstance(academic_year, str)) or (academic_year is None):
        academic_year = ""
    if (not isinstance(author, str)) or (author is None):
        author = ""

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
            academic_year LIKE ? AND
            lesson_author LIKE ?
        ORDER BY course_code ASC, lesson_number ASC
    """,
        f"%{course_code}%",
        f"%{title}%",
        f"%{lesson_number}%",
        f"%{academic_year}%",
        f"%{author}%"
    )

    return cursor.fetchall()

def get_lesson_by_id(cursor: Cursor, id: int) -> Row | None:
    if (not isinstance(id, int)) or (id < 1):
        return None

    cursor.execute("""
        SELECT
            id,
            course_code,
            title,
            academic_year,
            lesson_number,
            pdf_generated,
            lesson_author,
            naucno_polje
        FROM lesson
        WHERE id = ?
    """, id)

    return cursor.fetchone()
