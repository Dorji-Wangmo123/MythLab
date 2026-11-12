
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk, ImageOps
import customtkinter as ctk

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



# Additional entries for titles used on the Myths page.
MYTH_CONTENT.update({
    "Genyen Jagpa Melen": {
        "category": "Guardian Deity", "origin": "Thimphu, Bhutan",
        "image": "genyen_jagpa_melen.jpg",
        "subtitle": "A guardian deity associated with Dechenphu Lhakhang.",
        "overview": "Genyen Jagpa Melen is revered as a protective deity in Bhutanese religious tradition, especially in connection with Dechenphu Lhakhang near Thimphu.",
        "story": "Dechenphu Lhakhang is a place of worship associated with the guardian deity Genyen Jagpa Melen. Devotees visit the sacred site to offer prayers and seek blessings.\n\nIn local religious tradition, guardian deities are understood to protect particular places and the communities connected to them. The traditions surrounding Genyen Jagpa Melen are passed on through worship, local accounts and the practices of devotees.\n\nThis introduction describes the deity's place in the tradition; a longer narrative should be added from a documented local account rather than invented as an authentic legend.",
        "cultural_significance": "The deity is connected with the religious heritage of Dechenphu Lhakhang and with Bhutanese traditions of honouring local protectors.",
        "facts": [("Associated site", "Dechenphu Lhakhang"), ("Region", "Thimphu, Bhutan"), ("Type", "Guardian deity")]
    },
    "The Story of King Gesar": {
        "category": "Hero", "origin": "Tibetan and Himalayan epic tradition",
        "image": "heroes.png",
        "subtitle": "A celebrated hero of the epic of Gesar.",
        "overview": "King Gesar is the central hero of a vast oral epic told in different forms across Tibetan and Himalayan communities.",
        "story": "The Epic of King Gesar follows a heroic ruler whose adventures are remembered through generations of oral storytelling. In many versions, Gesar comes to lead the kingdom of Ling and faces challenges that test his courage, judgement and responsibilities as a leader.\n\nThe epic includes journeys, contests and encounters with powerful opponents. Storytellers have preserved different episodes and local variations, so there is no single short version that represents every tradition.\n\nThrough his adventures, Gesar is celebrated for protecting his people and overcoming adversity. The stories also explore leadership, loyalty and the consequences of human choices.\n\nThis is a brief introduction to the epic, not a complete translation or a claim that all versions tell the same events.",
        "cultural_significance": "The Gesar epic is an important living oral tradition. Its many versions demonstrate the role of storytellers in preserving language, cultural memory and shared values.",
        "facts": [("Tradition", "Himalayan oral epic"), ("Hero", "King Gesar of Ling"), ("Themes", "Leadership, courage and duty")]
    },
    "The Yeti": {
        "category": "Creature", "origin": "Himalayan folklore", "image": "yeti.png",
        "subtitle": "A mysterious mountain being of Himalayan storytelling.",
        "story": "Stories of the Yeti describe a mysterious being believed by some storytellers to inhabit remote Himalayan mountain areas. Accounts differ from place to place and often reflect the uncertainty and wonder of the high mountains.\n\nThe Yeti remains a figure of folklore rather than a scientifically established species.",
        "note": "Yeti stories reflect the imagination and oral traditions of Himalayan communities.",
        "facts": [("Region", "Himalayas"), ("Type", "Folklore creature")]
    },
    "The Snow Lion": {
        "category": "Creature", "origin": "Himalayan Buddhist traditions", "image": "snow_lion.png",
        "subtitle": "A symbolic creature of the snowy mountains.",
        "story": "The Snow Lion appears in Himalayan art and symbolic traditions. It is often portrayed as a lively, powerful white creature associated with the high mountains.\n\nIts image conveys spiritual qualities rather than representing a documented animal species.",
        "note": "The Snow Lion is a recognised symbolic figure in Himalayan cultural and religious imagery.",
        "facts": [("Region", "Himalayas"), ("Type", "Symbolic creature")]
    },
    "The Firebird": {
        "category": "Folklore", "origin": "Slavic folklore", "image": "firebird (1).png",
        "subtitle": "A glowing bird from Slavic fairy tales.",
        "story": "In Slavic fairy tales, the Firebird is a wondrous bird whose glowing feathers attract the attention of those who encounter it. Heroes may be sent to search for the bird, setting off journeys filled with difficult choices and magical events.\n\nDifferent tales tell different adventures involving the Firebird.",
        "note": "The Firebird belongs to Slavic folklore and should not be presented as a traditional Bhutanese legend.",
        "facts": [("Origin", "Slavic folklore"), ("Type", "Magical bird")]
    },
    "The Birth of the Universe": {
        "category": "Folklore", "origin": "Multiple world traditions", "image": "gods.png",
        "subtitle": "How different traditions explain beginnings.",
        "story": "Across the world, communities have told stories about how the universe began. Some describe the world emerging from darkness, water or a cosmic being; others explain creation through sacred teachings.\n\nThere is no single universal traditional story. A specific culture's version should be identified before presenting a detailed account.",
        "note": "Creation narratives vary widely and should be attributed to the communities and traditions from which they come.",
        "facts": [("Theme", "Origins"), ("Tradition", "Varies by culture")]
    },
    "The Demoness of Dochula": {
        "category": "Folklore", "origin": "Bhutan", "image": "dochula.jpg",
        "subtitle": "A Bhutanese legend associated with spiritual transformation.",
        "story": "Bhutanese oral traditions contain accounts of spiritual teachers confronting harmful forces and transforming places into sites of practice and devotion. Stories associated with Drukpa Kunley have multiple local retellings.\n\nA precise account of the Demoness of Dochula should be drawn from a documented version of that particular legend; this page currently provides an introduction rather than inventing an episode.",
        "note": "Local variants and place names should be verified with a reliable Bhutanese source.",
        "facts": [("Region", "Bhutan"), ("Type", "Local legend")]
    },
    "The Man Saved by a Dragon": {
        "category": "Folklore", "origin": "Bhutan (project classification)",
        "image": "thunder_dragon.png",
        "subtitle": "A story of rescue and the mysterious dragon.",
        "story": "This title refers to a story of a person rescued by a dragon. The source narrative is not included in the existing story data, so a detailed traditional account cannot yet be verified.\n\nOnce the original account is supplied, it can be presented here in the same story layout without changing the design.",
        "note": "This entry needs a documented story source before it can be described as an authentic traditional account.",
        "facts": [("Type", "Dragon legend"), ("Story status", "Original narrative needed")]
    }
})

