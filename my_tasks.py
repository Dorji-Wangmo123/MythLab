import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
from pathlib import Path


# ============================================================
# MYTHLAB - MY TASKS DASHBOARD
# Tkinter + Pillow
# ============================================================

root = tk.Tk()
root.title("MythLab - My Tasks")
root.geometry("1280x853")
root.minsize(1100, 700)
root.configure(bg="#061522")


# ============================================================
# COLORS
# ============================================================

BG = "#061522"
SIDEBAR = "#04131f"
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


# ============================================================
# IMAGE FOLDER
# ============================================================

IMAGE_FOLDER = Path(__file__).resolve().parent


# ============================================================
# IMAGE FUNCTIONS
# ============================================================

def find_image(keywords):

    extensions = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".bmp"
    }

    files = [
        file
        for file in IMAGE_FOLDER.iterdir()
        if file.is_file()
        and file.suffix.lower() in extensions
    ]

    # Find a file containing ALL keywords
    for file in files:

        filename = file.stem.lower()

        if all(
            word.lower() in filename
            for word in keywords
        ):
            return file

    # Find a file containing ANY keyword
    for file in files:

        filename = file.stem.lower()

        if any(
            word.lower() in filename
            for word in keywords
        ):
            return file

    return None


def load_task_image(
    keywords,
    width=54,
    height=48
):

    image_path = find_image(keywords)

    if image_path is None:
        return None

    try:

        image = Image.open(
            image_path
        ).convert("RGB")

        original_width, original_height = image.size

        scale = max(
            width / original_width,
            height / original_height
        )

        new_width = int(
            original_width * scale
        )

        new_height = int(
            original_height * scale
        )

        image = image.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS
        )

        left = (
            new_width - width
        ) // 2

        top = (
            new_height - height
        ) // 2

        right = left + width
        bottom = top + height

        image = image.crop(
            (
                left,
                top,
                right,
                bottom
            )
        )

        return ImageTk.PhotoImage(image)

    except Exception as error:

        print(
            "Could not load image:",
            image_path
        )

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
        "description":
            "Learn about the Thunder Dragon and its role in Bhutanese mythology.",
        "priority": "High",
        "status": "Pending",
        "date": "25 Apr 2026",
        "icon": "🐉",
        "image_keywords":
            TASK_IMAGE_KEYWORDS[0]
    },

    {
        "title":
            "Explore Bhutanese mythical creatures",
        "description":
            "Learn about Druk, Yeti, Migoi and other beings.",
        "priority": "Medium",
        "status": "Completed",
        "date": "24 Apr 2026",
        "icon": "👹",
        "image_keywords":
            TASK_IMAGE_KEYWORDS[1]
    },

    {
        "title":
            "Read the story of the Great Yeti",
        "description":
            "Discover the legend of the Yeti in the Himalayas.",
        "priority": "High",
        "status": "Pending",
        "date": "27 Apr 2026",
        "icon": "🏔",
        "image_keywords":
            TASK_IMAGE_KEYWORDS[2]
    },

    {
        "title":
            "Watch The Firebird",
        "description":
            "Learn about the symbol of rebirth and hope.",
        "priority": "Low",
        "status": "Pending",
        "date": "28 Apr 2026",
        "icon": "🔥",
        "image_keywords":
            TASK_IMAGE_KEYWORDS[3]
    },

    {
        "title":
            "Explore Punakha Dzong",
        "description":
            "Learn about the history and significance of Punakha Dzong.",
        "priority": "Medium",
        "status": "Completed",
        "date": "22 Apr 2026",
        "icon": "🏯",
        "image_keywords":
            TASK_IMAGE_KEYWORDS[4]
    },

    {
        "title":
            "Take the Mythology Quiz",
        "description":
            "Test what you've learned so far.",
        "priority": "High",
        "status": "Pending",
        "date": "30 Apr 2026",
        "icon": "🐲",
        "image_keywords":
            TASK_IMAGE_KEYWORDS[5]
    }
]


current_tasks = tasks.copy()


# ============================================================
# PRELOAD TASK IMAGES
# ============================================================

task_images = {}

