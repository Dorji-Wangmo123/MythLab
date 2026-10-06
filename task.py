'''import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path
from datetime import datetime, timedelta
import json
import shutil
import subprocess
import sys
import time
from PIL import Image, ImageTk, ImageOps


# ==================================================
# MAIN WINDOW
# ==================================================

root = tk.Tk()
root.title("MythLab - My Tasks")
root.geometry("1280x900")
root.minsize(1000, 700)
root.configure(bg="#061b2b")


# ==================================================
# COLOURS
# ==================================================

BG = "#061b2b"
SIDEBAR = "#071522"
CARD = "#092333"
FIELD = "#102b3d"
GOLD = "#d6a84f"
TEXT = "#f5ead0"
LIGHT_TEXT = "#c7c1b3"
RED = "#ff7b7b"
GREEN = "#6fcf97"
BLUE = "#8fb4f5"
AMBER = "#e6b84f"

PRIORITY_COLORS = {
    "High": ("#4a1a24", RED),
    "Medium": ("#3d3016", AMBER),
    "Low": ("#173d2a", GREEN)
}

STATUS_COLORS = {
    "Pending": ("#17325a", BLUE),
    "In Progress": ("#3d3016", AMBER),
    "Completed": ("#173d2a", GREEN)
}

PRIORITIES = ["High", "Medium", "Low"]
STATUSES = ["Pending", "In Progress", "Completed"]


# ==================================================
# IMAGE LOCATION
# All images are in the same folder as my_tasks.py
# ==================================================

IMAGE_DIR = Path(__file__).parent

image_refs = []


# ==================================================
# USER + TASK FILE
# username is sent by the login page (sys.argv[1])
# ==================================================

USERNAME = sys.argv[1] if len(sys.argv) > 1 else "guest"

TASKS_FILE = IMAGE_DIR / ("tasks_" + USERNAME + ".json")

DATE_FORMAT = "%d %b %Y"


def days_from_today(days):

    return (datetime.now() + timedelta(days=days)).strftime(DATE_FORMAT)


# image = file name in the same folder as this file
DEFAULT_TASKS = [

    {
        "title": "Read about the Thunder Dragon",
        "description": "Learn about the Thunder Dragon and its role in Bhutanese mythology.",
        "priority": "High",
        "status": "Pending",
        "due": days_from_today(3),
        "image": "thumb1.png"
    },

    {
        "title": "Explore Bhutanese mythical creatures",
        "description": "Learn about Druk, Yeti, Migoi and other beings.",
        "priority": "Medium",
        "status": "Completed",
        "due": days_from_today(2),
        "image": "thumb2.png"
    },

    {
        "title": "Read the story of The Great Yeti",
        "description": "Discover the legend of the Yeti in the Himalayas.",
        "priority": "High",
        "status": "Pending",
        "due": days_from_today(5),
        "image": "thumb3.png"
    },

    {
        "title": "Watch a short video: The Firebird",
        "description": "Learn about the symbol of rebirth and hope.",
        "priority": "Low",
        "status": "Pending",
        "due": days_from_today(6),
        "image": "thumb4.png"
    },

    {
        "title": "Explore Punakha Dzong",
        "description": "Learn about the history and significance of Punakha Dzong.",
        "priority": "Medium",
        "status": "Completed",
        "due": days_from_today(0),
        "image": "thumb5.png"
    },

    {
        "title": "Take the Mythology Quiz",
        "description": "Test what you've learned so far.",
        "priority": "High",
        "status": "Pending",
        "due": days_from_today(8),
        "image": "thumb6.png"
    }
]


def load_tasks():

    if TASKS_FILE.exists():

        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as file:
                return json.load(file)

        except (json.JSONDecodeError, OSError):
            pass

    return [dict(task) for task in DEFAULT_TASKS]


def save_tasks():

    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2, ensure_ascii=False)


def due_date(task):

    try:
        return datetime.strptime(task["due"], DATE_FORMAT)

    except ValueError:
        return datetime.max


def is_overdue(task):

    return (
        task["status"] != "Completed"
        and due_date(task).date() < datetime.now().date()
    )


tasks = load_tasks()

current_filter = "All Tasks"


# ==================================================
# LOAD IMAGE
# ==================================================

def load_image(filename, size):

    path = IMAGE_DIR / filename

    try:
        image = Image.open(path).convert("RGB")

        image = ImageOps.fit(
            image,
            size,
            method=Image.Resampling.LANCZOS
        )

        photo = ImageTk.PhotoImage(image)

        image_refs.append(photo)

        return photo

    except Exception as error:

        print("Could not load:", path)
        print("Error:", error)

        return None


# ==================================================
# CREATE TASK IMAGE
# ==================================================

def create_image(parent, filename, size):

    photo = load_image(filename, size) if filename else None

    if photo:

        label = tk.Label(
            parent,
            image=photo,
            bg=CARD
        )

    else:

        label = tk.Label(
            parent,
            text="NO\nIMAGE",
            font=("Arial", 8),
            bg="#183b50",
            fg=LIGHT_TEXT,
            width=10,
            height=4
        )

    return label


# ==================================================
# SIDEBAR
# ==================================================

sidebar = tk.Frame(
    root,
    bg=SIDEBAR,
    width=215
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


# ==================================================
# LOGO
# ==================================================

tk.Label(
    sidebar,
    text="🐉",
    font=("Arial", 32),
    bg=SIDEBAR,
    fg=GOLD
).pack(
    pady=(18, 0)
)

tk.Label(
    sidebar,
    text="MythLab",
    font=("Georgia", 22, "bold"),
    bg=SIDEBAR,
    fg=GOLD
).pack()

tk.Label(
    sidebar,
    text="Explore. Learn. Believe.",
    font=("Arial", 9),
    bg=SIDEBAR,
    fg=LIGHT_TEXT
).pack(
    pady=(0, 28)
)


# ==================================================
# SIDEBAR MENU
# Each page opens its own file if it exists
# ==================================================

PAGE_FILES = {
    "Home": "home.py",
    "Myths": "myths.py",
    "Creatures": "creatures.py",
    "Regions": "regions.py",
    "My Tasks": "my_tasks.py",
    "Quiz": "quiz.py",
    "Favourites": "favourites.py",
    "About": "about.py"
}


def open_page(page):

    if page == "My Tasks":
        return

    page_file = IMAGE_DIR / PAGE_FILES[page]

    if page_file.exists():

        root.destroy()

        subprocess.Popen(
            [sys.executable, str(page_file), USERNAME]
        )

    else:

        messagebox.showinfo(
            page,
            page + " page will be added here."
        )


menu_items = [
    ("⌂  Home", "Home"),
    ("📖  Myths", "Myths"),
    ("🐉  Creatures", "Creatures"),
    ("🌐  Regions", "Regions"),
    ("✓  My Tasks", "My Tasks"),
    ("?  Quiz", "Quiz"),
    ("♡  Favourites", "Favourites"),
    ("ⓘ  About", "About")
]


for text, page in menu_items:

    active = page == "My Tasks"

    tk.Button(
        sidebar,
        text=text,
        font=("Arial", 11),
        bg="#2a2518" if active else SIDEBAR,
        fg=GOLD if active else TEXT,
        activebackground="#263b47",
        activeforeground=GOLD,
        relief="flat",
        anchor="w",
        padx=20,
        pady=10,
        highlightthickness=1 if active else 0,
        highlightbackground=GOLD,
        command=lambda p=page: open_page(p)
    ).pack(
        fill="x",
        padx=10,
        pady=2
    )


# ==================================================
# SIDEBAR QUOTE
# ==================================================

mountain_img = load_image("mountains.png", (220, 150))

tk.Label(
    sidebar,
    text='“Every myth is a door\nto a deeper wisdom.”\n\n— Bhutanese Wisdom',
    font=("Georgia", 9, "italic"),
    bg=SIDEBAR,
    fg=GOLD,
    justify="center",
    image=mountain_img,
    compound="center"
).pack(side="bottom", pady=10)


# ==================================================
# MAIN AREA
# ==================================================

main_area = tk.Frame(
    root,
    bg=BG
)

main_area.pack(
    side="right",
    fill="both",
    expand=True
)


# ==================================================
# SCROLLABLE CANVAS
# ==================================================

canvas = tk.Canvas(
    main_area,
    bg=BG,
    highlightthickness=0
)

scrollbar = tk.Scrollbar(
    main_area,
    orient="vertical",
    command=canvas.yview
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

scrollbar.pack(
    side="right",
    fill="y"
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)


content = tk.Frame(
    canvas,
    bg=BG
)

content_window = canvas.create_window(
    (0, 0),
    window=content,
    anchor="nw"
)


def update_scroll(event=None):

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )


def resize_content(event):

    canvas.itemconfig(
        content_window,
        width=event.width
    )


content.bind(
    "<Configure>",
    update_scroll
)

canvas.bind(
    "<Configure>",
    resize_content
)


def scroll_canvas(event):

    canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


canvas.bind_all(
    "<MouseWheel>",
    scroll_canvas
)


# ==================================================
# HERO SECTION
# ==================================================

hero = tk.Frame(
    content,
    bg="#183b50",
    height=200
)

hero.pack(
    fill="x",
    padx=30,
    pady=(0, 15)
)

hero.pack_propagate(False)


hero_photo = load_image(
    "welcome.png",
    (1050, 200)
)


if hero_photo:

    tk.Label(
        hero,
        image=hero_photo,
        bg="#183b50"
    ).place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )

else:

    hero_img = load_image("banner.png", (800, 250))

hero_image = tk.Label(
    hero,
    image=hero_img
)

hero_image.place(
    x=0,
    y=0,
    relwidth=1,
    relheight=1
)

hero_image.image = hero_img

# ==================================================
# HERO TEXT
# ==================================================

hero_text = tk.Frame(
    hero,
    bg="#061b2b"
)

hero_text.place(
    x=25,
    y=25
)


tk.Label(
    hero_text,
    text="Tasks",
    font=("Arial", 10),
    bg="#061b2b",
    fg=GOLD
).pack(
    anchor="w"
)


tk.Label(
    hero_text,
    text="✥  My Tasks",
    font=("Georgia", 25, "bold"),
    bg="#061b2b",
    fg=TEXT
).pack(
    anchor="w",
    pady=5
)


tk.Label(
    hero_text,
    text="Complete your learning tasks, track your progress and\n"
         "build your knowledge about myths, legends and creatures.",
    font=("Arial", 10),
    bg="#061b2b",
    fg=LIGHT_TEXT,
    justify="left"
).pack(
    anchor="w",
    pady=(10, 0)
)


# ==================================================
# STATS CARDS
# ==================================================

stats_frame = tk.Frame(
    content,
    bg=BG
)

stats_frame.pack(
    fill="x",
    padx=30,
    pady=(0, 12)
)

stat_labels = {}

for column, (name, color) in enumerate([
    ("Total Tasks", GOLD),
    ("Completed", GREEN),
    ("In Progress", AMBER),
    ("Pending", BLUE),
    ("Overdue", RED)
]):

    stats_frame.grid_columnconfigure(column, weight=1, uniform="stat")

    box = tk.Frame(
        stats_frame,
        bg=CARD
    )

    box.grid(
        row=0,
        column=column,
        sticky="ew",
        padx=5
    )

    number = tk.Label(
        box,
        text="0",
        font=("Georgia", 22, "bold"),
        bg=CARD,
        fg=color
    )

    number.pack(
        pady=(10, 0)
    )

    tk.Label(
        box,
        text=name,
        font=("Arial", 9),
        bg=CARD,
        fg=LIGHT_TEXT
    ).pack(
        pady=(0, 10)
    )

    stat_labels[name] = number


# ==================================================
# PROGRESS BAR
# ==================================================

progress_frame = tk.Frame(
    content,
    bg=CARD
)

progress_frame.pack(
    fill="x",
    padx=35,
    pady=(0, 15)
)

progress_text = tk.Label(
    progress_frame,
    text="Your Progress",
    font=("Georgia", 11, "bold"),
    bg=CARD,
    fg=TEXT
)

progress_text.pack(
    anchor="w",
    padx=15,
    pady=(10, 4)
)

progress_bar = tk.Canvas(
    progress_frame,
    height=12,
    bg=CARD,
    highlightthickness=0
)

progress_bar.pack(
    fill="x",
    padx=15,
    pady=(0, 12)
)


def draw_progress(event=None):

    progress_bar.delete("all")

    width = progress_bar.winfo_width()

    done = sum(1 for task in tasks if task["status"] == "Completed")

    total = len(tasks)

    progress_bar.create_rectangle(
        0, 0, width, 12,
        fill="#183b50",
        outline=""
    )

    if total and done:

        progress_bar.create_rectangle(
            0, 0, width * done / total, 12,
            fill=GOLD,
            outline=""
        )


progress_bar.bind(
    "<Configure>",
    draw_progress
)


# ==================================================
# SEARCH BAR + ADD BUTTON
# ==================================================

search_frame = tk.Frame(
    content,
    bg=BG
)

search_frame.pack(
    fill="x",
    padx=30,
    pady=(0, 12)
)

search_var = tk.StringVar()

search_entry = tk.Entry(
    search_frame,
    textvariable=search_var,
    font=("Arial", 11),
    bg=FIELD,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat"
)

search_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=10,
    padx=(0, 10)
)

search_var.trace_add(
    "write",
    lambda *args: refresh()
)


# ==================================================
# FILTER BUTTONS
# ==================================================

filter_frame = tk.Frame(
    content,
    bg=BG
)

filter_frame.pack(
    fill="x",
    padx=30,
    pady=(0, 12)
)


def set_filter(name):

    global current_filter

    current_filter = name

    refresh()


# ==================================================
# TASK LIST AREA
# ==================================================

task_area = tk.Frame(
    content,
    bg=BG
)

task_area.pack(
    fill="x",
    padx=30
)


# ==================================================
# TASK ACTIONS
# ==================================================

def toggle_done(task):

    if task["status"] == "Completed":
        task["status"] = "Pending"
    else:
        task["status"] = "Completed"

    save_tasks()
    refresh()


def next_status(task):

    index = STATUSES.index(task["status"])

    task["status"] = STATUSES[(index + 1) % len(STATUSES)]

    save_tasks()
    refresh()


def delete_task(task):

    if messagebox.askyesno(
        "Delete task",
        "Delete '" + task["title"] + "'?"
    ):
        tasks.remove(task)
        save_tasks()
        refresh()


# ==================================================
# ADD / EDIT TASK WINDOW
# ==================================================

def task_window(task=None):

    win = tk.Toplevel(root)
    win.title("Edit Task" if task else "Add Task")
    win.configure(bg=CARD)
    win.resizable(False, False)
    win.transient(root)
    win.grab_set()

    data = task or {
        "title": "",
        "description": "",
        "priority": "Medium",
        "status": "Pending",
        "due": days_from_today(1),
        "image": ""
    }

    values = {
        key: tk.StringVar(value=data.get(key, ""))
        for key in ("title", "description", "priority", "status", "due")
    }

    def add_label(text):

        tk.Label(
            win,
            text=text,
            font=("Arial", 10),
            bg=CARD,
            fg=LIGHT_TEXT
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 0)
        )

    def add_entry(key, label):

        add_label(label)

        tk.Entry(
            win,
            textvariable=values[key],
            font=("Arial", 11),
            width=45,
            bg=FIELD,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat"
        ).pack(
            fill="x",
            padx=20,
            ipady=5
        )

    def add_menu(key, label, options):

        add_label(label)

        menu = tk.OptionMenu(win, values[key], *options)

        menu.config(
            bg=FIELD,
            fg=TEXT,
            activebackground=FIELD,
            activeforeground=GOLD,
            relief="flat",
            highlightthickness=0
        )

        menu.pack(
            fill="x",
            padx=20
        )

    add_entry("title", "Title")
    add_entry("description", "Description")
    add_menu("priority", "Priority", PRIORITIES)
    add_menu("status", "Status", STATUSES)
    add_entry("due", "Due date (example: 25 Apr 2026)")

    # ---------- image ----------

    chosen = {"path": None, "remove": False}

    add_label("Image (optional)")

    image_row = tk.Frame(win, bg=CARD)

    image_row.pack(
        fill="x",
        padx=20
    )

    image_name = tk.Label(
        image_row,
        text=data.get("image") or "No image",
        font=("Arial", 9),
        bg=CARD,
        fg=TEXT
    )

    def choose_image():

        path = filedialog.askopenfilename(
            parent=win,
            title="Choose an image",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.gif *.bmp *.webp")]
        )

        if path:
            chosen["path"] = path
            chosen["remove"] = False
            image_name.config(text=Path(path).name)

    def remove_image():

        chosen["path"] = None
        chosen["remove"] = True
        image_name.config(text="No image")

    tk.Button(
        image_row,
        text="Choose image…",
        bg=FIELD,
        fg=GOLD,
        relief="flat",
        padx=8,
        command=choose_image
    ).pack(side="left")

    tk.Button(
        image_row,
        text="Remove",
        bg=FIELD,
        fg=RED,
        relief="flat",
        padx=8,
        command=remove_image
    ).pack(side="left", padx=6)

    image_name.pack(side="left", padx=6)

    # ---------- save ----------

    def save():

        if not values["title"].get().strip():
            messagebox.showerror("Task", "Title is required.", parent=win)
            return

        try:
            datetime.strptime(values["due"].get().strip(), DATE_FORMAT)

        except ValueError:
            messagebox.showerror(
                "Task",
                "Date must look like 25 Apr 2026.",
                parent=win
            )
            return

        new = {key: var.get().strip() for key, var in values.items()}

        if chosen["path"]:

            # copy the picture into the same folder as this file
            source = Path(chosen["path"])
            target = IMAGE_DIR / source.name

            try:
                if source.resolve() != target.resolve():

                    if target.exists():
                        target = IMAGE_DIR / (str(int(time.time())) + "_" + source.name)

                    shutil.copy2(source, target)

                new["image"] = target.name

            except OSError as error:
                messagebox.showerror("Image", str(error), parent=win)
                return

        elif chosen["remove"]:
            new["image"] = ""

        if task:
            task.update(new)
        else:
            new.setdefault("image", "")
            tasks.append(new)

        save_tasks()
        win.destroy()
        refresh()

    tk.Button(
        win,
        text="Save",
        font=("Arial", 11, "bold"),
        bg=GOLD,
        fg=BG,
        relief="flat",
        pady=6,
        command=save
    ).pack(
        fill="x",
        padx=20,
        pady=16
    )


tk.Button(
    search_frame,
    text="＋ Add Task",
    font=("Arial", 10, "bold"),
    bg=GOLD,
    fg=BG,
    relief="flat",
    padx=15,
    pady=6,
    command=task_window
).pack(
    side="right"
)


# ==================================================
# REFRESH PAGE
# ==================================================

def make_badge(parent, text, colors, command=None):

    badge = tk.Label(
        parent,
        text=text,
        font=("Arial", 8),
        bg=colors[0],
        fg=colors[1],
        padx=10,
        pady=3
    )

    if command:
        badge.config(cursor="hand2")
        badge.bind("<Button-1>", lambda event: command())

    return badge


def refresh():

    # ---------- filter buttons ----------

    for widget in filter_frame.winfo_children():
        widget.destroy()

    for name in ["All Tasks", "Pending", "In Progress", "Completed"]:

        tk.Button(
            filter_frame,
            text=name,
            font=("Arial", 9),
            bg=GOLD if name == current_filter else BG,
            fg=BG if name == current_filter else TEXT,
            activebackground=GOLD,
            activeforeground=BG,
            relief="solid",
            bd=1,
            command=lambda n=name: set_filter(n)
        ).pack(
            side="left",
            padx=3,
            ipadx=8,
            ipady=2
        )

    # ---------- task cards ----------

    for widget in task_area.winfo_children():
        widget.destroy()

    search = search_var.get().strip().lower()

    shown = [
        task for task in tasks
        if (current_filter == "All Tasks" or task["status"] == current_filter)
        and (search in task["title"].lower()
             or search in task["description"].lower())
    ]

    if not shown:

        tk.Label(
            task_area,
            text="No tasks found.",
            font=("Arial", 11),
            bg=BG,
            fg=LIGHT_TEXT
        ).pack(
            pady=30
        )

    for task in shown:

        card = tk.Frame(
            task_area,
            bg=CARD
        )

        card.pack(
            fill="x",
            pady=5
        )

        card.grid_columnconfigure(2, weight=1)

        # checkbox

        var = tk.IntVar(
            value=1 if task["status"] == "Completed" else 0
        )

        tk.Checkbutton(
            card,
            variable=var,
            bg=CARD,
            activebackground=CARD,
            selectcolor=FIELD,
            highlightthickness=0,
            command=lambda t=task: toggle_done(t)
        ).grid(
            row=0,
            column=0,
            padx=(12, 4)
        )

        # image

        create_image(
            card,
            task.get("image", ""),
            (90, 70)
        ).grid(
            row=0,
            column=1,
            padx=8,
            pady=10
        )

        # title + description

        text_frame = tk.Frame(card, bg=CARD)

        text_frame.grid(
            row=0,
            column=2,
            sticky="w",
            padx=8
        )

        tk.Label(
            text_frame,
            text=task["title"],
            font=("Georgia", 11, "bold"),
            bg=CARD,
            fg=LIGHT_TEXT if task["status"] == "Completed" else TEXT
        ).pack(
            anchor="w"
        )

        tk.Label(
            text_frame,
            text=task["description"],
            font=("Arial", 8),
            bg=CARD,
            fg=LIGHT_TEXT,
            wraplength=380,
            justify="left"
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        # priority, status, date

        make_badge(
            card,
            task["priority"],
            PRIORITY_COLORS[task["priority"]]
        ).grid(
            row=0,
            column=3,
            padx=8
        )

        make_badge(
            card,
            task["status"],
            STATUS_COLORS[task["status"]],
            command=lambda t=task: next_status(t)
        ).grid(
            row=0,
            column=4,
            padx=8
        )

        tk.Label(
            card,
            text=task["due"] + ("  ⚠" if is_overdue(task) else ""),
            font=("Arial", 9),
            bg=CARD,
            fg=RED if is_overdue(task) else TEXT,
            width=14
        ).grid(
            row=0,
            column=5,
            padx=4
        )

        # edit + delete

        buttons = tk.Frame(card, bg=CARD)

        buttons.grid(
            row=0,
            column=6,
            padx=(4, 12)
        )

        tk.Button(
            buttons,
            text="✎",
            font=("Arial", 10),
            bg=FIELD,
            fg=GOLD,
            relief="flat",
            command=lambda t=task: task_window(t)
        ).pack(
            side="left",
            padx=2
        )

        tk.Button(
            buttons,
            text="🗑",
            font=("Arial", 10),
            bg=CARD,
            fg=RED,
            relief="flat",
            command=lambda t=task: delete_task(t)
        ).pack(
            side="left",
            padx=2
        )

    # ---------- numbers ----------

    done = sum(1 for task in tasks if task["status"] == "Completed")

    stat_labels["Total Tasks"].config(text=str(len(tasks)))
    stat_labels["Completed"].config(text=str(done))
    stat_labels["In Progress"].config(
        text=str(sum(1 for task in tasks if task["status"] == "In Progress"))
    )
    stat_labels["Pending"].config(
        text=str(sum(1 for task in tasks if task["status"] == "Pending"))
    )
    stat_labels["Overdue"].config(
        text=str(sum(1 for task in tasks if is_overdue(task)))
    )

    progress_text.config(
        text="Your Progress   " + str(done) + " / " + str(len(tasks)) + " completed"
    )

    draw_progress()


# ==================================================
# FOOTER MESSAGE
# ==================================================

footer = tk.Frame(
    content,
    bg=CARD
)

footer.pack(
    fill="x",
    padx=35,
    pady=20
)

tk.Label(
    footer,
    text="💡",
    font=("Arial", 22),
    bg=CARD,
    fg=GOLD
).pack(
    side="left",
    padx=15,
    pady=10
)

tk.Label(
    footer,
    text="Keep going!\nYou're doing great. Every task brings you closer to the legends.",
    font=("Arial", 9),
    bg=CARD,
    fg=TEXT,
    justify="left"
).pack(
    side="left"
)


# ==================================================
# RUN
# ==================================================

refresh()

root.mainloop()'''
import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path
from datetime import datetime, timedelta
from PIL import Image, ImageTk, ImageOps


