from database.db import get_connection
from database.transaction import TransactionManager
from database.repositories.lesson_repository import insert_lesson
from database.repositories.version_repository import insert_lesson_version
from database.repositories.review_repository import insert_lesson_review
from database.repositories.lesson_other_stats import insert_lesson_other_stats
from database.repositories.yt_videos import insert_yt_videos
from database.repositories.yt_links import insert_yt_links
from database.repositories.google_videos import insert_google_videos
from database.repositories.google_videos_uvod import insert_google_videos_uvod
from database.repositories.google_videos_lvl1 import insert_google_videos_lvl1
from database.repositories.google_videos_lvl2 import insert_google_videos_lvl2
from database.repositories.google_videos_lvl3 import insert_google_videos_lvl3
from database.repositories.google_videos_lvl0 import insert_google_videos_lvl0
from database.repositories.summary import insert_summary
from database.repositories.overview import insert_overview
from database.repositories.forums import insert_forums

class ETLService:
    def process_file(self, json_data):
        conn = get_connection()

        try:
            with TransactionManager(conn) as cursor:
                lessons_data = {}
                if len(json_data["data"]["OtherStats"]["lessons"]) > 0:
                    lessons_data = json_data["data"]["OtherStats"]["lessons"][0]

                lesson_id = insert_lesson(
                    cursor,
                    json_data["data"].get("CourseCode"),
                    json_data["data"].get("Title"),
                    json_data["data"].get("Year"),
                    json_data["data"].get("Lesson"),
                    json_data["data"].get("Author"),
                    lessons_data.get("NaucnoPolje")
                )

                version_id = insert_lesson_version(
                    cursor,
                    lesson_id,
                    json_data.get("fileId")
                )

                review_id = insert_lesson_review(
                    cursor,
                    version_id,
                    json_data.get("driveFileName"),
                    json_data.get("driveFileId")
                )

                if lessons_data:
                    other_stats_id = insert_lesson_other_stats(cursor, review_id, lessons_data)

                    insert_yt_videos(cursor, other_stats_id, lessons_data.get("ytVideos", []))
                    insert_yt_links(cursor, other_stats_id, lessons_data.get("ytLinks", []))
                    insert_google_videos(cursor, other_stats_id, lessons_data.get("googleVideos", []))
                    insert_google_videos_uvod(cursor, other_stats_id, lessons_data.get("googleVideosUVOD", []))
                    insert_google_videos_lvl1(cursor, other_stats_id, lessons_data.get("googleVideosLvl1", []))
                    insert_google_videos_lvl2(cursor, other_stats_id, lessons_data.get("googleVideosLvl2", []))
                    insert_google_videos_lvl3(cursor, other_stats_id, lessons_data.get("googleVideosLvl3", []))
                    insert_google_videos_lvl0(cursor, other_stats_id, lessons_data.get("googleVideosLvl0", []))

                if "Summary" in json_data["data"] and json_data["data"]["Summary"]:
                    insert_summary(
                        cursor,
                        review_id,
                        json_data["data"]["Summary"].get("SummaryId"),
                        json_data["data"]["Summary"].get("SummaryTitle")
                    )

                if "Overview" in json_data["data"] and json_data["data"]["Overview"]:
                    insert_overview(
                        cursor,
                        review_id,
                        json_data["data"]["Overview"].get("OverviewId"),
                        json_data["data"]["Overview"].get("OverviewTitle")
                    )
                
                insert_forums(
                    cursor,
                    review_id,
                    json_data["data"].get("Forums", [])
                )
        finally:
            conn.close()
            print(f"Processed file: {json_data.get("driveFileName", "N/A")}")
