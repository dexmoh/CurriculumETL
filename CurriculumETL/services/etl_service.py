from database.db import get_connection
from database.transaction import TransactionManager
from database.repositories.lesson_repository import insert_lesson
from database.repositories.version_repository import insert_lesson_version
from database.repositories.review_repository import insert_lesson_review

class ETLService:
    def process_file(self, json_data):
        conn = get_connection()

        try:
            with TransactionManager(conn) as cursor:
                lesson_id = insert_lesson(
                    cursor,
                    json_data["data"].get("CourseCode", None),
                    json_data["data"].get("Title", None),
                    json_data["data"].get("Year", None),
                    json_data["data"].get("Lesson", None),
                    json_data["data"].get("Author", None),
                    json_data["data"]["OtherStats"]["lessons"][0].get("NaucnoPolje", None)
                )

                version_id = insert_lesson_version(
                    cursor,
                    lesson_id,
                    json_data.get("fileId", None)
                )

                review_id = insert_lesson_review(
                    cursor,
                    version_id,
                    json_data.get("driveFileName", None),
                    json_data.get("driveFileId", None)
                )
        finally:
            conn.close()
            print(f"Processed file: {json_data.get("driveFileName", "N/A")}")