# ==================================================
# MAIN WINDOW
# ==================================================

root = tk.Tk()
root.title("MythLab - My Tasks")
root.geometry("1280x900")
root.minsize(1000, 700)
root.configure(bg="#061b2b")


# ==================================================
# COLOURS
# ==================================================

BG = "#061b2b"
SIDEBAR = "#071522"
CARD = "#092333"
FIELD = "#102b3d"
GOLD = "#d6a84f"
TEXT = "#f5ead0"
LIGHT_TEXT = "#c7c1b3"
RED = "#ff7b7b"
GREEN = "#6fcf97"
BLUE = "#8fb4f5"
AMBER = "#e6b84f"


PRIORITIES = ["High", "Medium", "Low"]
STATUSES = ["Pending", "In Progress", "Completed"]


PRIORITY_COLORS = {
    "High": ("#4a1a24", RED),
    "Medium": ("#3d3016", AMBER),
    "Low": ("#173d2a", GREEN)
}


STATUS_COLORS = {
    "Pending": ("#17325a", BLUE),
    "In Progress": ("#3d3016", AMBER),
    "Completed": ("#173d2a", GREEN)
}


# ==================================================
# IMAGE LOCATION
# ==================================================

IMAGE_DIR = Path(__file__).parent


def load_image(filename, size):

    try:
        path = IMAGE_DIR / filename

        image = Image.open(path).convert("RGB")

        image = ImageOps.fit(
            image,
            size,
            method=Image.Resampling.LANCZOS
        )

        return ImageTk.PhotoImage(image)

    except:
        return None


