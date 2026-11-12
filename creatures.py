#creature.py
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk, ImageOps

from myth_detail import show_myth_detail, MYTH_CONTENT

# ==========================================
# COLORS
# ==========================================

BG = "#0a0e13"
SIDEBAR = "#0d1218"
CARD = "#121820"
BORDER = "#2b2f33"
GOLD = "#d9a648"
GOLD_DARK = "#8a6a2f"
TEXT = "#f5ead0"
LIGHT_TEXT = "#9aa0a6"
ACTIVE_BG = "#1c1a14"

# ==========================================
# IMAGES
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent
IMAGE_DIR = PROJECT_DIR / "assets"

image_refs = []
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}

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

PLACEHOLDERS = {
    "giant_tortoise.png": ("🐢", "#2c3a1a"),
    "rangda.png": ("👺", "#3a1414"),
}


def normalize(text):
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
    files = all_images()
    base = Path(filename).stem
    target = normalize(base)

    for item in files:
        if normalize(item.stem) == target:
            return item

    for item in files:
        stem = normalize(item.stem)
        if stem.startswith(target) or target.startswith(stem):
            return item

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
        image = ImageOps.fit(
            image,
            size,
            method=Image.Resampling.LANCZOS
        )

        if darken_left:
            w, h = size
            mask = Image.linear_gradient("L")
            mask = mask.rotate(90)
            mask = mask.resize((w, h))
            dark = Image.new("RGB", size, BG)

            image = Image.composite(
                image,
                dark,
                mask.point(
                    lambda p: 255 - int(p * 0.85)
                ).transpose(Image.FLIP_LEFT_RIGHT)
            )

        return ImageTk.PhotoImage(image)

    except Exception as error:
        print("Could not load:", filename, error)
        return None


# ==========================================
# CREATURE DATA
# ==========================================

creatures = [
    (
        "The Thunder Dragon",
        "Dragon",
        "Dragons",
        "Bhutan",
        "thunder_dragon.png",
        "A powerful and sacred dragon that brings rain, fertility and protects the kingdom."
    ),
    (
        "The Yeti",
        "Spirit",
        "Spirits",
        "Bhutan",
        "yeti.png",
        "A mysterious being said to live in the high mountains of Bhutan and the Himalayas."
    ),
    (
        "The Firebird",
        "Bird",
        "Animals",
        "India",
        "firebird.png",
        "A magical bird that symbolizes rebirth, hope and the eternal cycle of life."
    ),
    (
        "Migoi",
        "Spirit",
        "Spirits",
        "Bhutan",
        "migoi.png",
        "A shape-shifting spirit that lives in the forests and mountains."
    ),
    (
        "Snow Lion",
        "Animal",
        "Animals",
        "Bhutan",
        "snow_lion.png",
        "A mythical creature that represents purity, strength and good fortune."
    ),
    (
        "The Serpent King",
        "Dragon",
        "Dragons",
        "India",
        "druk.png",
        "A giant serpent believed to dwell in rivers and lakes, controlling water and weather."
    ),
    (
        "The Giant Tortoise",
        "Animal",
        "Animals",
        "Asia",
        "giant_tortoise.png",
        "A symbol of longevity and stability, often found in sacred lakes and highlands."
    ),
    (
        "Rangda",
        "Spirit",
        "Spirits",
        "Asia",
        "rangda.png",
        "A fierce spirit that represents chaos and destruction, found in Buddhist and Hindu traditions."
    ),
]


# ==========================================
# FULL CREATURE STORIES
# ==========================================

