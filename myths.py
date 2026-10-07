import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from PIL import Image, ImageTk, ImageOps


# ==================================================
# MAIN WINDOW
# ==================================================

root = tk.Tk()
root.title("MythLab - Myths")
root.geometry("1280x900")
root.minsize(1000, 700)
root.configure(bg="#061b2b")


# ==================================================
# COLOURS
# ==================================================

BG = "#061b2b"
SIDEBAR = "#071522"
CARD = "#092333"
GOLD = "#d6a84f"
TEXT = "#f5ead0"
LIGHT_TEXT = "#c7c1b3"


# ==================================================
# IMAGE LOCATION
# All images are in the same folder as myths.py
# ==================================================

IMAGE_DIR = Path(__file__).parent

image_refs = []


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
# CREATE CARD IMAGE
# ==================================================

def create_image(parent, filename, size):

    photo = load_image(filename, size)

    if photo:

        label = tk.Label(
            parent,
            image=photo,
            bg=CARD
        )

    else:

        label = tk.Label(
            parent,
            text="IMAGE NOT FOUND",
            font=("Arial", 8),
            bg="#183b50",
            fg=LIGHT_TEXT
        )

    label.pack(
        fill="x",
        padx=5,
        pady=5
    )

    return label


# ==================================================
# FUNCTIONS
# ==================================================

def search_myth():

    search = search_entry.get().strip()

    if search == "":
        messagebox.showwarning(
            "Search",
            "Please enter a myth to search."
        )

    else:
        messagebox.showinfo(
            "Search",
            "You searched for: " + search
        )


def read_more(name):

    messagebox.showinfo(
        name,
        "More information about "
        + name
        + " will be added here."
    )


def favourite(name):

    messagebox.showinfo(
        "Favourite",
        name + " added to your favourites."
    )


def filter_region(region):

    messagebox.showinfo(
        "Region",
        "Showing myths from: " + region
    )


def filter_category(category):

    messagebox.showinfo(
        "Category",
        "Showing: " + category
    )


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
# ==================================================

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
        command=lambda p=page: messagebox.showinfo(
            p,
            p + " page will be added here."
        )
    ).pack(
        fill="x",
        padx=10,
        pady=2
    )


# ==================================================
# SIDEBAR QUOTE
# ==================================================

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
    height=250
)

hero.pack(
    fill="x",
    padx=30,
    pady=(0, 15)
)

hero.pack_propagate(False)


# ==================================================
# HERO BACKGROUND IMAGE
# ==================================================

hero_photo = load_image(
    "welcome.png",
    (1050, 250)
)


if hero_photo:

    hero_image = tk.Label(
        hero,
        image=hero_photo,
        bg="#183b50"
    )

    hero_image.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )

else:

    tk.Label(
        hero,
        text="Welcome to MythLab",
        font=("Georgia", 24, "bold"),
        bg="#183b50",
        fg=TEXT
    ).place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )


# ==================================================
# HERO TEXT
# ==================================================

# Slight dark transparent-style box
# to make the text easy to see

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
    text="Myths",
    font=("Arial", 10),
    bg="#061b2b",
    fg=GOLD
).pack(
    anchor="w"
)


tk.Label(
    hero_text,
    text="✥  Discover the Myths",
    font=("Georgia", 25, "bold"),
    bg="#061b2b",
    fg=TEXT
).pack(
    anchor="w",
    pady=5
)


tk.Label(
    hero_text,
    text="Discover ancient stories, legendary heroes, and magical beings\n"
         "from Bhutan and cultures around the world.",
    font=("Arial", 10),
    bg="#061b2b",
    fg=LIGHT_TEXT,
    justify="left"
).pack


# ==================================================
# SEARCH BAR
# ==================================================

search_frame = tk.Frame(
    content,
    bg=BG
)

search_frame.pack(
    fill="x",
    padx=30,
    pady=(0, 15)
)