# ==================================================
# TASK DATA
# ==================================================

def days_from_today(days):
    return (
        datetime.now() + timedelta(days=days)
    ).strftime("%d %b %Y")


tasks = [

    {
        "title": "Read about the Thunder Dragon",
        "description": "Learn about the Thunder Dragon and its role in Bhutanese mythology.",
        "priority": "High",
        "status": "Pending",
        "due": days_from_today(3),
        "image": "thumb1.png"
    },

    {
        "title": "Explore Bhutanese mythical creatures",
        "description": "Learn about Druk, Yeti, Migoi and other beings.",
        "priority": "Medium",
        "status": "Completed",
        "due": days_from_today(2),
        "image": "thumb2.png"
    },

    {
        "title": "Read the story of The Great Yeti",
        "description": "Discover the legend of the Yeti in the Himalayas.",
        "priority": "High",
        "status": "Pending",
        "due": days_from_today(5),
        "image": "thumb3.png"
    },

    {
        "title": "Watch a short video: The Firebird",
        "description": "Learn about the symbol of rebirth and hope.",
        "priority": "Low",
        "status": "Pending",
        "due": days_from_today(6),
        "image": "thumb4.png"
    },

    {
        "title": "Explore Punakha Dzong",
        "description": "Learn about the history and significance of Punakha Dzong.",
        "priority": "Medium",
        "status": "Completed",
        "due": days_from_today(0),
        "image": "thumb5.png"
    },

    {
        "title": "Take the Mythology Quiz",
        "description": "Test what you've learned so far.",
        "priority": "High",
        "status": "Pending",
        "due": days_from_today(8),
        "image": "thumb6.png"
    }
]