CREATURE_STORIES = {
    "The Yeti": {
        "origin": "Bhutan and the Himalayan region",
        "introduction": (
            "The Yeti is one of the most mysterious beings in Himalayan "
            "folklore. It is often described as a large, powerful creature "
            "that lives far away from human settlements."
        ),
        "story": (
            "Long ago, people living near the high mountains told stories "
            "about strange footprints appearing in the snow. Some believed "
            "that a mysterious creature wandered through the forests and "
            "mountain passes. Travellers shared tales of seeing a tall, "
            "hairy figure disappearing between the snowy peaks.\n\n"
            "The creature became known as the Yeti, or the Abominable "
            "Snowman. Although no scientific evidence has confirmed its "
            "existence, stories about the Yeti continue to capture the "
            "imagination of people across the Himalayas."
        ),
        "powers": (
            "The Yeti is traditionally imagined as extremely strong, "
            "well adapted to freezing weather, and able to move through "
            "remote mountain landscapes."
        ),
        "significance": (
            "The Yeti represents the mystery of the Himalayas and the "
            "many secrets people believe are hidden within its mountains."
        )
    },

    "The Firebird": {
        "origin": "Slavic folklore",
        "introduction": (
            "The Firebird is a magical bird from Slavic fairy tales. "
            "It is famous for its glowing feathers, which shine like fire."
        ),
        "story": (
            "In traditional fairy tales, a Firebird appears in a kingdom "
            "and illuminates the darkness with its golden and fiery feathers. "
            "A single feather can shine so brightly that it attracts the "
            "attention of kings and princes.\n\n"
            "In one famous type of tale, a young hero is sent on a difficult "
            "journey to find the mysterious bird. Along the way, he faces "
            "many challenges and discovers that the Firebird is not simply "
            "a treasure to capture, but part of a much greater adventure."
        ),
        "powers": (
            "The Firebird is associated with brilliant glowing feathers, "
            "magical light, and extraordinary beauty."
        ),
        "significance": (
            "The Firebird symbolizes wonder, hope, courage, and the search "
            "for something extraordinary."
        )
    },

    "Migoi": {
        "origin": "Bhutan and Himalayan folklore",
        "introduction": (
            "Migoi is a mysterious wild being associated with the remote "
            "forests and mountains of Bhutan and the wider Himalayan region."
        ),
        "story": (
            "For generations, people have shared stories about a mysterious "
            "being living deep within the forests and high mountain areas. "
            "Some tales describe the Migoi as a powerful creature that avoids "
            "human contact and remains hidden from ordinary travellers.\n\n"
            "Stories about strange footprints and unexplained encounters "
            "have helped keep the legend alive. The Migoi is often connected "
            "with the unknown wilderness and the mysteries of the mountains."
        ),
        "powers": (
            "Traditional accounts describe the Migoi as unusually strong, "
            "elusive, and difficult to find."
        ),
        "significance": (
            "The Migoi represents the mystery of the natural world and "
            "encourages respect for forests, wildlife, and the mountains."
        )
    },

    "Snow Lion": {
        "origin": "Tibetan and Himalayan Buddhist tradition",
        "introduction": (
            "The Snow Lion is a legendary creature found in Tibetan and "
            "Himalayan Buddhist art and stories. It is usually shown with "
            "a white body and a colourful mane."
        ),
        "story": (
            "According to traditional symbolism, the Snow Lion lives among "
            "the snowy mountains and represents strength, fearlessness, "
            "and joy. It is often shown standing proudly on mountain peaks.\n\n"
            "In Buddhist art, the Snow Lion is sometimes associated with "
            "the protection of sacred teachings and the fearless spirit "
            "of wisdom. Its powerful appearance reminds people to face "
            "difficulties with courage."
        ),
        "powers": (
            "The Snow Lion is traditionally associated with extraordinary "
            "strength, fearlessness, protection, and joyful energy."
        ),
        "significance": (
            "The Snow Lion symbolizes courage, purity, happiness, and "
            "spiritual strength. It is an important cultural symbol "
            "throughout the Himalayan region."
        )
    },

    "The Serpent King": {
        "origin": "Indian mythology and Naga traditions",
        "introduction": (
            "The Serpent King represents the powerful Nagas found in "
            "Indian mythology. Nagas are supernatural serpent beings "
            "associated with water and hidden treasures."
        ),
        "story": (
            "In Indian mythology, Nagas are often described as powerful "
            "serpent beings who live in underground kingdoms, rivers, "
            "and sacred waters.\n\n"
            "Some traditional stories describe Naga kings as guardians "
            "of precious treasures and sources of water. They can appear "
            "in serpent form or as human-like beings with serpent features. "
            "People have traditionally respected them as powerful beings "
            "connected with nature and the balance of the world."
        ),
        "powers": (
            "Nagas are associated with control over water, protection "
            "of hidden treasures, transformation, and supernatural power."
        ),
        "significance": (
            "Naga traditions represent the sacred connection between "
            "water, nature, protection, and spiritual life."
        )
    },

    "The Giant Tortoise": {
        "origin": "Indian mythology and wider Asian traditions",
        "introduction": (
            "The Giant Tortoise appears in different Asian myths and "
            "traditional stories. It is often connected with longevity, "
            "wisdom, and stability."
        ),
        "story": (
            "In Hindu mythology, the god Vishnu takes the form of a giant "
            "tortoise known as Kurma. In this story, the tortoise supports "
            "Mount Mandara during the churning of the cosmic ocean.\n\n"
            "The great tortoise provides a stable foundation while the "
            "gods and demons work together to churn the ocean in search "
            "of divine treasures. Its role makes it a powerful symbol "
            "of patience, support, and endurance."
        ),
        "powers": (
            "The legendary tortoise is associated with immense strength, "
            "endurance, protection, and the ability to support great weight."
        ),
        "significance": (
            "The Giant Tortoise symbolizes patience, stability, longevity, "
            "and the importance of a strong foundation."
        )
    },

    "Rangda": {
        "origin": "Balinese tradition, Indonesia",
        "introduction": (
            "Rangda is a powerful and fearsome figure in Balinese tradition. "
            "She is commonly portrayed as a frightening queen associated "
            "with dark supernatural forces."
        ),
        "story": (
            "In Balinese traditional performances, Rangda is known as a "
            "powerful figure who represents destructive forces. She is "
            "often shown with wild hair, sharp teeth, and a frightening face.\n\n"
            "Rangda is famously featured in the Barong and Rangda dance "
            "drama. In these performances, she confronts Barong, a protective "
            "creature. Their struggle represents the ongoing tension between "
            "opposing forces in the world.\n\n"
            "The story is not simply about one side winning. It reflects "
            "the belief that opposing forces are part of the balance of life."
        ),
        "powers": (
            "Rangda is traditionally portrayed with supernatural abilities "
            "and the power to command frightening spirits."
        ),
        "significance": (
            "Rangda is an important figure in Balinese performing arts "
            "and represents the relationship between opposing forces "
            "and the balance of the world."
        )
    }
}


