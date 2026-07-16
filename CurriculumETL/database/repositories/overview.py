def insert_overview(cursor, les_id: int, overview_id: str, overview_title: str):
    cursor.execute("""
        INSERT INTO overview (les_id, overview_id, overview_title)
        VALUES (?, ?, ?)
    """, les_id, overview_id, overview_title)
