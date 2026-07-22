from pyodbc import Cursor

def insert_lams_activities(cursor: Cursor, les_id: int, activities: list):
    for activity in activities:
        if not activity:
            continue

        cursor.execute("""
            INSERT INTO lams_activities (
                les_id,
                activity_title,
                tool_content_id,
                parent,
                activity_category_id,
                tool_display_name,
                tool_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            les_id,
            activity.get("ActivityTitle"),
            activity.get("ToolContentId"),
            activity.get("Parent"),
            activity.get("ActivityCategoryId"),
            activity.get("ToolDisplayName"),
            activity.get("ToolId")
        )
