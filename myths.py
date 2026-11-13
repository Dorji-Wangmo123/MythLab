
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import sqlite3
import customtkinter as ctk
from PIL import Image, ImageTk, ImageOps

# ============================================================
# MYTHLAB - MYTHS PAGE
# ============================================================

BG = "#061b2b"
SIDEBAR = "#071522"
CARD = "#092333"
GOLD = "#d6a84f"
TEXT = "#f5ead0"
LIGHT_TEXT = "#c7c1b3"

PROJECT_DIR = Path(__file__).resolve().parent
IMAGE_DIR = PROJECT_DIR / "assets"
DB_FILE = PROJECT_DIR / "mythlab.db"

image_refs = []

# Keep the King Gesar image consistent between the collection and story page.
# myth_detail.py is the existing story-detail module used by main.py.
# Updating its shared MYTH_CONTENT dictionary changes the story image
# without replacing or rewriting the story-detail module.
try:
    import myth_detail as _myth_detail
    if "The Story of King Gesar" in _myth_detail.MYTH_CONTENT:
        _myth_detail.MYTH_CONTENT["The Story of King Gesar"]["image"] = "king_gesar_custom.png"
    # Ensure the Serpent King detail uses the new PNG, not a dragon.
    if "The Serpent King" in _myth_detail.MYTH_CONTENT:
        _myth_detail.MYTH_CONTENT["The Serpent King"]["image"] = "serpent_king.png"
except (ImportError, AttributeError) as _image_error:
    print("King Gesar story image could not be configured:", _image_error)

# ============================================================
# MYTH DATA
# ============================================================

MYTHS = [
    # GODS AND GODDESSES
    ("Gods & Goddesses", "Genyen Jagpa Melen",
     "A powerful guardian deity associated with Dechenphu Lhakhang.",
     "genyen_jagpa_melen.png", "Bhutan"),

    ("Gods & Goddesses", "Ap Chhundu",
     "The traditional guardian deity of Haa Valley.",
     "ap_chhundu.png", "Bhutan"),

    ("Gods & Goddesses", "Jomo (Aum Jomo)",
     "The sacred mountain goddess associated with Mount Jomolhari.",
     "jomo.png", "Bhutan"),

    ("Gods & Goddesses", "Ap Genyen Domtshang",
     "A local guardian deity associated with Changangkha Lhakhang.",
     "ap_genyen_domtshang.png", "Bhutan"),

    ("Gods & Goddesses", "Guru Rinpoche",
     "The great Buddhist master whose teachings shaped Bhutan.",
     "guru_rinpoche.png", "Bhutan"),

    ("Gods & Goddesses", "Yeshey Gonpo",
     "A powerful Dharma protector revered in Bhutanese traditions.",
     "yeshey_gonpo.png", "Bhutan"),

    # HEROES
    ("Heroes", "The Story of King Gesar",
     "The legendary hero celebrated across Tibetan and Himalayan traditions.",
     "king_gesar_custom.png", "Asia"),

    ("Heroes", "Drukpa Kunley",
     "The Divine Madman remembered for his humour and unconventional teachings.",
     "drukpa_kuenley.jpg", "Bhutan"),

    # FOLKLORE
    ("Folklore", "The Black Mountain",
     "A sacred Bhutanese landscape connected with local traditions.",
     "black_mountain (2).png", "Bhutan"),

    ("Folklore", "The Legend of Paro Taktsang",
     "The sacred cliffside monastery associated with Guru Rinpoche.",
     "paro_taktsang.png", "Bhutan"),

    ("Folklore", "The Birth of the Universe",
     "Traditional explanations of the origins of the universe.",
     "gods.png", "Other"),

    ("Folklore", "The Demoness of Dochula",
     "A traditional story associated with Drukpa Kunley and Chimi Lhakhang.",
     "dochula.png", "Bhutan"),

    ("Folklore", "The Man Saved by a Dragon",
     "A mysterious survival tale associated with the mountains of Bhutan.",
     "thunder_dragon.png", "Bhutan"),
]

# Use the same creature catalogue on both pages.
from creatures import CREATURES
for title, kind, group, region, filename, description in CREATURES:
    origin = "Europe" if title == "The Firebird" else region
    MYTHS.append(("Creatures", title, description, filename, origin))

# Register expanded creature stories in the shared detail dictionary,
# including Migoi, Rangda, Firebird, and Giant Tortoise.
import creatures as _creature_story_registration

CATEGORIES = [
    "All",
    "Gods & Goddesses",
    "Heroes",
    "Creatures",
    "Folklore"
]

