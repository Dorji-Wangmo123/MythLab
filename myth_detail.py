
# myth_detail.py
# MYTHLAB - SHARED STORY DETAIL PAGE

import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk, ImageOps


# ============================================================
# COLOURS
# ============================================================

BG = "#061b2b"
CARD = "#0a2131"
CARD2 = "#102b3d"
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
# ============================================================

MYTH_CONTENT = {

    "Ap Chhundu": {
        "id": "MYT-001",
        "category": "Deity",
        "origin": "Haa Valley, Bhutan",
        "image": "ap_chhundu.png",
        "subtitle": "The protective guardian deity of Haa Valley.",
        "overview": (
            "Ap Chhundu is one of the most respected guardian "
            "deities associated with Haa Valley in western Bhutan. "
            "He is traditionally regarded as a powerful protector "
            "of the valley and its people."
        ),
        "story": (
            "In the beautiful Haa Valley, surrounded by mountains "
            "and forests, local communities have long maintained "
            "a deep respect for Ap Chhundu.\n\n"
            "According to local beliefs, Ap Chhundu watches over "
            "the land and the people who live there. Families "
            "have traditionally offered prayers seeking protection, "
            "peace and well-being.\n\n"
            "The stories associated with Ap Chhundu reflect the "
            "relationship between local communities, their "
            "guardian deities and the natural environment."
        ),
        "cultural_significance": (
            "Ap Chhundu holds an important place in the spiritual "
            "and cultural identity of Haa Valley. Traditions "
            "associated with guardian deities help preserve "
            "local beliefs and community heritage."
        ),
        "facts": [
            ("Origin", "Haa Valley, Bhutan"),
            ("Type", "Guardian deity"),
            ("Role", "Protector of the valley")
        ]
    },

    "Ap Genyen Domtshang": {
        "id": "MYT-002",
        "category": "Deity",
        "origin": "Bhutan",
        "image": "ap_genyen_domtshang.png",
        "subtitle": "A guardian deity in Bhutanese tradition.",
        "overview": (
            "Ap Genyen Domtshang is associated with local "
            "Bhutanese traditions concerning protective deities."
        ),
        "story": (
            "In Bhutan, stories of guardian deities have been "
            "shared through families and communities for "
            "generations.\n\n"
            "Ap Genyen Domtshang is remembered as a protective "
            "spiritual figure. Like other guardian deities, "
            "he is associated with the well-being of particular "
            "places and their inhabitants.\n\n"
            "These traditions remind people of the importance "
            "of respecting sacred places and maintaining "
            "harmony within their communities."
        ),
        "cultural_significance": (
            "The tradition reflects the close relationship "
            "between spiritual beliefs, local communities "
            "and the Bhutanese landscape."
        ),
        "facts": [
            ("Origin", "Bhutan"),
            ("Type", "Guardian deity"),
            ("Role", "Protection and guidance")
        ]
    },

    "Jomo": {
        "id": "MYT-003",
        "category": "Deity",
        "origin": "Bhutan and the Himalayas",
        "image": "jomo.png",
        "subtitle": "A sacred female mountain deity.",
        "overview": (
            "Jomo is associated with female protective deities "
            "and sacred mountains in Bhutanese and Himalayan "
            "traditions."
        ),
        "story": (
            "High in the Himalayan mountains, many peaks are "
            "regarded as sacred places.\n\n"
            "Traditional beliefs associate certain mountains "
            "with powerful spiritual beings. Jomo is one "
            "of the names connected with female mountain "
            "deities.\n\n"
            "Communities living near sacred mountains have "
            "traditionally shown respect through prayers "
            "and local customs. Such beliefs connect "
            "the natural landscape with the spiritual world."
        ),
        "cultural_significance": (
            "Jomo traditions highlight the importance of "
            "mountains in Himalayan spirituality and the "
            "respect shown towards sacred landscapes."
        ),
        "facts": [
            ("Region", "Bhutan and the Himalayas"),
            ("Type", "Mountain deity"),
            ("Association", "Sacred mountains")
        ]
    },

    "Jomo (Aum Jomo)": {
        "id": "MYT-003",
        "category": "Deity",
        "origin": "Bhutan",
        "image": "jomo.png",
        "subtitle": "The sacred mountain goddess associated with Jomolhari.",
        "overview": (
            "Aum Jomo is associated with sacred mountain "
            "traditions in the Himalayan region."
        ),
        "story": (
            "Mount Jomolhari rises above the landscape "
            "of western Bhutan.\n\n"
            "In local spiritual traditions, sacred mountains "
            "are associated with protective deities and "
            "are treated with great respect.\n\n"
            "Stories about Aum Jomo reflect the belief "
            "that mountains are more than physical "
            "landmarks. They are also places of "
            "spiritual and cultural importance."
        ),
        "cultural_significance": (
            "The traditions surrounding Aum Jomo express "
            "respect for sacred mountains and the "
            "natural environment."
        ),
        "facts": [
            ("Region", "Western Bhutan"),
            ("Type", "Mountain deity"),
            ("Association", "Mount Jomolhari")
        ]
    },

    "Guru Rinpoche": {
        "id": "MYT-004",
        "category": "Religious Figure",
        "origin": "India and Bhutan",
        "image": "guru_rinpoche.png",
        "subtitle": "The great Buddhist master Padmasambhava.",
        "overview": (
            "Guru Rinpoche, also known as Padmasambhava, "
            "is one of the most important figures "
            "in Bhutanese Buddhist tradition."
        ),
        "story": (
            "According to Buddhist religious accounts, "
            "Guru Rinpoche travelled to Bhutan during "
            "the eighth century.\n\n"
            "He is traditionally credited with helping "
            "establish Vajrayana Buddhist teachings "
            "throughout the Himalayan region.\n\n"
            "One of the most famous accounts connects "
            "Guru Rinpoche with Paro Taktsang, "
            "the Tiger's Nest.\n\n"
            "Tradition holds that he meditated at "
            "this sacred location and subdued harmful "
            "spiritual forces.\n\n"
            "His teachings and associated stories "
            "continue to influence Bhutanese "
            "religious life and culture."
        ),
        "cultural_significance": (
            "Guru Rinpoche occupies a central place "
            "in Bhutanese Buddhism, religious festivals, "
            "sacred art and pilgrimage traditions."
        ),
        "facts": [
            ("Other name", "Padmasambhava"),
            ("Period", "Traditionally the 8th century"),
            ("Importance", "Vajrayana Buddhism")
        ]
    },

    "Yeshey Gonpo": {
        "id": "MYT-005",
        "category": "Deity",
        "origin": "Bhutan and Tibetan Buddhist tradition",
        "image": "yeshey_gonpo.png",
        "subtitle": "A powerful Buddhist protective deity.",
        "overview": (
            "Yeshey Gonpo is associated with Mahakala, "
            "a protective deity in Vajrayana Buddhism."
        ),
        "story": (
            "In Vajrayana Buddhist traditions, "
            "protective deities are associated "
            "with overcoming obstacles and "
            "protecting Buddhist teachings.\n\n"
            "Yeshey Gonpo is commonly represented "
            "with a fierce appearance. This "
            "symbolises protective spiritual power "
            "rather than ordinary anger.\n\n"
            "In Bhutan, protective deities are "
            "honoured through religious ceremonies, "
            "prayers and traditional rituals."
        ),
        "cultural_significance": (
            "Yeshey Gonpo represents spiritual "
            "protection and the overcoming "
            "of obstacles in Buddhist practice."
        ),
        "facts": [
            ("Other name", "Mahakala"),
            ("Type", "Protective deity"),
            ("Association", "Protection of Buddhist teachings")
        ]
    },

    "Drukpa Kunley": {
        "id": "MYT-006",
        "category": "Hero",
        "origin": "Tibet and Bhutan",
        "image": "drukpa_kuenley.png",
        "subtitle": "The Divine Madman.",
        "overview": (
            "Drukpa Kunley was a Buddhist teacher "
            "remembered for his humour and "
            "unconventional methods of teaching."
        ),
        "story": (
            "Drukpa Kunley, popularly known as "
            "the Divine Madman, is remembered "
            "in many Bhutanese stories.\n\n"
            "Unlike conventional religious teachers, "
            "he often used humour and surprising "
            "situations to communicate spiritual "
            "lessons.\n\n"
            "Stories associated with him encourage "
            "listeners to question pride, "
            "pretence and attachment.\n\n"
            "His unusual approach made him "
            "one of the most memorable figures "
            "in Bhutanese religious folklore."
        ),
        "cultural_significance": (
            "Drukpa Kunley's stories remain "
            "important in Bhutanese folklore "
            "and religious traditions."
        ),
        "facts": [
            ("Known as", "The Divine Madman"),
            ("Region", "Tibet and Bhutan"),
            ("Known for", "Humour and unconventional teachings")
        ]
    },

    "The Thunder Dragon": {
        "id": "MYT-007",
        "category": "Creature",
        "origin": "Bhutan",
        "image": "thunder_dragon.png",
        "subtitle": "The legendary Druk of Bhutan.",
        "overview": (
            "The Thunder Dragon, known as Druk, "
            "is one of Bhutan's most important "
            "national and cultural symbols."
        ),
        "story": (
            "High above the mountains of Bhutan, "
            "thunderstorms have long inspired "
            "stories about powerful dragons.\n\n"
            "In Bhutanese tradition, the sound "
            "of thunder is sometimes associated "
            "with the roar of a dragon.\n\n"
            "The dragon is known as Druk, "
            "and Bhutan is called Druk Yul, "
            "meaning the Land of the Thunder Dragon.\n\n"
            "The Druk appears on Bhutan's "
            "national flag, where it represents "
            "the country's identity and strength.\n\n"
            "The Thunder Dragon remains an "
            "important symbol in Bhutanese "
            "history, culture and national life."
        ),
        "cultural_significance": (
            "The Thunder Dragon is closely "
            "associated with Bhutan's national "
            "identity. It appears on the "
            "national flag and is reflected "
            "in the country's traditional name."
        ),
        "facts": [
            ("Local name", "Druk"),
            ("Country", "Bhutan"),
            ("Symbolises", "National identity and strength")
        ]
    },

    "The Black Mountain": {
        "id": "MYT-008",
        "category": "Folklore",
        "origin": "Central Bhutan",
        "image": "black_mountain (2).png",
        "subtitle": "A sacred mountain landscape.",
        "overview": (
            "The Black Mountains are part of "
            "Bhutan's central landscape and "
            "are connected with local traditions."
        ),
        "story": (
            "Bhutan's mountains have long been "
            "associated with sacred places "
            "and local beliefs.\n\n"
            "The Black Mountains form an "
            "important part of the country's "
            "natural landscape.\n\n"
            "Stories connected with mountain "
            "areas reflect the mystery of "
            "nature and the respect traditionally "
            "shown towards the environment."
        ),
        "cultural_significance": (
            "The Black Mountains highlight "
            "the connection between Bhutanese "
            "landscapes and cultural traditions."
        ),
        "facts": [
            ("Location", "Central Bhutan"),
            ("Type", "Landscape tradition"),
            ("Association", "Mountains and local beliefs")
        ]
    },

    "Paro Taktsang": {
        "id": "MYT-009",
        "category": "Sacred Legend",
        "origin": "Paro, Bhutan",
        "image": "paro_taktsang.png",
        "subtitle": "The sacred Tiger's Nest monastery.",
        "overview": (
            "Paro Taktsang is one of Bhutan's "
            "most famous religious landmarks."
        ),
        "story": (
            "High above Paro Valley stands "
            "the famous Tiger's Nest monastery.\n\n"
            "According to religious tradition, "
            "Guru Rinpoche travelled to this "
            "sacred location on the back "
            "of a tigress.\n\n"
            "He is believed to have meditated "
            "in a cave and subdued harmful "
            "spiritual forces.\n\n"
            "The monastery later became "
            "one of Bhutan's most important "
            "places of pilgrimage."
        ),
        "cultural_significance": (
            "Paro Taktsang is an important "
            "symbol of Bhutanese Buddhist "
            "heritage and pilgrimage."
        ),
        "facts": [
            ("Location", "Paro, Bhutan"),
            ("Also known as", "Tiger's Nest"),
            ("Association", "Guru Rinpoche")
        ]
    },

    "The Legend of Paro Taktsang": {
        "id": "MYT-009",
        "category": "Sacred Legend",
        "origin": "Paro, Bhutan",
        "image": "paro_taktsang.png",
        "subtitle": "The legend of the Tiger's Nest.",
        "overview": (
            "Paro Taktsang is a sacred monastery "
            "associated with Guru Rinpoche."
        ),
        "story": (
            "According to Bhutanese Buddhist "
            "tradition, Guru Rinpoche travelled "
            "to a cave above Paro Valley "
            "on the back of a tigress.\n\n"
            "He meditated at this sacred site, "
            "which later became known as "
            "Paro Taktsang or Tiger's Nest.\n\n"
            "The monastery is now one of "
            "Bhutan's most recognised "
            "religious landmarks."
        ),
        "cultural_significance": (
            "The site represents Bhutan's "
            "religious heritage and the "
            "importance of sacred pilgrimage."
        ),
        "facts": [
            ("Location", "Paro, Bhutan"),
            ("Also known as", "Tiger's Nest"),
            ("Association", "Guru Rinpoche")
        ]
    },

    "Dochula": {
        "id": "MYT-010",
        "category": "Cultural Landmark",
        "origin": "Dochula Pass, Bhutan",
        "image": "dochula.png",
        "subtitle": "A mountain pass with 108 memorial chortens.",
        "overview": (
            "Dochula Pass is an important "
            "cultural landmark in Bhutan."
        ),
        "story": (
            "Dochula Pass lies between "
            "Thimphu and Punakha.\n\n"
            "It is especially known for "
            "the 108 Druk Wangyal Chortens.\n\n"
            "The site provides a place "
            "for remembrance and reflection "
            "surrounded by mountain scenery."
        ),
        "cultural_significance": (
            "Dochula represents remembrance, "
            "national identity and "
            "Bhutanese cultural heritage."
        ),
        "facts": [
            ("Location", "Dochula Pass"),
            ("Known for", "108 memorial chortens"),
            ("Type", "Cultural landmark")
        ]
    },

    "Tshomen Lu": {
        "id": "MYT-011",
        "category": "Water Spirit",
        "origin": "Bhutan and the Himalayas",
        "image": "tshomen_lu.png",
        "subtitle": "Traditional water spirits.",
        "overview": (
            "Tshomen and Lu are associated "
            "with water spirits in Bhutanese "
            "and Himalayan traditions."
        ),
        "story": (
            "In Bhutanese and Himalayan folklore, "
            "water sources are sometimes associated "
            "with supernatural beings.\n\n"
            "Lu are traditionally connected "
            "with rivers, lakes and springs.\n\n"
            "Tshomen are commonly associated "
            "with female water spirits.\n\n"
            "These traditions reflect the "
            "belief that natural water sources "
            "should be treated with respect."
        ),
        "cultural_significance": (
            "Water spirit traditions encourage "
            "respect for lakes, rivers "
            "and the natural environment."
        ),
        "facts": [
            ("Region", "Bhutan and Himalayas"),
            ("Type", "Water spirits"),
            ("Association", "Lakes and rivers")
        ]
    },

    "Tshomen and Lu": {
        "id": "MYT-011",
        "category": "Water Spirit",
        "origin": "Bhutan",
        "image": "tshomen_lu.png",
        "subtitle": "Sacred water beings.",
        "overview": (
            "Traditional beings associated "
            "with lakes, rivers and springs."
        ),
        "story": (
            "Bhutanese folklore includes "
            "stories of water spirits "
            "connected with natural places.\n\n"
            "Tshomen and Lu are associated "
            "with water and the protection "
            "of sacred environments.\n\n"
            "These traditions remind people "
            "of the importance of treating "
            "natural water sources with respect."
        ),
        "cultural_significance": (
            "These beliefs connect "
            "spiritual traditions with "
            "care for the environment."
        ),
        "facts": [
            ("Region", "Bhutan"),
            ("Type", "Water spirits"),
            ("Association", "Water sources")
        ]
    },

    "Heroes": {
        "id": "MYT-012",
        "category": "Folklore",
        "origin": "Bhutan",
        "image": "heroes.png",
        "subtitle": "Stories of courage and bravery.",
        "overview": (
            "Heroic stories teach values "
            "such as courage and kindness."
        ),
        "story": (
            "Heroic stories are important "
            "parts of oral traditions.\n\n"
            "They often describe people "
            "who demonstrate courage, "
            "wisdom and determination.\n\n"
            "Such stories are shared "
            "to teach lessons about "
            "human behaviour and values."
        ),
        "cultural_significance": (
            "Hero stories preserve "
            "traditional values "
            "for younger generations."
        ),
        "facts": [
            ("Region", "Bhutan"),
            ("Themes", "Courage and wisdom")
        ]
    },

    "Gods": {
        "id": "MYT-013",
        "category": "Mythology",
        "origin": "Bhutan",
        "image": "gods.png",
        "subtitle": "Divine beings in Bhutanese traditions.",
        "overview": (
            "Bhutanese religious traditions "
            "include many divine and "
            "protective beings."
        ),
        "story": (
            "Divine beings appear in "
            "Bhutanese religious paintings, "
            "temples and sacred stories.\n\n"
            "Different deities are associated "
            "with protection, compassion "
            "and wisdom.\n\n"
            "These traditions form part "
            "of Bhutan's religious "
            "and cultural heritage."
        ),
        "cultural_significance": (
            "Religious mythology reflects "
            "the importance of Buddhist "
            "traditions in Bhutan."
        ),
        "facts": [
            ("Region", "Bhutan"),
            ("Themes", "Protection and wisdom")
        ]
    }
}