# ==========================================
# CONNECT CREATURE STORIES TO MYTH DETAIL
# ==========================================

for creature in creatures:
    name, tag, creature_type, region, image_file, description = creature

    if name == "The Thunder Dragon":
        continue

    story_data = CREATURE_STORIES.get(name)

    if story_data:
        MYTH_CONTENT[name] = {
            "category": "Creatures",
            "origin": story_data["origin"],
            "image": image_file,
            "subtitle": description,
            "story": story_data["story"],
            "facts": [
                ("Region", region),
                ("Creature type", tag),
                ("Powers and abilities", story_data["powers"])
            ],
            "note": story_data["significance"]
        }


TYPES = ["All", "Dragons", "Spirits", "Animals", "Other"]
REGIONS = ["All", "Bhutan", "India", "Asia", "Europe", "Other"]

state = {
    "type": "All",
    "region": "All"
}

favourites = set()


# ==========================================
# CLEAR PARENT FRAME
# ==========================================

def clear_parent(parent):
    for widget in parent.winfo_children():
        widget.destroy()


# ==========================================
# CREATURE STORY DETAIL PAGE
# USES THE SAME LAYOUT AS MYTH DETAILS
# ==========================================

def show_creature_story(parent, name, back_callback):

    if name not in MYTH_CONTENT:
        return

    # Display the existing shared Myth detail page.
    show_myth_detail(parent, back_callback, name)

    # Change the back link from "Myths" to "Creatures".
    # This keeps myth_detail.py unchanged.
    def update_back_button(widget):
        for child in widget.winfo_children():
            if isinstance(child, tk.Button):
                button_text = child.cget("text").strip()

                if button_text == "←  Myths":
                    child.config(text="←  Creatures")

            update_back_button(child)

    update_back_button(parent)


# ==========================================
# MAIN CREATURES PAGE
# ==========================================

