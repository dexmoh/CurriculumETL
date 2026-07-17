def insert_lesson_stats(cursor, les_id: int, stats: dict):
    cursor.execute("""
        INSERT INTO lesson_stats (
            les_id,
            total_activity_counter,
            forum_counter,
            multiple_choice_counter,
            assessment_counter,
            q_and_a_counter,
            activity_after_summary_counter,
            forum_after_summary_counter,
            no_ou_predavanja,
            no_ou_pokazne_vezbe,
            no_ou_individualne_vezbe,
            no_ou_zadatak_za_samostalni_rad,
            no_ou_domaci_zadatak,
            no_ou_projekat,
            has_pokazne_vezbe,
            has_individualne_vezbe,
            has_zadatak_za_samostalni_rad,
            has_domaci_zadatak,
            has_projekat
        )
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        les_id,
        stats.get("TotalActivityCounter", 0),
        stats.get("ForumCounter", 0),
        stats.get("MultipleChoiceCounter", 0),
        stats.get("AssessmentCounter", 0),
        stats.get("QandACounter", 0),
        stats.get("ActivityAfterSummaryCounter", 0),
        stats.get("ForumAfterSummaryCounter", 0),
        stats.get("noOuPredavanja", 0),
        stats.get("noOuPokazneVezbe", 0),
        stats.get("noOuIndividualneVezbe", 0),
        stats.get("noOuZadatakZaSamostalniRad", 0),
        stats.get("noOuDomaciZadatak", 0),
        stats.get("noOuProjekat", 0),
        stats.get("hasPokazneVezbe", False),
        stats.get("hasIndividualneVezbe", False),
        stats.get("hasZadatakZaSamostalniRad", False),
        stats.get("hasDomaciZadatak", False),
        stats.get("hasProjekat", False)
    )

    lesson_stats_id: int = cursor.fetchone()[0]
