def insert_overview(cursor, les_id, overview_id, overview_title):
    cursor.execute("""
        INSERT INTO overview (les_id, overview_id, overview_title)
        VALUES (?, ?, ?)
    """, les_id, overview_id, overview_title)
