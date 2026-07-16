def insert_forums(cursor, les_id: int, forums: list):
    for forum in forums:
        if not forum:
            continue

        cursor.execute("""
            INSERT INTO forums (les_id, after_summary, tema, opis_teme)
            VALUES (?, ?, ?, ?)
        """,
            les_id,
            forum.get("AfterSummary"),
            forum.get("Tema"),
            forum.get("OpisTeme")
        )