for number, keywords in enumerate(
    TASK_IMAGE_KEYWORDS
):

    task_images[number] = load_task_image(
        keywords,
        54,
        48
    )


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def rounded_box(
    parent,
    width,
    height,
    bg,
    border=None
):

    frame = tk.Frame(
        parent,
        width=width,
        height=height,
        bg=bg,
        highlightbackground=
            border if border else bg,
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
        bg=kwargs.pop(
            "bg",
            parent.cget("bg")
        ),
        fg=color,
        font=(
            font,
            size,
            weight
        ),
        **kwargs
    )


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

    progress_label.config(
        text=f"{completed}/{total}"
    )

    total_label.config(
        text=str(total)
    )

    completed_label.config(
        text=str(completed)
    )

    pending_label.config(
        text=str(pending)
    )

    high_label.config(
        text=str(high)
    )


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
    ).pack(
        pady=20
    )

    tk.Label(
        window,
        text="Task title",
        bg=BG,
        fg=WHITE,
        font=("Segoe UI", 10)
    ).pack(
        anchor="w",
        padx=30
    )

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
        pady=8
    )

    title_entry.insert(
        0,
        task["title"]
    )

    tk.Label(
        window,
        text="Description",
        bg=BG,
        fg=WHITE,
        font=("Segoe UI", 10)
    ).pack(
        anchor="w",
        padx=30
    )

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
        pady=8
    )

    desc_entry.insert(
        0,
        task["description"]
    )

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
    ).pack(
        pady=20
    )


# ============================================================
# FILTER TASKS
# ============================================================

def filter_tasks(filter_type):

    if filter_type == "All":

        filtered = current_tasks

    elif filter_type == "Pending":

        filtered = [
            t
            for t in current_tasks
            if t["status"] == "Pending"
        ]

    elif filter_type == "In Progress":

        filtered = [
            t
            for t in current_tasks
            if t["status"] == "In Progress"
        ]

    elif filter_type == "Completed":

        filtered = [
            t
            for t in current_tasks
            if t["status"] == "Completed"
        ]

    display_tasks(filtered)


def search_tasks(*args):

    keyword = search_var.get().lower()

    filtered = [

        task

        for task in current_tasks

        if keyword in
        task["title"].lower()

        or keyword in
        task["description"].lower()
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
            height=74
        )

        row.pack(
            fill="x",
            padx=3,
            pady=0
        )

        row.pack_propagate(False)

        # ----------------------------------------------------
        # CHECKBOX
        # ----------------------------------------------------

        checked = (
            task["status"] == "Completed"
        )

        check_text = (
            "☑"
            if checked
            else "☐"
        )

        check_button = tk.Button(
            row,
            text=check_text,
            command=lambda t=task:
                toggle_task(t),
            bg=PANEL,
            fg=(
                GOLD
                if checked
                else "#8d9ba5"
            ),
            activebackground=PANEL,
            activeforeground=GOLD,
            borderwidth=0,
            font=("Segoe UI Symbol", 19),
            cursor="hand2"
        )

        check_button.place(
            x=13,
            y=20
        )

        # ----------------------------------------------------
        # REAL IMAGE
        # ----------------------------------------------------

        image_number = tasks.index(task)

        real_image = task_images.get(
            image_number
        )

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

        image_box.place(
            x=58,
            y=12,
            width=54,
            height=48
        )

        # ----------------------------------------------------
        # TASK TITLE
        # ----------------------------------------------------

        title_color = (
            MUTED
            if checked
            else WHITE
        )

        title = tk.Label(
            row,
            text=task["title"],
            bg=PANEL,
            fg=title_color,
            font=("Segoe UI", 9, "bold"),
            anchor="w"
        )

        title.place(
            x=120,
            y=8,
            width=245,
            height=22
        )

        # ----------------------------------------------------
        # DESCRIPTION
        # ----------------------------------------------------

        description = tk.Label(
            row,
            text=task["description"],
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 7),
            anchor="w"
        )

        description.place(
            x=120,
            y=32,
            width=245,
            height=18
        )

        # ----------------------------------------------------
        # PRIORITY
        # ----------------------------------------------------

        priority_colors = {
            "High": RED,
            "Medium": YELLOW,
            "Low": GREEN
        }

        priority = tk.Label(
            row,
            text=task["priority"],
            bg=priority_colors[
                task["priority"]
            ],
            fg=WHITE,
            font=("Segoe UI", 8, "bold"),
            width=8,
            pady=4
        )

        priority.place(
            x=380,
            y=24
        )

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

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
            pady=4
        )

        status.place(
            x=480,
            y=24
        )

        # ----------------------------------------------------
        # DATE
        # ----------------------------------------------------

        date = tk.Label(
            row,
            text=task["date"],
            bg=PANEL,
            fg=TEXT,
            font=("Segoe UI", 8)
        )

        date.place(
            x=600,
            y=27
        )

        # ----------------------------------------------------
        # EDIT BUTTON
        # ----------------------------------------------------

        edit = tk.Button(
            row,
            text="✎",
            command=lambda t=task:
                edit_task(t),
            bg=PANEL,
            fg=GOLD,
            activebackground=PANEL2,
            activeforeground=LIGHT_GOLD,
            borderwidth=0,
            font=("Segoe UI", 15),
            cursor="hand2"
        )

        edit.place(
            x=690,
            y=18
        )

        # ----------------------------------------------------
        # DELETE BUTTON
        # ----------------------------------------------------

        delete = tk.Button(
            row,
            text="♜",
            command=lambda t=task:
                delete_task(t),
            bg=PANEL,
            fg=RED,
            activebackground=PANEL2,
            activeforeground=RED,
            borderwidth=0,
            font=("Segoe UI", 13),
            cursor="hand2"
        )

        delete.place(
            x=725,
            y=20
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
    width=205
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
    font=("Segoe UI Emoji", 35)
)

