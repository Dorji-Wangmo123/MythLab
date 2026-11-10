"""Reusable detail page for MythLab myth cards."""
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk, ImageOps

BG = "#061b2b"
CARD = "#0a2131"
GOLD = "#d6a84f"
LIGHT_GOLD = "#e5c875"
TEXT = "#f5ead0"
LIGHT_TEXT = "#c7c1b3"
BORDER = "#755d2d"
IMAGE_DIR = Path(__file__).resolve().parent / "assets"
_image_refs = []

MYTH_CONTENT = {
    "The Story of King Gesar": {
        "category": "Heroes", "origin": "Tibet", "image": "heroes.png",
        "subtitle": "A legendary hero celebrated across Tibetan and Himalayan traditions.",
        "story": "King Gesar of Ling is the central hero of a vast Tibetan epic tradition. He is remembered for courage, wisdom and his struggles against powerful forces that threaten ordinary people. Stories of Gesar have been passed down through oral performance, song and storytelling, and different communities preserve different versions.\n\nAlthough the epic is traditionally associated with Tibet, Gesar is also respected in Bhutan. In Bhutanese communities he is associated with protection and spiritual strength, and the Temple of Ling Gesar in Trongsa reflects this cultural and religious connection.\n\nThis is a short introduction to the tradition; it is not one single definitive version of the epic.",
        "facts": [("Traditional origin", "Tibet"), ("Known for", "Courage and protection"), ("Tradition", "Epic storytelling")],
        "note": 'The Gesar epic is part of a living oral tradition. Storytellers perform different episodes, and communities preserve their own versions. In Bhutan, references to Gesar and the Temple of Ling Gesar in Trongsa show how traditions travel across the Himalayan region. The story is therefore a regional cultural connection, while its best-known epic tradition is Tibetan.'
    },
    "The Yeti": {
        "category": "Creatures", "origin": "Himalayan region", "image": "yeti.png",
        "subtitle": "A mysterious being from stories of the high Himalayan mountains.",
        "story": "The Yeti is a mysterious, human-like being described in stories from the Himalayan region. It is often imagined as living in remote, snowy mountains, far from villages and busy paths.\n\nTravellers and mountain communities have shared tales of strange footprints, distant sounds and brief sightings. These accounts have helped make the Yeti one of the best-known mysteries of Himalayan folklore.\n\nThe Yeti belongs to traditional stories and popular legend; its existence has not been scientifically established.",
        "facts": [("Region", "Himalayas"), ("Type", "Legendary being"), ("Associated with", "Snowy mountains")],
        "note": 'The Yeti is an important figure in Himalayan folklore and reflects the mystery people associate with remote mountain environments. Stories describe unusual tracks or encounters, but these accounts belong to oral tradition and popular legend. There is no reliable scientific evidence confirming the Yeti as a real animal.'
    },
    "The Firebird": {
        "category": "Folklore", "origin": "Slavic folklore", "image": "firebird (1).png",
        "subtitle": "A magical bird from traditional tales of Eastern Europe.",
        "story": "The Firebird is a magical bird found in traditional Slavic fairy tales. It is usually described as glowing with brilliant golden or fiery feathers. In many versions, a single feather from the bird shines brightly and can lead a hero into an extraordinary adventure.\n\nA character who discovers the Firebird may be sent on a difficult quest. The journey tests courage, patience and cleverness, and the bird becomes a symbol of wonder and the unknown.\n\nThere are many versions of Firebird stories, so details differ between tellings. It is included in MythLab as a myth from beyond Bhutan.",
        "facts": [("Origin", "Slavic traditions"), ("Type", "Magical bird"), ("Theme", "Wonder and adventure")],
        "note": 'The Firebird comes from Slavic folklore in Eastern Europe. Its glowing feathers and magical role often represent wonder, hope and the beginning of a difficult journey. Including it in MythLab helps compare Bhutanese and Himalayan traditions with stories from other parts of the world.'
    },
    "The Black Mountain": {
        "category": "Folklore", "origin": "Bhutan", "image": "black_mountain (2).png",
        "subtitle": "A Bhutanese landscape associated with sacred stories and local belief.",
        "story": "The Black Mountain is associated with Bhutan's central mountain landscape and the traditional stories connected with sacred places. Mountains in Bhutan are often regarded with deep respect and may be linked in local belief with protective deities, spirits and sacred histories.\n\nStories connected with particular mountains can vary between communities. For MythLab, this entry introduces the cultural idea of sacred mountains and the importance of respecting local accounts. It should be expanded with a specific oral account or a reliable local source before being presented as one fixed legend.",
        "facts": [("Country", "Bhutan"), ("Type", "Sacred landscape"), ("Theme", "Nature and belief")],
        "note": 'In Bhutan, mountains can hold religious and cultural significance and may be connected with local protective deities, sacred sites and community stories. The name Black Mountain is also associated with the Black Mountains of central Bhutan. This entry is a general introduction rather than one verified legend; a specific local oral account should be added before attributing particular events or beliefs to the mountain.'
    },
    "The Snow Lion": {
        "category": "Creatures", "origin": "Himalayan Buddhist traditions", "image": "snow_lion.png",
        "subtitle": "A mythical symbol of strength, joy and spiritual qualities.",
        "story": "The Snow Lion is a mythical creature found in Himalayan and Tibetan Buddhist art and tradition. It is commonly shown as a powerful lion-like animal living among snowy mountains.\n\nThe Snow Lion is often associated with fearlessness, strength, joy and spiritual vitality. Its image appears in religious art, stories and cultural symbols across the Himalayan world.\n\nThe Snow Lion is a symbolic mythical being rather than an ordinary animal. Meanings and artistic styles can differ across regions and traditions.",
        "facts": [("Region", "Himalayan traditions"), ("Type", "Mythical creature"), ("Symbolises", "Fearlessness and joy")],
        "note": 'The Snow Lion is widely used in Himalayan and Tibetan Buddhist art, including religious imagery and cultural emblems. It commonly represents fearlessness, strength, joy and spiritual energy. Its meaning can vary with the context, and it is best understood as a symbolic mythical being rather than a zoological creature.'
    },
    "The Legend of Paro Taktsang": {
        "category": "Folklore", "origin": "Paro, Bhutan", "image": "paro_taktsang.png",
        "subtitle": "The sacred cliffside monastery linked with Guru Rinpoche.",
        "story": "Paro Taktsang, widely known as the Tiger's Nest, is one of Bhutan's most revered sacred sites. Bhutanese religious tradition connects the place with Guru Rinpoche (Padmasambhava), who is said to have travelled to the site in the eighth century.\n\nAccording to the traditional account, Guru Rinpoche arrived riding a tigress, meditated in a cave and helped establish the teachings of Buddhism in Bhutan. The monastery was later built on the cliffside near the sacred meditation caves.\n\nThe story is an important part of Bhutan's spiritual heritage. The site remains a place of pilgrimage and devotion.",
        "facts": [("Location", "Paro, Bhutan"), ("Also known as", "Tiger's Nest"), ("Associated with", "Guru Rinpoche")],
        "note": "Paro Taktsang is both a sacred place and an important part of Bhutan's religious heritage. The traditional account of Guru Rinpoche arriving on a tigress is a devotional story, not a claim tested like an ordinary historical event. Visitors are expected to respect the monastery, its sacred spaces and the religious practices carried out there."
    },
    "The Birth of the Universe": {
        "category": "Folklore", "origin": "Mythological theme", "image": "gods.png",
        "subtitle": "A collection-style introduction to traditional explanations of creation.",
        "story": "Many cultures preserve stories that explain how the universe, the earth and living beings came into existence. These creation stories describe beginnings through divine actions, natural forces, cosmic beings or transformations.\n\nThere is no single universal version of a story called 'The Birth of the Universe'. Different Bhutanese, Himalayan and other traditions have their own accounts, with distinct characters and meanings.\n\nThis MythLab entry is a general introduction. To make it a specific cultural story, the project should identify the particular tradition and source used for the account.",
        "facts": [("Type", "Creation theme"), ("Found in", "Many cultures"), ("Theme", "Origins of life")],
        "note": 'Creation stories help communities express how they understand beginnings, nature, life and the relationship between people and the sacred. Different cultures have different accounts, so this page does not present one version as universal. For a specific Bhutanese entry, MythLab should name the community or tradition and identify the source of the story.'
    }
}


