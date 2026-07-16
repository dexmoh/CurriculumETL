def insert_summary(cursor, les_id, summary_id, summary_title):
    cursor.execute("""
        INSERT INTO summary (les_id, summary_id, summary_title)
        VALUES (?, ?, ?)
    """, les_id, summary_id, summary_title)
