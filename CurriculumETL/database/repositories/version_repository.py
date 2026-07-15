def insert_lesson_version (cursor, lesson_id, file_id):
    cursor.execute("""
        INSERT INTO lesson_version (les_id, fileId)
        OUTPUT INSERTED.id
        VALUES (?, ?)
    """, lesson_id, file_id)
    return cursor.fetchone()[0]
