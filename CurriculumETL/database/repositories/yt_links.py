def insert_yt_links(cursor, les_id: int, links: list[str]):
    for link in links:
        if not link or link == "":
            continue

        cursor.execute("""
            INSERT INTO yt_links (les_id, url)
            VALUES (?, ?)
        """, les_id, link)