def show_creatures(parent, saved_search=""):

    clear_parent(parent)

    # ==========================================
    # MAIN AREA + SCROLLING
    # ==========================================

    main_area = tk.Frame(parent, bg=BG)
    main_area.pack(fill="both", expand=True)

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

    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    content = tk.Frame(canvas, bg=BG)

    content_window = canvas.create_window(
        (0, 0),
        window=content,
        anchor="nw"
    )

    content.bind(
        "<Configure>",
        lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.bind(
        "<Configure>",
        lambda event: canvas.itemconfig(
            content_window,
            width=event.width
        )
    )

    # ==========================================
    # HERO BANNER
    # ==========================================

    HERO_H = 280

    hero = tk.Canvas(
        content,
        height=HERO_H,
        bg=BG,
        highlightthickness=0
    )
    hero.pack(fill="x")

    def draw_hero(event=None):
        w = max(hero.winfo_width(), 500)
        hero.delete("all")

        photo = load_image(
            "creatures_banner.png",
            (w, HERO_H),
            darken_left=True
        )

        if photo:
            hero.photo = photo
            hero.create_image(
                0,
                0,
                image=photo,
                anchor="nw"
            )

        hero.create_text(
            45,
            40,
            text="Home   ›   Creatures",
            anchor="w",
            fill=LIGHT_TEXT,
            font=("Arial", 10)
        )

        hero.create_text(
            45,
            120,
            text="🐉  Creatures",
            anchor="w",
            fill=GOLD,
            font=("Georgia", 40, "bold")
        )

        hero.create_text(
            45,
            195,
            anchor="w",
            fill=TEXT,
            font=("Arial", 12),
            width=460,
            text=(
                "Discover the mythical creatures of Bhutan and beyond — "
                "from powerful dragons to mysterious spirits."
            )
        )

    hero.bind("<Configure>", draw_hero)

    # ==========================================
    # SEARCH + FILTERS
    # ==========================================

    filters = tk.Frame(content, bg=BG)
    filters.pack(fill="x", padx=40, pady=(12, 0))

    search_box = tk.Frame(
        filters,
        bg=CARD,
        highlightthickness=1,
        highlightbackground=BORDER
    )
    search_box.pack(side="left")

    tk.Label(
        search_box,
        text="🔍",
        bg=CARD,
        fg=LIGHT_TEXT
    ).pack(side="left", padx=(8, 0))

    search_entry = tk.Entry(
        search_box,
        font=("Arial", 11),
        bg=CARD,
        fg=TEXT if saved_search else LIGHT_TEXT,
        insertbackground=TEXT,
        relief="flat",
        width=28
    )

    search_entry.pack(side="left", ipady=7, padx=6)

    if saved_search:
        search_entry.insert(0, saved_search)
    else:
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

    type_frame = tk.Frame(filters, bg=BG)
    type_frame.pack(side="right")

    region_row = tk.Frame(content, bg=BG)
    region_row.pack(fill="x", padx=40, pady=(10, 0))

    tk.Label(
        region_row,
        text="📍 Region:",
        font=("Arial", 9),
        bg=BG,
        fg=LIGHT_TEXT
    ).pack(side="left", padx=(0, 8))

    region_frame = tk.Frame(region_row, bg=BG)
    region_frame.pack(side="left")

    # ==========================================
    # FILTER FUNCTIONS
    # ==========================================

    def set_filter(key, value):
        state[key] = value
        draw_pills()
        draw_cards()

    def draw_pills():
        for frame, options, key in [
            (type_frame, TYPES, "type"),
            (region_frame, REGIONS, "region")
        ]:
            for widget in frame.winfo_children():
                widget.destroy()

            if key == "type":
                tk.Label(
                    frame,
                    text="Type:",
                    font=("Arial", 9),
                    bg=BG,
                    fg=LIGHT_TEXT
                ).pack(side="left", padx=(0, 8))

            for option in options:
                selected = state[key] == option

                tk.Button(
                    frame,
                    text=option,
                    font=(
                        "Arial",
                        9,
                        "bold" if selected else "normal"
                    ),
                    bg=GOLD if selected else CARD,
                    fg=BG if selected else TEXT,
                    activebackground=GOLD,
                    activeforeground=BG,
                    relief="flat",
                    padx=12,
                    pady=3,
                    command=lambda k=key, v=option: set_filter(k, v)
                ).pack(side="left", padx=3)

    # ==========================================
    # FEATURED CREATURES
    # ==========================================

    header = tk.Frame(content, bg=BG)
    header.pack(fill="x", padx=40, pady=(20, 8))

    tk.Label(
        header,
        text="❖  Featured Creatures",
        font=("Georgia", 15, "bold"),
        bg=BG,
        fg=GOLD
    ).pack(side="left")

    tk.Frame(
        header,
        bg=GOLD_DARK,
        height=1
    ).pack(
        side="left",
        fill="x",
        expand=True,
        padx=12,
        pady=(8, 0)
    )

    grid = tk.Frame(content, bg=BG)
    grid.pack(fill="x", padx=36, pady=(0, 30))

    for col in range(4):
        grid.columnconfigure(col, weight=1, uniform="card")

    CARD_IMG_H = 130

    # ==========================================
    # OPEN CREATURE STORY
    # ==========================================

    def read_creature(name):
        current_search = search_entry.get().strip()

        if current_search == "Search creatures...":
            current_search = ""

        def back_to_creatures():
            show_creatures(
                parent,
                saved_search=current_search
            )

        show_creature_story(
            parent,
            name,
            back_to_creatures
        )

    # ==========================================
    # FAVOURITE BUTTON
    # ==========================================

    def toggle_favourite(name, button):
        if name in favourites:
            favourites.remove(name)
            button.config(text="♡", fg=LIGHT_TEXT)
        else:
            favourites.add(name)
            button.config(text="♥", fg=GOLD)

    # ==========================================
    # CREATURE CARD
    # ==========================================

    def make_card(
        card_parent,
        name,
        tag,
        image_file,
        description
    ):
        card = tk.Frame(
            card_parent,
            bg=CARD,
            highlightthickness=1,
            highlightbackground=BORDER
        )

        pic = tk.Canvas(
            card,
            height=CARD_IMG_H,
            bg="#183040",
            highlightthickness=0
        )
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
                pic.create_image(
                    0,
                    0,
                    image=photo,
                    anchor="nw"
                )
            else:
                emoji, colour = PLACEHOLDERS.get(
                    image_file,
                    ("🐉", "#1b2a3a")
                )

                pic.create_rectangle(
                    0, 0, w, CARD_IMG_H,
                    fill=colour,
                    outline=""
                )

                pic.create_text(
                    w // 2,
                    CARD_IMG_H // 2,
                    text=emoji,
                    font=("Arial", 44)
                )

            pic.create_rectangle(
                8, 8,
                8 + 8 * len(tag) + 14,
                26,
                fill="#0a0e13",
                outline="#444"
            )

            pic.create_text(
                15,
                17,
                text=tag,
                anchor="w",
                fill=TEXT,
                font=("Arial", 8)
            )

        pic.bind("<Configure>", draw_pic)

        tk.Label(
            card,
            text=name,
            font=("Georgia", 10, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(anchor="w", padx=8)

        tk.Label(
            card,
            text=description,
            font=("Arial", 8),
            bg=CARD,
            fg=LIGHT_TEXT,
            wraplength=175,
            justify="left"
        ).pack(anchor="w", padx=8, pady=(3, 6))

        bottom = tk.Frame(card, bg=CARD)
        bottom.pack(
            fill="x",
            padx=8,
            pady=(0, 8),
            side="bottom"
        )

        tk.Button(
            bottom,
            text="Read More →",
            font=("Arial", 8),
            bg="#0c1117",
            fg=TEXT,
            activebackground="#1c1a14",
            activeforeground=GOLD,
            highlightthickness=1,
            highlightbackground=GOLD_DARK,
            relief="flat",
            padx=8,
            command=lambda creature_name=name: read_creature(
                creature_name
            )
        ).pack(side="left")

        fav = tk.Button(
            bottom,
            text="♥" if name in favourites else "♡",
            font=("Arial", 13),
            bg=CARD,
            fg=GOLD if name in favourites else LIGHT_TEXT,
            activebackground=CARD,
            relief="flat",
            bd=0
        )

        fav.config(
            command=lambda creature_name=name, button=fav:
                toggle_favourite(creature_name, button)
        )

        fav.pack(side="right")

        return card

    # ==========================================
    # DRAW CARDS
    # ==========================================

    def draw_cards():
        for widget in grid.winfo_children():
            widget.destroy()

        query = search_entry.get().strip().lower()

        if query == "search creatures...":
            query = ""

        shown = [
            creature
            for creature in creatures
            if (
                state["type"] == "All"
                or creature[2] == state["type"]
            )
            and (
                state["region"] == "All"
                or creature[3] == state["region"]
            )
            and query in creature[0].lower()
        ]

        if not shown:
            tk.Label(
                grid,
                text="No creatures match. Try a different search or filter.",
                font=("Arial", 10),
                bg=BG,
                fg=LIGHT_TEXT
            ).grid(
                row=0,
                column=0,
                columnspan=4,
                pady=40
            )
            return

        for i, (
            name,
            tag,
            _type,
            _region,
            image_file,
            description
        ) in enumerate(shown):

            make_card(
                grid,
                name,
                tag,
                image_file,
                description
            ).grid(
                row=i // 4,
                column=i % 4,
                padx=4,
                pady=4,
                sticky="nsew"
            )

    # ==========================================
    # SEARCH EVENT
    # ==========================================

    search_entry.bind(
        "<KeyRelease>",
        lambda event: draw_cards()
    )

    # ==========================================
    # INITIAL DISPLAY
    # ==========================================

    draw_pills()
    draw_cards()

    return canvas
