from database.repositories.learning_object_subobjects import insert_learning_object_subobjects

def insert_learning_objects(cursor, les_id: int, learning_objects: list) -> int:
    for object in learning_objects:
        if not object:
            continue

        cursor.execute("""
            INSERT INTO learning_objects (
                les_id,
                number,
                learning_content_id,
                title,
                classification,
                difficulty_level,
                keywords,
                audience,
                learning_duration,
                type,
                curriculum,
                domain,
                learning_outcomes,
                competences,
                knowledge_topic,
                learning_object_author,
                school_year,
                faculty
            )
            OUTPUT INSERTED.id
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            les_id,
            object.get("Number"),
            object.get("LearningContentId"),
            object.get("Title"),
            object.get("Classification"),
            object.get("DifficultyLevel"),
            object.get("Keywords"),
            object.get("Audience"),
            object.get("LearningDuration"),
            object.get("Type"),
            object.get("Curriculum"),
            object.get("Domain"),
            object.get("LearningOutcomes"),
            object.get("Competences"),
            object.get("KnowledgeTopic"),
            object.get("Author"),
            object.get("SchoolYear"),
            object.get("Faculty")
        )

        object_id: int = cursor.fetchone()[0]
        subobjects = object.get("Subobjects", [])

        if subobjects:
            insert_learning_object_subobjects(
                cursor,
                object_id,
                subobjects
            )

        return object_id
