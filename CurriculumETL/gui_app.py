import tkinter as tk
from tkinter import ttk

from database.db import get_connection
from database.transaction import TransactionManager
from database.repositories.lesson import search_lessons

WINDOW_TITLE: str = "Lesson Search"

class GuiApp:
    def __init__(self):
        self.root: tk.Tk = tk.Tk()
        self.root.geometry("1000x600")
        self.root.title(WINDOW_TITLE)

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

        search_btn = tk.Button(
            search_frame,
            text="Search",
            command=lambda: self.search()
        )

        search_btn.grid(row=5, column=1, sticky="nsew")

        ### TREEVIEW PANEL ###
        self.tree = ttk.Treeview(main_frame, show="tree")
        self.tree.bind("<<TreeviewOpen>>", self.on_row_expand)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.LEFT, fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def run(self):
        self.root.mainloop()

    def search(self):
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
                        text=f"#{id} - {course_code} - {lesson_number} - {academic_year} - {title}"
                    )

                    self.tree.insert(
                        id, "end",
                        text=f"Author: {get_sanitized(row.lesson_author)}"
                    )

                    self.tree.insert(
                        id, "end",
                        text=f"Science field: {get_sanitized(row.naucno_polje)}"
                    )

                    self.tree.insert(
                        id, "end",
                        text=f"PDF generated: {get_sanitized(row.pdf_generated)}"
                    )
        finally:
            conn.close()

    def on_row_expand(self, event):
        focus = self.tree.focus()
        self.tree.insert(focus, "end", text="Hello")

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
