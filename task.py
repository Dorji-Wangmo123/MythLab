# task.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path


# ============================================================
# MYTHLAB - MY TASKS DASHBOARD
# Tkinter + Pillow
# ============================================================

root = tk.Tk()
root.title("MythLab - My Tasks")

# ------------------------------------------------------------
# WINDOW SIZE: fit to the user's screen (never bigger than it)
# ------------------------------------------------------------
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

WIN_W = min(1180, int(screen_w * 0.92))
WIN_H = min(740, int(screen_h * 0.86))   # leaves room for the taskbar

pos_x = (screen_w - WIN_W) // 2
pos_y = max(0, (screen_h - WIN_H) // 2 - 20)

root.geometry(f"{WIN_W}x{WIN_H}+{pos_x}+{pos_y}")
root.minsize(980, 620)


# ============================================================
# COLORS  (same theme, more natural / less neon)
# ============================================================

BG = "#0b1a26"
SIDEBAR = "#08141d"
PANEL = "#10222f"
PANEL2 = "#18303f"
CARD = "#132b3a"
GOLD = "#c9a24d"
LIGHT_GOLD = "#e3c37a"
WHITE = "#ece8dc"
TEXT = "#cbd2d6"
MUTED = "#8a98a2"

GREEN = "#4f9a6f"
GREEN_LIGHT = "#7bbf98"

BLUE = "#4a7497"
RED = "#c0504d"
YELLOW = "#cc9a3a"

BORDER = "#5e4d2e"
IMG_BG = "#1b3646"

root.configure(bg=BG)


# ============================================================
# IMAGE FOLDER
# ============================================================

IMAGE_FOLDER = Path(__file__).resolve().parent


# ============================================================
# IMAGE FUNCTIONS
# ============================================================

def find_image(keywords):
    extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

    files = [
        file
        for file in IMAGE_FOLDER.iterdir()
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


def cover_crop(image, width, height):
    """Resize + center-crop so the image fills the box without stretching."""
    original_width, original_height = image.size

    scale = max(width / original_width, height / original_height)
    new_width = int(original_width * scale) + 1
    new_height = int(original_height * scale) + 1

    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    left = (new_width - width) // 2
    top = (new_height - height) // 2

    return image.crop((left, top, left + width, top + height))


def load_task_image(keywords, width=48, height=42):
    image_path = find_image(keywords)

    if image_path is None:
        return None

    try:
        image = Image.open(image_path).convert("RGB")
        image = cover_crop(image, width, height)
        return ImageTk.PhotoImage(image)

    except Exception as error:
        print("Could not load image:", image_path)
        print(error)
        return None


# ============================================================
# TASK IMAGE KEYWORDS
# ============================================================

TASK_IMAGE_KEYWORDS = [
    ["thunder", "dragon"],
    ["creature"],
    ["yeti"],
    ["firebird"],
    ["punakha", "dzong"],
    ["thunder", "dragon"]
]


# ============================================================
# TASK DATA
# ============================================================

tasks = [
    {
        "title": "Read about the Thunder Dragon",
        "description": "Learn about the Thunder Dragon and its role in Bhutanese mythology.",
        "priority": "High",
        "status": "Pending",
        "date": "25 Apr 2026",
        "icon": "🐉",
        "image_keywords": TASK_IMAGE_KEYWORDS[0]
    },
    {
        "title": "Explore Bhutanese mythical creatures",
        "description": "Learn about Druk, Yeti, Migoi and other beings.",
        "priority": "Medium",
        "status": "Completed",
        "date": "24 Apr 2026",
        "icon": "👹",
        "image_keywords": TASK_IMAGE_KEYWORDS[1]
    },
    {
        "title": "Read the story of the Great Yeti",
        "description": "Discover the legend of the Yeti in the Himalayas.",
        "priority": "High",
        "status": "Pending",
        "date": "27 Apr 2026",
        "icon": "🏔",
        "image_keywords": TASK_IMAGE_KEYWORDS[2]
    },
    {
        "title": "Watch The Firebird",
        "description": "Learn about the symbol of rebirth and hope.",
        "priority": "Low",
        "status": "Pending",
        "date": "28 Apr 2026",
        "icon": "🔥",
        "image_keywords": TASK_IMAGE_KEYWORDS[3]
    },
    {
        "title": "Explore Punakha Dzong",
        "description": "Learn about the history and significance of Punakha Dzong.",
        "priority": "Medium",
        "status": "Completed",
        "date": "22 Apr 2026",
        "icon": "🏯",
        "image_keywords": TASK_IMAGE_KEYWORDS[4]
    },
    {
        "title": "Take the Mythology Quiz",
        "description": "Test what you've learned so far.",
        "priority": "High",
        "status": "Pending",
        "date": "30 Apr 2026",
        "icon": "🐲",
        "image_keywords": TASK_IMAGE_KEYWORDS[5]
    }
]

current_tasks = tasks.copy()


# ============================================================
# PRELOAD TASK IMAGES
# ============================================================

task_images = {}

for number, keywords in enumerate(TASK_IMAGE_KEYWORDS):
    task_images[number] = load_task_image(keywords, 48, 42)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def rounded_box(parent, width, height, bg, border=None):
    frame = tk.Frame(
        parent,
        width=width,
        height=height,
        bg=bg,
        highlightbackground=border if border else bg,
        highlightthickness=1
    )
    frame.pack_propagate(False)
    return frame


def create_label(
    parent,
    text,
    size=10,
    color=TEXT,
    font="Segoe UI",
    weight="normal",
    **kwargs
):
    return tk.Label(
        parent,
        text=text,
        bg=kwargs.pop("bg", parent.cget("bg")),
        fg=color,
        font=(font, size, weight),
        **kwargs
    )


# ============================================================
# TABLE COLUMN POSITIONS (relative, so rows fit any width)
# ============================================================

COL_PRIORITY = 0.47
COL_STATUS = 0.60
COL_DATE = 0.75
COL_EDIT = 0.90
COL_DELETE = 0.95


# ============================================================
# UPDATE STATISTICS
# ============================================================

def update_statistics():
    total = len(current_tasks)

    completed = sum(
        1
        for task in current_tasks
        if task["status"] == "Completed"
    )

    pending = total - completed

    high = sum(
        1
        for task in current_tasks
        if task["priority"] == "High"
    )

    progress_label.config(text=f"{completed}/{total}")

    total_label.config(text=str(total))
    completed_label.config(text=str(completed))
    pending_label.config(text=str(pending))
    high_label.config(text=str(high))

    if total > 0:
        arc_extent = 180 * (completed / total)
    else:
        arc_extent = 0

    circle.itemconfig(progress_arc, extent=arc_extent)

    if "Completed" in legend_labels:
        legend_labels["Completed"].config(text=str(completed))

    if "Pending" in legend_labels:
        legend_labels["Pending"].config(text=str(pending))

    if "Overdue" in legend_labels:
        legend_labels["Overdue"].config(text="0")


# ============================================================
# TASK FUNCTIONS
# ============================================================

def toggle_task(task):
    if task["status"] == "Completed":
        task["status"] = "Pending"
    else:
        task["status"] = "Completed"

    refresh_tasks()
    update_statistics()


def delete_task(task):
    answer = messagebox.askyesno(
        "Delete Task",
        f"Do you want to delete:\n\n{task['title']}?"
    )

    if answer:
        if task in current_tasks:
            current_tasks.remove(task)

        refresh_tasks()
        update_statistics()


def edit_task(task):
    window = tk.Toplevel(root)
    window.title("Edit Task")
    window.geometry("450x330")
    window.configure(bg=BG)
    window.resizable(False, False)

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

    title_entry.pack(
        fill="x",
        padx=30,
        pady=(0, 15)
    )

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

    desc_entry.pack(
        fill="x",
        padx=30,
        pady=(0, 20)
    )

    desc_entry.insert(0, task["description"])

    def save_changes():
        task["title"] = title_entry.get()
        task["description"] = desc_entry.get()

        refresh_tasks()
        window.destroy()

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


# ============================================================
# FILTER TASKS
# ============================================================

def filter_tasks(filter_type):

    if filter_type == "All":
        filtered = current_tasks

    elif filter_type == "Pending":
        filtered = [
            t for t in current_tasks
            if t["status"] == "Pending"
        ]

    elif filter_type == "In Progress":
        filtered = [
            t for t in current_tasks
            if t["status"] == "In Progress"
        ]

    elif filter_type == "Completed":
        filtered = [
            t for t in current_tasks
            if t["status"] == "Completed"
        ]

    else:
        filtered = current_tasks

    display_tasks(filtered)


def search_tasks(*args):

    keyword = search_var.get().lower()

    filtered = [
        task
        for task in current_tasks
        if keyword in task["title"].lower()
        or keyword in task["description"].lower()
    ]

    display_tasks(filtered)


# ============================================================
# DISPLAY TASKS
# ============================================================

def display_tasks(task_list):

    for widget in task_container.winfo_children():
        widget.destroy()

    for task in task_list:

        row = tk.Frame(
            task_container,
            bg=PANEL,
            height=62
        )

        row.pack(
            fill="x",
            padx=2,
            pady=1
        )

        row.pack_propagate(False)

        checked = task["status"] == "Completed"

        check_text = "☑" if checked else "☐"

        check_button = tk.Button(
            row,
            text=check_text,
            command=lambda t=task: toggle_task(t),
            bg=PANEL,
            fg=GOLD if checked else "#8695a0",
            activebackground=PANEL,
            activeforeground=GOLD,
            borderwidth=0,
            font=("Segoe UI Symbol", 17),
            cursor="hand2"
        )

        check_button.place(
            x=8,
            y=14
        )

        image_number = tasks.index(task)

        real_image = task_images.get(image_number)

        if real_image:

            image_box = tk.Label(
                row,
                image=real_image,
                bg=IMG_BG,
                borderwidth=0
            )

        else:

            image_box = tk.Label(
                row,
                text=task["icon"],
                bg=IMG_BG,
                fg=WHITE,
                font=("Segoe UI Emoji", 18)
            )

        image_box.place(
            x=46,
            y=10,
            width=48,
            height=42
        )

        title_color = MUTED if checked else WHITE

        short_title = task["title"]

        if len(short_title) > 30:
            short_title = short_title[:27] + "..."

        title = tk.Label(
            row,
            text=short_title,
            bg=PANEL,
            fg=title_color,
            font=("Segoe UI", 9, "bold"),
            anchor="w",
            justify="left"
        )

        title.place(
            x=104,
            y=7,
            relwidth=0.30,
            height=22
        )

        short_desc = task["description"]

        if len(short_desc) > 50:
            short_desc = short_desc[:47] + "..."

        description = tk.Label(
            row,
            text=short_desc,
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 7),
            anchor="w",
            justify="left"
        )

        description.place(
            x=104,
            y=30,
            relwidth=0.32,
            height=18
        )

        priority_colors = {
            "High": RED,
            "Medium": YELLOW,
            "Low": GREEN
        }

        priority = tk.Label(
            row,
            text=task["priority"],
            bg=priority_colors[task["priority"]],
            fg=WHITE,
            font=("Segoe UI", 8, "bold"),
            width=8,
            pady=3
        )

        priority.place(
            relx=COL_PRIORITY,
            y=19
        )

        status_bg = (
            GREEN
            if task["status"] == "Completed"
            else BLUE
        )

        status = tk.Label(
            row,
            text=task["status"],
            bg=status_bg,
            fg=WHITE,
            font=("Segoe UI", 8, "bold"),
            width=10,
            pady=3
        )

        status.place(
            relx=COL_STATUS,
            y=19
        )

        date = tk.Label(
            row,
            text=task["date"],
            bg=PANEL,
            fg=TEXT,
            font=("Segoe UI", 8)
        )

        date.place(
            relx=COL_DATE,
            y=22
        )

        edit = tk.Button(
            row,
            text="✎",
            command=lambda t=task: edit_task(t),
            bg=PANEL,
            fg=GOLD,
            activebackground=PANEL2,
            activeforeground=LIGHT_GOLD,
            borderwidth=0,
            font=("Segoe UI", 14),
            cursor="hand2"
        )

        edit.place(
            relx=COL_EDIT,
            y=14
        )

        delete = tk.Button(
            row,
            text="♜",
            command=lambda t=task: delete_task(t),
            bg=PANEL,
            fg=RED,
            activebackground=PANEL2,
            activeforeground=RED,
            borderwidth=0,
            font=("Segoe UI", 12),
            cursor="hand2"
        )

        delete.place(
            relx=COL_DELETE,
            y=16
        )


def refresh_tasks():
    display_tasks(current_tasks)
    update_statistics()


# ============================================================
# SIDEBAR
# ============================================================

sidebar = tk.Frame(
    root,
    bg=SIDEBAR,
    width=185
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


# ============================================================
# LOGO
# ============================================================

logo = tk.Label(
    sidebar,
    text="🐉",
    bg=SIDEBAR,
    fg=GOLD,
    font=("Segoe UI Emoji", 30)
)

logo.pack(
    pady=(16, 2)
)

logo_title = tk.Label(
    sidebar,
    text="MythLab",
    bg=SIDEBAR,
    fg=LIGHT_GOLD,
    font=("Georgia", 20, "bold")
)

logo_title.pack()

tagline = tk.Label(
    sidebar,
    text="Explore. Learn. Believe.",
    bg=SIDEBAR,
    fg=MUTED,
    font=("Segoe UI", 8)
)

tagline.pack(
    pady=(3, 16)
)


# ============================================================
# SIDEBAR BUTTON
# ============================================================

def sidebar_button(text, icon, active=False):

    bg = "#37352c" if active else SIDEBAR

    button = tk.Frame(
        sidebar,
        bg=bg,
        height=38
    )

    button.pack(
        fill="x",
        padx=8,
        pady=2
    )

    button.pack_propagate(False)

    icon_label = tk.Label(
        button,
        text=icon,
        bg=bg,
        fg=GOLD,
        font=("Segoe UI Emoji", 15)
    )

    icon_label.pack(
        side="left",
        padx=(10, 10)
    )

    text_label = tk.Label(
        button,
        text=text,
        bg=bg,
        fg=WHITE,
        font=("Segoe UI", 10)
    )

    text_label.pack(
        side="left"
    )

    return button


sidebar_button("Home", "⌂")
sidebar_button("Myths", "📖")
sidebar_button("Creatures", "🐉")
sidebar_button("Regions", "🌐")
sidebar_button("My Tasks", "▣", True)
sidebar_button("Quiz", "?")
sidebar_button("Favourites", "♡")
sidebar_button("About", "ⓘ")


# ============================================================
# SIDEBAR BOTTOM QUOTE
# ============================================================

quote_frame = tk.Frame(
    sidebar,
    bg=SIDEBAR
)

quote_frame.pack(
    side="bottom",
    fill="x",
    padx=14,
    pady=(10, 14)
)

tk.Label(
    quote_frame,
    text="╱╲╱╲╱╲",
    bg=SIDEBAR,
    fg="#2b4254",
    font=("Segoe UI", 15)
).pack()

tk.Label(
    quote_frame,
    text='"Every myth is a door\nto a deeper wisdom."',
    bg=SIDEBAR,
    fg=LIGHT_GOLD,
    font=("Georgia", 9, "italic"),
    justify="left"
).pack(
    pady=6
)

tk.Label(
    quote_frame,
    text="— Bhutanese Wisdom",
    bg=SIDEBAR,
    fg=MUTED,
    font=("Segoe UI", 8)
).pack()


# ============================================================
# MAIN AREA
# ============================================================

main = tk.Frame(
    root,
    bg=BG
)

main.pack(
    side="left",
    fill="both",
    expand=True
)


# ============================================================
# TOP HEADER
# ============================================================

header = tk.Frame(
    main,
    bg=BG,
    height=118
)

header.pack(
    fill="x"
)

header.pack_propagate(False)


# ============================================================
# HEADER BACKGROUND IMAGE
# ============================================================

header_image_path = find_image(["welcome"])

if header_image_path is None:
    header_image_path = find_image(["background"])

if header_image_path is None:
    header_image_path = find_image(["mountain"])

if header_image_path is None:
    header_image_path = find_image(["bhutan"])


# ============================================================
# HEADER CANVAS
# ============================================================

header_canvas = tk.Canvas(
    header,
    bg=BG,
    highlightthickness=0,
    borderwidth=0
)

header_canvas.pack(
    fill="both",
    expand=True
)

header_photo = None
header_image_item = None


def update_header_image(event=None):

    global header_photo
    global header_image_item

    if header_image_path is None:
        position_header_icons()
        return

    try:

        width = header_canvas.winfo_width()
        height = header_canvas.winfo_height()

        if width <= 1 or height <= 1:
            return

        image = Image.open(
            header_image_path
        ).convert("RGB")

        image = cover_crop(image, width, height)

        overlay = Image.new(
            "RGB",
            image.size,
            BG
        )

        image = Image.blend(
            image,
            overlay,
            0.40
        )

        header_photo = ImageTk.PhotoImage(image)

        if header_image_item is None:

            header_image_item = header_canvas.create_image(
                0,
                0,
                image=header_photo,
                anchor="nw"
            )

            header_canvas.tag_lower(
                header_image_item
            )

        else:

            header_canvas.itemconfig(
                header_image_item,
                image=header_photo
            )

        position_header_icons()

    except Exception as error:

        print(
            "Header image error:",
            error
        )


# ============================================================
# HEADER TEXT
# ============================================================

header_canvas.create_text(
    28,
    50,
    text="▣",
    fill=GOLD,
    font=("Segoe UI", 30),
    anchor="w"
)

header_canvas.create_text(
    72,
    48,
    text="My Tasks",
    fill=LIGHT_GOLD,
    font=("Georgia", 26, "bold"),
    anchor="w"
)

header_canvas.create_text(
    74,
    76,
    text="Complete your learning tasks, track your progress and build your knowledge",
    fill=TEXT,
    font=("Segoe UI", 9),
    anchor="w"
)

header_canvas.create_text(
    74,
    92,
    text="about myths, legends and creatures.",
    fill=TEXT,
    font=("Segoe UI", 9),
    anchor="w"
)


# ============================================================
# TOP RIGHT ICONS
# ============================================================

search_icon = header_canvas.create_text(
    0,
    0,
    text="⌕",
    fill=GOLD,
    font=("Segoe UI", 22),
    anchor="center",
    tags="header_icon"
)

notification_icon = header_canvas.create_text(
    0,
    0,
    text="♧",
    fill=GOLD,
    font=("Segoe UI", 18),
    anchor="center",
    tags="header_icon"
)

profile_icon = header_canvas.create_text(
    0,
    0,
    text="●",
    fill=LIGHT_GOLD,
    font=("Segoe UI", 22),
    anchor="center",
    tags="header_icon"
)


def position_header_icons():

    width = header_canvas.winfo_width()

    if width <= 1:
        return

    header_canvas.coords(
        search_icon,
        width * 0.91,
        26
    )

    header_canvas.coords(
        notification_icon,
        width * 0.95,
        25
    )

    header_canvas.coords(
        profile_icon,
        width * 0.98,
        25
    )


header_canvas.bind(
    "<Configure>",
    update_header_image
)


# ============================================================
# CONTENT
# ============================================================

content = tk.Frame(
    main,
    bg=BG
)

content.pack(
    fill="both",
    expand=True,
    padx=16,
    pady=10
)


# ============================================================
# RIGHT SIDEBAR  (packed first so it always keeps its space)
# ============================================================

right = tk.Frame(
    content,
    bg=BG,
    width=262
)

right.pack(
    side="right",
    fill="y",
    padx=(14, 0)
)

right.pack_propagate(False)


# ============================================================
# LEFT CONTENT
# ============================================================

left_content = tk.Frame(
    content,
    bg=BG
)

left_content.pack(
    side="left",
    fill="both",
    expand=True
)


# ============================================================
# FILTER BAR
# ============================================================

filter_bar = tk.Frame(
    left_content,
    bg=PANEL,
    height=50,
    highlightbackground=BORDER,
    highlightthickness=1
)

filter_bar.pack(
    fill="x"
)

filter_bar.pack_propagate(False)


def filter_button(text, active=False):

    button = tk.Button(
        filter_bar,
        text=text,
        command=lambda: filter_tasks(
            "All" if text == "All Tasks" else text
        ),
        bg=GOLD if active else PANEL,
        fg=BG if active else WHITE,
        activebackground=LIGHT_GOLD,
        activeforeground=BG,
        relief="flat",
        font=(
            "Segoe UI",
            9,
            "bold" if active else "normal"
        ),
        padx=12,
        pady=4,
        cursor="hand2"
    )

    button.pack(
        side="left",
        padx=(10 if active else 3, 3),
        pady=10
    )


filter_button("All Tasks", True)
filter_button("Pending")
filter_button("In Progress")
filter_button("Completed")


# ============================================================
# SEARCH
# ============================================================

search_var = tk.StringVar()

search_var.trace_add(
    "write",
    search_tasks
)

search = tk.Entry(
    filter_bar,
    textvariable=search_var,
    bg="#0a1824",
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat",
    font=("Segoe UI", 9),
    width=22
)

search.pack(
    side="right",
    padx=14,
    pady=10,
    ipady=5
)


# ============================================================
# TABLE HEADER
# ============================================================

table_header = tk.Frame(
    left_content,
    bg=PANEL2,
    height=34
)

table_header.pack(
    fill="x"
)

table_header.pack_propagate(False)

tk.Label(
    table_header,
    text="Task",
    bg=PANEL2,
    fg=TEXT,
    font=("Segoe UI", 8, "bold")
).place(
    x=50,
    y=9
)

tk.Label(
    table_header,
    text="Priority",
    bg=PANEL2,
    fg=TEXT,
    font=("Segoe UI", 8, "bold")
).place(
    relx=COL_PRIORITY,
    y=9
)

tk.Label(
    table_header,
    text="Status",
    bg=PANEL2,
    fg=TEXT,
    font=("Segoe UI", 8, "bold")
).place(
    relx=COL_STATUS,
    y=9
)

tk.Label(
    table_header,
    text="Due Date",
    bg=PANEL2,
    fg=TEXT,
    font=("Segoe UI", 8, "bold")
).place(
    relx=COL_DATE,
    y=9
)


# ============================================================
# KEEP GOING BOX  (packed at the bottom BEFORE the task list,
# so it can never be pushed off-screen)
# ============================================================

keep_going = tk.Frame(
    left_content,
    bg=PANEL,
    height=64,
    highlightbackground=BORDER,
    highlightthickness=1
)

keep_going.pack(
    side="bottom",
    fill="x",
    pady=(10, 0)
)

keep_going.pack_propagate(False)

tk.Label(
    keep_going,
    text="💡",
    bg=PANEL,
    fg=GOLD,
    font=("Segoe UI Emoji", 24)
).pack(
    side="left",
    padx=(16, 14)
)

keep_text_frame = tk.Frame(
    keep_going,
    bg=PANEL
)

keep_text_frame.pack(
    side="left",
    fill="y"
)

tk.Label(
    keep_text_frame,
    text="Keep going!",
    bg=PANEL,
    fg=LIGHT_GOLD,
    font=("Georgia", 12, "bold")
).pack(
    anchor="w",
    pady=(12, 2)
)

tk.Label(
    keep_text_frame,
    text="You're doing great. Every task brings you closer to the legends.",
    bg=PANEL,
    fg=MUTED,
    font=("Segoe UI", 8)
).pack(
    anchor="w"
)


# ============================================================
# TASK CONTAINER
# ============================================================

task_container = tk.Frame(
    left_content,
    bg=PANEL,
    highlightbackground=BORDER,
    highlightthickness=1
)

task_container.pack(
    fill="both",
    expand=True
)


# ============================================================
# PROGRESS BOX
# ============================================================

progress_box = tk.Frame(
    right,
    bg=PANEL,
    height=140,
    highlightbackground=BORDER,
    highlightthickness=1
)

progress_box.pack(
    fill="x"
)

progress_box.pack_propagate(False)

tk.Label(
    progress_box,
    text="Your Progress",
    bg=PANEL,
    fg=LIGHT_GOLD,
    font=("Georgia", 12, "bold")
).pack(
    anchor="w",
    padx=14,
    pady=(8, 6)
)

circle = tk.Canvas(
    progress_box,
    width=90,
    height=90,
    bg=PANEL,
    highlightthickness=0
)

circle.place(
    x=8,
    y=38
)

circle.create_oval(
    10,
    10,
    80,
    80,
    outline="#27414f",
    width=9
)

progress_arc = circle.create_arc(
    10,
    10,
    80,
    80,
    start=45,
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

progress_label.place(
    x=45,
    y=36,
    anchor="center"
)

tk.Label(
    circle,
    text="Tasks",
    bg=PANEL,
    fg=MUTED,
    font=("Segoe UI", 7)
).place(
    x=45,
    y=54,
    anchor="center"
)


legend_items = [
    ("Completed", GREEN),
    ("Pending", "#6c93b8"),
    ("Overdue", RED)
]

legend_labels = {}


for i, (name, color) in enumerate(legend_items):

    y = 50 + i * 26

    tk.Label(
        progress_box,
        text="●",
        bg=PANEL,
        fg=color,
        font=("Segoe UI", 12)
    ).place(
        x=112,
        y=y
    )

    tk.Label(
        progress_box,
        text=name,
        bg=PANEL,
        fg=TEXT,
        font=("Segoe UI", 8)
    ).place(
        x=130,
        y=y + 3
    )

    value_label = tk.Label(
        progress_box,
        text="0",
        bg=PANEL,
        fg=WHITE,
        font=("Segoe UI", 8, "bold")
    )

    value_label.place(
        x=226,
        y=y + 3
    )

    legend_labels[name] = value_label


# ============================================================
# TASK OVERVIEW
# ============================================================

overview = tk.Frame(
    right,
    bg=PANEL,
    height=158,
    highlightbackground=BORDER,
    highlightthickness=1
)

overview.pack(
    fill="x",
    pady=8
)

overview.pack_propagate(False)

tk.Label(
    overview,
    text="Task Overview",
    bg=PANEL,
    fg=LIGHT_GOLD,
    font=("Georgia", 12, "bold")
).pack(
    anchor="w",
    padx=14,
    pady=(8, 6)
)


def overview_card(
    parent,
    x,
    y,
    title,
    value,
    icon,
    color
):

    card = tk.Frame(
        parent,
        bg=CARD,
        width=118,
        height=54
    )

    card.place(
        x=x,
        y=y
    )

    card.pack_propagate(False)

    tk.Label(
        card,
        text=icon,
        bg=CARD,
        fg=color,
        font=("Segoe UI Emoji", 15)
    ).place(
        x=8,
        y=8
    )

    tk.Label(
        card,
        text=title,
        bg=CARD,
        fg=MUTED,
        font=("Segoe UI", 7)
    ).place(
        x=36,
        y=8
    )

    label = tk.Label(
        card,
        text=value,
        bg=CARD,
        fg=WHITE,
        font=("Segoe UI", 13, "bold")
    )

    label.place(
        x=36,
        y=24
    )

    return label


total_label = overview_card(
    overview,
    8,
    42,
    "Total Tasks",
    "0",
    "▣",
    GOLD
)

completed_label = overview_card(
    overview,
    134,
    42,
    "Completed",
    "0",
    "✓",
    GREEN_LIGHT
)

pending_label = overview_card(
    overview,
    8,
    100,
    "Pending",
    "0",
    "◷",
    "#7ba3c6"
)

high_label = overview_card(
    overview,
    134,
    100,
    "High Priority",
    "0",
    "!",
    RED
)


# ============================================================
# QUOTE BOX  (packed at the bottom so it always stays visible)
# ============================================================

quote = tk.Frame(
    right,
    bg=PANEL,
    height=84,
    highlightbackground=BORDER,
    highlightthickness=1
)

quote.pack(
    side="bottom",
    fill="x"
)

quote.pack_propagate(False)

tk.Label(
    quote,
    text='"The mountains, the rivers — all are\npart of who we are."',
    bg=PANEL,
    fg=LIGHT_GOLD,
    font=("Georgia", 9, "italic"),
    justify="left"
).pack(
    anchor="w",
    padx=14,
    pady=(12, 4)
)

tk.Label(
    quote,
    text="──── ❈ ────",
    bg=PANEL,
    fg=GOLD,
    font=("Segoe UI", 9)
).pack()


# ============================================================
# PRIORITY GUIDE
# ============================================================

guide = tk.Frame(
    right,
    bg=PANEL,
    highlightbackground=BORDER,
    highlightthickness=1
)

guide.pack(
    side="top",
    fill="both",
    expand=True,
    pady=(0, 8)
)

guide.pack_propagate(False)

tk.Label(
    guide,
    text="Priority Guide",
    bg=PANEL,
    fg=LIGHT_GOLD,
    font=("Georgia", 12, "bold")
).pack(
    anchor="w",
    padx=14,
    pady=(8, 6)
)

priority_data = [
    (
        "!",
        "High",
        "Important tasks that you want\nto complete first.",
        RED
    ),
    (
        "−",
        "Medium",
        "Tasks that are important\nbut not urgent.",
        YELLOW
    ),
    (
        "↓",
        "Low",
        "Tasks for later exploration\nand learning.",
        GREEN
    )
]


for i, (icon, title, description, color) in enumerate(priority_data):

    y = 40 + i * 42

    tk.Label(
        guide,
        text=icon,
        bg=color,
        fg=WHITE,
        font=("Segoe UI", 11, "bold"),
        width=3,
        height=1
    ).place(
        x=14,
        y=y
    )

    tk.Label(
        guide,
        text=title,
        bg=PANEL,
        fg=WHITE,
        font=("Segoe UI", 8, "bold")
    ).place(
        x=54,
        y=y - 2
    )

    tk.Label(
        guide,
        text=description,
        bg=PANEL,
        fg=MUTED,
        font=("Segoe UI", 7),
        justify="left"
    ).place(
        x=54,
        y=y + 12
    )


# ============================================================
# START
# ============================================================

refresh_tasks()

root.after(
    200,
    update_header_image
)

root.mainloop()