current_filter = "All Tasks"


# ==================================================
# SIDEBAR
# ==================================================

sidebar = tk.Frame(
    root,
    bg=SIDEBAR,
    width=215
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


# Logo

tk.Label(
    sidebar,
    text="🐉",
    font=("Arial", 32),
    bg=SIDEBAR,
    fg=GOLD
).pack(pady=(18, 0))


tk.Label(
    sidebar,
    text="MythLab",
    font=("Georgia", 22, "bold"),
    bg=SIDEBAR,
    fg=GOLD
).pack()


tk.Label(
    sidebar,
    text="Explore. Learn. Believe.",
    font=("Arial", 9),
    bg=SIDEBAR,
    fg=LIGHT_TEXT
).pack(pady=(0, 28))


# ==================================================
# SIDEBAR MENU
# ==================================================

menu_items = [
    "⌂  Home",
    "📖  Myths",
    "🐉  Creatures",
    "🌐  Regions",
    "✓  My Tasks",
    "?  Quiz",
    "♡  Favourites",
    "ⓘ  About"
]


for item in menu_items:

    active = item == "✓  My Tasks"

    tk.Button(
        sidebar,
        text=item,
        font=("Arial", 11),
        bg="#2a2518" if active else SIDEBAR,
        fg=GOLD if active else TEXT,
        activebackground="#263b47",
        activeforeground=GOLD,
        relief="flat",
        anchor="w",
        padx=20,
        pady=10
    ).pack(
        fill="x",
        padx=10,
        pady=2
    )


# ==================================================
# SIDEBAR IMAGE + QUOTE
# ==================================================

mountain_img = load_image(
    "mountains.png",
    (200, 130)
)


if mountain_img:

    mountain_label = tk.Label(
        sidebar,
        image=mountain_img,
        bg=SIDEBAR
    )

    mountain_label.pack(
        side="bottom",
        pady=5
    )

    mountain_label.image = mountain_img


tk.Label(
    sidebar,
    text='“Every myth is a door\nto a deeper wisdom.”\n\n— Bhutanese Wisdom',
    font=("Georgia", 9, "italic"),
    bg=SIDEBAR,
    fg=GOLD,
    justify="center"
).pack(
    side="bottom",
    pady=8
)


# ==================================================
# MAIN AREA
# ==================================================

main_area = tk.Frame(
    root,
    bg=BG
)

main_area.pack(
    side="right",
    fill="both",
    expand=True
)


# ==================================================
# SCROLL
# ==================================================

canvas = tk.Canvas(
    main_area,
    bg=BG,
    highlightthickness=0
)

scrollbar = tk.Scrollbar(
    main_area,
    orient="vertical",
    command=canvas.yview
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

scrollbar.pack(
    side="right",
    fill="y"
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)


content = tk.Frame(
    canvas,
    bg=BG
)

content_window = canvas.create_window(
    (0, 0),
    window=content,
    anchor="nw"
)


def update_scroll(event=None):

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )


def resize_content(event):

    canvas.itemconfig(
        content_window,
        width=event.width
    )


content.bind(
    "<Configure>",
    update_scroll
)

canvas.bind(
    "<Configure>",
    resize_content
)


def scroll_canvas(event):

    canvas.yview_scroll(
        int(-event.delta / 120),
        "units"
    )


canvas.bind_all(
    "<MouseWheel>",
    scroll_canvas
)


# ==================================================
# HERO
# ==================================================

hero = tk.Frame(
    content,
    bg="#183b50",
    height=200
)

hero.pack(
    fill="x",
    padx=30,
    pady=(0, 15)
)

hero.pack_propagate(False)


hero_img = load_image(
    "welcome.png",
    (1050, 200)
)


if hero_img:

    hero_image = tk.Label(
        hero,
        image=hero_img,
        bg="#183b50"
    )

    hero_image.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )

    hero_image.image = hero_img


