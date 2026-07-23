import time
from pathlib import Path

import tkinter as tk
from tkinter import ttk

from database.db import get_connection
from database.transaction import TransactionManager
from database.repositories.lesson import search_lessons
from database.repositories.lesson import get_lesson_by_id
from database.repositories.lesson_version import get_lesson_version
from database.repositories.lesson_review import get_lesson_review
from database.repositories.overview import get_overview
from database.repositories.summary import get_summary
from database.repositories.forums import get_forums

WINDOW_TITLE: str     = "Lesson Search"
WINDOW_SIZE: str      = "1000x600"
WINDOW_ICON_PATH: str = "icon.png"
THEME: str            = "alt"

class GuiApp:
    def __init__(self):
        ### GUI WINDOW INIT ###
        self.root: tk.Tk = tk.Tk()
        self.root.geometry(WINDOW_SIZE)
        self.root.title(WINDOW_TITLE)
        self.root.bind("<Return>", self.on_enter_pressed)

        if THEME in ttk.Style().theme_names():
            ttk.Style().theme_use(THEME)

        # Window icon.
        if Path(WINDOW_ICON_PATH).is_file():
            self.root.iconphoto(
                True, tk.PhotoImage(file=WINDOW_ICON_PATH)
            )

        main_frame = tk.Frame(self.root, bd=4, relief=tk.GROOVE)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ### SEARCH PANEL ###
        search_frame = tk.Frame(main_frame, bd=4, relief=tk.GROOVE)
        search_frame.pack(side=tk.LEFT, anchor="n", padx=5, pady=5, ipadx=5, ipady=5)

        # Course code input.
        tk.Label(search_frame, anchor="w", width=14, text="COURSE CODE").grid(row=0, column=0)
        self.course_sterm = tk.StringVar()
        tk.Entry(
            search_frame, textvariable=self.course_sterm
        ).grid(row=0, column=1)

        # Title input.
        tk.Label(search_frame, anchor="w", width=14, text="TITLE").grid(row=1, column=0)
        self.title_sterm = tk.StringVar()
        tk.Entry(
            search_frame, textvariable=self.title_sterm
        ).grid(row=1, column=1)

        # Lesson number input.
        tk.Label(search_frame, anchor="w", width=14, text="LESSON NUMBER").grid(row=2, column=0)
        self.lesson_sterm = tk.StringVar()
        tk.Entry(
            search_frame, textvariable=self.lesson_sterm
        ).grid(row=2, column=1)

        # Year input.
        tk.Label(search_frame, anchor="w", width=14, text="YEAR").grid(row=3, column=0)
        self.year_sterm = tk.StringVar()
        tk.Entry(
            search_frame, textvariable=self.year_sterm
        ).grid(row=3, column=1)

        # Author input.
        tk.Label(search_frame, anchor="w", width=14, text="AUTHOR").grid(row=4, column=0)
        self.author_sterm = tk.StringVar()
        tk.Entry(
            search_frame, textvariable=self.author_sterm
        ).grid(row=4, column=1)

        # Search button.
        search_btn = tk.Button(
            search_frame,
            text="SEARCH",
            command=lambda: self.search()
        )

        search_btn.grid(row=5, column=1, pady=(5, 0), sticky="nsew")

        ### SEARCH RESULTS LABEL ###
        self.info_label = tk.Label(
            main_frame, anchor="center", width=100, text=""
        )
        self.info_label.pack(side=tk.BOTTOM)

        ### TREEVIEW PANEL ###
        self.tree = ttk.Treeview(main_frame, show="tree")
        self.tree.bind("<Control-c>", self.handle_copy)
        self.tree.tag_bind("lesson", "<<TreeviewOpen>>", self.on_row_expand)
        self.tree.tag_bind("lesson", "<<TreeviewClose>>", self.on_row_collapse)
        self.tree.tag_configure("lesson", foreground="maroon")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.LEFT, fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def run(self):
        self.root.mainloop()

    # Called when user presses the search button.
    def search(self):
        start_time = time.perf_counter()
        conn = get_connection()

        try:
            with TransactionManager(conn) as cursor:
                result = search_lessons(
                    cursor,
                    self.course_sterm.get(),
                    self.title_sterm.get(),
                    self.lesson_sterm.get(),
                    self.year_sterm.get(),
                    self.author_sterm.get()
                )

                self.tree.delete(*self.tree.get_children())

                if len(result) < 1:
                    self.tree.insert("", "end", text="No results.")

                for row in result:
                    id = row.id
                    if not id:
                        continue

                    course_code = get_sanitized(row.course_code)
                    lesson_number = get_sanitized(row.lesson_number)
                    academic_year = get_sanitized(row.academic_year)
                    title = get_sanitized(row.title, True)

                    self.tree.insert(
                        "", "end", id,
                        tags=["lesson"],
                        text=f"#{id} - {course_code} - {lesson_number} - {academic_year} - {title}"
                    )

                    self.tree.insert(id, "end", text="Loading...")

                self.info_label.config(
                    text=f"Found {len(result)} results in {round(time.perf_counter() - start_time, 2)} seconds."
                )
        finally:
            conn.close()

    # Called when user expands a lesson item.
    def on_row_expand(self, event):
        focus: str = self.tree.focus()
        if not focus:
            return

        lesson_id: int = 0
        try:
            lesson_id = int(focus)
        except ValueError:
            return

        conn = get_connection()

        try:
            with TransactionManager(conn) as cursor:
                lesson_data = get_lesson_by_id(cursor, lesson_id)
                if not lesson_data:
                    return

                self.tree.delete(*self.tree.get_children(focus))

                self.tree.insert(
                    focus, "end",
                    text=f"Author: {get_sanitized(lesson_data.lesson_author)}"
                )

                self.tree.insert(
                    focus, "end",
                    text=f"Science field: {get_sanitized(lesson_data.naucno_polje)}"
                )

                self.tree.insert(
                    focus, "end",
                    text=f"PDF generated: {get_sanitized(lesson_data.pdf_generated)}"
                )

                ### FILE INFO TAB ###
                version_data = get_lesson_version(cursor, lesson_id)
                if not version_data:
                    return

                file_info_tab: str = self.tree.insert(focus, "end", text="File Info")

                self.tree.insert(
                    file_info_tab, "end",
                    text=f"File ID: {get_sanitized(version_data.fileId, True)}"
                )

                review_data = get_lesson_review(cursor, version_data.id)
                if not review_data:
                    return

                self.tree.insert(
                    file_info_tab, "end",
                    text=f"JSON file name: {get_sanitized(review_data.json_file_name, True)}"
                )

                self.tree.insert(
                    file_info_tab, "end",
                    text=f"Drive file ID: {get_sanitized(review_data.drive_file_id, True)}"
                )

                self.tree.insert(
                    file_info_tab, "end",
                    text=f"Imported at: {get_sanitized(review_data.imported_at)}"
                )

                ### OVERVIEW TAB ###
                overview_data = get_overview(cursor, review_data.id)

                if overview_data:
                    overview_tab: str = self.tree.insert(focus, "end", text="Overview")

                    self.tree.insert(
                        overview_tab, "end",
                        text=f"ID: {get_sanitized(overview_data.overview_id)}"
                    )

                    self.tree.insert(
                        overview_tab, "end",
                        text=f"Title: {get_sanitized(overview_data.overview_title, True)}"
                    )

                ### SUMMARY TAB ###
                summary_data = get_summary(cursor, review_data.id)

                if summary_data:
                    summary_tab: str = self.tree.insert(focus, "end", text="Summary")

                    self.tree.insert(
                        summary_tab, "end",
                        text=f"ID: {get_sanitized(summary_data.summary_id)}"
                    )

                    self.tree.insert(
                        summary_tab, "end",
                        text=f"Title: {get_sanitized(summary_data.summary_title, True)}"
                    )

                ### FORUMS TAB ###
                forums_data = get_forums(cursor, review_data.id)

                if forums_data:
                    forums_tab: str = self.tree.insert(focus, "end", text="Forums")

                    for forum in forums_data:
                        if not forum:
                            continue

                        forum_id: str = self.tree.insert(
                            forums_tab, "end",
                            text=get_sanitized(forum.tema, True)
                        )

                        self.tree.insert(
                            forum_id, "end",
                            text=f"Description: {get_sanitized(forum.opis_teme, True)}"
                        )

                        self.tree.insert(
                            forum_id, "end",
                            text=f"After summary: {get_sanitized(forum.after_summary)}"
                        )
        finally:
            conn.close()

    # Called when user closes an opened lesson item.
    def on_row_collapse(self, event):
        focus: str = self.tree.focus()
        if not focus:
            return
        
        self.tree.delete(*self.tree.get_children(focus))
        self.tree.insert(focus, "end", text="Loading...")

    # Called when user presses enter.
    def on_enter_pressed(self, event):
        self.search()

    # Called when user presses Ctrl+C.
    def handle_copy(self, event):
        focus: str = self.tree.focus()
        if not focus:
            return

        text: str = self.tree.item(focus, "text")
        if not text:
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(text)

def get_sanitized(var, add_quotes: bool = False, if_none = "N/A"):
    if var is None:
        return if_none
    elif add_quotes:
        return f"\"{str(var)}\""
    else:
        return var

def main():
    app = GuiApp()
    app.run()

if __name__ == "__main__":
    main()
