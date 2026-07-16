def insert_google_videos_lvl1(cursor, les_id, durations: list[str]):
    for duration in durations:
        if not duration or duration == "":
            continue

        cursor.execute("""
            INSERT INTO google_videos_lvl1 (les_id, duration)
            VALUES (?, ?)
        """, les_id, duration)