# Hero text

hero_text = tk.Frame(
    hero,
    bg="#061b2b"
)

hero_text.place(
    x=25,
    y=25
)


tk.Label(
    hero_text,
    text="Tasks",
    font=("Arial", 10),
    bg="#061b2b",
    fg=GOLD
).pack(anchor="w")


tk.Label(
    hero_text,
    text="✥  My Tasks",
    font=("Georgia", 25, "bold"),
    bg="#061b2b",
    fg=TEXT
).pack(
    anchor="w",
    pady=5
)


tk.Label(
    hero_text,
    text="Complete your learning tasks, track your progress and\n"
         "build your knowledge about myths, legends and creatures.",
    font=("Arial", 10),
    bg="#061b2b",
    fg=LIGHT_TEXT,
    justify="center"
).pack(
    anchor="center",
    pady=(10, 0)
)



# ==================================================
# STATISTICS
# ==================================================

stats_frame = tk.Frame(
    content,
    bg=BG
)

stats_frame.pack(
    fill="x",
    padx=30,
    pady=(0, 12)
)


stat_labels = {}


stat_info = [
    ("Total Tasks", GOLD),
    ("Completed", GREEN),
    ("In Progress", AMBER),
    ("Pending", BLUE),
    ("Overdue", RED)
]


for column, (name, color) in enumerate(stat_info):

    stats_frame.grid_columnconfigure(
        column,
        weight=1
    )

    box = tk.Frame(
        stats_frame,
        bg=CARD
    )

    box.grid(
        row=0,
        column=column,
        sticky="ew",
        padx=5
    )

    number = tk.Label(
        box,
        text="0",
        font=("Georgia", 22, "bold"),
        bg=CARD,
        fg=color
    )

    number.pack(
        pady=(10, 0)
    )

    tk.Label(
        box,
        text=name,
        font=("Arial", 9),
        bg=CARD,
        fg=LIGHT_TEXT
    ).pack(
        pady=(0, 10)
    )

    stat_labels[name] = number