REGIONS = ["All", "Bhutan", "Asia", "Europe", "Other"]

PAGE_SIZE = 8


def show_myths(parent, open_detail=None, initial_category="All",
               get_current_username=None, request_login=None):

    global image_refs
    image_refs = []

    for widget in parent.winfo_children():
        widget.destroy()

    # ========================================================
    # IMAGE HELPERS
    # ========================================================

    def normalise_filename(filename):
        """Remove spaces and symbols for flexible filename matching."""
        return "".join(
            character.lower()
            for character in Path(filename).stem
            if character.isalnum()
        )

    def find_image(filename):
        """Find a matching local image, prioritising exact filenames."""
        # These specific images must never be replaced by an unrelated
        # similarly named picture when their exact files are missing.
        if filename.lower() in {"drukpa_kuenley.jpg", "serpent_king.png"}:
            for folder in (IMAGE_DIR, PROJECT_DIR):
                candidate = folder / filename
                if candidate.is_file():
                    return candidate
            print("IMAGE NOT FOUND:", filename)
            return None

        extensions = [".png", ".jpg", ".jpeg", ".webp"]

        requested = Path(filename)
        target_name = normalise_filename(filename)

        # Check exact locations first
        possible_paths = [
            IMAGE_DIR / filename,
            PROJECT_DIR / filename
        ]

        for path in possible_paths:
            if path.exists() and path.is_file():
                print("IMAGE FOUND:", path)
                return path

        # Search the assets folder
        if IMAGE_DIR.exists():

            for item in IMAGE_DIR.iterdir():

                if not item.is_file():
                    continue

                if item.suffix.lower() not in extensions:
                    continue

                item_name = normalise_filename(item.name)

                if (
                    item_name == target_name
                    or item_name.startswith(target_name)
                    or target_name.startswith(item_name)
                ):
                    print("IMAGE FOUND:", item)
                    return item

        print("IMAGE NOT FOUND:", filename)
        return None

    def load_image(filename, size):
        path = find_image(filename)

        if path is None:
            return None

        try:
            image = Image.open(path).convert("RGB")

            # Fill every card consistently. For the two tall portraits,
            # position the crop toward the top so faces remain visible.
            portrait_names = {
                "guru_rinpoche.png", "guru.jpg",
                "king_gesar_custom.png", "king gesar.jpg"
            }
            if filename.lower() in portrait_names:
                image = ImageOps.fit(
                    image, size,
                    method=Image.Resampling.LANCZOS,
                    centering=(0.5, 0.12)
                )
            else:
                image = ImageOps.fit(
                    image, size,
                    method=Image.Resampling.LANCZOS
                )

            photo = ImageTk.PhotoImage(image)
            image_refs.append(photo)

            return photo

        except Exception as error:
            print("IMAGE ERROR:", filename, error)
            return None

    # ========================================================
    # FILTER STATE
    # ========================================================

    if initial_category not in CATEGORIES:
        initial_category = "All"

    state = {
        "category": initial_category,
        "region": "All",
        "search": "",
        "page": 1
    }

    category_buttons = {}
    region_buttons = {}

    # ========================================================
    # SCROLLABLE PAGE
    # ========================================================

    canvas = tk.Canvas(
        parent,
        bg=BG,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        parent,
        orient="vertical",
        command=canvas.yview
    )

    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    content = tk.Frame(canvas, bg=BG)

    window_id = canvas.create_window(
        (0, 0),
        window=content,
        anchor="nw"
    )

    def update_scroll(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def resize_content(event):
        canvas.itemconfigure(window_id, width=event.width)

    content.bind("<Configure>", update_scroll)
    canvas.bind("<Configure>", resize_content)

    def scroll_canvas(event):
        if getattr(event, "num", None) == 4:
            direction = -1
        elif getattr(event, "num", None) == 5:
            direction = 1
        else:
            direction = -1 if event.delta > 0 else 1

        canvas.yview_scroll(direction, "units")

    canvas.bind_all("<MouseWheel>", scroll_canvas)

    # ========================================================
    # HERO BANNER
    # ========================================================

    hero = tk.Canvas(
        content,
        height=240,
        bg="#183b50",
        highlightthickness=0
    )

    hero.pack(fill="x", padx=30, pady=(20, 18))

    hero_ref = [None]

    def draw_hero(event=None):
        width = max(hero.winfo_width(), 900)
        height = 240

        hero.delete("all")

        path = find_image("welcome.png")

        if path:
            try:
                image = Image.open(path).convert("RGB")

                image = ImageOps.fit(
                    image,
                    (width, height),
                    method=Image.Resampling.LANCZOS
                )

                photo = ImageTk.PhotoImage(image)
                hero_ref[0] = photo
                image_refs.append(photo)

                hero.create_image(
                    0, 0,
                    image=photo,
                    anchor="nw"
                )

            except Exception as error:
                print("Hero image error:", error)

        hero.create_text(
            45, 45,
            text="MYTHLAB COLLECTION",
            anchor="w",
            font=("Arial", 10, "bold"),
            fill=GOLD
        )

        hero.create_text(
            45, 88,
            text="Discover the Myths",
            anchor="w",
            font=("Georgia", 27, "bold"),
            fill=TEXT
        )

        hero.create_text(
            45, 145,
            text=(
                "Explore ancient stories, guardian deities, legendary heroes\n"
                "and mysterious creatures from Bhutan and beyond."
            ),
            anchor="w",
            justify="left",
            font=("Arial", 11),
            fill=LIGHT_TEXT
        )

    hero.bind("<Configure>", draw_hero)
    hero.update_idletasks()
    draw_hero()

    # ========================================================
    # SEARCH
    # ========================================================

    search_frame = tk.Frame(content, bg=BG)
    search_frame.pack(fill="x", padx=30, pady=(0, 15))

    search_entry = ctk.CTkEntry(
        search_frame,
        font=("Arial", 11),
        fg_color="#102b3d",
        text_color=TEXT,
        border_color="#365469",
        border_width=1,
        corner_radius=16,
        height=42,
        placeholder_text="Search myths..."
    )

    search_entry.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(0, 10)
    )

    # ========================================================
    # FILTER AREA
    # ========================================================

    filter_frame = tk.Frame(content, bg=BG)
    filter_frame.pack(fill="x", padx=30, pady=(0, 15))

    category_row = tk.Frame(filter_frame, bg=BG)
    category_row.pack(fill="x", pady=(0, 10))

    tk.Label(
        category_row,
        text="CATEGORY",
        font=("Arial", 9, "bold"),
        bg=BG,
        fg=GOLD
    ).pack(side="left", padx=(0, 10))

    region_row = tk.Frame(filter_frame, bg=BG)
    region_row.pack(fill="x")

    tk.Label(
        region_row,
        text="REGION",
        font=("Arial", 9, "bold"),
        bg=BG,
        fg=GOLD
    ).pack(side="left", padx=(0, 10))

    # ========================================================
    # CARD AREA
    # ========================================================

    card_area = tk.Frame(content, bg=BG)
    card_area.pack(fill="x", padx=30)

    page_frame = tk.Frame(content, bg=BG)
    page_frame.pack(pady=25)

    # ========================================================
    # FILTER FUNCTIONS
    # ========================================================

    def highlight(buttons, selected):
        for label, button in buttons.items():
            active = label == selected

            button.configure(
                fg_color=GOLD if active else "#102b3d",
                text_color=BG if active else TEXT,
                hover_color="#e5bd68" if active else "#1c4055"
            )

    def filter_category(category):
        state["category"] = category
        state["page"] = 1

        highlight(category_buttons, category)
        render_cards()

    def filter_region(region):
        state["region"] = region
        state["page"] = 1

        highlight(region_buttons, region)
        render_cards()

    def search_myth(event=None):
        """Search every MythLab story, regardless of previously selected filters."""
        state["search"] = search_entry.get().strip().casefold()
        state["page"] = 1
        if state["search"]:
            state["category"] = "All"
            state["region"] = "All"
            highlight(category_buttons, "All")
            highlight(region_buttons, "All")
        render_cards()

    def read_more(name):
        if open_detail:
            open_detail(name, state["category"])
        else:
            messagebox.showinfo(
                "MythLab",
                "The story detail page is not connected."
            )

    def favourite(name, button=None):
        """Toggle a myth in the existing per-user favourites table."""
        username = get_current_username() if callable(get_current_username) else None
        if not username and callable(request_login):
            if not request_login():
                return
            username = get_current_username() if callable(get_current_username) else None
        if not username:
            messagebox.showwarning("Login required", "Please log in to save favourites.")
            return

        myth = next((item for item in MYTHS if item[1] == name), None)
        if myth is None:
            return
        category, title, description, image_file, region = myth
        try:
            with sqlite3.connect(DB_FILE) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT id FROM users WHERE LOWER(username) = LOWER(?)", (username.strip(),))
                user = cursor.fetchone()
                if user is None:
                    messagebox.showwarning("Login required", "Your user account was not found.")
                    return
                user_id = user[0]
                cursor.execute("""CREATE TABLE IF NOT EXISTS favourites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL, item_type TEXT NOT NULL,
                    item_id INTEGER, title TEXT, description TEXT,
                    region TEXT, image TEXT)""")
                cursor.execute("""SELECT id FROM favourites
                    WHERE user_id = ? AND LOWER(item_type) = 'myth' AND title = ?""",
                    (user_id, title))
                existing = cursor.fetchall()
                if existing:
                    cursor.executemany("DELETE FROM favourites WHERE id = ? AND user_id = ?",
                                       [(row[0], user_id) for row in existing])
                    added = False
                else:
                    # The original database requires a non-NULL item_id.
                    # Use the myth's stable position in the MYTHS collection.
                    myth_id = MYTHS.index(myth) + 1
                    cursor.execute("""INSERT INTO favourites
                        (user_id, item_type, item_id, title, description, region, image)
                        VALUES (?, 'myth', ?, ?, ?, ?, ?)""",
                        (user_id, myth_id, title, description, region, image_file))
                    added = True
            if button is not None and button.winfo_exists():
                button.configure(text="♥" if added else "♡")
            messagebox.showinfo("Favourites", f"{title} {'added to' if added else 'removed from'} your favourites.")
        except sqlite3.Error as error:
            messagebox.showerror("Favourites", f"Could not update favourites: {error}")

    def is_favourite(name):
        username = get_current_username() if callable(get_current_username) else None
        if not username or not DB_FILE.exists():
            return False
        try:
            with sqlite3.connect(DB_FILE) as connection:
                return connection.execute("""SELECT 1 FROM favourites f
                    JOIN users u ON u.id = f.user_id
                    WHERE LOWER(u.username) = LOWER(?)
                      AND LOWER(f.item_type) = 'myth' AND f.title = ? LIMIT 1""",
                    (username.strip(), name)).fetchone() is not None
        except sqlite3.Error:
            return False

    # ========================================================
    # FILTER BUTTONS
    # ========================================================

    for category in CATEGORIES:
        button = ctk.CTkButton(
            category_row,
            text=category,
            font=("Arial", 11, "bold"),
            fg_color="#102b3d",
            text_color=TEXT,
            hover_color="#1c4055",
            border_color="#365469",
            border_width=1,
            corner_radius=14,
            height=34,
            width=max(58, len(category) * 8 + 26),
            command=lambda c=category: filter_category(c)
        )
        button.pack(side="left", padx=3)
        category_buttons[category] = button

    for region in REGIONS:
        button = ctk.CTkButton(
            region_row,
            text=region,
            font=("Arial", 11),
            fg_color="#102b3d",
            text_color=TEXT,
            hover_color="#1c4055",
            border_color="#365469",
            border_width=1,
            corner_radius=14,
            height=34,
            width=max(58, len(region) * 8 + 26),
            command=lambda r=region: filter_region(r)
        )
        button.pack(side="left", padx=3)
        region_buttons[region] = button

    ctk.CTkButton(
        search_frame,
        text="SEARCH",
        font=("Arial", 11, "bold"),
        fg_color=GOLD,
        text_color=BG,
        hover_color="#e5bd68",
        corner_radius=15,
        width=100,
        height=42,
        command=search_myth
    ).pack(side="right")

    # Update results while typing, not only when the Search button is clicked.
    search_entry.bind("<KeyRelease>", search_myth)
    search_entry.bind("<Return>", search_myth)

    # ========================================================
    # MATCHING STORIES
    # ========================================================

    def matching_myths():
        found = []

        for myth in MYTHS:

            category, name, description, image, region = myth

            if (
                state["category"] != "All"
                and category != state["category"]
            ):
                continue

            if (
                state["region"] != "All"
                and region != state["region"]
            ):
                continue

            searchable = (
                category + " " + name + " " + description + " " + region
            ).casefold()

            if (
                state["search"]
                and state["search"] not in searchable
            ):
                continue

            found.append(myth)

        return found

    # ========================================================
    # PAGINATION
    # ========================================================

    def go_to_page(number):
        state["page"] = number
        render_cards()
        canvas.yview_moveto(0)

    def render_pagination(total_pages):

        for widget in page_frame.winfo_children():
            widget.destroy()

        if total_pages <= 1:
            return

        current = state["page"]

        tk.Button(
            page_frame,
            text="←",
            bg=BG,
            fg=GOLD,
            relief="flat",
            command=lambda: go_to_page(current - 1),
            state="normal" if current > 1 else "disabled"
        ).pack(side="left", padx=5)

        for number in range(1, total_pages + 1):

            tk.Button(
                page_frame,
                text=str(number),
                bg=GOLD if number == current else BG,
                fg=BG if number == current else TEXT,
                relief="solid",
                bd=1,
                width=3,
                command=lambda n=number: go_to_page(n)
            ).pack(side="left", padx=3)

        tk.Button(
            page_frame,
            text="→",
            bg=BG,
            fg=GOLD,
            relief="flat",
            command=lambda: go_to_page(current + 1),
            state="normal" if current < total_pages else "disabled"
        ).pack(side="left", padx=5)

    # ========================================================
    # STORY CARDS
    # ========================================================

    def render_cards():

        for widget in card_area.winfo_children():
            widget.destroy()

        matches = matching_myths()

        total_pages = max(
            1,
            (len(matches) + PAGE_SIZE - 1) // PAGE_SIZE
        )

        state["page"] = min(state["page"], total_pages)

        start = (state["page"] - 1) * PAGE_SIZE
        page_items = matches[start:start + PAGE_SIZE]

        if not page_items:

            tk.Label(
                card_area,
                text="No stories found.\nTry another category, region or search.",
                font=("Georgia", 14, "italic"),
                bg=BG,
                fg=LIGHT_TEXT,
                pady=70
            ).pack()

            render_pagination(total_pages)
            return

        for index, myth in enumerate(page_items):

            category, name, description, image_file, region = myth

            # Create a new row after every four cards
            if index % 4 == 0:

                row = tk.Frame(card_area, bg=BG)
                row.pack(fill="x", pady=7)

                for col in range(4):
                    row.grid_columnconfigure(
                        col,
                        weight=1,
                        uniform="myth_cards"
                    )

            card = tk.Frame(
                row,
                bg=CARD,
                height=300,
                highlightbackground="#755d2d",
                highlightthickness=1
            )

            card.grid(
                row=0,
                column=index % 4,
                sticky="nsew",
                padx=6
            )

            card.grid_propagate(False)

            # CARD IMAGE
            photo = load_image(image_file, (250, 135))

            if photo:

                image_label = tk.Label(
                    card,
                    image=photo,
                    bg=CARD
                )

            else:

                image_label = tk.Label(
                    card,
                    text="MYTHLAB",
                    font=("Georgia", 18, "bold"),
                    bg="#183b50",
                    fg=GOLD,
                    height=5
                )

            image_label.pack(
                fill="x",
                padx=5,
                pady=5
            )

            # CATEGORY
            tk.Label(
                card,
                text=category.upper(),
                font=("Arial", 7, "bold"),
                bg=CARD,
                fg=GOLD
            ).pack(
                anchor="w",
                padx=10,
                pady=(3, 0)
            )

            # TITLE
            tk.Label(
                card,
                text=name,
                font=("Georgia", 11, "bold"),
                bg=CARD,
                fg=TEXT,
                wraplength=235,
                justify="left"
            ).pack(
                anchor="w",
                padx=10,
                pady=(5, 2)
            )

            # DESCRIPTION
            tk.Label(
                card,
                text=description,
                font=("Arial", 8),
                bg=CARD,
                fg=LIGHT_TEXT,
                wraplength=235,
                justify="left"
            ).pack(
                anchor="w",
                padx=10
            )

            # BUTTONS
            button_frame = tk.Frame(card, bg=CARD)

            button_frame.pack(
                side="bottom",
                fill="x",
                padx=10,
                pady=10
            )

            tk.Button(
                button_frame,
                text="Read Story  →",
                font=("Arial", 8, "bold"),
                bg=GOLD,
                fg=BG,
                activebackground="#e5c875",
                relief="flat",
                cursor="hand2",
                command=lambda n=name: read_more(n)
            ).pack(side="left")

            heart_button = tk.Button(
                button_frame,
                text="♥" if is_favourite(name) else "♡",
                font=("Arial", 13),
                bg=CARD,
                fg=GOLD,
                relief="flat",
                cursor="hand2"
            )
            heart_button.configure(command=lambda n=name, b=heart_button: favourite(n, b))
            heart_button.pack(side="right")

        render_pagination(total_pages)

    # ========================================================
    # INITIAL DISPLAY
    # ========================================================

    highlight(category_buttons, state["category"])
    highlight(region_buttons, state["region"])

    render_cards()


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()
    root.title("MythLab - Myths")
    root.geometry("1280x900")
    root.configure(bg=BG)

    show_myths(root)
    root.mainloop()
