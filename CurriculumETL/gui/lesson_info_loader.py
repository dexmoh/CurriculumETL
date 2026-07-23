from pyodbc import Cursor
from tkinter import ttk

from database.repositories.lesson_version import get_lesson_version
from database.repositories.lesson_review import get_lesson_review
from database.repositories.lams_activities import get_activities
from database.repositories.lesson import get_lesson_by_id
from database.repositories.lesson_stats import get_stats
from database.repositories.overview import get_overview
from database.repositories.summary import get_summary
from database.repositories.forums import get_forums
from database.db import sanitize

# Load lesson info from the database and display it inside a Treeview.
def load_lesson_info(
        cursor: Cursor,
        lesson_id: int,
        tree: ttk.Treeview
):
    lesson_data = get_lesson_by_id(cursor, lesson_id)
    if not lesson_data:
        return

    tree.delete(*tree.get_children(lesson_id))

    tree.insert(
        lesson_id, "end",
        text=f"Author: {sanitize(lesson_data.lesson_author)}"
    )

    tree.insert(
        lesson_id, "end",
        text=f"Science field: {sanitize(lesson_data.naucno_polje)}"
    )

    tree.insert(
        lesson_id, "end",
        text=f"PDF generated: {sanitize(lesson_data.pdf_generated)}"
    )

    ### FILE INFO TAB ###
    version_data = get_lesson_version(cursor, lesson_id)
    if not version_data:
        return

    file_info_tab: str = tree.insert(lesson_id, "end", text="File Info")

    tree.insert(
        file_info_tab, "end",
        text=f"File ID: {sanitize(version_data.fileId, True)}"
    )

    review_data = get_lesson_review(cursor, version_data.id)
    if not review_data:
        return

    tree.insert(
        file_info_tab, "end",
        text=f"JSON file name: {sanitize(review_data.json_file_name, True)}"
    )

    tree.insert(
        file_info_tab, "end",
        text=f"Drive file ID: {sanitize(review_data.drive_file_id, True)}"
    )

    tree.insert(
        file_info_tab, "end",
        text=f"Imported at: {sanitize(review_data.imported_at)}"
    )

    ### OVERVIEW TAB ###
    overview_data = get_overview(cursor, review_data.id)

    if overview_data:
        overview_tab: str = tree.insert(lesson_id, "end", text="Overview")

        tree.insert(
            overview_tab, "end",
            text=f"ID: {sanitize(overview_data.overview_id)}"
        )

        tree.insert(
            overview_tab, "end",
            text=f"Title: {sanitize(overview_data.overview_title, True)}"
        )

    ### SUMMARY TAB ###
    summary_data = get_summary(cursor, review_data.id)

    if summary_data:
        summary_tab: str = tree.insert(lesson_id, "end", text="Summary")

        tree.insert(
            summary_tab, "end",
            text=f"ID: {sanitize(summary_data.summary_id)}"
        )

        tree.insert(
            summary_tab, "end",
            text=f"Title: {sanitize(summary_data.summary_title, True)}"
        )

    ### LAMS ACTIVITIES TAB ###
    activities_data = get_activities(cursor, review_data.id)

    if activities_data:
        activities_tab: str = tree.insert(lesson_id, "end", text="LAMS Activities")

        for activity in activities_data:
            if not activity:
                continue

            activity_id: str = tree.insert(
                activities_tab, "end",
                text=sanitize(activity.activity_title, True)
            )

            tree.insert(
                activity_id, "end",
                text=f"Tool content ID: {sanitize(activity.tool_content_id)}"
            )

            tree.insert(
                activity_id, "end",
                text=f"Tool display name: {sanitize(activity.tool_display_name, True)}"
            )

            tree.insert(
                activity_id, "end",
                text=f"Tool ID: {sanitize(activity.tool_id)}"
            )

            tree.insert(
                activity_id, "end",
                text=f"Parent: {sanitize(activity.parent)}"
            )

            tree.insert(
                activity_id, "end",
                text=f"Activity category ID: {sanitize(activity.activity_category_id)}"
            )

    ### FORUMS TAB ###
    forums_data = get_forums(cursor, review_data.id)

    if forums_data:
        forums_tab: str = tree.insert(lesson_id, "end", text="Forums")

        for forum in forums_data:
            if not forum:
                continue

            forum_id: str = tree.insert(
                forums_tab, "end",
                text=sanitize(forum.tema, True)
            )

            tree.insert(
                forum_id, "end",
                text=f"Description: {sanitize(forum.opis_teme, True)}"
            )

            tree.insert(
                forum_id, "end",
                text=f"After summary: {sanitize(forum.after_summary)}"
            )

    ### STATS TAB ###
    stats_data = get_stats(cursor, review_data.id)

    if stats_data:
        stats_tab: str = tree.insert(lesson_id, "end", text="Stats")

        tree.insert(
            stats_tab, "end",
            text=f"Total activity counter: {sanitize(stats_data.total_activity_counter)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Forum counter: {sanitize(stats_data.forum_counter)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Multiple choice counter: {sanitize(stats_data.multiple_choice_counter)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Assessment counter: {sanitize(stats_data.assessment_counter)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Q&A counter: {sanitize(stats_data.q_and_a_counter)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Activity after summary counter: {sanitize(stats_data.activity_after_summary_counter)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Forum after summary counter: {sanitize(stats_data.forum_after_summary_counter)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Number of predavanja: {sanitize(stats_data.no_ou_predavanja)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Number of pokazne vežbe: {sanitize(stats_data.no_ou_pokazne_vezbe)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Number of individualne vežbe: {sanitize(stats_data.no_ou_individualne_vezbe)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Number of zadatak za samostalni rad: {sanitize(stats_data.no_ou_zadatak_za_samostalni_rad)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Number of domaći zadatak: {sanitize(stats_data.no_ou_domaci_zadatak)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Number of projekat: {sanitize(stats_data.no_ou_projekat)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Has pokazne vežbe: {sanitize(stats_data.has_pokazne_vezbe)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Has individualne vežbe: {sanitize(stats_data.has_individualne_vezbe)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Has zadatak za samostalni rad: {sanitize(stats_data.has_zadatak_za_samostalni_rad)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Has domaći zadatak: {sanitize(stats_data.has_domaci_zadatak)}"
        )

        tree.insert(
            stats_tab, "end",
            text=f"Has projekat: {sanitize(stats_data.has_projekat)}"
        )