# ==================================================
# PROGRESS
# ==================================================

progress_frame = tk.Frame(
    content,
    bg=CARD
)

progress_frame.pack(
    fill="x",
    padx=35,
    pady=(0, 15)
)


progress_text = tk.Label(
    progress_frame,
    text="Your Progress",
    font=("Georgia", 11, "bold"),
    bg=CARD,
    fg=TEXT
)

progress_text.pack(
    anchor="w",
    padx=15,
    pady=(10, 4)
)


progress_bar = tk.Canvas(
    progress_frame,
    height=12,
    bg=CARD,
    highlightthickness=0
)

progress_bar.pack(
    fill="x",
    padx=15,
    pady=(0, 12)
)


def draw_progress():

    progress_bar.delete("all")

    width = progress_bar.winfo_width()

    completed = sum(
        task["status"] == "Completed"
        for task in tasks
    )

    total = len(tasks)

    progress_bar.create_rectangle(
        0, 0,
        width, 12,
        fill="#183b50",
        outline=""
    )

    if total > 0:

        progress_bar.create_rectangle(
            0, 0,
            width * completed / total,
            12,
            fill=GOLD,
            outline=""
        )


progress_bar.bind(
    "<Configure>",
    lambda event: draw_progress()
)


# ==================================================
# SEARCH
# ==================================================