logo.pack(
    pady=(20, 0)
)

logo_title = tk.Label(
    sidebar,
    text="MythLab",
    bg=SIDEBAR,
    fg=LIGHT_GOLD,
    font=("Georgia", 22, "bold")
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
    pady=(0, 25)
)


# ============================================================
# SIDEBAR BUTTON
# ============================================================

def sidebar_button(
    text,
    icon,
    active=False
):

    bg = (
        "#3d3b31"
        if active
        else SIDEBAR
    )

    button = tk.Frame(
        sidebar,
        bg=bg,
        height=45
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
        font=("Segoe UI Emoji", 18)
    )

    icon_label.pack(
        side="left",
        padx=(12, 12)
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
sidebar_button(
    "My Tasks",
    "▣",
    True
)
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
    padx=18,
    pady=25
)

tk.Label(
    quote_frame,
    text="╱╲╱╲╱╲",
    bg=SIDEBAR,
    fg="#294152",
    font=("Segoe UI", 18)
).pack()

tk.Label(
    quote_frame,
    text='"Every myth is a door\nto a deeper wisdom."',
    bg=SIDEBAR,
    fg=LIGHT_GOLD,
    font=("Georgia", 10, "italic"),
    justify="left"
).pack(
    pady=8
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
    height=155
)

header.pack(
    fill="x"
)

header.pack_propagate(False)


# ============================================================
# HEADER BACKGROUND IMAGE
# ============================================================

header_image_path = find_image(
    ["welcome"]
)

if header_image_path is None:

    header_image_path = find_image(
        ["background"]
    )

if header_image_path is None:

    header_image_path = find_image(
        ["mountain"]
    )

if header_image_path is None:

    header_image_path = find_image(
        ["bhutan"]
    )


header_image_label = None
header_photo = None


def update_header_image(event=None):

    global header_photo

    if header_image_path is None:
        return

    try:

        width = header.winfo_width()
        height = header.winfo_height()

        if width <= 1 or height <= 1:
            return

        image = Image.open(
            header_image_path
        ).convert("RGB")

        image = image.resize(
            (width, height),
            Image.Resampling.LANCZOS
        )

        overlay = Image.new(
            "RGB",
            image.size,
            "#061522"
        )

        image = Image.blend(
            image,
            overlay,
            0.35
        )

        header_photo = ImageTk.PhotoImage(
            image
        )

        header_image_label.config(
            image=header_photo
        )

    except Exception as error:

        print(
            "Header image error:",
            error
        )


if header_image_path:

    header_image_label = tk.Label(
        header,
        bg=BG,
        borderwidth=0
    )

    header_image_label.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )

    header.bind(
        "<Configure>",
        update_header_image
    )


# ============================================================
# HEADER TEXT
# ============================================================

tk.Label(
    header,
    text="▣",
    bg=BG,
    fg=GOLD,
    font=("Segoe UI", 36)
).place(
    x=35,
    y=50
)

tk.Label(
    header,
    text="My Tasks",
    bg=BG,
    fg=LIGHT_GOLD,
    font=("Georgia", 30, "bold")
).place(
    x=85,
    y=48
)

tk.Label(
    header,
    text="Complete your learning tasks, track your progress and build your knowledge",
    bg=BG,
    fg=TEXT,
    font=("Segoe UI", 9)
).place(
    x=87,
    y=91
)

tk.Label(
    header,
    text="about myths, legends and creatures.",
    bg=BG,
    fg=TEXT,
    font=("Segoe UI", 9)
).place(
    x=87,
    y=108
)


