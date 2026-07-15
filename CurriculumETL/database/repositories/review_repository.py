def insert_lesson_review(cursor, lesson_version_id, json_file_name, drive_file_id):
    cursor.execute("""
        INSERT INTO lesson_review (lesson_version_id, json_file_name, drive_file_id)
        OUTPUT INSERTED.id
        VALUES (?, ?, ?)
    """, lesson_version_id, json_file_name, drive_file_id)
    return cursor.fetchone()[0]