def show_myth_detail(parent, back_command, name):
    """Display a myth's detail page inside the existing MythLab content frame."""
    global _image_refs
    for widget in parent.winfo_children():
        widget.destroy()
    _image_refs = []

    data = MYTH_CONTENT.get(name)
    if not data:
        tk.Label(parent, text=f"Story for {name} is not available yet.", bg=BG, fg=TEXT).pack(padx=30, pady=30)
        return

    canvas = tk.Canvas(parent, bg=BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    content = tk.Frame(canvas, bg=BG)
    window_id = canvas.create_window((0, 0), window=content, anchor="nw")
    content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfigure(window_id, width=e.width))

    page = tk.Frame(content, bg=BG)
    page.pack(fill="both", expand=True, padx=30, pady=24)

    tk.Button(page, text="←  Myths", command=back_command, bg=BG, fg=LIGHT_TEXT,
              activebackground=BG, activeforeground=GOLD, relief="flat", cursor="hand2").pack(anchor="w", pady=(0, 16))

    hero = tk.Frame(page, bg=BG)
    hero.pack(fill="x", pady=(0, 18))
    text_area = tk.Frame(hero, bg=BG)
    text_area.pack(side="left", fill="both", expand=True, padx=(0, 18))
    tk.Label(text_area, text=name, font=("Georgia", 26, "bold"), bg=BG, fg=GOLD,
             wraplength=560, justify="left").pack(anchor="w", pady=(5, 10))
    tk.Label(text_area, text=f" {data['category']} ", font=("Arial", 9, "bold"), bg="#1b3040", fg=TEXT).pack(anchor="w", pady=(0, 12))
    tk.Label(text_area, text=data["subtitle"], font=("Arial", 11), bg=BG, fg=TEXT,
             wraplength=560, justify="left").pack(anchor="w")
    tk.Label(text_area, text=f"ORIGIN  ·  {data['origin']}", font=("Arial", 9, "bold"), bg=BG, fg=LIGHT_GOLD).pack(anchor="w", pady=16)

    image_path = IMAGE_DIR / data["image"]
    try:
        if image_path.exists():
            im = Image.open(image_path).convert("RGB")
            im = ImageOps.fit(im, (390, 235), method=Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(im)
            _image_refs.append(photo)
            tk.Label(hero, image=photo, bg=BG).pack(side="right")
        else:
            tk.Label(hero, text="Image not found\n" + data["image"], bg=CARD, fg=LIGHT_TEXT,
                     width=28, height=10).pack(side="right")
    except Exception as exc:
        print("Myth image error:", exc)

    # Clickable section tabs. The selected section is highlighted.
    tabs = tk.Frame(page, bg="#0b2535")
    tabs.pack(fill="x", pady=(0, 16))
    section_container = tk.Frame(page, bg=BG, height=380)
    section_container.pack(fill="both", expand=True)
    # Frames managed by grid/place do not contribute their requested size.
    # Give this area a real height so its content remains visible in the Canvas.
    section_container.pack_propagate(False)
    section_container.grid_rowconfigure(0, weight=1)
    section_container.grid_columnconfigure(0, weight=1)
    tab_buttons = {}
    section_pages = {}

    # Overview: a short introduction and key facts.
    overview_page = tk.Frame(section_container, bg=BG)
    overview_page.grid(row=0, column=0, sticky="nsew")
    overview_columns = tk.Frame(overview_page, bg=BG)
    overview_columns.pack(fill="both", expand=True)
    overview_left = tk.Frame(overview_columns, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
    overview_left.pack(side="left", fill="both", expand=True, padx=(0, 14))
    tk.Label(overview_left, text="Overview", font=("Georgia", 16, "bold"), bg=CARD, fg=GOLD).pack(anchor="w", padx=20, pady=(18, 12))
    overview_text = data["subtitle"] + "\n\n" + data["story"].split("\n\n")[0]
    tk.Label(overview_left, text=overview_text, font=("Arial", 10), bg=CARD, fg=TEXT,
             justify="left", anchor="nw", wraplength=650).pack(fill="both", expand=True, padx=20, pady=(0, 20))
    overview_right = tk.Frame(overview_columns, bg=CARD, width=270, highlightbackground=BORDER, highlightthickness=1)
    overview_right.pack(side="right", fill="y")
    overview_right.pack_propagate(False)
    tk.Label(overview_right, text="Key Facts", font=("Georgia", 14, "bold"), bg=CARD, fg=GOLD).pack(anchor="w", padx=16, pady=(18, 12))
    for label, value in data["facts"]:
        tk.Label(overview_right, text=label.upper(), font=("Arial", 8), bg=CARD, fg=LIGHT_TEXT).pack(anchor="w", padx=16, pady=(8, 1))
        tk.Label(overview_right, text=value, font=("Arial", 10, "bold"), bg=CARD, fg=TEXT,
                 wraplength=230, justify="left").pack(anchor="w", padx=16)
    section_pages["Overview"] = overview_page

    def add_text_page(tab_name, heading, body):
        frame = tk.Frame(section_container, bg=BG)
        frame.grid(row=0, column=0, sticky="nsew")
        card = tk.Frame(frame, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="both", expand=True)
        tk.Label(card, text=heading, font=("Georgia", 16, "bold"), bg=CARD, fg=GOLD).pack(anchor="w", padx=22, pady=(20, 12))
        tk.Label(card, text=body, font=("Arial", 10), bg=CARD, fg=TEXT, justify="left", anchor="nw",
                 wraplength=900).pack(fill="both", expand=True, anchor="nw", padx=22, pady=(0, 24))
        section_pages[tab_name] = frame

    add_text_page("Story", "The Story", data["story"])
    add_text_page("Cultural Note", "Cultural Note", data["note"])

    def show_section(selected):
        # Raise the selected page instead of repeatedly packing/unpacking it.
        # This keeps tab switching reliable inside the scrollable Canvas.
        section_pages[selected].tkraise()
        for tab_name, button in tab_buttons.items():
            active = tab_name == selected
            button.configure(font=("Arial", 9, "bold" if active else "normal"),
                             bg=GOLD if active else "#0b2535", fg=BG if active else TEXT)

    for tab in ("Overview", "Story", "Cultural Note"):
        button = tk.Button(tabs, text=tab,
            font=("Arial", 9, "bold" if tab == "Overview" else "normal"),
            bg=GOLD if tab == "Overview" else "#0b2535", fg=BG if tab == "Overview" else TEXT,
            activebackground=GOLD, activeforeground=BG, relief="flat", padx=20, pady=10,
            cursor="hand2", command=lambda t=tab: show_section(t))
        button.pack(side="left")
        tab_buttons[tab] = button
    show_section("Overview")
