import tkinter as tk
from tkinter import messagebox
from pathlib import Path

from quiz import show_quiz

# Pillow is used to resize the PNG images.
# If Pillow is not installed, run:
# pip install pillow
from PIL import Image, ImageTk, ImageOps


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()
root.title("MythLab - Mythology Library")
root.geometry("1200x900")
root.minsize(900, 650)
root.configure(bg="#071b2b")


# ==========================================
# COLOURS
# ==========================================

BG = "#071b2b"
SIDEBAR = "#061522"
CARD = "#102b3d"
GOLD = "#d6a84f"
TEXT = "#f5ead0"
LIGHT_TEXT = "#c7c1b3"


# ==========================================
# IMAGE FOLDER
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent
IMAGE_DIR = PROJECT_DIR / "images"

# Keep image objects in memory so Tkinter does not remove them.
image_refs = []


def find_image(filename):
    """Find an image whether it is inside images/ or beside main.py."""
    # First check the images folder.
    path = IMAGE_DIR / filename
    if path.exists():
        return path

    # Also check beside main.py.
    path = PROJECT_DIR / filename
    if path.exists():
        return path

    # Finally, look for a similar filename.
    # This handles names such as:
    # black_mountain (2).png
    # druk (3).png
    # firebird (1).png
    stem = Path(filename).stem.lower()
    extension = Path(filename).suffix.lower()

    for folder in [IMAGE_DIR, PROJECT_DIR]:
        # Only scan folders. Your current "images" item may be a file,
        # so pathlib would raise NotADirectoryError if we tried to open it.
        if folder.is_dir():
            for item in folder.iterdir():
                if item.is_file() and item.suffix.lower() == extension:
                    item_stem = item.stem.lower()
                    if item_stem.startswith(stem) or stem.startswith(item_stem):
                        return item

    return None


def load_image(filename, size):
    """Load and resize an image for a card."""
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
        print("Could not load:", filename, error)
        return None


def image_label(parent, filename, size, bg="#183b50"):
    """Create an image label for a card."""
    photo = load_image(filename, size)

    if photo:
        label = tk.Label(
            parent,
            image=photo,
            bg=bg
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


def welcome_image_label(parent):
    """Show the large welcome banner."""
    welcome_path = Path(__file__).resolve().parent / "welcome.png"

    if not welcome_path.is_file():
        print("WELCOME IMAGE NOT FOUND:")
        print(welcome_path)
        return None

    try:
        image = Image.open(welcome_path).convert("RGB")
        image = ImageOps.fit(
            image,
            (1050, 300),
            method=Image.Resampling.LANCZOS
        )
        photo = ImageTk.PhotoImage(image)

        # Keep a reference so Tkinter continues showing the image.
        image_refs.append(photo)

        label = tk.Label(
            parent,
            image=photo,
            bg=BG,
            bd=0
        )
        label.pack(
            fill="x",
            padx=40,
            pady=(0, 18)
        )
        return label

    except Exception as error:
        print("Could not load welcome.png:", error)
        return None


# ==========================================
# FUNCTIONS
# ==========================================

def search_myth():
    search = search_entry.get().strip()

    if search == "":
        messagebox.showwarning(
            "Search",
            "Please enter something to search."
        )
    else:
        messagebox.showinfo(
            "Search Result",
            "You searched for: " + search
        )


def open_page(page):

    if page == "Quiz":
        show_quiz(content)

    else:
        messagebox.showinfo(
            page,
            page + " page will be added here."
        )


def read_myth(name):
    messagebox.showinfo(
        "Myth",
        name + "\n\nMore information will be added here."
    )


def read_creature(name):
    messagebox.showinfo(
        "Creature",
        name + "\n\nMore information will be added here."
    )


def recent_item(name):
    messagebox.showinfo(
        "Recently Explored",
        "You selected: " + name
    )


# ==========================================
# SIDEBAR
# ==========================================

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


# ==========================================
# LOGO
# ==========================================

tk.Label(
    sidebar,
    text="🐉",
    font=("Arial", 30),
    bg=SIDEBAR,
    fg=GOLD
).pack(pady=(25, 0))


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
    fg=LIGHT_TEXT
).pack(pady=(0, 25))


# ==========================================
# SIDEBAR MENU
# ==========================================

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


# ==========================================
# SIDEBAR QUOTE
# ==========================================

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


# ==========================================
# MAIN AREA
# ==========================================

main_area = tk.Frame(
    root,
    bg=BG
)

main_area.pack(
    side="right",
    fill="both",
    expand=True
)


# ==========================================
# CANVAS + SCROLLBAR
# ==========================================

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


def update_scroll_region(event=None):
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
    update_scroll_region
)

canvas.bind(
    "<Configure>",
    resize_content
)


# ==========================================
# MOUSE WHEEL SCROLLING
# ==========================================

def scroll_canvas(event):
    canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


canvas.bind_all(
    "<MouseWheel>",
    scroll_canvas
)


# ==========================================
# WELCOME
# ==========================================

tk.Label(
    content,
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
    content,
    text="MythLab",
    font=("Georgia", 32, "bold"),
    bg=BG,
    fg=GOLD
).pack(
    anchor="w",
    padx=40
)

tk.Label(
    content,
    text="Explore the myths, legends and mythical creatures\n"
         "of Bhutan and beyond.",)


tk.Label(
    content,
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


# ==========================================
# WELCOME IMAGE
# ==========================================

welcome_image_label(content)


# ==========================================
# SEARCH
# ==========================================

search_frame = tk.Frame(
    content,
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


# ==========================================
# EXPLORE BY CATEGORY
# ==========================================

tk.Label(
    content,
    text="✥  Explore by Category",
    font=("Georgia", 17, "bold"),
    bg=BG,
    fg=GOLD
).pack(
    anchor="w",
    padx=40
)


tk.Label(
    content,
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
    content,
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

    tk.Button(
        card,
        text="→",
        font=("Arial", 11),
        bg=CARD,
        fg=GOLD,
        relief="flat",
        command=lambda n=name: open_page(n)
    ).pack(
        anchor="e",
        padx=8
    )


# ==========================================
# FEATURED MYTHS
# ==========================================

myth_header = tk.Frame(
    content,
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
    content,
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


# ==========================================
# FEATURED CREATURES
# ==========================================

creature_header = tk.Frame(
    content,
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
    content,
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


# ==========================================
# RECENTLY EXPLORED
# ==========================================

recent_header = tk.Frame(
    content,
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
    content,
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


# ==========================================
# BOTTOM NAVIGATION
# ==========================================

bottom = tk.Frame(
    content,
    bg=BG
)

bottom.pack(
    fill="x",
    padx=40,
    pady=(0, 25)
)


tk.Button(
    bottom,
    text="←",
    font=("Arial", 14),
    bg=BG,
    fg=GOLD,
    activebackground=BG,
    activeforeground=TEXT,
    relief="flat",
    command=lambda: messagebox.showinfo(
        "Navigation",
        "Previous page"
    )
).pack(
    side="right",
    padx=5
)


tk.Button(
    bottom,
    text="→",
    font=("Arial", 14),
    bg=BG,
    fg=GOLD,
    activebackground=BG,
    activeforeground=TEXT,
    relief="flat",
    command=lambda: messagebox.showinfo(
        "Navigation",
        "Next page"
    )
).pack(
    side="right",
    padx=5
)


# ==========================================
# START PROGRAM
# ==========================================

root.mainloop()