search_frame = tk.Frame(
    content,
    bg=BG
)

search_frame.pack(
    fill="x",
    padx=30,
    pady=(0, 12)
)


search_var = tk.StringVar()


search_entry = tk.Entry(
    search_frame,
    textvariable=search_var,
    font=("Arial", 11),
    bg=FIELD,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat"
)

search_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=10,
    padx=(0, 10)
)


# ==================================================
# FILTER
# ==================================================

filter_frame = tk.Frame(
    content,
    bg=BG
)

filter_frame.pack(
    fill="x",
    padx=30,
    pady=(0, 12)
)


def set_filter(name):

    global current_filter

    current_filter = name

    refresh()


# ==================================================
# TASK AREA
# ==================================================

task_area = tk.Frame(
    content,
    bg=BG
)

task_area.pack(
    fill="x",
    padx=30
)


# ==================================================
# TASK FUNCTIONS
# ==================================================

def toggle_done(task):

    if task["status"] == "Completed":
        task["status"] = "Pending"
    else:
        task["status"] = "Completed"

    refresh()


def next_status(task):

    index = STATUSES.index(
        task["status"]
    )

    task["status"] = STATUSES[
        (index + 1) % len(STATUSES)
    ]

    refresh()


def delete_task(task):

    answer = messagebox.askyesno(
        "Delete Task",
        "Delete '" + task["title"] + "'?"
    )

    if answer:

        tasks.remove(task)

        refresh()


def is_overdue(task):

    try:

        date = datetime.strptime(
            task["due"],
            "%d %b %Y"
        )

        return (
            task["status"] != "Completed"
            and date.date() < datetime.now().date()
        )

    except:

        return False


# ==================================================
# ADD / EDIT TASK
# ==================================================

def task_window(task=None):

    win = tk.Toplevel(root)

    win.title(
        "Edit Task" if task else "Add Task"
    )

    win.configure(bg=CARD)

    win.resizable(False, False)


    data = task or {
        "title": "",
        "description": "",
        "priority": "Medium",
        "status": "Pending",
        "due": days_from_today(1),
        "image": ""
    }


    title = tk.StringVar(
        value=data["title"]
    )

    description = tk.StringVar(
        value=data["description"]
    )

    priority = tk.StringVar(
        value=data["priority"]
    )

    status = tk.StringVar(
        value=data["status"]
    )

    due = tk.StringVar(
        value=data["due"]
    )

    image = tk.StringVar(
        value=data.get("image", "")
    )


    def label(text):

        tk.Label(
            win,
            text=text,
            bg=CARD,
            fg=LIGHT_TEXT,
            font=("Arial", 10)
        ).pack(
            anchor="w",
            padx=20,
            pady=(10, 2)
        )


    def entry(variable):

        tk.Entry(
            win,
            textvariable=variable,
            font=("Arial", 11),
            bg=FIELD,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat"
        ).pack(
            fill="x",
            padx=20,
            ipady=5
        )


    label("Title")
    entry(title)

    label("Description")
    entry(description)

    label("Priority")

    tk.OptionMenu(
        win,
        priority,
        *PRIORITIES
    ).pack(
        fill="x",
        padx=20
    )


    label("Status")

    tk.OptionMenu(
        win,
        status,
        *STATUSES
    ).pack(
        fill="x",
        padx=20
    )


    label("Due date")
    entry(due)


    label("Image")


    image_name = tk.Label(
        win,
        text=image.get() or "No image",
        bg=CARD,
        fg=TEXT
    )

    image_name.pack(
        pady=5
    )


    def choose_image():

        path = filedialog.askopenfilename(
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.gif")
            ]
        )

        if path:

            image.set(
                Path(path).name
            )

            image_name.config(
                text=Path(path).name
            )


    tk.Button(
        win,
        text="Choose Image",
        bg=FIELD,
        fg=GOLD,
        relief="flat",
        command=choose_image
    ).pack(
        pady=5
    )


    def save():

        if not title.get().strip():

            messagebox.showerror(
                "Error",
                "Please enter a title."
            )

            return


        try:

            datetime.strptime(
                due.get(),
                "%d %b %Y"
            )

        except:

            messagebox.showerror(
                "Error",
                "Use date format: 25 Apr 2026"
            )

            return


        new_task = {
            "title": title.get(),
            "description": description.get(),
            "priority": priority.get(),
            "status": status.get(),
            "due": due.get(),
            "image": image.get()
        }


        if task:

            task.update(new_task)

        else:

            tasks.append(new_task)


        win.destroy()

        refresh()


    tk.Button(
        win,
        text="Save",
        font=("Arial", 11, "bold"),
        bg=GOLD,
        fg=BG,
        relief="flat",
        command=save
    ).pack(
        fill="x",
        padx=20,
        pady=20
    )


# Add button

tk.Button(
    search_frame,
    text="＋ Add Task",
    font=("Arial", 10, "bold"),
    bg=GOLD,
    fg=BG,
    relief="flat",
    padx=15,
    pady=6,
    command=task_window
).pack(
    side="right"
)


