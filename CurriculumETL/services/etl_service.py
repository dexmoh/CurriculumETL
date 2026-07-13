from database.connection import get_connection
from database.transaction import TransactionManager
from database.repositories.lesson_repository import insert_lesson
from database.repositories.version_repository import insert_lesson_version
from database.repositories.review_repository import insert_lesson_review
from parsers.lesson_parser import LessonParser


class ETLService:

    def process_file(self, file, json_data):

        parsed = LessonParser.parse(json_data)

        conn = get_connection()

        try:
            with TransactionManager(conn) as cursor:

                lesson_id = insert_lesson(
                    cursor,
                    parsed["course_code"],
                    parsed["lesson_code"]
                )

                version_id = insert_lesson_version(
                    cursor,
                    lesson_id,
                    parsed["title"],
                    parsed["school_year"]
                )

                review_id = insert_lesson_review(
                    cursor,
                    version_id,
                    file["name"],
                    file["id"]
                )

                print(f"Inserted review ID: {review_id}")

        finally:
            conn.close()
