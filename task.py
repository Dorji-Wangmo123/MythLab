
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path
import sqlite3


# ============================================================
# MYTHLAB - MY TASKS
# ============================================================

BG = "#061522"
PANEL = "#0a1d2b"
PANEL2 = "#102b3d"
GOLD = "#e8b85b"
LIGHT_GOLD = "#f5d58b"
WHITE = "#f3f0e5"
TEXT = "#d7dce0"
MUTED = "#9ba8b1"

GREEN = "#3ba875"
GREEN_LIGHT = "#70d39b"
BLUE = "#416d96"
RED = "#d94c5b"
YELLOW = "#d7a842"
BORDER = "#735d35"

BASE_DIR = Path(__file__).resolve().parent
IMAGE_FOLDER = BASE_DIR / "assets"
DB_FILE = BASE_DIR / "mythlab.db"


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    return sqlite3.connect(DB_FILE)


def get_user_id(username):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id FROM users WHERE LOWER(username) = LOWER(?)",
            (username,)
        )
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        conn.close()


def prepare_tasks_table():
    """Create the tasks table if necessary and safely update its schema."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            completed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("PRAGMA table_info(tasks)")
    columns = {row[1] for row in cursor.fetchall()}

    if "completed" not in columns:
        cursor.execute(
            "ALTER TABLE tasks ADD COLUMN completed INTEGER DEFAULT 0"
        )

    if "priority" not in columns:
        cursor.execute(
            "ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT 'Medium'"
        )

    if "status" not in columns:
        cursor.execute(
            "ALTER TABLE tasks ADD COLUMN status TEXT DEFAULT 'Pending'"
        )

        cursor.execute("""
            UPDATE tasks
            SET status = CASE
                WHEN completed = 1 THEN 'Completed'
                ELSE 'Pending'
            END
        """)

    if "due_date" not in columns:
        cursor.execute(
            "ALTER TABLE tasks ADD COLUMN due_date TEXT"
        )

    # Keep the old completed column synchronized with status.
    cursor.execute("""
        UPDATE tasks
        SET completed = CASE
            WHEN status = 'Completed' THEN 1
            ELSE 0
        END
    """)

    conn.commit()
    conn.close()


# ============================================================
# TASK IMAGES
# ============================================================

def find_image(keywords):
    extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

    if not IMAGE_FOLDER.exists():
        return None

    files = [
        file for file in IMAGE_FOLDER.iterdir()
        if file.is_file() and file.suffix.lower() in extensions
    ]

    for file in files:
        filename = file.stem.lower()
        if all(word.lower() in filename for word in keywords):
            return file

    for file in files:
        filename = file.stem.lower()
        if any(word.lower() in filename for word in keywords):
            return file

    return None


def load_task_image(keywords, width=54, height=48):
    image_path = find_image(keywords)

    if image_path is None:
        return None

    try:
        image = Image.open(image_path).convert("RGB")

        original_width, original_height = image.size
        scale = max(width / original_width, height / original_height)

        new_width = int(original_width * scale)
        new_height = int(original_height * scale)

        image = image.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS
        )

        left = (new_width - width) // 2
        top = (new_height - height) // 2

        image = image.crop(
            (left, top, left + width, top + height)
        )

        return ImageTk.PhotoImage(image)

    except Exception as error:
        print("Could not load task image:", error)
        return None


def get_task_image_keywords(title):
    title = title.lower()

    if "thunder" in title or "dragon" in title:
        return ["thunder", "dragon"]
    if "creature" in title:
        return ["creature"]
    if "yeti" in title:
        return ["yeti"]
    if "firebird" in title:
        return ["firebird"]
    if "punakha" in title or "dzong" in title:
        return ["punakha", "dzong"]

    return ["myth"]


def get_task_icon(title):
    title = title.lower()

    if "dragon" in title:
        return "🐉"
    if "creature" in title:
        return "👹"
    if "yeti" in title:
        return "🏔"
    if "firebird" in title:
        return "🔥"
    if "punakha" in title or "dzong" in title:
        return "🏯"
    if "quiz" in title:
        return "📚"

    return "📖"


# ============================================================
# MAIN PAGE FUNCTION
# ============================================================

def show_tasks(parent, username=None):

    # --------------------------------------------------------
    # DATABASE SETUP
    # --------------------------------------------------------

    try:
        prepare_tasks_table()

        if not username:
            messagebox.showerror(
                "My Tasks",
                "Please log in before opening My Tasks."
            )
            return

        user_id = get_user_id(username)

        if user_id is None:
            messagebox.showerror(
                "My Tasks",
                "Could not identify the logged-in user."
            )
            return

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not prepare the tasks database:\n{error}"
        )
        return

    # --------------------------------------------------------
    # LOAD TASKS FROM DATABASE
    # --------------------------------------------------------

    default_tasks = [
        (
            "Read about the Thunder Dragon",
            "Learn about the Thunder Dragon and its role in Bhutanese mythology.",
            "High", "Pending", "25 Apr 2026"
        ),
        (
            "Explore Bhutanese mythical creatures",
            "Learn about Druk, Yeti, Migoi and other beings.",
            "Medium", "Completed", "24 Apr 2026"
        ),
        (
            "Read the story of the Great Yeti",
            "Discover the legend of the Yeti in the Himalayas.",
            "High", "Pending", "27 Apr 2026"
        ),
        (
            "Watch The Firebird",
            "Learn about the symbol of rebirth and hope.",
            "Low", "Pending", "28 Apr 2026"
        ),
        (
            "Explore Punakha Dzong",
            "Learn about the history and significance of Punakha Dzong.",
            "Medium", "Completed", "22 Apr 2026"
        ),
        (
            "Take the Mythology Quiz",
            "Test what you've learned so far.",
            "High", "Pending", "30 Apr 2026"
        )
    ]

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM tasks WHERE user_id = ?",
            (user_id,)
        )
        task_count = cursor.fetchone()[0]

        if task_count == 0:
            for title, description, priority, status, due_date in default_tasks:
                cursor.execute("""
                    INSERT INTO tasks (
                        user_id, title, description,
                        completed, priority, status, due_date
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    title,
                    description,
                    1 if status == "Completed" else 0,
                    priority,
                    status,
                    due_date
                ))

        conn.commit()

        cursor.execute("""
            SELECT id, title, description, priority, status, due_date
            FROM tasks
            WHERE user_id = ?
            ORDER BY id
        """, (user_id,))

        rows = cursor.fetchall()
        conn.close()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"Could not load tasks:\n{error}"
        )
        return

    current_tasks = []

    for row in rows:
        task_id, title, description, priority, status, due_date = row

        current_tasks.append({
            "id": task_id,
            "title": title,
            "description": description or "",
            "priority": priority or "Medium",
            "status": status or "Pending",
            "date": due_date or "",
            "icon": get_task_icon(title),
            "image_keywords": get_task_image_keywords(title)
        })

    # --------------------------------------------------------
    # CLEAR PAGE
    # --------------------------------------------------------

    for widget in parent.winfo_children():
        widget.destroy()

    # Keep image references alive.
    task_images = {}

    for task in current_tasks:
        task_images[task["id"]] = load_task_image(
            task["image_keywords"]
        )

    # --------------------------------------------------------
    # VARIABLES
    # --------------------------------------------------------

    search_var = tk.StringVar()
    active_filter = {"value": "All"}
    filter_buttons = {}

    # --------------------------------------------------------
    # SCROLLABLE PAGE
    # --------------------------------------------------------

    outer = tk.Frame(parent, bg=BG)
    outer.pack(fill="both", expand=True)

    canvas = tk.Canvas(
        outer,
        bg=BG,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        outer,
        orient="vertical",
        command=canvas.yview
    )

    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    page = tk.Frame(canvas, bg=BG)

    canvas_window = canvas.create_window(
        (0, 0),
        window=page,
        anchor="nw"
    )

    def update_scroll_region(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def resize_page(event):
        canvas.itemconfig(canvas_window, width=event.width)

    page.bind("<Configure>", update_scroll_region)
    canvas.bind("<Configure>", resize_page)

    # Mouse wheel works when the pointer is over this page.
    def mousewheel(event):
        canvas.yview_scroll(int(-event.delta / 120), "units")

    canvas.bind("<MouseWheel>", mousewheel)
    page.bind("<MouseWheel>", mousewheel)

    canvas.bind(
        "<Button-4>",
        lambda event: canvas.yview_scroll(-3, "units")
    )
    canvas.bind(
        "<Button-5>",
        lambda event: canvas.yview_scroll(3, "units")
    )

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    header = tk.Frame(page, bg=BG, height=155)
    header.pack(fill="x")
    header.pack_propagate(False)

    header_image_path = (
        find_image(["welcome"])
        or find_image(["background"])
        or find_image(["mountain"])
        or find_image(["bhutan"])
    )

    header_image_label = None
    header_photo = None

    def update_header_image(event=None):
        nonlocal header_photo

        if not header_image_path or not header_image_label:
            return

        width = header.winfo_width()
        height = header.winfo_height()

        if width <= 1 or height <= 1:
            return

        try:
            image = Image.open(header_image_path).convert("RGB")
            image = image.resize(
                (width, height),
                Image.Resampling.LANCZOS
            )

            overlay = Image.new("RGB", image.size, BG)
            image = Image.blend(image, overlay, 0.35)

            header_photo = ImageTk.PhotoImage(image)
            header_image_label.config(image=header_photo)

        except Exception as error:
            print("Header image error:", error)

    if header_image_path:
        header_image_label = tk.Label(
            header,
            bg=BG,
            borderwidth=0
        )
        header_image_label.place(
            x=0, y=0, relwidth=1, relheight=1
        )

        header.bind("<Configure>", update_header_image)

    tk.Label(
        header,
        text="▣",
        bg=BG,
        fg=GOLD,
        font=("Segoe UI", 36)
    ).place(x=35, y=48)

    tk.Label(
        header,
        text="My Tasks",
        bg=BG,
        fg=LIGHT_GOLD,
        font=("Georgia", 30, "bold")
    ).place(x=85, y=46)

    tk.Label(
        header,
        text="Complete your learning tasks, track your progress and build your knowledge",
        bg=BG,
        fg=TEXT,
        font=("Segoe UI", 9)
    ).place(x=87, y=90)

    tk.Label(
        header,
        text="about myths, legends and creatures.",
        bg=BG,
        fg=TEXT,
        font=("Segoe UI", 9)
    ).place(x=87, y=106)

    tk.Label(
        header,
        text="⌕",
        bg=BG,
        fg=GOLD,
        font=("Segoe UI", 25)
    ).place(relx=0.91, y=18)

    tk.Label(
        header,
        text="♧",
        bg=BG,
        fg=GOLD,
        font=("Segoe UI", 20)
    ).place(relx=0.95, y=20)

    tk.Label(
        header,
        text="●",
        bg=BG,
        fg=LIGHT_GOLD,
        font=("Segoe UI", 25)
    ).place(relx=0.98, y=17)

    # --------------------------------------------------------
    # CONTENT AREA
    # --------------------------------------------------------

    content = tk.Frame(page, bg=BG)
    content.pack(fill="x", padx=20, pady=16)

    # Right panel is packed first to reserve its width.
    right = tk.Frame(content, bg=BG, width=280)
    right.pack(side="right", fill="y", padx=(16, 0))
    right.pack_propagate(False)

    left_content = tk.Frame(content, bg=BG)
    left_content.pack(side="left", fill="both", expand=True)

    # --------------------------------------------------------
    # FILTER BAR
    # --------------------------------------------------------

    filter_bar = tk.Frame(
        left_content,
        bg=PANEL,
        height=56,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    filter_bar.pack(fill="x")
    filter_bar.pack_propagate(False)

    # --------------------------------------------------------
    # TASK TABLE
    # --------------------------------------------------------

    table_header = tk.Frame(
        left_content,
        bg=PANEL2,
        height=42
    )
    table_header.pack(fill="x")
    table_header.pack_propagate(False)

    tk.Label(
        table_header,
        text="Task",
        bg=PANEL2,
        fg=TEXT,
        font=("Segoe UI", 8, "bold")
    ).place(x=60, y=14)

    tk.Label(
        table_header,
        text="Priority",
        bg=PANEL2,
        fg=TEXT,
        font=("Segoe UI", 8, "bold")
    ).place(x=368, y=14)

    tk.Label(
        table_header,
        text="Status",
        bg=PANEL2,
        fg=TEXT,
        font=("Segoe UI", 8, "bold")
    ).place(x=468, y=14)

    tk.Label(
        table_header,
        text="Due Date",
        bg=PANEL2,
        fg=TEXT,
        font=("Segoe UI", 8, "bold")
    ).place(x=586, y=14)

    task_container = tk.Frame(
        left_content,
        bg=PANEL,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    task_container.pack(fill="x")

    # --------------------------------------------------------
    # STATISTICS WIDGETS
    # --------------------------------------------------------

    progress_box = tk.Frame(
        right,
        bg=PANEL,
        height=154,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    progress_box.pack(fill="x")
    progress_box.pack_propagate(False)

    tk.Label(
        progress_box,
        text="Your Progress",
        bg=PANEL,
        fg=LIGHT_GOLD,
        font=("Georgia", 12, "bold")
    ).pack(anchor="w", padx=16, pady=(12, 10))

    circle = tk.Canvas(
        progress_box,
        width=90,
        height=90,
        bg=PANEL,
        highlightthickness=0
    )
    circle.place(x=12, y=44)

    circle.create_oval(
        10, 10, 80, 80,
        outline="#253f4f",
        width=9
    )

    progress_arc = circle.create_arc(
        10, 10, 80, 80,
        start=90,
        extent=0,
        style="arc",
        outline=GREEN_LIGHT,
        width=9
    )

    progress_label = tk.Label(
        circle,
        text="0/0",
        bg=PANEL,
        fg=WHITE,
        font=("Segoe UI", 12, "bold")
    )
    progress_label.place(x=45, y=30, anchor="center")

    tk.Label(
        circle,
        text="Tasks",
        bg=PANEL,
        fg=MUTED,
        font=("Segoe UI", 7)
    ).place(x=45, y=52, anchor="center")

    legend_items = [
        ("Completed", GREEN),
        ("Pending", "#6996c2"),
        ("Overdue", RED)
    ]

    legend_labels = {}

    for i, (name, color) in enumerate(legend_items):
        y = 57 + i * 25

        tk.Label(
            progress_box,
            text="●",
            bg=PANEL,
            fg=color,
            font=("Segoe UI", 12)
        ).place(x=142, y=y)

        tk.Label(
            progress_box,
            text=name,
            bg=PANEL,
            fg=TEXT,
            font=("Segoe UI", 8)
        ).place(x=158, y=y + 2)

        value_label = tk.Label(
            progress_box,
            text="0",
            bg=PANEL,
            fg=WHITE,
            font=("Segoe UI", 8, "bold")
        )
        value_label.place(x=246, y=y + 2)

        legend_labels[name] = value_label

    # --------------------------------------------------------
    # TASK OVERVIEW
    # --------------------------------------------------------

    overview = tk.Frame(
        right,
        bg=PANEL,
        height=175,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    overview.pack(fill="x", pady=12)
    overview.pack_propagate(False)

    tk.Label(
        overview,
        text="Task Overview",
        bg=PANEL,
        fg=LIGHT_GOLD,
        font=("Georgia", 12, "bold")
    ).pack(anchor="w", padx=16, pady=(12, 10))

    def overview_card(parent_frame, x, y, title, icon, color):
        card = tk.Frame(
            parent_frame,
            bg="#0d2637",
            width=120,
            height=62
        )
        card.place(x=x, y=y)
        card.pack_propagate(False)

        tk.Label(
            card,
            text=icon,
            bg="#0d2637",
            fg=color,
            font=("Segoe UI Emoji", 16)
        ).place(x=10, y=10)

        tk.Label(
            card,
            text=title,
            bg="#0d2637",
            fg=MUTED,
            font=("Segoe UI", 7)
        ).place(x=38, y=10)

        value_label = tk.Label(
            card,
            text="0",
            bg="#0d2637",
            fg=WHITE,
            font=("Segoe UI", 14, "bold")
        )
        value_label.place(x=38, y=28)

        return value_label

    total_label = overview_card(
        overview, 12, 48, "Total Tasks", "▣", GOLD
    )
    completed_label = overview_card(
        overview, 142, 48, "Completed", "✓", GREEN_LIGHT
    )
    pending_label = overview_card(
        overview, 12, 114, "Pending", "◷", "#6f9ec5"
    )
    high_label = overview_card(
        overview, 142, 114, "High Priority", "!", RED
    )

    # --------------------------------------------------------
    # PRIORITY GUIDE
    # --------------------------------------------------------

    guide = tk.Frame(
        right,
        bg=PANEL,
        height=200,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    guide.pack(fill="x")
    guide.pack_propagate(False)

    tk.Label(
        guide,
        text="Priority Guide",
        bg=PANEL,
        fg=LIGHT_GOLD,
        font=("Georgia", 12, "bold")
    ).pack(anchor="w", padx=16, pady=(12, 10))

    priority_data = [
        ("!", "High", "Important tasks that you want\nto complete first.", RED),
        ("−", "Medium", "Tasks that are important\nbut not urgent.", YELLOW),
        ("↓", "Low", "Tasks for later exploration\nand learning.", GREEN)
    ]

    for i, (icon, title, description, color) in enumerate(priority_data):
        y = 48 + i * 50

        tk.Label(
            guide,
            text=icon,
            bg=color,
            fg=WHITE,
            font=("Segoe UI", 12, "bold"),
            width=3
        ).place(x=16, y=y)

        tk.Label(
            guide,
            text=title,
            bg=PANEL,
            fg=WHITE,
            font=("Segoe UI", 8, "bold")
        ).place(x=56, y=y)

        tk.Label(
            guide,
            text=description,
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 7),
            justify="left"
        ).place(x=56, y=y + 16)

    # --------------------------------------------------------
    # QUOTE BOX
    # --------------------------------------------------------

    quote = tk.Frame(
        right,
        bg=PANEL,
        height=120,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    quote.pack(fill="x", pady=12)
    quote.pack_propagate(False)

    tk.Label(
        quote,
        text='"The mountains, the rivers — all are\npart of who we are."',
        bg=PANEL,
        fg=LIGHT_GOLD,
        font=("Georgia", 10, "italic"),
        justify="left"
    ).pack(anchor="w", padx=18, pady=(20, 6))

    tk.Label(
        quote,
        text="──── ❈ ────",
        bg=PANEL,
        fg=GOLD,
        font=("Segoe UI", 9)
    ).pack()

    # --------------------------------------------------------
    # KEEP GOING BOX
    # --------------------------------------------------------

    keep_going = tk.Frame(
        left_content,
        bg=PANEL,
        height=76,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    keep_going.pack(fill="x", pady=(14, 0))
    keep_going.pack_propagate(False)

    tk.Label(
        keep_going,
        text="💡",
        bg=PANEL,
        fg=GOLD,
        font=("Segoe UI Emoji", 28)
    ).pack(side="left", padx=(18, 16))

    keep_text_frame = tk.Frame(keep_going, bg=PANEL)
    keep_text_frame.pack(side="left", fill="y")

    tk.Label(
        keep_text_frame,
        text="Keep going!",
        bg=PANEL,
        fg=LIGHT_GOLD,
        font=("Georgia", 13, "bold")
    ).pack(anchor="w", pady=(16, 2))

    tk.Label(
        keep_text_frame,
        text="You're doing great. Every task brings you closer to the legends.",
        bg=PANEL,
        fg=MUTED,
        font=("Segoe UI", 8)
    ).pack(anchor="w")

    # --------------------------------------------------------
    # DATABASE UPDATE FUNCTIONS
    # --------------------------------------------------------

    def save_task_status(task):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE tasks
                SET status = ?, completed = ?
                WHERE id = ? AND user_id = ?
            """, (
                task["status"],
                1 if task["status"] == "Completed" else 0,
                task["id"],
                user_id
            ))

            conn.commit()
            conn.close()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not update task:\n{error}"
            )

    def toggle_task(task):
        old_status = task["status"]

        if old_status == "Completed":
            task["status"] = "Pending"
        else:
            task["status"] = "Completed"

        save_task_status(task)
        refresh_tasks()

    def delete_task(task):
        answer = messagebox.askyesno(
            "Delete Task",
            f"Do you want to delete:\n\n{task['title']}?"
        )

        if not answer:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM tasks
                WHERE id = ? AND user_id = ?
            """, (task["id"], user_id))

            conn.commit()
            conn.close()

            current_tasks.remove(task)
            task_images.pop(task["id"], None)

            refresh_tasks()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                f"Could not delete task:\n{error}"
            )

    def edit_task(task):
        window = tk.Toplevel(parent)
        window.title("Edit Task")
        window.geometry("450x330")
        window.configure(bg=BG)
        window.resizable(False, False)
        window.transient(parent.winfo_toplevel())
        window.grab_set()

        tk.Label(
            window,
            text="Edit Task",
            bg=BG,
            fg=GOLD,
            font=("Georgia", 20, "bold")
        ).pack(pady=20)

        tk.Label(
            window,
            text="Task title",
            bg=BG,
            fg=WHITE,
            font=("Segoe UI", 10)
        ).pack(anchor="w", padx=30)

        title_entry = tk.Entry(
            window,
            bg=PANEL2,
            fg=WHITE,
            insertbackground=WHITE,
            font=("Segoe UI", 11),
            relief="flat"
        )
        title_entry.pack(fill="x", padx=30, pady=(0, 15))
        title_entry.insert(0, task["title"])

        tk.Label(
            window,
            text="Description",
            bg=BG,
            fg=WHITE,
            font=("Segoe UI", 10)
        ).pack(anchor="w", padx=30)

        desc_entry = tk.Entry(
            window,
            bg=PANEL2,
            fg=WHITE,
            insertbackground=WHITE,
            font=("Segoe UI", 10),
            relief="flat"
        )
        desc_entry.pack(fill="x", padx=30, pady=(0, 20))
        desc_entry.insert(0, task["description"])

        def save_changes():
            new_title = title_entry.get().strip()
            new_description = desc_entry.get().strip()

            if not new_title:
                messagebox.showwarning(
                    "Edit Task",
                    "Task title cannot be empty.",
                    parent=window
                )
                return

            try:
                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    UPDATE tasks
                    SET title = ?, description = ?
                    WHERE id = ? AND user_id = ?
                """, (
                    new_title,
                    new_description,
                    task["id"],
                    user_id
                ))

                conn.commit()
                conn.close()

                task["title"] = new_title
                task["description"] = new_description
                task["icon"] = get_task_icon(new_title)
                task["image_keywords"] = get_task_image_keywords(new_title)
                task_images[task["id"]] = load_task_image(
                    task["image_keywords"]
                )

                window.destroy()
                refresh_tasks()

            except sqlite3.Error as error:
                messagebox.showerror(
                    "Database Error",
                    f"Could not save changes:\n{error}",
                    parent=window
                )

        tk.Button(
            window,
            text="Save Changes",
            command=save_changes,
            bg=GOLD,
            fg=BG,
            activebackground=LIGHT_GOLD,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(pady=20)

        title_entry.focus_set()

    # --------------------------------------------------------
    # DISPLAY TASKS
    # --------------------------------------------------------

    def display_tasks(task_list):
        for widget in task_container.winfo_children():
            widget.destroy()

        if not task_list:
            tk.Label(
                task_container,
                text="No tasks found.",
                bg=PANEL,
                fg=MUTED,
                font=("Segoe UI", 11)
            ).pack(pady=35)
            return

        for task in task_list:
            row = tk.Frame(
                task_container,
                bg=PANEL,
                height=74
            )
            row.pack(fill="x", padx=2, pady=2)
            row.pack_propagate(False)

            checked = task["status"] == "Completed"

            tk.Button(
                row,
                text="☑" if checked else "☐",
                command=lambda t=task: toggle_task(t),
                bg=PANEL,
                fg=GOLD if checked else "#8d9ba5",
                activebackground=PANEL,
                activeforeground=GOLD,
                borderwidth=0,
                font=("Segoe UI Symbol", 19),
                cursor="hand2"
            ).place(x=12, y=20)

            real_image = task_images.get(task["id"])

            if real_image:
                image_box = tk.Label(
                    row,
                    image=real_image,
                    bg="#17384a",
                    borderwidth=0
                )
            else:
                image_box = tk.Label(
                    row,
                    text=task["icon"],
                    bg="#17384a",
                    fg=WHITE,
                    font=("Segoe UI Emoji", 20)
                )

            image_box.place(x=56, y=13, width=54, height=48)

            title_color = MUTED if checked else WHITE

            short_title = task["title"]
            if len(short_title) > 24:
                short_title = short_title[:21] + "..."

            tk.Label(
                row,
                text=short_title,
                bg=PANEL,
                fg=title_color,
                font=("Segoe UI", 9, "bold"),
                anchor="w",
                justify="left",
                wraplength=200
            ).place(x=118, y=8, width=220, height=22)

            short_desc = task["description"]
            if len(short_desc) > 46:
                short_desc = short_desc[:43] + "..."

            tk.Label(
                row,
                text=short_desc,
                bg=PANEL,
                fg=MUTED,
                font=("Segoe UI", 7),
                anchor="w",
                justify="left",
                wraplength=220
            ).place(x=118, y=32, width=220, height=18)

            priority_colors = {
                "High": RED,
                "Medium": YELLOW,
                "Low": GREEN
            }

            tk.Label(
                row,
                text=task["priority"],
                bg=priority_colors.get(task["priority"], YELLOW),
                fg=WHITE,
                font=("Segoe UI", 8, "bold"),
                width=8,
                pady=4
            ).place(x=368, y=24)

            status_bg = (
                GREEN if checked else BLUE
            )

            tk.Label(
                row,
                text=task["status"],
                bg=status_bg,
                fg=WHITE,
                font=("Segoe UI", 8, "bold"),
                width=10,
                pady=4
            ).place(x=468, y=24)

            tk.Label(
                row,
                text=task["date"],
                bg=PANEL,
                fg=TEXT,
                font=("Segoe UI", 8)
            ).place(x=586, y=27)

            tk.Button(
                row,
                text="✎",
                command=lambda t=task: edit_task(t),
                bg=PANEL,
                fg=GOLD,
                activebackground=PANEL2,
                activeforeground=LIGHT_GOLD,
                borderwidth=0,
                font=("Segoe UI", 15),
                cursor="hand2"
            ).place(x=685, y=18)

            tk.Button(
                row,
                text="♜",
                command=lambda t=task: delete_task(t),
                bg=PANEL,
                fg=RED,
                activebackground=PANEL2,
                activeforeground=RED,
                borderwidth=0,
                font=("Segoe UI", 13),
                cursor="hand2"
            ).place(x=720, y=20)

    # --------------------------------------------------------
    # STATISTICS
    # --------------------------------------------------------

    def update_statistics():
        total = len(current_tasks)

        completed = sum(
            1 for task in current_tasks
            if task["status"] == "Completed"
        )

        pending = sum(
            1 for task in current_tasks
            if task["status"] == "Pending"
        )

        high = sum(
            1 for task in current_tasks
            if task["priority"] == "High"
        )

        progress_label.config(text=f"{completed}/{total}")
        total_label.config(text=str(total))
        completed_label.config(text=str(completed))
        pending_label.config(text=str(pending))
        high_label.config(text=str(high))

        extent = 180 * completed / total if total else 0

        circle.itemconfig(
            progress_arc,
            extent=extent
        )

        legend_labels["Completed"].config(text=str(completed))
        legend_labels["Pending"].config(text=str(pending))
        legend_labels["Overdue"].config(text="0")

    # --------------------------------------------------------
    # FILTER AND SEARCH
    # --------------------------------------------------------

    def apply_filters(*args):
        selected_filter = active_filter["value"]
        keyword = search_var.get().strip().lower()

        filtered = []

        for task in current_tasks:
            matches_filter = (
                selected_filter == "All"
                or task["status"] == selected_filter
            )

            matches_search = (
                keyword in task["title"].lower()
                or keyword in task["description"].lower()
            )

            if matches_filter and matches_search:
                filtered.append(task)

        display_tasks(filtered)

        page.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def select_filter(filter_type):
        active_filter["value"] = filter_type

        for name, button in filter_buttons.items():
            selected = name == filter_type

            button.config(
                bg=GOLD if selected else PANEL,
                fg=BG if selected else WHITE,
                font=(
                    "Segoe UI",
                    9,
                    "bold" if selected else "normal"
                )
            )

        apply_filters()

    def refresh_tasks():
        apply_filters()
        update_statistics()

        page.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    # --------------------------------------------------------
    # FILTER BUTTONS
    # --------------------------------------------------------

    def create_filter_button(label, filter_type):
        button = tk.Button(
            filter_bar,
            text=label,
            command=lambda: select_filter(filter_type),
            bg=GOLD if filter_type == "All" else PANEL,
            fg=BG if filter_type == "All" else WHITE,
            activebackground=LIGHT_GOLD,
            activeforeground=BG,
            relief="flat",
            font=(
                "Segoe UI",
                9,
                "bold" if filter_type == "All" else "normal"
            ),
            padx=12,
            pady=6,
            cursor="hand2"
        )

        button.pack(side="left", padx=3, pady=14)
        filter_buttons[filter_type] = button

    create_filter_button("All Tasks", "All")
    create_filter_button("Pending", "Pending")
    create_filter_button("Completed", "Completed")

    # --------------------------------------------------------
    # SEARCH BOX
    # --------------------------------------------------------

    search = tk.Entry(
        filter_bar,
        textvariable=search_var,
        bg="#071522",
        fg=WHITE,
        insertbackground=WHITE,
        relief="flat",
        font=("Segoe UI", 9)
    )

    search.pack(
        side="right",
        padx=12,
        pady=14,
        ipady=6,
        ipadx=20
    )

    search_var.trace_add("write", apply_filters)

    # --------------------------------------------------------
    # INITIAL DISPLAY
    # --------------------------------------------------------

    refresh_tasks()

    page.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(0)

    if header_image_path:
        parent.after(150, update_header_image)
