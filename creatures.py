import tkinter as tk
from tkinter import messagebox
from pathlib import Path

# pip install pillow
from PIL import Image, ImageTk, ImageOps


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()
root.title("MythLab - Creatures")
root.geometry("1200x850")
root.minsize(900, 650)

BG = "#0a0e13"
SIDEBAR = "#0d1218"
CARD = "#121820"
BORDER = "#2b2f33"
GOLD = "#d9a648"
GOLD_DARK = "#8a6a2f"
TEXT = "#f5ead0"
LIGHT_TEXT = "#9aa0a6"
ACTIVE_BG = "#1c1a14"

root.configure(bg=BG)


# ==========================================
# IMAGES  (put PNG/JPG files in an "images" folder next to this file)
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent
IMAGE_DIR = PROJECT_DIR / "images"
image_refs = []


IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}

# Extra words to look for if the exact filename is not found.
# If your file is called "druk (3).png", the "druk" word below will match it.
# Edit this list to match YOUR file names.
ALIASES = {
    "creatures_banner": ["banner", "hero", "creatures"],
    "thunder_dragon": ["thunder", "druk"],
    "yeti": ["yeti"],
    "firebird": ["firebird", "phoenix"],
    "migoi": ["migoi"],
    "snow_lion": ["snowlion", "snow", "lion"],
    "druk": ["druk", "dragon"],
    "giant_tortoise": ["tortoise", "turtle"],
    "rangda": ["rangda"],
}


# Shown on a card when its image file does not exist.
# Add the real image later (e.g. rangda.png) and it will replace the placeholder.
PLACEHOLDERS = {
    "giant_tortoise.png": ("🐢", "#2c3a1a"),
    "rangda.png": ("👺", "#3a1414"),
}


def normalize(text):
    """'Snow_Lion (2)' -> 'snowlion2'"""
    return "".join(ch for ch in text.lower() if ch.isalnum())


def all_images():
    files = []
    for folder in [IMAGE_DIR, PROJECT_DIR]:
        if folder.is_dir():
            for item in folder.iterdir():
                if item.is_file() and item.suffix.lower() in IMAGE_EXTS:
                    files.append(item)
    return files


def find_image(filename):
    """Find an image by name, ignoring extension, spaces, underscores and (1) numbers."""
    files = all_images()
    base = Path(filename).stem
    target = normalize(base)

    # 1) same name (any extension)
    for item in files:
        if normalize(item.stem) == target:
            return item

    # 2) similar name, e.g. "firebird (1)"
    for item in files:
        s = normalize(item.stem)
        if s.startswith(target) or target.startswith(s):
            return item

    # 3) alias words
    for word in ALIASES.get(base, []):
        for item in files:
            if normalize(word) in normalize(item.stem):
                return item

    return None


print("Images found:", [f.name for f in all_images()])


def load_image(filename, size, darken_left=False):
    path = find_image(filename)
    if path is None:
        print("IMAGE NOT FOUND:", filename)
        return None
    try:
        image = Image.open(path).convert("RGB")
        image = ImageOps.fit(image, size, method=Image.Resampling.LANCZOS)

        if darken_left:
            # dark fade from the left so the title stays readable
            w, h = size
            mask = Image.linear_gradient("L").rotate(90).resize((w, h))
            dark = Image.new("RGB", size, BG)
            image = Image.composite(image, dark, mask.point(lambda p: 255 - int(p * 0.85)).transpose(Image.FLIP_LEFT_RIGHT))

        return ImageTk.PhotoImage(image)
    except Exception as error:
        print("Could not load:", filename, error)
        return None


# ==========================================
# DATA
# ==========================================