# ==================================================
# REFRESH
# ==================================================

def refresh():

    # Filter buttons

    for widget in filter_frame.winfo_children():
        widget.destroy()


    for name in [
        "All Tasks",
        "Pending",
        "In Progress",
        "Completed"
    ]:

        tk.Button(
            filter_frame,
            text=name,
            font=("Arial", 9),
            bg=GOLD if name == current_filter else BG,
            fg=BG if name == current_filter else TEXT,
            relief="solid",
            bd=1,
            command=lambda n=name: set_filter(n)
        ).pack(
            side="left",
            padx=3,
            ipadx=8
        )


    # Search text

    search = search_var.get().lower()


    # Remove old cards

    for widget in task_area.winfo_children():
        widget.destroy()


    # Find tasks

    shown = []

    for task in tasks:

        if (
            current_filter != "All Tasks"
            and task["status"] != current_filter
        ):
            continue

        if (
            search not in task["title"].lower()
            and search not in task["description"].lower()
        ):
            continue

        shown.append(task)


    # Show message

    if not shown:

        tk.Label(
            task_area,
            text="No tasks found.",
            font=("Arial", 11),
            bg=BG,
            fg=LIGHT_TEXT
        ).pack(
            pady=30
        )


    # Create cards

    for task in shown:

        card = tk.Frame(
            task_area,
            bg=CARD
        )

        card.pack(
            fill="x",
            pady=5
        )


        # Checkbox

        checked = tk.IntVar(
            value=1 if task["status"] == "Completed" else 0
        )


        tk.Checkbutton(
            card,
            variable=checked,
            bg=CARD,
            activebackground=CARD,
            selectcolor=FIELD,
            command=lambda t=task: toggle_done(t)
        ).grid(
            row=0,
            column=0,
            padx=10
        )


        # Image

        photo = load_image(
            task.get("image", ""),
            (90, 70)
        ) if task.get("image") else None


        if photo:

            image_label = tk.Label(
                card,
                image=photo,
                bg=CARD
            )

            image_label.image = photo

        else:

            image_label = tk.Label(
                card,
                text="NO\nIMAGE",
                bg="#183b50",
                fg=LIGHT_TEXT,
                width=10,
                height=4
            )


        image_label.grid(
            row=0,
            column=1,
            padx=8,
            pady=10
        )


        # Text

        text_frame = tk.Frame(
            card,
            bg=CARD
        )

        text_frame.grid(
            row=0,
            column=2,
            sticky="w",
            padx=8
        )


        tk.Label(
            text_frame,
            text=task["title"],
            font=("Georgia", 11, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(
            anchor="w"
        )


        tk.Label(
            text_frame,
            text=task["description"],
            font=("Arial", 8),
            bg=CARD,
            fg=LIGHT_TEXT,
            wraplength=380,
            justify="left"
        ).pack(
            anchor="w"
        )


        # Priority

        tk.Label(
            card,
            text=task["priority"],
            bg=PRIORITY_COLORS[task["priority"]][0],
            fg=PRIORITY_COLORS[task["priority"]][1],
            padx=8,
            pady=3
        ).grid(
            row=0,
            column=3,
            padx=5
        )


        # Status

        tk.Button(
            card,
            text=task["status"],
            bg=STATUS_COLORS[task["status"]][0],
            fg=STATUS_COLORS[task["status"]][1],
            relief="flat",
            command=lambda t=task: next_status(t)
        ).grid(
            row=0,
            column=4,
            padx=5
        )


        # Date

        tk.Label(
            card,
            text=task["due"],
            bg=CARD,
            fg=RED if is_overdue(task) else TEXT
        ).grid(
            row=0,
            column=5,
            padx=5
        )


        # Edit

        tk.Button(
            card,
            text="✎",
            bg=FIELD,
            fg=GOLD,
            relief="flat",
            command=lambda t=task: task_window(t)
        ).grid(
            row=0,
            column=6,
            padx=3
        )


        # Delete

        tk.Button(
            card,
            text="🗑",
            bg=CARD,
            fg=RED,
            relief="flat",
            command=lambda t=task: delete_task(t)
        ).grid(
            row=0,
            column=7,
            padx=3
        )


    # ==================================================
    # UPDATE STATISTICS
    # ==================================================

    completed = sum(
        task["status"] == "Completed"
        for task in tasks
    )

    in_progress = sum(
        task["status"] == "In Progress"
        for task in tasks
    )

    pending = sum(
        task["status"] == "Pending"
        for task in tasks
    )

    overdue = sum(
        is_overdue(task)
        for task in tasks
    )


    stat_labels["Total Tasks"].config(
        text=len(tasks)
    )

    stat_labels["Completed"].config(
        text=completed
    )

    stat_labels["In Progress"].config(
        text=in_progress
    )

    stat_labels["Pending"].config(
        text=pending
    )

    stat_labels["Overdue"].config(
        text=overdue
    )


    progress_text.config(
        text=f"Your Progress   {completed} / {len(tasks)} completed"
    )


    draw_progress()


# ==================================================
# FOOTER
# ==================================================

footer = tk.Frame(
    content,
    bg=CARD
)

footer.pack(
    fill="x",
    padx=35,
    pady=20
)


tk.Label(
    footer,
    text="💡",
    font=("Arial", 22),
    bg=CARD,
    fg=GOLD
).pack(
    side="left",
    padx=15,
    pady=10
)


tk.Label(
    footer,
    text="Keep going!\nYou're doing great. Every task brings you closer to the legends.",
    font=("Arial", 9),
    bg=CARD,
    fg=TEXT,
    justify="left"
).pack(
    side="left"
)


# ==================================================
# START
# ==================================================

refresh()

root.mainloop()