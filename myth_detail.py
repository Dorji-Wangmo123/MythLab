
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk, ImageOps

# ============================================================
# MYTHLAB - SHARED MYTH DETAIL PAGE
# ============================================================

BG = "#061b2b"
CARD = "#0a2131"
GOLD = "#d6a84f"
LIGHT_GOLD = "#e5c875"
TEXT = "#f5ead0"
LIGHT_TEXT = "#c7c1b3"
BORDER = "#755d2d"

PROJECT_DIR = Path(__file__).resolve().parent
IMAGE_DIR = PROJECT_DIR / "assets"

_image_refs = []

# ============================================================
# MYTH CONTENT
# Add or edit stories here.
# Creature stories are added by creature.py.
# ============================================================

MYTH_CONTENT = {

    "Ap Chhundu": {
        "category": "Deity",
        "origin": "Haa Valley, Bhutan",
        "image": "ap_chhundu.jpg",
        "subtitle": "The protective guardian deity of Haa Valley.",
        "story": (
            "Ap Chhundu is widely revered as a guardian deity of Haa "
            "Valley in Bhutan. Local traditions describe him as a "
            "powerful protector who watches over the valley and its "
            "people.\n\n"
            "People have traditionally prayed to Ap Chhundu for "
            "protection, well-being, and peace. His presence is closely "
            "connected with the cultural and spiritual identity of Haa."
        ),
        "facts": [
            ("Origin", "Haa Valley, Bhutan"),
            ("Type", "Guardian deity"),
            ("Role", "Protector of the valley")
        ],
        "note": (
            "Ap Chhundu reflects the importance of local guardian "
            "deities in Bhutanese culture and community traditions."
        )
    },

    "Ap Genyen Domtshang": {
        "category": "Deity",
        "origin": "Bhutan",
        "image": "ap_genyen_domtshang.jpg",
        "subtitle": "A guardian spirit associated with Bhutanese tradition.",
        "story": (
            "Ap Genyen Domtshang is remembered in Bhutanese local "
            "traditions as a protective spiritual figure. Stories "
            "about guardian deities are often passed down through "
            "families and communities.\n\n"
            "Such figures are traditionally respected because they "
            "are believed to protect particular places and the people "
            "who live there."
        ),
        "facts": [
            ("Origin", "Bhutan"),
            ("Type", "Guardian spirit"),
            ("Role", "Protection and guidance")
        ],
        "note": (
            "The tradition reflects the close relationship between "
            "spiritual beliefs, local communities, and the landscape."
        )
    },

    "Jomo": {
        "category": "Deity",
        "origin": "Bhutan and Himalayan region",
        "image": "jomo.jpg",
        "subtitle": "A sacred female mountain deity in Himalayan traditions.",
        "story": (
            "Jomo is a name associated with female protective deities "
            "in Bhutanese and Himalayan traditions. Some mountains "
            "are regarded as sacred places and are believed to be "
            "the homes of powerful spiritual beings.\n\n"
            "People living near these mountains may show respect "
            "through prayers, offerings, and local religious customs. "
            "These beliefs connect the spiritual world with the "
            "natural environment."
        ),
        "facts": [
            ("Region", "Bhutan and Himalayan region"),
            ("Type", "Mountain deity"),
            ("Association", "Sacred mountains and protection")
        ],
        "note": (
            "Jomo traditions show how mountains are respected not "
            "only as natural landmarks but also as sacred places."
        )
    },

    "Guru Rinpoche": {
        "category": "Religious Figure",
        "origin": "India and Bhutan",
        "image": "guru.jpg",
        "subtitle": "The great Buddhist master who brought Vajrayana Buddhism to Bhutan.",
        "story": (
            "Guru Rinpoche, also known as Padmasambhava, is one of "
            "the most important figures in Bhutanese Buddhist "
            "tradition. According to religious accounts, he travelled "
            "to Bhutan in the eighth century and helped establish "
            "Buddhism in the region.\n\n"
            "One of the best-known traditions tells of his meditation "
            "at Paro Taktsang, also known as the Tiger's Nest. He is "
            "believed to have subdued harmful forces and helped spread "
            "Buddhist teachings throughout the Himalayan region."
        ),
        "facts": [
            ("Name", "Padmasambhava"),
            ("Period", "Traditionally associated with the 8th century"),
            ("Importance", "Spread of Vajrayana Buddhism")
        ],
        "note": (
            "Guru Rinpoche holds a central place in Bhutanese "
            "religious life, festivals, art, and cultural heritage."
        )
    },

    "Yeshey Gonpo": {
        "category": "Deity",
        "origin": "Bhutan and Tibetan Buddhist tradition",
        "image": "yeshey_gonpo.jpg",
        "subtitle": "A powerful protective deity also known as Mahakala.",
        "story": (
            "Yeshey Gonpo is associated with Mahakala, a protective "
            "deity in Vajrayana Buddhism. He is often represented "
            "with a fierce appearance to symbolize the power to "
            "overcome obstacles and protect Buddhist teachings.\n\n"
            "In Bhutan, protective deities have an important place "
            "in religious practices. They are honoured through "
            "prayers, rituals, and religious ceremonies."
        ),
        "facts": [
            ("Other name", "Mahakala"),
            ("Type", "Protective deity"),
            ("Association", "Protection of Buddhist teachings")
        ],
        "note": (
            "Yeshey Gonpo represents spiritual protection and the "
            "overcoming of obstacles."
        )
    },

    "Drukpa Kunley": {
        "category": "Historical Religious Figure",
        "origin": "Tibet and Bhutan",
        "image": "drukpa_kuenley.jpg",
        "subtitle": "The Divine Madman known for his unusual teaching methods.",
        "story": (
            "Drukpa Kunley, popularly known as the Divine Madman, "
            "was a Buddhist teacher whose life became part of many "
            "stories in Bhutan.\n\n"
            "Unlike conventional religious teachers, he was known "
            "for his unconventional behaviour, humour, and unusual "
            "ways of sharing spiritual lessons. Many stories about "
            "him use jokes and surprising situations to communicate "
            "ideas about wisdom, pride, and human behaviour."
        ),
        "facts": [
            ("Known as", "The Divine Madman"),
            ("Region", "Tibet and Bhutan"),
            ("Known for", "Unconventional teachings and humour")
        ],
        "note": (
            "His stories remain an important part of Bhutanese "
            "folklore and are often used to share moral and spiritual lessons."
        )
    },

    "The Black Mountain": {
        "category": "Legend",
        "origin": "Central Bhutan",
        "image": "black_mountain (2).png",
        "subtitle": "A legendary mountain landscape associated with mystery and local beliefs.",
        "story": (
            "The Black Mountains are an important part of Bhutan's "
            "central landscape. Mountains in Bhutan are often linked "
            "with local legends, sacred places, and spiritual beliefs.\n\n"
            "Stories connected with mountain areas reflect the "
            "mystery of the natural world and the respect people "
            "have traditionally shown towards the environment."
        ),
        "facts": [
            ("Location", "Central Bhutan"),
            ("Type", "Landscape legend"),
            ("Association", "Mountains and local traditions")
        ],
        "note": (
            "The story highlights the cultural importance of "
            "Bhutan's mountains and the traditions connected to them."
        )
    },

    "Paro Taktsang": {
        "category": "Sacred Legend",
        "origin": "Paro, Bhutan",
        "image": "paro_taktsang.png",
        "subtitle": "The sacred Tiger's Nest monastery built on a cliff.",
        "story": (
            "Paro Taktsang, popularly known as the Tiger's Nest, "
            "is one of Bhutan's most famous sacred sites. According "
            "to tradition, Guru Rinpoche travelled to this location "
            "on the back of a tigress.\n\n"
            "He is believed to have meditated in a cave there and "
            "helped subdue harmful spiritual forces. The monastery "
            "was later built around the sacred site and became "
            "an important place of pilgrimage."
        ),
        "facts": [
            ("Location", "Paro, Bhutan"),
            ("Also known as", "Tiger's Nest"),
            ("Association", "Guru Rinpoche")
        ],
        "note": (
            "Paro Taktsang is one of Bhutan's most treasured "
            "religious and cultural landmarks."
        )
    },

    "Dochula": {
        "category": "Historical and Cultural Legend",
        "origin": "Dochula Pass, Bhutan",
        "image": "dochula.jpg",
        "subtitle": "A mountain pass known for its 108 memorial chortens.",
        "story": (
            "Dochula Pass is a well-known mountain pass between "
            "Thimphu and Punakha. It is especially recognised for "
            "the 108 Druk Wangyal Chortens built on the hillside.\n\n"
            "The site is a place of remembrance and reflection. "
            "Surrounded by mountain scenery, it has become an "
            "important landmark for visitors and local people."
        ),
        "facts": [
            ("Location", "Dochula Pass, Bhutan"),
            ("Known for", "108 Druk Wangyal Chortens"),
            ("Type", "Cultural landmark")
        ],
        "note": (
            "Dochula represents remembrance, national identity, "
            "and Bhutan's cultural heritage."
        )
    },

    "Tshomen Lu": {
        "category": "Water Spirit",
        "origin": "Bhutan and Himalayan folklore",
        "image": "tshomen_lu.jpg",
        "subtitle": "A supernatural water being from Himalayan traditions.",
        "story": (
            "In Bhutanese and Himalayan folklore, Lu are supernatural "
            "beings associated with water, lakes, rivers, and the "
            "natural environment. Tshomen is commonly associated "
            "with female water spirits.\n\n"
            "Traditional stories describe these beings as powerful "
            "and deserving of respect. People have often connected "
            "water spirits with the protection and balance of "
            "natural water sources."
        ),
        "facts": [
            ("Region", "Bhutan and Himalayan region"),
            ("Type", "Water spirit"),
            ("Association", "Lakes, rivers, and water")
        ],
        "note": (
            "These stories encourage respect for water and the "
            "natural environment."
        )
    },

    "The Thunder Dragon": {
        "category": "National Symbol",
        "origin": "Bhutan",
        "image": "thunder_dragon.png",
        "subtitle": "The Druk, the legendary Thunder Dragon of Bhutan.",
        "story": (
            "The Thunder Dragon, known as Druk, is one of the most "
            "recognisable symbols of Bhutan. In Bhutanese tradition, "
            "the sound of thunder is sometimes associated with "
            "the roar of a powerful dragon.\n\n"
            "The dragon appears on Bhutan's national flag and is "
            "closely connected with the country's name, Druk Yul, "
            "meaning the Land of the Thunder Dragon."
        ),
        "facts": [
            ("Local name", "Druk"),
            ("Country", "Bhutan"),
            ("Symbolises", "Strength and protection")
        ],
        "note": (
            "The Thunder Dragon is an important national and "
            "cultural symbol of Bhutan."
        )
    },

    "Heroes": {
        "category": "Folklore",
        "origin": "Bhutan",
        "image": "heroes.png",
        "subtitle": "Stories of courage and bravery passed down through generations.",
        "story": (
            "Stories of heroes are an important part of oral "
            "traditions. They often describe people who demonstrate "
            "courage, wisdom, kindness, and determination when "
            "facing difficult situations.\n\n"
            "These stories are shared across generations to teach "
            "important values and remind listeners that bravery "
            "can be shown through both great actions and everyday choices."
        ),
        "facts": [
            ("Region", "Bhutan"),
            ("Type", "Heroic folklore"),
            ("Themes", "Courage, wisdom, and kindness")
        ],
        "note": (
            "Hero stories preserve traditional values and provide "
            "lessons for younger generations."
        )
    },

    "Gods": {
        "category": "Mythology",
        "origin": "Bhutan and Himalayan Buddhist tradition",
        "image": "gods.png",
        "subtitle": "Divine beings represented in Bhutanese religious traditions.",
        "story": (
            "Bhutanese religious traditions include many divine "
            "and protective beings. They are represented in "
            "religious paintings, statues, temples, and sacred "
            "stories.\n\n"
            "Different deities are associated with protection, "
            "wisdom, compassion, and the overcoming of obstacles. "
            "Their stories form an important part of the country's "
            "religious and cultural heritage."
        ),
        "facts": [
            ("Region", "Bhutan and Himalayan region"),
            ("Type", "Religious mythology"),
            ("Themes", "Protection, wisdom, and compassion")
        ],
        "note": (
            "These traditions reflect the importance of Buddhist "
            "beliefs and religious art in Bhutanese culture."
        )
    }
}


