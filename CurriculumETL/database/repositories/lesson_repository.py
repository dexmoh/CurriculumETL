from database.db import get_connection

def insert_lesson(cursor, course_code: str, title: str, academic_year: str, lesson_number: str, lesson_author: str, naucno_polje: str):
    cursor.execute("""
        INSERT INTO lesson (course_code, title, academic_year, lesson_number, lesson_author, naucno_polje)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?, ?, ?)
    """, course_code, title, academic_year, lesson_number, lesson_author, naucno_polje)
    return cursor.fetchone()[0]

def get_lesson_id_by_code(code: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM lesson
        WHERE code = ?
    """, code)

    row = cursor.fetchone()

    conn.close()

    return row[0] if row else None