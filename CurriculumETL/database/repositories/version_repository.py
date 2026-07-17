def insert_lesson_version (cursor, les_id: int, file_id: str) -> int:
    cursor.execute("""
        INSERT INTO lesson_version (les_id, fileId)
        OUTPUT INSERTED.id
        VALUES (?, ?)
    """, les_id, file_id)

    return cursor.fetchone()[0]