# ============================================================
# IMAGE HELPER
# ============================================================

def find_image(filename):
    if not filename:
        return None

    direct = IMAGE_DIR / filename
    if direct.exists():
        return direct

    direct = PROJECT_DIR / filename
    if direct.exists():
        return direct

    target = "".join(
        ch for ch in Path(filename).stem.lower()
        if ch.isalnum()
    )

    folders = [IMAGE_DIR, PROJECT_DIR]

    for folder in folders:
        if not folder.exists():
            continue

        for item in folder.iterdir():
            if not item.is_file():
                continue

            if item.suffix.lower() not in {
                ".png", ".jpg", ".jpeg", ".webp"
            }:
                continue

            stem = "".join(
                ch for ch in item.stem.lower()
                if ch.isalnum()
            )

            if stem == target:
                return item

    return None


def load_detail_image(filename, size):
    path = find_image(filename)

    if path is None:
        print("DETAIL IMAGE NOT FOUND:", filename)
        return None

    try:
        image = Image.open(path).convert("RGB")
        image = ImageOps.fit(
            image,
            size,
            method=Image.Resampling.LANCZOS
        )
        return ImageTk.PhotoImage(image)

    except Exception as error:
        print("Could not load detail image:", error)
        return None


# ============================================================
# CLEAR PARENT
# ============================================================

