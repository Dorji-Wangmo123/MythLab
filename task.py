import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import sqlite3

from PIL import Image, ImageTk, ImageOps
import customtkinter as ctk


# ============================================================
# MYTHLAB - MY TASKS
# Complete redesigned page with rounded cards and progress bar
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
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM users WHERE LOWER(username) = LOWER(?)",
            (username,)
        )
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        conn.close()


def prepare_tasks_table():
    conn = get_connection()
    try:
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
                SET status = CASE WHEN completed = 1
                    THEN 'Completed' ELSE 'Pending' END
            """)
        if "due_date" not in columns:
            cursor.execute("ALTER TABLE tasks ADD COLUMN due_date TEXT")

        cursor.execute("""
            UPDATE tasks
            SET completed = CASE WHEN status = 'Completed'
                THEN 1 ELSE 0 END
        """)
        conn.commit()
    finally:
        conn.close()


# ============================================================
# IMAGE HELPERS
# ============================================================

def find_image(keywords):
    extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
    if not IMAGE_FOLDER.exists():
        return None

    files = [
        f for f in IMAGE_FOLDER.iterdir()
        if f.is_file() and f.suffix.lower() in extensions
    ]

    # Prefer a filename containing every keyword.
    for file in files:
        stem = file.stem.lower().replace("_", " ").replace("-", " ")
        if all(word.lower() in stem for word in keywords):
            return file

    # Otherwise accept any matching keyword.
    for file in files:
        stem = file.stem.lower().replace("_", " ").replace("-", " ")
        if any(word.lower() in stem for word in keywords):
            return file
    return None


def load_task_image(keywords, width=58, height=54):
    path = find_image(keywords)
    if not path:
        return None
    try:
        image = Image.open(path).convert("RGB")
        image = ImageOps.fit(
            image,
            (width, height),
            method=Image.Resampling.LANCZOS
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
        return ["punakha"]
    if "quiz" in title:
        return ["quiz"]
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
# MAIN PAGE
# ============================================================

def show_tasks(parent, username=None):
    # -------------------- Database setup --------------------
    try:
        prepare_tasks_table()
        if not username:
            messagebox.showerror(
                "My Tasks", "Please log in before opening My Tasks."
            )
            return

        user_id = get_user_id(username)
        if user_id is None:
            messagebox.showerror(
                "My Tasks", "Could not identify the logged-in user."
            )
            return
    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error", f"Could not prepare the tasks database:\n{error}"
        )
        return

    # -------------------- Tasks based on existing MythLab content --------------------
    # Read titles and descriptions directly from the MythLab Myths and Creatures
    # catalogs. This avoids adding stories that are not in the application.
    from myths import MYTHS
    from creatures import creatures

    # Exact names from MythLab, not newly invented story titles.
    featured_titles = [
        "The Thunder Dragon",
        "Ap Chhundu",
        "Guru Rinpoche",
        "The Yeti",
        "The Black Mountain",
        "The Legend of Paro Taktsang",
        "Migoi",
        "Snow Lion",
    ]

    catalog = {}
    for category, title, description, image_name, region in MYTHS:
        catalog[title] = (description, image_name)
    for title, kind, category, region, image_name, description in creatures:
        catalog.setdefault(title, (description, image_name))

    # These are the old sample tasks from the previous version. Update only
    # exact matches so that user-created or edited tasks are never overwritten.
    legacy_titles = {
        "Read about the Thunder Dragon": "The Thunder Dragon",
        "Explore Bhutanese mythical creatures": "Migoi",
        "Read the story of the Great Yeti": "The Yeti",
        "Watch The Firebird": "The Firebird",
        "Explore Punakha Dzong": "The Legend of Paro Taktsang",
        "Take the Mythology Quiz": "Ap Chhundu",
    }

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, description, priority, status, due_date "
            "FROM tasks WHERE user_id = ? ORDER BY id", (user_id,)
        )
        existing = cursor.fetchall()
        old_default_titles = set(legacy_titles)
        # Only replace an old sample set when all records are old samples.
        # Otherwise retain all user data as-is.
        is_original_sample_set = bool(existing) and all(
            row[1] in old_default_titles for row in existing
        )
        if is_original_sample_set:
            for task_id, old_title, desc, priority, status, date in existing:
                new_title = legacy_titles[old_title]
                if new_title in catalog:
                    new_desc, _ = catalog[new_title]
                    cursor.execute(
                        "UPDATE tasks SET title = ?, description = ?, due_date = NULL "
                        "WHERE id = ? AND user_id = ?",
                        (new_title, new_desc, task_id, user_id)
                    )

        cursor.execute("SELECT title FROM tasks WHERE user_id = ?", (user_id,))
        existing_titles = {row[0] for row in cursor.fetchall()}
        # Seed the featured catalog items only for a new user or for the
        # untouched old sample set. Don't append tasks to customized lists.
        if not existing or is_original_sample_set:
            for title in featured_titles:
                if title not in catalog or title in existing_titles:
                    continue
                description, _ = catalog[title]
                cursor.execute("""
                    INSERT INTO tasks
                    (user_id, title, description, completed, priority, status, due_date)
                    VALUES (?, ?, ?, 0, 'Medium', 'Pending', NULL)
                """, (user_id, title, description))
                existing_titles.add(title)
        conn.commit()
        cursor.execute("""
            SELECT id, title, description, priority, status, due_date
            FROM tasks WHERE user_id = ? ORDER BY id
        """, (user_id,))
        rows = cursor.fetchall()
    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error", f"Could not load tasks:\n{error}"
        )
        return
    finally:
        conn.close()

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

    # -------------------- Clear previous page --------------------
    for widget in parent.winfo_children():
        widget.destroy()

    def task_photo(task):
        # Use the actual image files from MythLab assets. Some catalog
        # entries use .png while the supplied images are .jpg.
        image_aliases = {
            "Ap Chhundu": ["ap_chhundu.jpg", "ap_chhundu.png"],
            "Guru Rinpoche": ["guru_rinpocheo.jpg", "guru.jpg", "guru_rinpoche.png"],
        }
        entry = catalog.get(task["title"])
        candidates = list(image_aliases.get(task["title"], []))
        if entry and entry[1]:
            candidates.append(entry[1])
            stem = Path(entry[1]).stem
            for extension in (".jpg", ".jpeg", ".png", ".webp"):
                candidates.append(stem + extension)

        for filename in dict.fromkeys(candidates):
            image_file = IMAGE_FOLDER / filename
            if not image_file.is_file():
                continue
            try:
                with Image.open(image_file) as original:
                    picture = ImageOps.fit(
                        original.convert("RGB"), (58, 54),
                        method=Image.Resampling.LANCZOS
                    )
                return ImageTk.PhotoImage(picture)
            except (OSError, ValueError) as error:
                print("Could not load task image:", image_file, error)

        return load_task_image(task["image_keywords"])

    task_images = {task["id"]: task_photo(task) for task in current_tasks}

    search_var = tk.StringVar()
    active_filter = {"value": "All"}
    filter_buttons = {}

    # -------------------- Rounded card helper --------------------
    def rounded_card(master, height=None, **kwargs):
        card = ctk.CTkFrame(
            master,
            fg_color=kwargs.get("fg_color", PANEL),
            corner_radius=14,
            border_width=1,
            border_color=BORDER,
            height=height if height else 100
        )
        if height:
            card.pack_propagate(False)
        return card

    # -------------------- Scrollable page --------------------
    outer = tk.Frame(parent, bg=BG)
    outer.pack(fill="both", expand=True)

    canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    page = tk.Frame(canvas, bg=BG)
    canvas_window = canvas.create_window((0, 0), window=page, anchor="nw")

    def update_scroll_region(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def resize_page(event):
        canvas.itemconfig(canvas_window, width=event.width)

    page.bind("<Configure>", update_scroll_region)
    canvas.bind("<Configure>", resize_page)

    def mousewheel(event):
        if getattr(event, "delta", 0):
            canvas.yview_scroll(int(-event.delta / 120), "units")
        elif getattr(event, "num", None) == 4:
            canvas.yview_scroll(-3, "units")
        elif getattr(event, "num", None) == 5:
            canvas.yview_scroll(3, "units")

    canvas.bind_all("<MouseWheel>", mousewheel)
    canvas.bind_all("<Button-4>", mousewheel)
    canvas.bind_all("<Button-5>", mousewheel)

    # -------------------- Header with fitted banner --------------------
    header = tk.Frame(page, bg=BG, height=155)
    header.pack(fill="x")
    header.pack_propagate(False)

    header_canvas = tk.Canvas(header, bg=BG, highlightthickness=0)
    header_canvas.pack(fill="both", expand=True)

    banner_path = IMAGE_FOLDER / "banner.jpg"
    header_photo = None
    image_item = header_canvas.create_image(0, 0, anchor="nw")

    header_canvas.create_text(
        38, 75, text="▣", fill=GOLD,
        font=("Segoe UI", 34), anchor="w", tags="header_text"
    )
    header_canvas.create_text(
        88, 67, text="My Tasks", fill=LIGHT_GOLD,
        font=("Georgia", 30, "bold"), anchor="w", tags="header_text"
    )
    header_canvas.create_text(
        91, 105,
        text="Complete your learning tasks, track your progress and build your knowledge",
        fill=WHITE, font=("Segoe UI", 9), anchor="w", tags="header_text"
    )
    header_canvas.create_text(
        91, 123, text="about myths, legends and creatures.",
        fill=WHITE, font=("Segoe UI", 9), anchor="w", tags="header_text"
    )

    def update_header_image(event=None):
        nonlocal header_photo
        if not banner_path.exists():
            print("Header image not found:", banner_path)
            return
        width, height = header.winfo_width(), header.winfo_height()
        if width <= 1 or height <= 1:
            return
        try:
            image = Image.open(banner_path).convert("RGB")
            image = ImageOps.fit(
                image, (width, height),
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5)
            )
            overlay = Image.new("RGB", image.size, BG)
            image = Image.blend(image, overlay, 0.30)
            header_photo = ImageTk.PhotoImage(image)
            header_canvas.itemconfig(image_item, image=header_photo)
            header_canvas.tag_lower(image_item)
        except Exception as error:
            print("Header image error:", error)

    header.bind("<Configure>", update_header_image)

    # -------------------- Main content layout --------------------
    content = tk.Frame(page, bg=BG)
    content.pack(fill="x", padx=20, pady=16)

    right = tk.Frame(content, bg=BG, width=280)
    right.pack(side="right", fill="y", padx=(16, 0))
    right.pack_propagate(False)

    left_content = tk.Frame(content, bg=BG)
    left_content.pack(side="left", fill="both", expand=True)

    # -------------------- Filter bar --------------------
    filter_bar = rounded_card(left_content, height=126)
    filter_bar.pack(fill="x", pady=(0, 0))

    # -------------------- Task table heading --------------------
    table_header = tk.Frame(left_content, bg=PANEL2, height=42)
    table_header.pack(fill="x", pady=(8, 0))
    table_header.pack_propagate(False)

    for x, label in [(72, "Task"), (368, "Priority"),
                     (468, "Status")]:
        tk.Label(
            table_header, text=label, bg=PANEL2, fg=TEXT,
            font=("Segoe UI", 8, "bold")
        ).place(x=x, y=14)

    task_container = rounded_card(left_content)
    task_container.pack(fill="x")

    # -------------------- Progress card --------------------
    progress_box = rounded_card(right, height=160)
    progress_box.pack(fill="x")

    tk.Label(
        progress_box, text="Your Progress", bg=PANEL,
        fg=LIGHT_GOLD, font=("Georgia", 12, "bold")
    ).pack(anchor="w", padx=16, pady=(12, 4))

    progress_label = tk.Label(
        progress_box, text="0%", bg=PANEL, fg=WHITE,
        font=("Segoe UI", 18, "bold")
    )
    progress_label.place(x=18, y=45)

    tk.Label(
        progress_box, text="Tasks completed", bg=PANEL,
        fg=MUTED, font=("Segoe UI", 8)
    ).place(x=20, y=78)

    progress_bar = ctk.CTkProgressBar(
        progress_box, width=112, height=10,
        corner_radius=8, fg_color="#253f4f",
        progress_color=GREEN_LIGHT
    )
    progress_bar.place(x=18, y=111)
    progress_bar.set(0)

    legend_labels = {}
    for i, (name, color) in enumerate([
        ("Completed", GREEN), ("Pending", "#6996c2"), ("Overdue", RED)
    ]):
        y = 48 + i * 30
        tk.Label(
            progress_box, text="●", bg=PANEL, fg=color,
            font=("Segoe UI", 11)
        ).place(x=150, y=y)
        tk.Label(
            progress_box, text=name, bg=PANEL, fg=TEXT,
            font=("Segoe UI", 8)
        ).place(x=167, y=y + 1)
        value = tk.Label(
            progress_box, text="0", bg=PANEL, fg=WHITE,
            font=("Segoe UI", 8, "bold")
        )
        value.place(x=245, y=y + 1)
        legend_labels[name] = value

    # -------------------- Task overview card --------------------
    overview = rounded_card(right, height=175)
    overview.pack(fill="x", pady=12)

    tk.Label(
        overview, text="Task Overview", bg=PANEL,
        fg=LIGHT_GOLD, font=("Georgia", 12, "bold")
    ).pack(anchor="w", padx=16, pady=(12, 10))

    def overview_card(master, x, y, title, icon, color):
        card = ctk.CTkFrame(
            master, fg_color="#0d2637", corner_radius=10,
            width=120, height=58
        )
        card.place(x=x, y=y)
        card.pack_propagate(False)
        tk.Label(
            card, text=icon, bg="#0d2637", fg=color,
            font=("Segoe UI", 16)
        ).place(x=9, y=8)
        tk.Label(
            card, text=title, bg="#0d2637", fg=MUTED,
            font=("Segoe UI", 7)
        ).place(x=36, y=8)
        value = tk.Label(
            card, text="0", bg="#0d2637", fg=WHITE,
            font=("Segoe UI", 14, "bold")
        )
        value.place(x=37, y=27)
        return value

    total_label = overview_card(overview, 12, 48, "Total Tasks", "▣", GOLD)
    completed_label = overview_card(
        overview, 142, 48, "Completed", "✓", GREEN_LIGHT
    )
    pending_label = overview_card(
        overview, 12, 112, "Pending", "◷", "#6f9ec5"
    )
    high_label = overview_card(overview, 142, 112, "High Priority", "!", RED)

    # -------------------- Priority guide --------------------
    guide = rounded_card(right, height=200)
    guide.pack(fill="x")

    tk.Label(
        guide, text="Priority Guide", bg=PANEL,
        fg=LIGHT_GOLD, font=("Georgia", 12, "bold")
    ).pack(anchor="w", padx=16, pady=(12, 10))

    priority_data = [
        ("!", "High", "Important tasks that you want\nto complete first.", RED),
        ("−", "Medium", "Tasks that are important\nbut not urgent.", YELLOW),
        ("↓", "Low", "Tasks for later exploration\nand learning.", GREEN)
    ]

    for i, (icon, title, description, color) in enumerate(priority_data):
        y = 48 + i * 49
        ctk.CTkLabel(
            guide, text=icon, fg_color=color, text_color=WHITE,
            font=("Segoe UI", 12, "bold"),
            width=36, height=28, corner_radius=10
        ).place(x=16, y=y)
        tk.Label(
            guide, text=title, bg=PANEL, fg=WHITE,
            font=("Segoe UI", 8, "bold")
        ).place(x=56, y=y)
        tk.Label(
            guide, text=description, bg=PANEL, fg=MUTED,
            font=("Segoe UI", 7), justify="left"
        ).place(x=56, y=y + 16)

    # -------------------- Quote card --------------------
    quote = rounded_card(right, height=120)
    quote.pack(fill="x", pady=12)

    tk.Label(
        quote,
        text='"The mountains, the rivers — all are\npart of who we are."',
        bg=PANEL, fg=LIGHT_GOLD,
        font=("Georgia", 10, "italic"), justify="left"
    ).pack(anchor="w", padx=18, pady=(20, 6))

    tk.Label(
        quote, text="──── ❈ ────", bg=PANEL,
        fg=GOLD, font=("Segoe UI", 9)
    ).pack()

    # -------------------- Keep going card --------------------
    keep_going = tk.Frame(left_content, bg=BG, height=76)
    keep_going.pack(fill="x", pady=(14, 0))
    keep_going.pack_propagate(False)

    # Use transparent CustomTkinter children so they do not paint
    # rectangular backgrounds over the rounded card.
    ctk.CTkLabel(
        keep_going,
        text="💡",
        fg_color="transparent",
        text_color=GOLD,
        font=("Segoe UI Emoji", 28)
    ).pack(side="left", padx=(18, 16))

    keep_text_frame = ctk.CTkFrame(
        keep_going,
        fg_color="transparent",
        corner_radius=0
    )
    keep_text_frame.pack(side="left", fill="y")

    ctk.CTkLabel(
        keep_text_frame,
        text="Keep going!",
        fg_color="transparent",
        text_color=LIGHT_GOLD,
        font=("Georgia", 13, "bold")
    ).pack(anchor="w", pady=(16, 2))

    ctk.CTkLabel(
        keep_text_frame,
        text="You're doing great. Every task brings you closer to the legends.",
        fg_color="transparent",
        text_color=MUTED,
        font=("Segoe UI", 8)
    ).pack(anchor="w")

    # ========================================================
    # DATABASE ACTIONS
    # ========================================================

    def save_task_status(task):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tasks SET status = ?, completed = ?
                WHERE id = ? AND user_id = ?
            """, (
                task["status"],
                1 if task["status"] == "Completed" else 0,
                task["id"], user_id
            ))
            conn.commit()
            conn.close()
        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error", f"Could not update task:\n{error}"
            )

    def toggle_task(task):
        task["status"] = (
            "Pending" if task["status"] == "Completed" else "Completed"
        )
        save_task_status(task)
        refresh_tasks()

    def delete_task(task):
        answer = messagebox.askyesno(
            "Delete Task", f"Do you want to delete:\n\n{task['title']}?"
        )
        if not answer:
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM tasks WHERE id = ? AND user_id = ?",
                (task["id"], user_id)
            )
            conn.commit()
            conn.close()
            current_tasks.remove(task)
            task_images.pop(task["id"], None)
            refresh_tasks()
        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error", f"Could not delete task:\n{error}"
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
            window, text="Edit Task", bg=BG, fg=GOLD,
            font=("Georgia", 20, "bold")
        ).pack(pady=20)

        tk.Label(
            window, text="Task title", bg=BG, fg=WHITE,
            font=("Segoe UI", 10)
        ).pack(anchor="w", padx=30)

        title_entry = tk.Entry(
            window, bg=PANEL2, fg=WHITE,
            insertbackground=WHITE, font=("Segoe UI", 11), relief="flat"
        )
        title_entry.pack(fill="x", padx=30, pady=(0, 15))
        title_entry.insert(0, task["title"])

        tk.Label(
            window, text="Description", bg=BG, fg=WHITE,
            font=("Segoe UI", 10)
        ).pack(anchor="w", padx=30)

        desc_entry = tk.Entry(
            window, bg=PANEL2, fg=WHITE,
            insertbackground=WHITE, font=("Segoe UI", 10), relief="flat"
        )
        desc_entry.pack(fill="x", padx=30, pady=(0, 20))
        desc_entry.insert(0, task["description"])

        def save_changes():
            new_title = title_entry.get().strip()
            new_description = desc_entry.get().strip()
            if new_title not in catalog:
                messagebox.showwarning(
                    "Edit Task",
                    "Choose an existing MythLab story title. "
                    "New stories cannot be added from My Tasks.",
                    parent=window
                )
                return
            # Keep descriptions consistent with the existing MythLab story.
            new_description = catalog[new_title][0]
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE tasks SET title = ?, description = ?
                    WHERE id = ? AND user_id = ?
                """, (
                    new_title, new_description, task["id"], user_id
                ))
                conn.commit()
                conn.close()
                task["title"] = new_title
                task["description"] = new_description
                task["icon"] = get_task_icon(new_title)
                task["image_keywords"] = get_task_image_keywords(new_title)
                task_images[task["id"]] = task_photo(task)
                window.destroy()
                refresh_tasks()
            except sqlite3.Error as error:
                messagebox.showerror(
                    "Database Error", f"Could not save changes:\n{error}",
                    parent=window
                )

        ctk.CTkButton(
            window, text="Save Changes", command=save_changes,
            fg_color=GOLD, hover_color=LIGHT_GOLD,
            text_color=BG, corner_radius=9,
            font=("Segoe UI", 10, "bold"), width=150, height=36
        ).pack(pady=12)
        title_entry.focus_set()

    # ========================================================
    # TASK DISPLAY
    # ========================================================

    def display_tasks(task_list):
        for widget in task_container.winfo_children():
            widget.destroy()

        if not task_list:
            tk.Label(
                task_container, text="No tasks found.",
                bg=PANEL, fg=MUTED, font=("Segoe UI", 11)
            ).pack(pady=35)
            return

        for task in task_list:
            row = tk.Frame(task_container, bg=PANEL, height=76)
            row.pack(fill="x", padx=4, pady=2)
            row.pack_propagate(False)

            checked = task["status"] == "Completed"

            tk.Button(
                row, text="☑" if checked else "☐",
                command=lambda t=task: toggle_task(t),
                bg=PANEL, fg=GOLD if checked else "#8d9ba5",
                activebackground=PANEL, activeforeground=GOLD,
                borderwidth=0, font=("Segoe UI Symbol", 19),
                cursor="hand2"
            ).place(x=12, y=21)

            real_image = task_images.get(task["id"])
            if real_image:
                image_box = tk.Label(
                    row, image=real_image, bg="#17384a", borderwidth=0
                )
            else:
                image_box = tk.Label(
                    row, text=task["icon"], bg="#17384a",
                    fg=WHITE, font=("Segoe UI Emoji", 20)
                )
            image_box.place(x=56, y=11, width=58, height=54)

            title_color = MUTED if checked else WHITE
            short_title = task["title"]
            if len(short_title) > 27:
                short_title = short_title[:24] + "..."

            tk.Label(
                row, text=short_title, bg=PANEL, fg=title_color,
                font=("Segoe UI", 9, "bold"), anchor="w",
                justify="left", wraplength=220
            ).place(x=124, y=9, width=220, height=22)

            short_desc = task["description"]
            if len(short_desc) > 48:
                short_desc = short_desc[:45] + "..."
            tk.Label(
                row, text=short_desc, bg=PANEL, fg=MUTED,
                font=("Segoe UI", 7), anchor="w", justify="left",
                wraplength=220
            ).place(x=124, y=34, width=220, height=18)

            priority_colors = {"High": RED, "Medium": YELLOW, "Low": GREEN}
            ctk.CTkLabel(
                row, text=task["priority"],
                fg_color=priority_colors.get(task["priority"], YELLOW),
                text_color=WHITE, font=("Segoe UI", 8, "bold"),
                width=68, height=28, corner_radius=14
            ).place(x=368, y=24)

            status_bg = GREEN if checked else BLUE
            ctk.CTkLabel(
                row, text=task["status"],
                fg_color=status_bg, text_color=WHITE,
                font=("Segoe UI", 8, "bold"),
                width=86, height=28, corner_radius=14
            ).place(x=468, y=24)

            tk.Button(
                row, text="✎", command=lambda t=task: edit_task(t),
                bg=PANEL, fg=GOLD, activebackground=PANEL2,
                activeforeground=LIGHT_GOLD, borderwidth=0,
                font=("Segoe UI", 15), cursor="hand2"
            ).place(x=561, y=19, width=30, height=34)

            tk.Button(
                row, text="🗑", command=lambda t=task: delete_task(t),
                bg=PANEL, fg=RED, activebackground=PANEL2,
                activeforeground=RED, borderwidth=0,
                font=("Segoe UI Emoji", 13), cursor="hand2"
            ).place(x=596, y=19, width=32, height=34)

    # ========================================================
    # STATISTICS AND FILTERING
    # ========================================================

    def update_statistics():
        total = len(current_tasks)
        completed = sum(
            1 for task in current_tasks if task["status"] == "Completed"
        )
        pending = sum(
            1 for task in current_tasks if task["status"] == "Pending"
        )
        high = sum(
            1 for task in current_tasks if task["priority"] == "High"
        )
        percentage = completed / total if total else 0

        progress_label.config(text=f"{int(percentage * 100)}%")
        progress_bar.set(percentage)
        total_label.config(text=str(total))
        completed_label.config(text=str(completed))
        pending_label.config(text=str(pending))
        high_label.config(text=str(high))
        legend_labels["Completed"].config(text=str(completed))
        legend_labels["Pending"].config(text=str(pending))
        legend_labels["Overdue"].config(text="0")

    def apply_filters(*args):
        selected_filter = active_filter["value"]
        keyword = search_var.get().strip().lower()
        filtered = []

        for task in current_tasks:
            matches_filter = (
                selected_filter == "All" or task["status"] == selected_filter
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
            button.configure(
                fg_color=GOLD if selected else PANEL,
                text_color=BG if selected else WHITE,
                font=("Segoe UI", 10, "bold" if selected else "normal"),
                border_width=1,
                border_color=GOLD if selected else "#3d5363"
            )
        apply_filters()

    def refresh_tasks():
        apply_filters()
        update_statistics()
        page.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    # Put filters and search on separate lines so the search text is visible.
    filter_buttons_row = ctk.CTkFrame(filter_bar, fg_color="transparent", height=54)
    filter_buttons_row.pack(fill="x", padx=10, pady=(7, 0))
    search_row = ctk.CTkFrame(filter_bar, fg_color="transparent", height=48)
    search_row.pack(fill="x", padx=15, pady=(0, 10))

    # -------------------- Rounded pill filters --------------------
    def create_filter_button(label, filter_type):
        selected = filter_type == "All"
        button = ctk.CTkButton(
            filter_buttons_row,
            text=label,
            command=lambda: select_filter(filter_type),
            fg_color=GOLD if selected else PANEL2,
            hover_color=LIGHT_GOLD if selected else "#25465a",
            text_color=BG if selected else WHITE,
            border_width=1,
            border_color=GOLD if selected else "#3d5363",
            corner_radius=24,
            font=("Segoe UI", 10, "bold" if selected else "normal"),
            width=105,
            height=38
        )
        button.pack(side="left", padx=(4, 4), pady=6)
        filter_buttons[filter_type] = button

    create_filter_button("All Tasks", "All")
    create_filter_button("Pending", "Pending")
    create_filter_button("Completed", "Completed")

    # -------------------- Rounded search field --------------------
    search = ctk.CTkEntry(
        search_row,
        textvariable=search_var,
        placeholder_text="Search tasks...",
        placeholder_text_color=MUTED,
        fg_color="#102b3d",
        text_color=WHITE,
        border_color=GOLD,
        border_width=1,
        corner_radius=24,
        height=38,
        font=("Segoe UI", 10)
    )
    search.pack(side="left", fill="x", expand=True, padx=4, pady=3)
    search_var.trace_add("write", apply_filters)

    # -------------------- Initial display --------------------
    refresh_tasks()
    page.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.yview_moveto(0)
    parent.after(150, update_header_image)
