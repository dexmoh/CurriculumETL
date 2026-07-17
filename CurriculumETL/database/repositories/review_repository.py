def insert_lesson_review(
        cursor,
        lesson_version_id: int,
        json_file_name: str,
        drive_file_id: str
) -> int:
    cursor.execute("""
        INSERT INTO lesson_review (lesson_version_id, json_file_name, drive_file_id)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?)
    """, lesson_version_id, json_file_name, drive_file_id)

    return cursor.fetchone()[0]