def clear_parent(parent):
    for widget in parent.winfo_children():
        widget.destroy()


# ============================================================
# SHARED MYTH DETAIL PAGE
# ============================================================

def show_myth_detail(parent, back_command, name):

    clear_parent(parent)
    _image_refs.clear()

    data = MYTH_CONTENT.get(name)

    if data is None:
        message = tk.Frame(parent, bg=BG)
        message.pack(fill="both", expand=True)

        tk.Button(
            message,
            text="←  Back",
            command=back_command,
            bg=CARD,
            fg=GOLD,
            relief="flat",
            font=("Arial", 10)
        ).pack(anchor="w", padx=30, pady=25)

        tk.Label(
            message,
            text="Story not found",
            bg=BG,
            fg=TEXT,
            font=("Georgia", 22, "bold")
        ).pack(pady=30)

        tk.Label(
            message,
            text=f"No story has been added for: {name}",
            bg=BG,
            fg=LIGHT_TEXT,
            font=("Arial", 11)
        ).pack()

        print("MYTH DETAIL NOT FOUND:", name)
        return

    # Scrollable page
    page = tk.Frame(parent, bg=BG)
    page.pack(fill="both", expand=True)

    canvas = tk.Canvas(
        page,
        bg=BG,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        page,
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

    content.bind(
        "<Configure>",
        lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.bind(
        "<Configure>",
        lambda event: canvas.itemconfigure(
            window_id,
            width=event.width
        )
    )

    # Back button
    tk.Button(
        content,
        text="←  Myths",
        command=back_command,
        font=("Arial", 10, "bold"),
        bg=BG,
        fg=GOLD,
        activebackground=BG,
        activeforeground=LIGHT_GOLD,
        relief="flat",
        cursor="hand2"
    ).pack(anchor="w", padx=40, pady=(25, 12))

    # Heading section
    heading = tk.Frame(content, bg=BG)
    heading.pack(fill="x", padx=40, pady=(5, 20))

    heading.columnconfigure(0, weight=3)
    heading.columnconfigure(1, weight=2)

    left = tk.Frame(heading, bg=BG)
    left.grid(row=0, column=0, sticky="nsew", padx=(0, 25))

    tk.Label(
        left,
        text=data.get("category", "Myth"),
        bg=CARD,
        fg=GOLD,
        font=("Arial", 9, "bold"),
        padx=12,
        pady=5
    ).pack(anchor="w", pady=(5, 12))

    tk.Label(
        left,
        text=name,
        bg=BG,
        fg=TEXT,
        font=("Georgia", 27, "bold"),
        wraplength=550,
        justify="left"
    ).pack(anchor="w", pady=(0, 12))

    tk.Label(
        left,
        text=data.get("subtitle", ""),
        bg=BG,
        fg=LIGHT_TEXT,
        font=("Arial", 11),
        wraplength=520,
        justify="left"
    ).pack(anchor="w", pady=(0, 18))

    tk.Label(
        left,
        text="ORIGIN",
        bg=BG,
        fg=GOLD,
        font=("Arial", 9, "bold")
    ).pack(anchor="w")

    tk.Label(
        left,
        text=data.get("origin", "Unknown"),
        bg=BG,
        fg=TEXT,
        font=("Arial", 11)
    ).pack(anchor="w", pady=(5, 0))

    # Image
    image_frame = tk.Frame(
        heading,
        bg=CARD,
        highlightthickness=1,
        highlightbackground=BORDER
    )
    image_frame.grid(row=0, column=1, sticky="nsew")

    photo = load_detail_image(
        data.get("image"),
        (420, 260)
    )

    if photo:
        _image_refs.append(photo)

        image_label = tk.Label(
            image_frame,
            image=photo,
            bg=CARD
        )
        image_label.pack(fill="both", expand=True)
        image_label.image = photo
    else:
        tk.Label(
            image_frame,
            text="MythLab",
            bg=CARD,
            fg=GOLD,
            font=("Georgia", 22, "bold"),
            height=8
        ).pack(fill="both", expand=True)

    # Divider
    tk.Frame(
        content,
        bg=BORDER,
        height=1
    ).pack(fill="x", padx=40, pady=(5, 20))

    # Overview section
    tk.Label(
        content,
        text="Overview",
        bg=BG,
        fg=GOLD,
        font=("Georgia", 18, "bold")
    ).pack(anchor="w", padx=40, pady=(0, 10))

    overview_text = data.get("story", "")

    tk.Label(
        content,
        text=overview_text,
        bg=CARD,
        fg=TEXT,
        font=("Arial", 11),
        justify="left",
        anchor="nw",
        wraplength=1050,
        padx=22,
        pady=20
    ).pack(fill="x", padx=40, pady=(0, 25))

    # Lower two-column section
    lower = tk.Frame(content, bg=BG)
    lower.pack(fill="x", padx=40, pady=(0, 35))

    lower.columnconfigure(0, weight=3)
    lower.columnconfigure(1, weight=2)

    # Key facts
    facts_card = tk.Frame(
        lower,
        bg=CARD,
        highlightthickness=1,
        highlightbackground=BORDER
    )
    facts_card.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=(0, 12)
    )

    tk.Label(
        facts_card,
        text="Key Facts",
        bg=CARD,
        fg=GOLD,
        font=("Georgia", 15, "bold")
    ).pack(anchor="w", padx=18, pady=(18, 12))

    for label, value in data.get("facts", []):
        fact_row = tk.Frame(facts_card, bg=CARD)
        fact_row.pack(fill="x", padx=18, pady=7)

        tk.Label(
            fact_row,
            text=label,
            bg=CARD,
            fg=LIGHT_TEXT,
            font=("Arial", 10, "bold"),
            width=19,
            anchor="nw"
        ).pack(side="left")

        tk.Label(
            fact_row,
            text=value,
            bg=CARD,
            fg=TEXT,
            font=("Arial", 10),
            wraplength=300,
            justify="left",
            anchor="nw"
        ).pack(side="left", fill="x", expand=True)

    # Cultural note
    note_card = tk.Frame(
        lower,
        bg=CARD,
        highlightthickness=1,
        highlightbackground=BORDER
    )
    note_card.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=(12, 0)
    )

    tk.Label(
        note_card,
        text="Cultural Significance",
        bg=CARD,
        fg=GOLD,
        font=("Georgia", 15, "bold")
    ).pack(anchor="w", padx=18, pady=(18, 12))

    tk.Label(
        note_card,
        text=data.get("note", ""),
        bg=CARD,
        fg=TEXT,
        font=("Arial", 10),
        wraplength=330,
        justify="left",
        anchor="nw"
    ).pack(fill="x", padx=18, pady=(0, 20))

    # Bottom back button
    tk.Button(
        content,
        text="←  Back to Myths",
        command=back_command,
        font=("Arial", 10, "bold"),
        bg=CARD,
        fg=GOLD,
        activebackground=GOLD,
        activeforeground=BG,
        relief="flat",
        padx=18,
        pady=9,
        cursor="hand2"
    ).pack(anchor="w", padx=40, pady=(0, 35))

    return page
