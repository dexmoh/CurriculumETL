def insert_google_videos_uvod(cursor, les_id, durations: list[str]):
    for duration in durations:
        if not duration or duration == "":
            continue

        cursor.execute("""
            INSERT INTO google_videos_uvod (les_id, duration)
            VALUES (?, ?)
        """, les_id, duration)