creatures = [
    ("The Thunder Dragon", "Dragon", "Dragons", "Bhutan", "thunder_dragon.png",
     "A powerful and sacred dragon that brings rain, fertility and protects the kingdom."),
    ("The Yeti", "Spirit", "Spirits", "Bhutan", "yeti.png",
     "A mysterious being said to live in the high mountains of Bhutan and the Himalayas."),
    ("The Firebird", "Bird", "Animals", "India", "firebird.png",
     "A magical bird that symbolizes rebirth, hope and the eternal cycle of life."),
    ("Migoi", "Spirit", "Spirits", "Bhutan", "migoi.png",
     "A shape-shifting spirit that lives in the forests and mountains."),
    ("Snow Lion", "Animal", "Animals", "Bhutan", "snow_lion.png",
     "A mythical creature that represents purity, strength and good fortune."),
    ("The Serpent King", "Dragon", "Dragons", "India", "druk.png",
     "A giant serpent believed to dwell in rivers and lakes, controlling water and weather."),
    ("The Giant Tortoise", "Animal", "Animals", "Asia", "giant_tortoise.png",
     "A symbol of longevity and stability, often found in sacred lakes and highlands."),
    ("Rangda", "Spirit", "Spirits", "Asia", "rangda.png",
     "A fierce spirit that represents chaos and destruction, found in Buddhist and Hindu traditions."),
]

TYPES = ["All", "Dragons", "Spirits", "Animals", "Other"]
REGIONS = ["All", "Bhutan", "India", "Asia", "Europe", "Other"]

state = {"type": "All", "region": "All"}
favourites = set()


# ==========================================
# FUNCTIONS
# ==========================================

def open_page(page):
    messagebox.showinfo(page, page + " page will be added here.")


def read_creature(name):
    messagebox.showinfo("Creature", name + "\n\nMore information will be added here.")


def toggle_favourite(name, button):
    if name in favourites:
        favourites.remove(name)
        button.config(text="♡", fg=LIGHT_TEXT)
    else:
        favourites.add(name)
        button.config(text="♥", fg=GOLD)


def set_filter(key, value):
    state[key] = value
    draw_pills()
    draw_cards()


# ==========================================
# SIDEBAR
# ==========================================

sidebar = tk.Frame(root, bg=SIDEBAR, width=210)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(sidebar, text="🐉", font=("Arial", 30), bg=SIDEBAR, fg=GOLD).pack(pady=(25, 0))
tk.Label(sidebar, text="MythLab", font=("Georgia", 22, "bold"), bg=SIDEBAR, fg=GOLD).pack()
tk.Label(sidebar, text="Explore. Learn. Believe.", font=("Arial", 9),
         bg=SIDEBAR, fg=LIGHT_TEXT).pack(pady=(0, 25))

menu_items = [
    ("⌂  Home", "Home"), ("📖  Myths", "Myths"), ("🐉  Creatures", "Creatures"),
    ("🌐  Regions", "Regions"), ("✓  My Tasks", "My Tasks"), ("?  Quiz", "Quiz"),
    ("♡  Favourites", "Favourites"), ("ⓘ  About", "About"),
]

for text, page in menu_items:
    active = page == "Creatures"
    tk.Button(
        sidebar, text=text, font=("Arial", 11),
        bg=ACTIVE_BG if active else SIDEBAR,
        fg=GOLD if active else TEXT,
        activebackground="#1c2530", activeforeground=GOLD,
        highlightthickness=1 if active else 0,
        highlightbackground=GOLD_DARK,
        relief="flat", anchor="w", padx=20, pady=9,
        command=lambda p=page: open_page(p),
    ).pack(fill="x", padx=10, pady=2)

tk.Label(
    sidebar,
    text='“Every myth is a door\nto a deeper wisdom.”\n\n— Bhutanese Wisdom',
    font=("Georgia", 9, "italic"), bg=SIDEBAR, fg=GOLD, justify="center",
).pack(side="bottom", pady=25)


# ==========================================
# MAIN AREA + SCROLLING
# ==========================================

main_area = tk.Frame(root, bg=BG)
main_area.pack(side="right", fill="both", expand=True)

canvas = tk.Canvas(main_area, bg=BG, highlightthickness=0)
scrollbar = tk.Scrollbar(main_area, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

content = tk.Frame(canvas, bg=BG)
content_window = canvas.create_window((0, 0), window=content, anchor="nw")

content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.bind("<Configure>", lambda e: canvas.itemconfig(content_window, width=e.width))
canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))