# Match alternative card titles to the same detailed entries.
MYTH_CONTENT["Jomo (Aum Jomo)"] = dict(MYTH_CONTENT["Jomo"])
MYTH_CONTENT["The Legend of Paro Taktsang"] = dict(MYTH_CONTENT["Paro Taktsang"])
MYTH_CONTENT["Tshomen and Lu"] = dict(MYTH_CONTENT["Tshomen Lu"])

# Correct images that actually exist in the original assets folder.
MYTH_CONTENT["Guru Rinpoche"]["image"] = "guru_rinpocheo.jpg"
MYTH_CONTENT["Ap Genyen Domtshang"]["image"] = "ap_genyen_domtshang.jpg"
MYTH_CONTENT["Yeshey Gonpo"]["image"] = "yeshey_gonpo.jpg"

# Preserve existing cultural notes while making all entries use consistent keys.
for _title, _entry in MYTH_CONTENT.items():
    _entry.setdefault("overview", _entry.get("subtitle", ""))
    _entry.setdefault("cultural_significance", _entry.get("note", ""))


# ============================================================
# IMAGE HELPERS
# ============================================================

def find_image(filename):
    """Find an image in assets, accepting different extensions."""
    if not filename:
        return None
    folders = (IMAGE_DIR, PROJECT_DIR, PROJECT_DIR / "images")
    filename_path = Path(filename)
    for folder in folders:
        exact = folder / filename
        if exact.is_file():
            return exact
    target = "".join(c.lower() for c in filename_path.stem if c.isalnum())
    for folder in folders:
        if not folder.is_dir():
            continue
        for candidate in folder.iterdir():
            if candidate.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
                continue
            stem = "".join(c.lower() for c in candidate.stem if c.isalnum())
            if stem == target:
                return candidate
    return None