# ============================================================
# IMAGE FUNCTIONS
# ============================================================

def find_image(filename):

    if not filename:
        return None

    for folder in [IMAGE_DIR, PROJECT_DIR]:
        path = folder / filename

        if path.is_file():
            return path

    target = "".join(
        character.lower()
        for character in Path(filename).stem
        if character.isalnum()
    )

    for folder in [IMAGE_DIR, PROJECT_DIR]:

        if not folder.is_dir():
            continue

        for file in folder.iterdir():

            if not file.is_file():
                continue

            if file.suffix.lower() not in {
                ".png", ".jpg", ".jpeg", ".webp"
            }:
                continue

            current = "".join(
                character.lower()
                for character in file.stem
                if character.isalnum()
            )

            if current == target:
                return file

    return None


def load_detail_image(filename, size):

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

        return ImageTk.PhotoImage(image)

    except Exception as error:
        print("Image error:", error)
        return None


# ============================================================
# STORY DETAIL PAGE
# ============================================================

def show_myth_detail(parent, back_command, name):

    global _image_refs
    _image_refs.clear()

    for widget in parent.winfo_children():
        widget.destroy()

    data = MYTH_CONTENT.get(name)

    main = tk.Frame(parent, bg=BG)
    main.pack(fill="both", expand=True)

    # --------------------------------------------------------
    # BACK BUTTON
    # --------------------------------------------------------

    top_bar = tk.Frame(main, bg=BG)
    top_bar.pack(fill="x", padx=25, pady=15)

    tk.Button(
        top_bar,
        text="←  Back",
        command=back_command,
        bg=BG,
        fg=GOLD,
        font=("Arial", 11, "bold"),
        activebackground=BG,
        activeforeground=LIGHT_GOLD,
        relief="flat",
        cursor="hand2"
    ).pack(side="left")

    if data is None:

        tk.Label(
            main,
            text="Story not found",
            bg=BG,
            fg=GOLD,
            font=("Georgia", 24, "bold")
        ).pack(pady=40)

        tk.Label(
            main,
            text="No story has been added for: " + name,
            bg=BG,
            fg=TEXT,
            font=("Arial", 11)
        ).pack()

        return main

    # --------------------------------------------------------
    # SCROLLABLE AREA
    # --------------------------------------------------------

    canvas = tk.Canvas(
        main,
        bg=BG,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        main,
        orient="vertical",
        command=canvas.yview
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    scrollbar.pack(side="right", fill="y")

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    content = tk.Frame(canvas, bg=BG)

    window_id = canvas.create_window(
        (0, 0),
        window=content,
        anchor="nw"
    )

    def update_scroll(event=None):
        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    def resize_content(event):
        canvas.itemconfigure(
            window_id,
            width=event.width
        )

    content.bind("<Configure>", update_scroll)
    canvas.bind("<Configure>", resize_content)

    def mousewheel(event):

        if getattr(event, "num", None) == 4:
            direction = -1

        elif getattr(event, "num", None) == 5:
            direction = 1

        else:
            direction = -1 if event.delta > 0 else 1

        canvas.yview_scroll(direction, "units")

    canvas.bind(
        "<Enter>",
        lambda event: canvas.bind_all(
            "<MouseWheel>",
            mousewheel
        )
    )

    canvas.bind(
        "<Leave>",
        lambda event: canvas.unbind_all(
            "<MouseWheel>"
        )
    )

    # --------------------------------------------------------
    # TITLE AND INFORMATION
    # --------------------------------------------------------

    header = tk.Frame(content, bg=BG)

    header.pack(
        fill="x",
        padx=30,
        pady=(20, 15)
    )

    tk.Label(
        header,
        text=data.get("id", "MYTHLAB"),
        bg=BG,
        fg=GOLD,
        font=("Arial", 10, "bold")
    ).pack(anchor="w")

    tk.Label(
        header,
        text=name,
        bg=BG,
        fg=TEXT,
        font=("Georgia", 28, "bold"),
        wraplength=850,
        justify="left"
    ).pack(anchor="w", pady=(10, 10))

    tk.Label(
        header,
        text=data.get("subtitle", ""),
        bg=BG,
        fg=LIGHT_TEXT,
        font=("Arial", 11),
        wraplength=850,
        justify="left"
    ).pack(anchor="w")

    tk.Label(
        header,
        text=(
            data.get("category", "Myth")
            + "  •  "
            + data.get("origin", "Unknown")
        ),
        bg=BG,
        fg=GOLD,
        font=("Arial", 10)
    ).pack(anchor="w", pady=(15, 0))

    # --------------------------------------------------------
    # IMAGE
    # --------------------------------------------------------

    image_frame = tk.Frame(
        content,
        bg=CARD,
        highlightthickness=1,
        highlightbackground=BORDER
    )

    image_frame.pack(
        fill="x",
        padx=30,
        pady=(5, 20)
    )

    photo = load_detail_image(
        data.get("image"),
        (800, 290)
    )

    if photo:

        _image_refs.append(photo)

        image_label = tk.Label(
            image_frame,
            image=photo,
            bg=CARD
        )

        image_label.image = photo
        image_label.pack(pady=8)

    else:

        tk.Label(
            image_frame,
            text="MYTHLAB",
            bg=CARD,
            fg=GOLD,
            font=("Georgia", 24, "bold"),
            height=6
        ).pack(fill="x")

    # --------------------------------------------------------
    # TAB BUTTONS
    # --------------------------------------------------------

    tab_bar = tk.Frame(content, bg=BG)

    tab_bar.pack(
        fill="x",
        padx=30,
        pady=(0, 15)
    )

    tab_buttons = {}

    display_area = tk.Frame(
        content,
        bg=CARD,
        highlightthickness=1,
        highlightbackground=BORDER
    )

    display_area.pack(
        fill="x",
        padx=30,
        pady=(0, 25)
    )

    def add_paragraph(container, paragraph):

        paragraph = str(paragraph).strip()

        if not paragraph:
            return

        tk.Label(
            container,
            text=paragraph,
            bg=CARD,
            fg=TEXT,
            font=("Arial", 11),
            justify="left",
            anchor="nw",
            wraplength=790
        ).pack(
            fill="x",
            anchor="w",
            pady=(0, 17)
        )

    # --------------------------------------------------------
    # EVENT HANDLING FOR TABS
    # --------------------------------------------------------

    def show_section(section):

        for widget in display_area.winfo_children():
            widget.destroy()

        for title, button in tab_buttons.items():

            is_active = title == section

            button.configure(
                bg=GOLD if is_active else CARD2,
                fg=BG if is_active else TEXT
            )

        tk.Label(
            display_area,
            text=section,
            bg=CARD,
            fg=GOLD,
            font=("Georgia", 20, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 15)
        )

        body = tk.Frame(display_area, bg=CARD)

        body.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        if section == "Overview":

            add_paragraph(
                body,
                data.get(
                    "overview",
                    data.get("subtitle", "")
                )
            )

            tk.Label(
                body,
                text="KEY FACTS",
                bg=CARD,
                fg=GOLD,
                font=("Arial", 11, "bold")
            ).pack(
                anchor="w",
                pady=(12, 12)
            )

            for label, value in data.get("facts", []):

                add_paragraph(
                    body,
                    str(label) + ": " + str(value)
                )

        elif section == "Story":

            story = data.get("story", "")

            if story.strip():

                for paragraph in story.split("\n\n"):
                    add_paragraph(body, paragraph)

            else:

                add_paragraph(
                    body,
                    "The story has not been added yet."
                )

        elif section == "Cultural Significance":

            cultural_text = data.get(
                "cultural_significance",
                data.get("note", "")
            )

            if cultural_text.strip():

                for paragraph in cultural_text.split("\n\n"):
                    add_paragraph(body, paragraph)

            else:

                add_paragraph(
                    body,
                    "Cultural information has not been added yet."
                )

        content.update_idletasks()
        update_scroll()

        # Scroll to the tab section
        section_position = tab_bar.winfo_y()

        content_height = max(
            1,
            content.winfo_height()
        )

        canvas.yview_moveto(
            min(1.0, section_position / content_height)
        )

    # --------------------------------------------------------
    # CREATE THREE CLICKABLE BUTTONS
    # --------------------------------------------------------

    sections = [
        "Overview",
        "Story",
        "Cultural Significance"
    ]

    for section in sections:

        button = tk.Button(
            tab_bar,
            text=section,
            font=("Arial", 10, "bold"),
            bg=CARD2,
            fg=TEXT,
            activebackground=GOLD,
            activeforeground=BG,
            relief="flat",
            padx=12,
            pady=12,
            cursor="hand2",
            command=lambda selected=section: show_section(
                selected
            )
        )

        button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=4
        )

        tab_buttons[section] = button

    # --------------------------------------------------------
    # BOTTOM BACK BUTTON
    # --------------------------------------------------------

    tk.Button(
        content,
        text="←  Back",
        command=back_command,
        font=("Arial", 10, "bold"),
        bg=GOLD,
        fg=BG,
        activebackground=LIGHT_GOLD,
        relief="flat",
        padx=22,
        pady=10,
        cursor="hand2"
    ).pack(
        anchor="w",
        padx=30,
        pady=(0, 35)
    )

    # Show Overview when story first opens
    show_section("Overview")
    canvas.yview_moveto(0)

    return main