# ============================================================
# TOP RIGHT ICONS
# ============================================================

tk.Label(
    header,
    text="⌕",
    bg=BG,
    fg=GOLD,
    font=("Segoe UI", 25)
).place(
    relx=0.91,
    y=18
)

tk.Label(
    header,
    text="♧",
    bg=BG,
    fg=GOLD,
    font=("Segoe UI", 20)
).place(
    relx=0.95,
    y=20
)

tk.Label(
    header,
    text="●",
    bg=BG,
    fg=LIGHT_GOLD,
    font=("Segoe UI", 25)
).place(
    relx=0.98,
    y=17
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
    padx=18,
    pady=(0, 12)
)


# ============================================================
# LEFT CONTENT
# KEEP WIDE
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
    height=55,
    highlightbackground=BORDER,
    highlightthickness=1
)

filter_bar.pack(
    fill="x"
)

filter_bar.pack_propagate(False)


def filter_button(
    text,
    active=False
):

    button = tk.Button(
        filter_bar,
        text=text,
        command=lambda:
            filter_tasks(
                "All"
                if text == "All Tasks"
                else text
            ),
        bg=(
            GOLD
            if active
            else PANEL
        ),
        fg=(
            BG
            if active
            else WHITE
        ),
        activebackground=LIGHT_GOLD,
        activeforeground=BG,
        relief="flat",
        font=(
            "Segoe UI",
            9,
            "bold"
            if active
            else "normal"
        ),
        padx=15,
        pady=5,
        cursor="hand2"
    )

    button.pack(
        side="left",
        padx=(
            8 if active else 2,
            2
        ),
        pady=12
    )


filter_button(
    "All Tasks",
    True
)

filter_button(
    "Pending"
)

filter_button(
    "In Progress"
)

filter_button(
    "Completed"
)


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
    bg="#071522",
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat",
    font=("Segoe UI", 9)
)

search.pack(
    side="right",
    padx=15,
    pady=12,
    ipady=5,
    ipadx=40
)


# ============================================================
# TABLE HEADER
# ============================================================

table_header = tk.Frame(
    left_content,
    bg=PANEL2,
    height=40
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
    x=60,
    y=13
)

tk.Label(
    table_header,
    text="Priority",
    bg=PANEL2,
    fg=TEXT,
    font=("Segoe UI", 8, "bold")
).place(
    x=380,
    y=13
)

tk.Label(
    table_header,
    text="Status",
    bg=PANEL2,
    fg=TEXT,
    font=("Segoe UI", 8, "bold")
).place(
    x=480,
    y=13
)