search_entry = tk.Entry(
    search_frame,
    font=("Arial", 11),
    bg="#102b3d",
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


tk.Button(
    search_frame,
    text="🔍",
    font=("Arial", 12),
    bg=GOLD,
    fg=BG,
    relief="flat",
    padx=15,
    pady=6,
    command=search_myth
).pack(
    side="right"
)


# ==================================================
# FILTERS
# ==================================================

filter_frame = tk.Frame(
    content,
    bg=BG
)

filter_frame.pack(
    fill="x",
    padx=30,
    pady=(0, 18)
)


tk.Label(
    filter_frame,
    text="📍 Region:",
    font=("Arial", 9, "bold"),
    bg=BG,
    fg=TEXT
).pack(
    side="left",
    padx=(0, 8)
)


regions = [
    "All",
    "Bhutan",
    "Asia",
    "Europe",
    "Other"
]


for region in regions:

    tk.Button(
        filter_frame,
        text=region,
        font=("Arial", 8),
        bg=GOLD if region == "All" else BG,
        fg=BG if region == "All" else TEXT,
        activebackground=GOLD,
        activeforeground=BG,
        relief="solid",
        bd=1,
        command=lambda r=region: filter_region(r)
    ).pack(
        side="left",
        padx=3,
        ipadx=7
    )


tk.Label(
    filter_frame,
    text="   Categories:",
    font=("Arial", 9, "bold"),
    bg=BG,
    fg=TEXT
).pack(
    side="left",
    padx=(15, 5)
)


categories = [
    "All",
    "Legendary Beings",
    "Heroic Tales",
    "Creation Myths",
    "Folk Tales"
]


for category in categories:

    tk.Button(
        filter_frame,
        text=category,
        font=("Arial", 7),
        bg=GOLD if category == "All" else BG,
        fg=BG if category == "All" else TEXT,
        activebackground=GOLD,
        activeforeground=BG,
        relief="solid",
        bd=1,
        command=lambda c=category: filter_category(c)
    ).pack(
        side="left",
        padx=2,
        ipadx=5
    )


# ==================================================
# MYTH DATA
# ==================================================

myths = [

    (
        "Legendary Beings",
        "The Thunder Dragon",
        "A powerful and sacred dragon that\n"
        "brings rain, fertility and protects the\n"
        "kingdom.",
        "thunder_dragon.png"
    ),

    (
        "Heroic Tales",
        "The Story of King Gesar",
        "The legendary hero who fought against\n"
        "evil and brought peace to the land.",
        "heroes.png"
    ),

    (
        "Creation Myths",
        "The Yeti",
        "A mysterious being said to live in the\n"
        "high mountains of Bhutan and the\n"
        "Himalayas.",
        "yeti.png"
    ),

    (
        "Folk Tales",
        "The Firebird",
        "A magical bird that symbolizes\n"
        "rebirth, hope and the eternal cycle\n"
        "of life.",
        "firebird (1).png"
    ),

    (
        "Legendary Beings",
        "The Black Mountain",
        "A sacred mountain with hidden\n"
        "powers and ancient secrets.",
        "black_mountain (2).png"
    ),

    (
        "Folk Tales",
        "The Snow Lion",
        "A mythical creature symbolizing\n"
        "strength, purity and good fortune.",
        "snow_lion.png"
    ),

    (
        "Heroic Tales",
        "The Legend of Paro Taktsang",
        "The story of Guru Rinpoche and the\n"
        "sacred monastery built in a cliff.",
        "paro_taktsang.png"
    ),

    (
        "Creation Myths",
        "The Birth of the Universe",
        "How the world, its beings and\n"
        "humanity came into existence.",
        "gods.png"
    )
]


# ==================================================
# MYTH CARDS
# ==================================================

card_area = tk.Frame(
    content,
    bg=BG
)

card_area.pack(
    fill="x",
    padx=30
)


for index, myth in enumerate(myths):

    category = myth[0]
    name = myth[1]
    description = myth[2]
    image_file = myth[3]


    if index % 4 == 0:

        row = tk.Frame(
            card_area,
            bg=BG
        )

        row.pack(
            fill="x",
            pady=5
        )


    card = tk.Frame(
        row,
        bg=CARD,
        height=250
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=5
    )

    card.pack_propagate(False)


    create_image(
        card,
        image_file,
        (235, 125)
    )


    tk.Label(
        card,
        text=category,
        font=("Arial", 7),
        bg=CARD,
        fg=GOLD
    ).pack(
        anchor="w",
        padx=10,
        pady=(2, 0)
    )


    tk.Label(
        card,
        text=name,
        font=("Georgia", 11, "bold"),
        bg=CARD,
        fg=TEXT
    ).pack(
        anchor="w",
        padx=10,
        pady=(3, 0)
    )


    tk.Label(
        card,
        text=description,
        font=("Arial", 7),
        bg=CARD,
        fg=LIGHT_TEXT,
        justify="left"
    ).pack(
        anchor="w",
        padx=10,
        pady=(2, 0)
    )


    button_frame = tk.Frame(
        card,
        bg=CARD
    )

    button_frame.pack(
        fill="x",
        padx=10,
        pady=7
    )


    tk.Button(
        button_frame,
        text="Read More →",
        font=("Arial", 7),
        bg=BG,
        fg=GOLD,
        activebackground=GOLD,
        activeforeground=BG,
        relief="solid",
        bd=1,
        command=lambda n=name: read_more(n)
    ).pack(
        side="left"
    )


    tk.Button(
        button_frame,
        text="♡",
        font=("Arial", 11),
        bg=CARD,
        fg=GOLD,
        activebackground=CARD,
        activeforeground=GOLD,
        relief="flat",
        command=lambda n=name: favourite(n)
    ).pack(
        side="right"
    )


# ==================================================
# PAGE NUMBERS
# ==================================================

page_frame = tk.Frame(
    content,
    bg=BG
)

page_frame.pack(
    pady=25
)


tk.Button(
    page_frame,
    text="←",
    font=("Arial", 11),
    bg=BG,
    fg=GOLD,
    relief="solid",
    bd=1,
    command=lambda: messagebox.showinfo(
        "Navigation",
        "Previous page"
    )
).pack(
    side="left",
    padx=8
)


for number in ["1", "2", "3", "4", "5"]:

    tk.Button(
        page_frame,
        text=number,
        font=("Arial", 9, "bold"),
        bg=GOLD if number == "1" else BG,
        fg=BG if number == "1" else TEXT,
        activebackground=GOLD,
        activeforeground=BG,
        relief="solid",
        bd=1,
        width=3,
        command=lambda n=number: messagebox.showinfo(
            "Page",
            "You selected page " + n
        )
    ).pack(
        side="left",
        padx=3
    )


tk.Button(
    page_frame,
    text="→",
    font=("Arial", 11),
    bg=BG,
    fg=GOLD,
    relief="solid",
    bd=1,
    command=lambda: messagebox.showinfo(
        "Navigation",
        "Next page"
    )
).pack(
    side="left",
    padx=8
)


# ==================================================
# RUN
# ==================================================

root.mainloop()