def load_detail_image(filename, size):
    """Resize proportionally, returning an image without empty padding."""
    path = find_image(filename)
    if not path:
        print("DETAIL IMAGE NOT FOUND:", filename)
        return None
    try:
        with Image.open(path) as original:
            image = original.convert("RGB")
        image = ImageOps.contain(image, size, method=Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as error:
        print("DETAIL IMAGE ERROR:", filename, error)
        return None


def clear_parent(parent):
    for child in parent.winfo_children():
        child.destroy()


# ============================================================
# SHARED STORY PAGE WITH ROUNDED TABS
# ============================================================

def show_myth_detail(parent, back_command, name):
    clear_parent(parent)
    _image_refs.clear()
    data = MYTH_CONTENT.get(name)

    root = tk.Frame(parent, bg=BG)
    root.pack(fill="both", expand=True)

    # Keep the back arrow visible while reading and scrolling.
    top = tk.Frame(root, bg=BG)
    top.pack(fill="x", padx=26, pady=(12, 8))
    ctk.CTkButton(
        top, text="←  Back", command=back_command,
        fg_color="transparent", hover_color=CARD,
        text_color=GOLD, corner_radius=12,
        font=("Segoe UI", 13, "bold"), width=105, height=35
    ).pack(side="left")

    if data is None:
        tk.Label(root, text="Story not found: " + name, bg=BG, fg=TEXT,
                 font=("Georgia", 20, "bold")).pack(pady=45)
        return root

    outer = tk.Frame(root, bg=BG)
    outer.pack(fill="both", expand=True)
    canvas = tk.Canvas(outer, bg=BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    content = tk.Frame(canvas, bg=BG)
    window = canvas.create_window((0, 0), window=content, anchor="nw")
    content.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda event: canvas.itemconfigure(window, width=event.width))

    def wheel(event):
        if getattr(event, "num", None) == 4:
            direction = -1
        elif getattr(event, "num", None) == 5:
            direction = 1
        else:
            direction = -1 if event.delta > 0 else 1
        canvas.yview_scroll(direction, "units")

    # Bind only to this page, not to unrelated application pages.
    def bind_wheel(event):
        canvas.bind_all("<MouseWheel>", wheel)
        canvas.bind_all("<Button-4>", wheel)
        canvas.bind_all("<Button-5>", wheel)

    def unbind_wheel(event):
        canvas.unbind_all("<MouseWheel>")
        canvas.unbind_all("<Button-4>")
        canvas.unbind_all("<Button-5>")

    canvas.bind("<Enter>", bind_wheel)
    canvas.bind("<Leave>", unbind_wheel)

    heading = tk.Frame(content, bg=BG)
    heading.pack(fill="x", padx=28, pady=(15, 15))
    # Keep a stable ID without changing existing story data.
    story_id = data.get("id")
    if not story_id:
        story_id = "MYT-{:03d}".format(list(MYTH_CONTENT).index(name) + 1)
    tk.Label(heading, text=story_id, bg=BG, fg=GOLD,
             font=("Segoe UI", 10, "bold")).pack(anchor="w")
    tk.Label(heading, text=name, bg=BG, fg=TEXT,
             font=("Georgia", 29, "bold"), anchor="w", justify="left",
             wraplength=840).pack(fill="x", pady=(9, 8))
    tk.Label(heading, text=data.get("subtitle", ""), bg=BG, fg=LIGHT_TEXT,
             font=("Segoe UI", 11), anchor="w", justify="left",
             wraplength=840).pack(fill="x")
    tk.Label(heading, text=data.get("category", "Myth") + "  •  " + data.get("origin", ""),
             bg=BG, fg=GOLD, font=("Segoe UI", 10), anchor="w").pack(fill="x", pady=(12, 0))

    # The rounded border follows each image's actual proportions.
    image_outer = tk.Frame(content, bg=BG)
    image_outer.pack(fill="x", padx=28, pady=(4, 18))
    image_surface = ctk.CTkFrame(
        image_outer, fg_color=CARD, border_color=BORDER,
        border_width=1, corner_radius=14
    )
    image_surface.pack(anchor="center")
    image_label = tk.Label(image_surface, bg=CARD, bd=0, highlightthickness=0)
    image_label.pack(padx=7, pady=7)
    image_path = data.get("image")
    current_size = [0]

    def update_image(event=None):
        # The width adapts to the window, while height preserves aspect ratio.
        width = min(940, max(180, image_outer.winfo_width() - 16))
        if abs(width - current_size[0]) < 12:
            return
        current_size[0] = width
        photo = load_detail_image(image_path, (width, 360))
        if photo:
            image_label.configure(image=photo, text="")
            image_label.image = photo
            _image_refs[:] = [photo]
        else:
            image_label.configure(image="", text="Image not available",
                                  fg=LIGHT_TEXT, font=("Segoe UI", 12))

    image_outer.bind("<Configure>", update_image)

    # Tabs are rounded CustomTkinter buttons, not square Tkinter buttons.
    tabs = tk.Frame(content, bg=BG)
    tabs.pack(fill="x", padx=28, pady=(0, 12))
    detail = ctk.CTkFrame(content, fg_color=CARD, corner_radius=14,
                          border_width=1, border_color=BORDER)
    detail.pack(fill="x", padx=28, pady=(0, 24))
    buttons = {}

    def paragraph(master, value):
        for part in str(value).split("\n\n"):
            part = part.strip()
            if not part:
                continue
            label = tk.Label(master, text=part, bg=CARD, fg=TEXT,
                             font=("Segoe UI", 11), justify="left", anchor="nw",
                             wraplength=770)
            label.pack(fill="x", anchor="w", pady=(0, 15))
            # Adapt wrapping when the window is resized.
            label.bind("<Configure>", lambda e, lbl=label: lbl.configure(
                wraplength=max(200, e.width - 10)))

    def show_section(section):
        for child in detail.winfo_children():
            child.destroy()
        for label, button in buttons.items():
            active = label == section
            button.configure(fg_color=GOLD if active else "#102b3d",
                             text_color=BG if active else TEXT)
        inner = tk.Frame(detail, bg=CARD)
        inner.pack(fill="x", padx=24, pady=23)
        tk.Label(inner, text=section, bg=CARD, fg=GOLD,
                 font=("Georgia", 19, "bold")).pack(anchor="w", pady=(0, 15))
        if section == "Overview":
            paragraph(inner, data.get("overview", data.get("subtitle", "")))
            tk.Label(inner, text="KEY FACTS", bg=CARD, fg=GOLD,
                     font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(7, 12))
            for key, value in data.get("facts", []):
                paragraph(inner, f"{key}: {value}")
        elif section == "Story":
            paragraph(inner, data.get("story") or "The story has not been added yet.")
        else:
            paragraph(inner, data.get("cultural_significance") or data.get("note")
                      or "Cultural information has not been added yet.")
        content.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.yview_moveto(min(1.0, tabs.winfo_y() / max(1, content.winfo_height())))

    for section in ("Overview", "Story", "Cultural Significance"):
        button = ctk.CTkButton(
            tabs, text=section, fg_color="#102b3d", hover_color=LIGHT_GOLD,
            text_color=TEXT, corner_radius=13, height=48,
            font=("Segoe UI", 11, "bold"),
            command=lambda selected=section: show_section(selected))
        button.pack(side="left", fill="x", expand=True, padx=4)
        buttons[section] = button

    ctk.CTkButton(content, text="←  Back to Myths", command=back_command,
                  fg_color=GOLD, hover_color=LIGHT_GOLD, text_color=BG,
                  corner_radius=12, width=160, height=38,
                  font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=32, pady=(0, 30))

    show_section("Overview")
    canvas.yview_moveto(0)
    return root