# ==========================================
# HERO BANNER  (image with text drawn on top)
# ==========================================

HERO_W, HERO_H = 1000, 280   # change 280 to make the banner taller or shorter

hero = tk.Canvas(content, width=HERO_W, height=HERO_H, bg=BG, highlightthickness=0)
hero.pack(fill="x")

def draw_hero(event=None):
    w = max(hero.winfo_width(), 500)
    hero.delete("all")
    photo = load_image("creatures_banner.png", (w, HERO_H), darken_left=True)
    if photo:
        hero.photo = photo
        hero.create_image(0, 0, image=photo, anchor="nw")
    hero.create_text(45, 40, text="Home   ›   Creatures", anchor="w", fill=LIGHT_TEXT, font=("Arial", 10))
    hero.create_text(45, 120, text="🐉  Creatures", anchor="w", fill=GOLD, font=("Georgia", 40, "bold"))
    hero.create_text(
        45, 195, anchor="w", fill=TEXT, font=("Arial", 12), width=460,
        text="Discover the mythical creatures of Bhutan and beyond — "
             "from powerful dragons to mysterious spirits.",
    )


hero.bind("<Configure>", draw_hero)


# ==========================================
# SEARCH + FILTERS
# ==========================================

filters = tk.Frame(content, bg=BG)
filters.pack(fill="x", padx=40, pady=(12, 0))

search_box = tk.Frame(filters, bg=CARD, highlightthickness=1, highlightbackground=BORDER)
search_box.pack(side="left")

tk.Label(search_box, text="🔍", bg=CARD, fg=LIGHT_TEXT).pack(side="left", padx=(8, 0))
search_entry = tk.Entry(search_box, font=("Arial", 11), bg=CARD, fg=LIGHT_TEXT,
                        insertbackground=TEXT, relief="flat", width=28)
search_entry.pack(side="left", ipady=7, padx=6)
search_entry.insert(0, "Search creatures...")


def clear_placeholder(event):
    if search_entry.get() == "Search creatures...":
        search_entry.delete(0, "end")
        search_entry.config(fg=TEXT)


def restore_placeholder(event):
    if search_entry.get().strip() == "":
        search_entry.insert(0, "Search creatures...")
        search_entry.config(fg=LIGHT_TEXT)


search_entry.bind("<FocusIn>", clear_placeholder)
search_entry.bind("<FocusOut>", restore_placeholder)
search_entry.bind("<KeyRelease>", lambda e: draw_cards())

type_frame = tk.Frame(filters, bg=BG)
type_frame.pack(side="right")

region_row = tk.Frame(content, bg=BG)
region_row.pack(fill="x", padx=40, pady=(10, 0))
tk.Label(region_row, text="📍 Region:", font=("Arial", 9), bg=BG, fg=LIGHT_TEXT).pack(side="left", padx=(0, 8))
region_frame = tk.Frame(region_row, bg=BG)
region_frame.pack(side="left")


def draw_pills():
    for frame, options, key in [(type_frame, TYPES, "type"), (region_frame, REGIONS, "region")]:
        for w in frame.winfo_children():
            w.destroy()
        if key == "type":
            tk.Label(frame, text="Type:", font=("Arial", 9), bg=BG, fg=LIGHT_TEXT).pack(side="left", padx=(0, 8))
        for option in options:
            on = state[key] == option
            tk.Button(
                frame, text=option, font=("Arial", 9, "bold" if on else "normal"),
                bg=GOLD if on else CARD, fg=BG if on else TEXT,
                activebackground=GOLD, activeforeground=BG,
                relief="flat", padx=12, pady=3,
                command=lambda k=key, v=option: set_filter(k, v),
            ).pack(side="left", padx=3)


# ==========================================
# FEATURED CREATURES
# ==========================================

header = tk.Frame(content, bg=BG)
header.pack(fill="x", padx=40, pady=(20, 8))

tk.Label(header, text="❖  Featured Creatures", font=("Georgia", 15, "bold"),
         bg=BG, fg=GOLD).pack(side="left")