tk.Label(
    table_header,
    text="Due Date",
    bg=PANEL2,
    fg=TEXT,
    font=("Segoe UI", 8, "bold")
).place(
    x=600,
    y=13
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
# KEEP GOING BOX
# ============================================================

keep_going = tk.Frame(
    left_content,
    bg=PANEL,
    height=72,
    highlightbackground=BORDER,
    highlightthickness=1
)

keep_going.pack(
    fill="x",
    pady=(12, 0)
)

keep_going.pack_propagate(False)

tk.Label(
    keep_going,
    text="💡",
    bg=PANEL,
    fg=GOLD,
    font=("Segoe UI Emoji", 27)
).pack(
    side="left",
    padx=18
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
    font=("Georgia", 13, "bold")
).pack(
    anchor="w",
    pady=(15, 0)
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
# RIGHT SIDEBAR
# ============================================================

right = tk.Frame(
    content,
    bg=BG,
    width=280
)

right.pack(
    side="right",
    fill="y",
    padx=(12, 0)
)

right.pack_propagate(False)


# ============================================================
# PROGRESS BOX
# ============================================================

progress_box = tk.Frame(
    right,
    bg=PANEL,
    height=150,
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
    padx=15,
    pady=10
)


circle = tk.Canvas(
    progress_box,
    width=90,
    height=90,
    bg=PANEL,
    highlightthickness=0
)

circle.place(
    x=10,
    y=43
)

circle.create_oval(
    10,
    10,
    80,
    80,
    outline="#253f4f",
    width=9
)

circle.create_arc(
    10,
    10,
    80,
    80,
    start=45,
    extent=180,
    style="arc",
    outline=GREEN_LIGHT,
    width=9
)

progress_label = tk.Label(
    circle,
    text="3/6",
    bg=PANEL,
    fg=WHITE,
    font=("Segoe UI", 13, "bold")
)

progress_label.place(
    x=31,
    y=29
)

tk.Label(
    circle,
    text="Tasks",
    bg=PANEL,
    fg=MUTED,
    font=("Segoe UI", 7)
).place(
    x=31,
    y=47
)


legend_items = [
    ("Completed", GREEN, "3"),
    ("Pending", "#6996c2", "3"),
    ("Overdue", RED, "0")
]


for i, (
    name,
    color,
    value
) in enumerate(
    legend_items
):

    y = 57 + i * 25

    tk.Label(
        progress_box,
        text="●",
        bg=PANEL,
        fg=color,
        font=("Segoe UI", 12)
    ).place(
        x=140,
        y=y
    )

    tk.Label(
        progress_box,
        text=name,
        bg=PANEL,
        fg=TEXT,
        font=("Segoe UI", 8)
    ).place(
        x=157,
        y=y + 2
    )

    tk.Label(
        progress_box,
        text=value,
        bg=PANEL,
        fg=WHITE,
        font=("Segoe UI", 8, "bold")
    ).place(
        x=245,
        y=y + 2
    )


# ============================================================
# TASK OVERVIEW
# ============================================================

overview = tk.Frame(
    right,
    bg=PANEL,
    height=170,
    highlightbackground=BORDER,
    highlightthickness=1
)

overview.pack(
    fill="x",
    pady=10
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
    padx=15,
    pady=10
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
        bg="#0d2637",
        width=120,
        height=60
    )

    card.place(
        x=x,
        y=y
    )

    card.pack_propagate(False)

    tk.Label(
        card,
        text=icon,
        bg="#0d2637",
        fg=color,
        font=("Segoe UI Emoji", 16)
    ).place(
        x=10,
        y=10
    )

    tk.Label(
        card,
        text=title,
        bg="#0d2637",
        fg=MUTED,
        font=("Segoe UI", 7)
    ).place(
        x=38,
        y=10
    )

    label = tk.Label(
        card,
        text=value,
        bg="#0d2637",
        fg=WHITE,
        font=("Segoe UI", 14, "bold")
    )

    label.place(
        x=38,
        y=28
    )

    return label


total_label = overview_card(
    overview,
    10,
    45,
    "Total Tasks",
    "6",
    "▣",
    GOLD
)

completed_label = overview_card(
    overview,
    140,
    45,
    "Completed",
    "3",
    "✓",
    GREEN_LIGHT
)

pending_label = overview_card(
    overview,
    10,
    110,
    "Pending",
    "3",
    "◷",
    "#6f9ec5"
)

high_label = overview_card(
    overview,
    140,
    110,
    "High Priority",
    "3",
    "!",
    RED
)


# ============================================================
# PRIORITY GUIDE
# ============================================================

guide = tk.Frame(
    right,
    bg=PANEL,
    height=195,
    highlightbackground=BORDER,
    highlightthickness=1
)

guide.pack(
    fill="x"
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
    padx=15,
    pady=10
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


for i, (
    icon,
    title,
    description,
    color
) in enumerate(
    priority_data
):

    y = 45 + i * 48

    tk.Label(
        guide,
        text=icon,
        bg=color,
        fg=WHITE,
        font=("Segoe UI", 12, "bold"),
        width=3,
        height=1
    ).place(
        x=15,
        y=y
    )

    tk.Label(
        guide,
        text=title,
        bg=PANEL,
        fg=WHITE,
        font=("Segoe UI", 8, "bold")
    ).place(
        x=55,
        y=y
    )

    tk.Label(
        guide,
        text=description,
        bg=PANEL,
        fg=MUTED,
        font=("Segoe UI", 7),
        justify="left"
    ).place(
        x=55,
        y=y + 15
    )


# ============================================================
# QUOTE BOX
# ============================================================

quote = tk.Frame(
    right,
    bg=PANEL,
    height=115,
    highlightbackground=BORDER,
    highlightthickness=1
)

quote.pack(
    fill="x",
    pady=10
)

quote.pack_propagate(False)

tk.Label(
    quote,
    text='"The mountains, the rivers — all are\npart of who we are."',
    bg=PANEL,
    fg=LIGHT_GOLD,
    font=("Georgia", 10, "italic"),
    justify="left"
).pack(
    anchor="w",
    padx=18,
    pady=(25, 5)
)

tk.Label(
    quote,
    text="──── ❈ ────",
    bg=PANEL,
    fg=GOLD,
    font=("Segoe UI", 9)
).pack()


# ============================================================
# START
# ============================================================

refresh_tasks()

root.after(
    200,
    update_header_image
)

root.mainloop()