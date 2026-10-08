import tkinter as tk
from tkinter import messagebox, simpledialog
from pathlib import Path
import sqlite3
import sys

from PIL import Image, ImageTk, ImageOps

from quiz import show_quiz
from myths import show_myths
from creatures import show_creatures
from exploreBhutan import show_regions
from task import show_tasks
from mythlab_favorites import MythLabFavourites
from about import show_about


# ============================================================
# MYTHLAB MAIN APPLICATION
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent
ASSETS_DIR = PROJECT_DIR / "assets"
DB_FILE = PROJECT_DIR / "mythlab.db"

BG = "#071b2b"
SIDEBAR = "#061522"
CARD = "#102b3d"
GOLD = "#d6a84f"
TEXT = "#f5ead0"
LIGHT_TEXT = "#c7c1b3"

image_refs = []
current_username = sys.argv[1].strip() if len(sys.argv) > 1 else None


# ============================================================
# DATABASE / USER
# ============================================================

def get_connection():
    return sqlite3.connect(DB_FILE)


def username_exists(username):
    if not username:
        return False

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM users WHERE LOWER(username) = LOWER(?)",
            (username.strip(),)
        )
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as error:
        print("User check error:", error)
        return False


def find_single_user():
    """If there is only one account, use it automatically."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username FROM users ORDER BY id LIMIT 2"
        )
        rows = cursor.fetchall()
        conn.close()

        if len(rows) == 1:
            return rows[0][0]

    except Exception as error:
        print("Could not read users:", error)

    return None


def ensure_logged_in_user():
    """
    My Tasks and Favourites need a real username because both
    features store data using the users table.
    """
    global current_username

    if current_username and username_exists(current_username):
        return True

    # If there is only one user, do not ask the user anything.
    single_user = find_single_user()

    if single_user:
        current_username = single_user
        return True

    # If there are multiple users, ask which account is being used.
    while True:
        username = simpledialog.askstring(
            "MythLab Login",
            "Enter your MythLab username:",
            parent=root
        )

        if username is None:
            return False

        username = username.strip()

        if not username:
            messagebox.showwarning(
                "Username",
                "Please enter your username.",
                parent=root
            )
            continue

        if username_exists(username):
            current_username = username
            return True

        messagebox.showerror(
            "Login",
            "Username not found.\nPlease enter a valid MythLab username.",
            parent=root
        )


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()
root.title("MythLab - Mythology Library")
root.geometry("1200x900")
root.minsize(900, 650)
root.configure(bg=BG)


# ============================================================
# IMAGE FUNCTIONS
# ============================================================

def find_image(filename):
    """Find an image in assets/ or in the project folder."""
    possible = [
        ASSETS_DIR / filename,
        PROJECT_DIR / filename
    ]

    for path in possible:
        if path.is_file():
            return path

    requested_stem = Path(filename).stem.lower()
    requested_ext = Path(filename).suffix.lower()

    for folder in (ASSETS_DIR, PROJECT_DIR):
        if not folder.is_dir():
            continue

        for item in folder.iterdir():
            if not item.is_file():
                continue

            if item.suffix.lower() != requested_ext:
                continue

            stem = item.stem.lower()

            if (
                stem.startswith(requested_stem)
                or requested_stem.startswith(stem)
            ):
                return item

    return None


def load_image(filename, size):
    path = find_image(filename)

    if path is None:
        return None

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
        print("Could not load image:", filename, error)
        return None


def image_label(parent, filename, size, bg=CARD):
    photo = load_image(filename, size)

    if photo:
        label = tk.Label(
            parent,
            image=photo,
            bg=bg,
            bd=0
        )
    else:
        label = tk.Label(
            parent,
            text="IMAGE NOT FOUND",
            font=("Arial", 8),
            bg=bg,
            fg=LIGHT_TEXT
        )

    label.pack(
        fill="x",
        padx=5,
        pady=5
    )

    return label


# ============================================================
# PAGE FRAMES
# ============================================================

sidebar = tk.Frame(
    root,
    bg=SIDEBAR,
    width=210
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


main_area = tk.Frame(
    root,
    bg=BG
)

main_area.pack(
    side="right",
    fill="both",
    expand=True
)


# ============================================================
# HOME SCROLL AREA
# ============================================================

home_canvas = tk.Canvas(
    main_area,
    bg=BG,
    highlightthickness=0
)

home_scrollbar = tk.Scrollbar(
    main_area,
    orient="vertical",
    command=home_canvas.yview
)

home_canvas.configure(
    yscrollcommand=home_scrollbar.set
)

home_content = tk.Frame(
    home_canvas,
    bg=BG
)

home_window = home_canvas.create_window(
    (0, 0),
    window=home_content,
    anchor="nw"
)


def update_home_scroll(event=None):
    home_canvas.configure(
        scrollregion=home_canvas.bbox("all")
    )


def resize_home(event):
    home_canvas.itemconfig(
        home_window,
        width=event.width
    )


home_content.bind(
    "<Configure>",
    update_home_scroll
)

home_canvas.bind(
    "<Configure>",
    resize_home
)


def home_mousewheel(event):
    home_canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


# ============================================================
# OTHER PAGE FRAMES
# ============================================================

myths_page = tk.Frame(main_area, bg=BG)
creatures_page = tk.Frame(main_area, bg=BG)
regions_page = tk.Frame(main_area, bg=BG)
tasks_page = tk.Frame(main_area, bg=BG)
favourites_page = tk.Frame(main_area, bg=BG)
about_page = tk.Frame(main_area, bg=BG)

# Quiz gets its OWN canvas.
# This is the important fix: quiz is no longer placed inside
# the hidden Home canvas.
quiz_canvas = tk.Canvas(
    main_area,
    bg=BG,
    highlightthickness=0
)

quiz_scrollbar = tk.Scrollbar(
    main_area,
    orient="vertical",
    command=quiz_canvas.yview
)

quiz_canvas.configure(
    yscrollcommand=quiz_scrollbar.set
)

quiz_content = tk.Frame(
    quiz_canvas,
    bg=BG
)

quiz_window = quiz_canvas.create_window(
    (0, 0),
    window=quiz_content,
    anchor="nw"
)


def update_quiz_scroll(event=None):
    quiz_canvas.configure(
        scrollregion=quiz_canvas.bbox("all")
    )


def resize_quiz(event):
    quiz_canvas.itemconfig(
        quiz_window,
        width=event.width
    )


quiz_content.bind(
    "<Configure>",
    update_quiz_scroll
)

quiz_canvas.bind(
    "<Configure>",
    resize_quiz
)


def quiz_mousewheel(event):
    quiz_canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


# ============================================================
# PAGE SWITCHING
# ============================================================

def hide_all_pages():
    home_canvas.pack_forget()
    home_scrollbar.pack_forget()

    quiz_canvas.pack_forget()
    quiz_scrollbar.pack_forget()

    myths_page.pack_forget()
    creatures_page.pack_forget()
    regions_page.pack_forget()
    tasks_page.pack_forget()
    favourites_page.pack_forget()
    about_page.pack_forget()


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def open_mythlab_page(page):
    open_page(page)


def open_page(page):
    global current_username

    # Remove old mouse-wheel bindings.
    root.unbind_all("<MouseWheel>")
    root.unbind_all("<Button-4>")
    root.unbind_all("<Button-5>")

    hide_all_pages()

    # --------------------------------------------------------
    # HOME
    # --------------------------------------------------------

    if page == "Home":

        home_scrollbar.pack(
            side="right",
            fill="y"
        )

        home_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        home_canvas.yview_moveto(0)

        root.bind_all(
            "<MouseWheel>",
            home_mousewheel
        )

    # --------------------------------------------------------
    # MYTHS
    # --------------------------------------------------------

    elif page == "Myths":

        clear_frame(myths_page)

        myths_page.pack(
            fill="both",
            expand=True
        )

        show_myths(myths_page)

    # --------------------------------------------------------
    # CREATURES
    # --------------------------------------------------------

    elif page == "Creatures":

        clear_frame(creatures_page)

        creatures_page.pack(
            fill="both",
            expand=True
        )

        show_creatures(creatures_page)

    # --------------------------------------------------------
    # REGIONS
    # --------------------------------------------------------

    elif page == "Regions":

        clear_frame(regions_page)

        regions_page.pack(
            fill="both",
            expand=True
        )

        show_regions(regions_page)

    # --------------------------------------------------------
    # MY TASKS
    # --------------------------------------------------------

    elif page == "My Tasks":

        if not ensure_logged_in_user():
            return

        clear_frame(tasks_page)

        tasks_page.pack(
            fill="both",
            expand=True
        )

        show_tasks(
            tasks_page,
            current_username
        )

    # --------------------------------------------------------
    # QUIZ
    # --------------------------------------------------------

    elif page == "Quiz":

        clear_frame(quiz_content)

        quiz_scrollbar.pack(
            side="right",
            fill="y"
        )

        quiz_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        show_quiz(quiz_content)

        quiz_content.update_idletasks()

        quiz_canvas.configure(
            scrollregion=quiz_canvas.bbox("all")
        )

        root.bind_all(
            "<MouseWheel>",
            quiz_mousewheel
        )

    # --------------------------------------------------------
    # FAVOURITES
    # --------------------------------------------------------

    elif page == "Favourites":

        if not ensure_logged_in_user():
            return

        clear_frame(favourites_page)

        favourites_page.pack(
            fill="both",
            expand=True
        )

        favourites_page.open_mythlab_page = open_mythlab_page

        # Keep a reference so the object is not garbage-collected.
        favourites_page.app = MythLabFavourites(
            favourites_page,
            current_username
        )

        favourites_page.open_mythlab_page = open_mythlab_page

    # --------------------------------------------------------
    # ABOUT
    # --------------------------------------------------------

    elif page == "About":

        clear_frame(about_page)

        about_page.pack(
            fill="both",
            expand=True
        )

        show_about(about_page)

    else:

        messagebox.showinfo(
            page,
            page + " page will be connected next."
        )


# ============================================================
# SIDEBAR LOGO
# ============================================================

tk.Label(
    sidebar,
    text="🐉",
    font=("Arial", 30),
    bg=SIDEBAR,
    fg=GOLD
).pack(
    pady=(25, 0)
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
    text="Discover the stories, legends, and mythical creatures of Bhutan and beyond.",
    font=("Arial", 9),
    bg=SIDEBAR,
    fg=LIGHT_TEXT,
    wraplength=190,
    justify="center"
).pack(
    pady=(0, 25),
    padx=8
)


# ============================================================
# SIDEBAR MENU
# ============================================================

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

    tk.Button(
        sidebar,
        text=text,
        font=("Arial", 11),
        bg=SIDEBAR,
        fg=TEXT,
        activebackground="#263b47",
        activeforeground=GOLD,
        relief="flat",
        anchor="w",
        padx=20,
        pady=10,
        command=lambda p=page: open_page(p)
    ).pack(
        fill="x",
        padx=10,
        pady=2
    )


# ============================================================
# SIDEBAR QUOTE
# ============================================================

tk.Label(
    sidebar,
    text='“Every myth is a door\nto a deeper wisdom.”\n\n— Bhutanese Wisdom',
    font=("Georgia", 9, "italic"),
    bg=SIDEBAR,
    fg=GOLD,
    justify="center"
).pack(
    side="bottom",
    pady=25
)


# ============================================================
# HOME PAGE
# ============================================================

tk.Label(
    home_content,
    text="Welcome to",
    font=("Georgia", 15),
    bg=BG,
    fg=TEXT
).pack(
    anchor="w",
    padx=40,
    pady=(25, 0)
)

tk.Label(
    home_content,
    text="MythLab",
    font=("Georgia", 32, "bold"),
    bg=BG,
    fg=GOLD
).pack(
    anchor="w",
    padx=40
)

tk.Label(
    home_content,
    text="Explore the myths, legends and mythical creatures\n"
         "of Bhutan and beyond.",
    font=("Arial", 11),
    bg=BG,
    fg=LIGHT_TEXT,
    justify="left"
).pack(
    anchor="w",
    padx=40,
    pady=(0, 15)
)


# ============================================================
# HOME BANNER
# ============================================================

welcome_path = ASSETS_DIR / "welcome.png"

if welcome_path.is_file():

    try:
        welcome_image = Image.open(
            welcome_path
        ).convert("RGB")

        welcome_image = ImageOps.fit(
            welcome_image,
            (1050, 300),
            method=Image.Resampling.LANCZOS
        )

        welcome_photo = ImageTk.PhotoImage(
            welcome_image
        )

        image_refs.append(welcome_photo)

        tk.Label(
            home_content,
            image=welcome_photo,
            bg=BG,
            bd=0
        ).pack(
            fill="x",
            padx=40,
            pady=(0, 18)
        )

    except Exception as error:
        print("Welcome image error:", error)


# ============================================================
# SEARCH
# ============================================================

def search_myth():
    value = search_entry.get().strip()

    if not value:
        messagebox.showwarning(
            "Search",
            "Please enter something to search."
        )
        return

    messagebox.showinfo(
        "Search Result",
        "You searched for: " + value
    )


search_frame = tk.Frame(
    home_content,
    bg=BG
)

search_frame.pack(
    fill="x",
    padx=40,
    pady=(0, 15)
)

search_entry = tk.Entry(
    search_frame,
    font=("Arial", 12),
    bg=CARD,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat"
)

search_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=9,
    padx=(0, 10)
)

tk.Button(
    search_frame,
    text="🔍 Search",
    font=("Arial", 10, "bold"),
    bg=GOLD,
    fg=BG,
    relief="flat",
    padx=18,
    pady=8,
    command=search_myth
).pack(
    side="right"
)


# ============================================================
# HOME CATEGORY CARDS
# ============================================================

tk.Label(
    home_content,
    text="✥  Explore by Category",
    font=("Georgia", 17, "bold"),
    bg=BG,
    fg=GOLD
).pack(
    anchor="w",
    padx=40
)

tk.Label(
    home_content,
    text="Discover fascinating worlds of mythology.",
    font=("Arial", 9),
    bg=BG,
    fg=LIGHT_TEXT
).pack(
    anchor="w",
    padx=40,
    pady=(0, 8)
)

category_frame = tk.Frame(
    home_content,
    bg=BG
)

category_frame.pack(
    fill="x",
    padx=40
)

categories = [
    ("Gods & Goddesses", "Powerful divine beings.", "gods.png"),
    ("Heroes", "Brave legendary figures.", "heroes.png"),
    ("Creatures", "Mythical beasts and spirits.", "creatures.png"),
    ("Folklore", "Traditional stories and legends.", "folklore.png")
]

for name, description, image_file in categories:

    card = tk.Frame(
        category_frame,
        bg=CARD,
        height=170
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=4
    )

    card.pack_propagate(False)

    image_label(
        card,
        image_file,
        (190, 85)
    )

    tk.Label(
        card,
        text=name,
        font=("Georgia", 11, "bold"),
        bg=CARD,
        fg=GOLD
    ).pack(
        anchor="w",
        padx=8
    )

    tk.Label(
        card,
        text=description,
        font=("Arial", 8),
        bg=CARD,
        fg=LIGHT_TEXT
    ).pack(
        anchor="w",
        padx=8
    )

    # Only use valid page names here.
    if name == "Creatures":
        command = lambda: open_page("Creatures")
    else:
        command = lambda: messagebox.showinfo(
            "Category",
            name + " will be added to the library."
        )

    tk.Button(
        card,
        text="→",
        font=("Arial", 11),
        bg=CARD,
        fg=GOLD,
        relief="flat",
        command=command
    ).pack(
        anchor="e",
        padx=8
    )


# ============================================================
# FEATURED MYTHS
# ============================================================

def read_myth(name):
    messagebox.showinfo(
        "Myth",
        name + "\n\nMore information will be added here."
    )


myth_header = tk.Frame(
    home_content,
    bg=BG
)

myth_header.pack(
    fill="x",
    padx=40,
    pady=(18, 5)
)

tk.Label(
    myth_header,
    text="✥  Featured Myths",
    font=("Georgia", 17, "bold"),
    bg=BG,
    fg=GOLD
).pack(
    side="left"
)

tk.Button(
    myth_header,
    text="View all →",
    font=("Arial", 9),
    bg=BG,
    fg=GOLD,
    relief="flat",
    command=lambda: open_page("Myths")
).pack(
    side="right"
)

myth_frame = tk.Frame(
    home_content,
    bg=BG
)

myth_frame.pack(
    fill="x",
    padx=40
)

myths = [
    ("The Thunder Dragon", "Bhutan", "thunder_dragon.png"),
    ("The Yeti", "Bhutan", "yeti.png"),
    ("The Firebird", "Tibet", "firebird (1).png"),
    ("The Black Mountain", "Bhutan", "black_mountain (2).png")
]

for name, region, image_file in myths:

    card = tk.Frame(
        myth_frame,
        bg=CARD,
        height=190
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=4
    )

    card.pack_propagate(False)

    image_label(
        card,
        image_file,
        (190, 90)
    )

    tk.Label(
        card,
        text=name,
        font=("Georgia", 10, "bold"),
        bg=CARD,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=8
    )

    tk.Label(
        card,
        text="📍 " + region,
        font=("Arial", 8),
        bg=CARD,
        fg=LIGHT_TEXT
    ).pack(
        anchor="w",
        padx=8
    )

    tk.Button(
        card,
        text="Read More →",
        font=("Arial", 8),
        bg="#1b3a4d",
        fg=TEXT,
        relief="flat",
        command=lambda n=name: read_myth(n)
    ).pack(
        anchor="w",
        padx=8,
        pady=3
    )


# ============================================================
# FEATURED CREATURES
# ============================================================

def read_creature(name):
    messagebox.showinfo(
        "Creature",
        name + "\n\nMore information will be added here."
    )


creature_header = tk.Frame(
    home_content,
    bg=BG
)

creature_header.pack(
    fill="x",
    padx=40,
    pady=(18, 5)
)

tk.Label(
    creature_header,
    text="✥  Featured Creatures",
    font=("Georgia", 17, "bold"),
    bg=BG,
    fg=GOLD
).pack(
    side="left"
)

tk.Button(
    creature_header,
    text="View all →",
    font=("Arial", 9),
    bg=BG,
    fg=GOLD,
    relief="flat",
    command=lambda: open_page("Creatures")
).pack(
    side="right"
)

creature_frame = tk.Frame(
    home_content,
    bg=BG
)

creature_frame.pack(
    fill="x",
    padx=40
)

creatures = [
    ("Druk", "Dragon", "druk (3).png"),
    ("Yeti", "Yeti", "yeti_creature.png"),
    ("Migoi", "Spirit", "migoi.png"),
    ("Snow Lion", "Mythical Beast", "snow_lion.png")
]

for name, creature_type, image_file in creatures:

    card = tk.Frame(
        creature_frame,
        bg=CARD,
        height=180
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=4
    )

    card.pack_propagate(False)

    image_label(
        card,
        image_file,
        (190, 85)
    )

    tk.Label(
        card,
        text=name,
        font=("Georgia", 10, "bold"),
        bg=CARD,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=8
    )

    tk.Label(
        card,
        text=creature_type,
        font=("Arial", 8),
        bg=CARD,
        fg=LIGHT_TEXT
    ).pack(
        anchor="w",
        padx=8
    )

    tk.Button(
        card,
        text="Read More →",
        font=("Arial", 8),
        bg="#1b3a4d",
        fg=TEXT,
        relief="flat",
        command=lambda n=name: read_creature(n)
    ).pack(
        anchor="w",
        padx=8,
        pady=3
    )


# ============================================================
# RECENTLY EXPLORED
# ============================================================

def recent_item(name):
    messagebox.showinfo(
        "Recently Explored",
        "You selected: " + name
    )


recent_header = tk.Frame(
    home_content,
    bg=BG
)

recent_header.pack(
    fill="x",
    padx=40,
    pady=(18, 5)
)

tk.Label(
    recent_header,
    text="◷  Recently Explored",
    font=("Georgia", 17, "bold"),
    bg=BG,
    fg=GOLD
).pack(
    side="left"
)

recent_frame = tk.Frame(
    home_content,
    bg=BG
)

recent_frame.pack(
    fill="x",
    padx=40,
    pady=(0, 15)
)

recent_items = [
    ("The Black Mountain", "Bhutan", "recent_black_mountain.png"),
    ("The Legend of Paro Taktsang", "Bhutan", "paro_taktsang.png"),
    ("The Firebird", "Tibet", "recent_firebird.png"),
    ("The Snake Princess", "Bhutan", "snake_princess.png"),
    ("Mount Jomolhari", "Bhutan", "jomolhari.png"),
    ("The Water Spirit", "Bhutan", "water_spirit.png")
]

for name, region, image_file in recent_items:

    card = tk.Frame(
        recent_frame,
        bg=CARD,
        height=170
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=3
    )

    card.pack_propagate(False)

    image_label(
        card,
        image_file,
        (145, 65)
    )

    tk.Label(
        card,
        text=name,
        font=("Georgia", 8, "bold"),
        bg=CARD,
        fg=TEXT,
        wraplength=125,
        justify="left"
    ).pack(
        anchor="w",
        padx=6,
        pady=(3, 0)
    )

    tk.Label(
        card,
        text="📍 " + region,
        font=("Arial", 7),
        bg=CARD,
        fg=LIGHT_TEXT
    ).pack(
        anchor="w",
        padx=6,
        pady=(3, 0)
    )

    tk.Button(
        card,
        text="Open",
        font=("Arial", 7),
        bg="#1b3a4d",
        fg=TEXT,
        relief="flat",
        command=lambda n=name: recent_item(n)
    ).pack(
        anchor="w",
        padx=6,
        pady=3
    )


# ============================================================
# HOME BOTTOM
# ============================================================

bottom = tk.Frame(
    home_content,
    bg=BG
)

bottom.pack(
    fill="x",
    padx=40,
    pady=(0, 30)
)

tk.Label(
    bottom,
    text="MythLab • Bhutanese mythology and legends",
    font=("Arial", 9),
    bg=BG,
    fg=LIGHT_TEXT
).pack(
    side="left"
)


# ============================================================
# START
# ============================================================

open_page("Home")
root.mainloop()