tk.Button(header, text="View all →", font=("Arial", 9), bg=BG, fg=TEXT,
          activebackground=BG, activeforeground=GOLD, relief="flat",
          command=lambda: open_page("Creatures")).pack(side="right")
tk.Frame(header, bg=GOLD_DARK, height=1).pack(side="left", fill="x", expand=True, padx=12, pady=(8, 0))

grid = tk.Frame(content, bg=BG)
grid.pack(fill="x", padx=36, pady=(0, 30))

for col in range(4):
    grid.columnconfigure(col, weight=1, uniform="card")


CARD_IMG_H = 130


def make_card(parent, name, tag, image_file, description):
    card = tk.Frame(parent, bg=CARD, highlightthickness=1, highlightbackground=BORDER)

    # image fills the card width; redraws when the window is resized
    pic = tk.Canvas(card, height=CARD_IMG_H, bg="#183040", highlightthickness=0)
    pic.pack(fill="x")
    pic.last_width = 0

    def draw_pic(event):
        w = event.width
        if w < 20 or w == pic.last_width:
            return
        pic.last_width = w
        pic.delete("all")

        photo = load_image(image_file, (w, CARD_IMG_H))
        if photo:
            pic.photo = photo
            pic.create_image(0, 0, image=photo, anchor="nw")
        else:
            emoji, colour = PLACEHOLDERS.get(image_file, ("🐉", "#1b2a3a"))
            pic.create_rectangle(0, 0, w, CARD_IMG_H, fill=colour, outline="")
            pic.create_text(w // 2, CARD_IMG_H // 2, text=emoji, font=("Arial", 44))

        pic.create_rectangle(8, 8, 8 + 8 * len(tag) + 14, 26, fill="#0a0e13", outline="#444")
        pic.create_text(15, 17, text=tag, anchor="w", fill=TEXT, font=("Arial", 8))

    pic.bind("<Configure>", draw_pic)

    tk.Label(card, text=name, font=("Georgia", 10, "bold"), bg=CARD, fg=TEXT).pack(anchor="w", padx=8)
    tk.Label(card, text=description, font=("Arial", 8), bg=CARD, fg=LIGHT_TEXT,
             wraplength=175, justify="left").pack(anchor="w", padx=8, pady=(3, 6))

    bottom = tk.Frame(card, bg=CARD)
    bottom.pack(fill="x", padx=8, pady=(0, 8), side="bottom")

    tk.Button(bottom, text="Read More →", font=("Arial", 8), bg="#0c1117", fg=TEXT,
              activebackground="#1c1a14", activeforeground=GOLD,
              highlightthickness=1, highlightbackground=GOLD_DARK, relief="flat",
              padx=8, command=lambda n=name: read_creature(n)).pack(side="left")

    fav = tk.Button(bottom, text="♥" if name in favourites else "♡", font=("Arial", 13),
                    bg=CARD, fg=GOLD if name in favourites else LIGHT_TEXT,
                    activebackground=CARD, relief="flat", bd=0)
    fav.config(command=lambda n=name, b=fav: toggle_favourite(n, b))
    fav.pack(side="right")

    return card


def draw_cards():
    for w in grid.winfo_children():
        w.destroy()

    query = search_entry.get().strip().lower()
    if query == "search creatures...":
        query = ""

    shown = [
        c for c in creatures
        if (state["type"] == "All" or c[2] == state["type"])
        and (state["region"] == "All" or c[3] == state["region"])
        and query in c[0].lower()
    ]

    if not shown:
        tk.Label(grid, text="No creatures match. Try a different search or filter.",
                 font=("Arial", 10), bg=BG, fg=LIGHT_TEXT).grid(row=0, column=0, columnspan=4, pady=40)
        return

    for i, (name, tag, _type, _region, image_file, description) in enumerate(shown):
        make_card(grid, name, tag, image_file, description).grid(
            row=i // 4, column=i % 4, padx=4, pady=4, sticky="nsew")


draw_pills()
draw_cards()

root.mainloop()