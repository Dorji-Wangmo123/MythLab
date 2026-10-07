import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from PIL import Image, ImageTk, ImageOps


# ============================================================
# MYTHLAB - REGIONS
# Embedded page for main.py
# ============================================================

ROOT = Path(__file__).resolve().parent

# All project images are inside assets/
IMAGE_FOLDER = ROOT / "assets"

# Keep PhotoImage objects alive
image_refs = []


# ============================================================
# COLORS
# ============================================================

BG = "#031521"
SIDEBAR = "#061c2b"
CARD = "#071d2a"
CARD2 = "#0a2534"

GOLD = "#d6a84f"
LIGHT_GOLD = "#efd27c"

TEXT = "#f5ead0"
MUTED = "#c4c0b6"
BORDER = "#765d31"


# ============================================================
# IMAGE FILES
# ============================================================

IMAGES = {

    "hero": "explore_bhutan.png",

    "explore_background": "welcome.png",

    "map": [
        "bhutan map.png",
        "bhutan_map.png"
    ],

    "paro": [
        "paro_taktsang.png",
        "jomolhari.png",
        "welcome.png"
    ],

    "dragon": [
        "thunder_dragon.png",
        "druk (3).png",
        "creatures.png"
    ],

    "bumthang": [
        "bumthang.png",
        "welcome.png",
        "jomolhari.png"
    ],

    "trashigang": [
        "welcome.png",
        "jomolhari.png"
    ],

    "trashiyangtse": [
        "jomolhari.png",
        "welcome.png"
    ],

    "mongar": [
        "welcome.png",
        "jomolhari.png"
    ],

    "samdrup jongkhar": [
        "welcome.png",
        "jomolhari.png"
    ],

    "zhemgang": [
        "black_mountain (2).png",
        "welcome.png"
    ],

    "trongsa": [
        "jomolhari.png",
        "welcome.png"
    ],

    "wangdue phodrang": [
        "welcome.png",
        "jomolhari.png"
    ],

    "thimphu": [
        "thimphu_dzongkha.png",
        "welcome.png",
        "jomolhari.png"
    ],

    "punakha": [
        "punakha.png",
        "welcome.png",
        "jomolhari.png"
    ],

    "kyichu": [
        "kyichu lhakhang.png",
        "kyichu_lhakhang.png",
        "kyichu.png"
    ]
}


# ============================================================
# IMAGE HELPERS
# ============================================================

def find_image(names):

    if isinstance(names, str):
        names = [names]

    # Exact filename
    for name in names:

        path = IMAGE_FOLDER / name

        if path.is_file():
            return path

        path = ROOT / name

        if path.is_file():
            return path

    # Case-insensitive recursive search
    for name in names:

        target = Path(name).name.lower()

        try:

            for path in ROOT.rglob("*"):

                if path.is_file() and path.name.lower() == target:
                    return path

        except Exception:
            pass

    # Flexible filename search
    for name in names:

        target = Path(name).stem.lower()

        target = (
            target
            .replace("_", " ")
            .replace("-", " ")
            .strip()
        )

        try:

            for path in ROOT.rglob("*"):

                if not path.is_file():
                    continue

                if path.suffix.lower() not in {
                    ".png",
                    ".jpg",
                    ".jpeg",
                    ".webp"
                }:
                    continue

                current = path.stem.lower()

                current = (
                    current
                    .replace("_", " ")
                    .replace("-", " ")
                    .strip()
                )

                if current == target:
                    return path

        except Exception:
            pass

    return None


def load_photo(names, size):

    path = find_image(names)

    if not path:
        print("IMAGE NOT FOUND:", names)
        return None

    try:

        img = Image.open(path).convert("RGB")

        img = ImageOps.fit(
            img,
            size,
            method=Image.Resampling.LANCZOS
        )

        photo = ImageTk.PhotoImage(img)

        image_refs.append(photo)

        return photo

    except Exception as error:

        print("IMAGE ERROR:", path)
        print(error)

        return None


# ============================================================
# MAIN REGIONS PAGE
# ============================================================

def show_regions(parent):

    # Clear previous Regions widgets
    for widget in parent.winfo_children():
        widget.destroy()

    image_refs.clear()

    # --------------------------------------------------------
    # Scrollable page
    # --------------------------------------------------------

    holder = tk.Frame(
        parent,
        bg=BG
    )

    holder.pack(
        fill="both",
        expand=True
    )

    canvas = tk.Canvas(
        holder,
        bg=BG,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        holder,
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

    page = tk.Frame(
        canvas,
        bg=BG
    )

    window = canvas.create_window(
        (0, 0),
        window=page,
        anchor="nw"
    )

    page.bind(
        "<Configure>",
        lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.bind(
        "<Configure>",
        lambda event: canvas.itemconfigure(
            window,
            width=event.width
        )
    )

    def mousewheel(event):
        canvas.yview_scroll(
        -int(event.delta / 120),
        "units"
    )
    canvas.bind_all(
    "<MouseWheel>",
    mousewheel
)
    
    # ========================================================
    # HELPER FUNCTIONS INSIDE REGIONS
    # ========================================================

    def open_dzongkhag(name):

        messagebox.showinfo(
            "MythLab",
            f"Opening {name}\n\n"
            f"The {name} detail page can be connected later."
        )

    def create_pill(parent_widget, text):

        return tk.Button(
            parent_widget,
            text=text,
            relief="solid",
            bd=1,
            bg=BG,
            fg=TEXT,
            activebackground="#173547",
            activeforeground=TEXT,
            font=("Segoe UI", 8),
            padx=8,
            pady=2
        )

    # --------------------------------------------------------
    # Small popular card
    # --------------------------------------------------------

    def small_card(
        parent_widget,
        image_names,
        title,
        tag,
        column
    ):

        box = tk.Frame(
            parent_widget,
            bg=CARD2,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        box.grid(
            row=0,
            column=column,
            padx=3,
            sticky="nsew"
        )

        photo = load_photo(
            image_names,
            (120, 85)
        )

        if photo:

            tk.Label(
                box,
                image=photo,
                bg=CARD2
            ).pack()

        else:

            tk.Label(
                box,
                text="Image",
                bg="#173547",
                fg=MUTED,
                width=13,
                height=4
            ).pack()

        tk.Label(
            box,
            text=title,
            bg=CARD2,
            fg=TEXT,
            font=("Segoe UI", 8, "bold")
        ).pack(
            anchor="w",
            padx=6,
            pady=(5, 1)
        )

        tk.Label(
            box,
            text=tag,
            bg=CARD2,
            fg=LIGHT_GOLD,
            font=("Segoe UI", 7)
        ).pack(
            anchor="w",
            padx=6,
            pady=(0, 5)
        )

        parent_widget.columnconfigure(
            column,
            weight=1
        )

    # --------------------------------------------------------
    # Other region card
    # --------------------------------------------------------

    def other_card(parent_widget, name, column):

        box = tk.Frame(
            parent_widget,
            bg=CARD2,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        box.grid(
            row=0,
            column=column,
            padx=4,
            sticky="nsew"
        )

        image_names = IMAGES.get(
            name.lower(),
            IMAGES["hero"]
        )

        photo = load_photo(
            image_names,
            (120, 85)
        )

        if photo:

            tk.Label(
                box,
                image=photo,
                bg=CARD2
            ).pack()

        else:

            tk.Label(
                box,
                text=name,
                bg="#173547",
                fg=TEXT,
                width=13,
                height=4
            ).pack()

        tk.Label(
            box,
            text=name,
            bg=CARD2,
            fg=TEXT,
            font=("Segoe UI", 8, "bold")
        ).pack(
            pady=6
        )

        parent_widget.columnconfigure(
            column,
            weight=1
        )

    # --------------------------------------------------------
    # Dzongkhag card
    # --------------------------------------------------------

    def dzongkhag_card(
        parent_widget,
        name,
        description,
        image_names,
        tags,
        index
    ):

        box = tk.Frame(
            parent_widget,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        box.grid(
            row=index // 4,
            column=index % 4,
            padx=7,
            pady=8,
            sticky="nsew"
        )

        photo = load_photo(
            image_names,
            (260, 115)
        )

        if photo:

            tk.Label(
                box,
                image=photo,
                bg=CARD
            ).pack(
                fill="x"
            )

        else:

            tk.Label(
                box,
                text=name,
                bg="#173547",
                fg=LIGHT_GOLD,
                font=("Georgia", 16, "bold"),
                height=5
            ).pack(
                fill="x"
            )

        tk.Label(
            box,
            text=f"⌖  {name}",
            bg=CARD,
            fg=LIGHT_GOLD,
            font=("Georgia", 12, "bold")
        ).pack(
            anchor="w",
            padx=12,
            pady=(9, 4)
        )

        tk.Label(
            box,
            text=description,
            bg=CARD,
            fg=TEXT,
            justify="left",
            font=("Segoe UI", 8)
        ).pack(
            anchor="w",
            padx=12
        )

        tag_row = tk.Frame(
            box,
            bg=CARD
        )

        tag_row.pack(
            fill="x",
            padx=9,
            pady=10
        )

        for tag in tags:

            create_pill(
                tag_row,
                tag
            ).pack(
                side="left",
                padx=2
            )

        tk.Button(
            tag_row,
            text="→",
            command=lambda n=name: open_dzongkhag(n),
            bg=BG,
            fg=LIGHT_GOLD,
            activebackground="#1a3444",
            relief="solid",
            bd=1,
            font=("Segoe UI", 11)
        ).pack(
            side="right"
        )

        parent_widget.rowconfigure(
            index // 4,
            weight=1
        )

    # ========================================================
    # OTHER DZONGKHAGS PAGE
    # ========================================================

    def show_other_dzongkhags():

        for widget in page.winfo_children():
            widget.destroy()

        image_refs.clear()

        # Breadcrumb
        tk.Label(
            page,
            text="Home  ›  Regions  ›  Other Dzongkhags",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=38,
            pady=(20, 4)
        )

        # Title
        title_box = tk.Frame(
            page,
            bg=BG
        )

        title_box.pack(
            fill="x",
            padx=38,
            pady=(8, 16)
        )

        tk.Label(
            title_box,
            text="⌘",
            bg=BG,
            fg=GOLD,
            font=("Segoe UI Symbol", 28)
        ).pack(
            side="left",
            padx=(0, 12)
        )

        title_words = tk.Frame(
            title_box,
            bg=BG
        )

        title_words.pack(
            side="left"
        )

        tk.Label(
            title_words,
            text="Other Dzongkhags",
            bg=BG,
            fg=LIGHT_GOLD,
            font=("Georgia", 29, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            title_words,
            text="Explore the unique myths, legends and sacred stories from\n"
                 "Bhutan's other Dzongkhags.",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

        # Header image
        photo = load_photo(
            IMAGES["hero"],
            (1050, 180)
        )

        header = tk.Frame(
            page,
            bg="#082333",
            height=180
        )

        header.pack(
            fill="x",
            padx=25,
            pady=(0, 15)
        )

        header.pack_propagate(False)

        if photo:

            tk.Label(
                header,
                image=photo,
                bg="#082333"
            ).pack(
                fill="both",
                expand=True
            )

        else:

            tk.Label(
                header,
                text="BHUTAN • MYTHS • LEGENDS",
                bg="#082333",
                fg=LIGHT_GOLD,
                font=("Georgia", 24, "bold")
            ).pack(
                expand=True
            )

        # Search and filters
        controls = tk.Frame(
            page,
            bg=BG
        )

        controls.pack(
            fill="x",
            padx=38,
            pady=(0, 18)
        )

        search = tk.Entry(
            controls,
            bg=BG,
            fg=TEXT,
            insertbackground=TEXT,
            relief="solid",
            bd=1,
            font=("Segoe UI", 10)
        )

        search.insert(
            0,
            "🔍  Search dzongkhags..."
        )

        search.pack(
            side="left",
            ipady=8,
            ipadx=12,
            fill="x",
            expand=True
        )

        def clear_search(event):

            if search.get().startswith("🔍"):
                search.delete(0, "end")

        search.bind(
            "<FocusIn>",
            clear_search
        )

        for text in [
            "All",
            "Myths",
            "Creatures",
            "Sacred Places",
            "Stories"
        ]:

            active = text == "All"

            tk.Button(
                controls,
                text=text,
                bg=LIGHT_GOLD if active else BG,
                fg="#17222a" if active else TEXT,
                activebackground=LIGHT_GOLD,
                activeforeground="#17222a",
                relief="solid",
                bd=1,
                font=("Segoe UI", 8),
                padx=13,
                pady=7
            ).pack(
                side="left",
                padx=4
            )

        # Section title
        section = tk.Frame(
            page,
            bg=BG
        )

        section.pack(
            fill="x",
            padx=38
        )

        tk.Label(
            section,
            text="🐉  Other Dzongkhags",
            bg=BG,
            fg=LIGHT_GOLD,
            font=("Georgia", 15, "bold")
        ).pack(
            side="left"
        )

        tk.Frame(
            section,
            bg=BORDER,
            height=1
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=15,
            pady=4
        )

        # Grid
        grid = tk.Frame(
            page,
            bg=BG
        )

        grid.pack(
            fill="x",
            padx=38,
            pady=15
        )

        data = [

            (
                "Bumthang",
                "Known as the spiritual heart of Bhutan,\n"
                "Bumthang is home to ancient temples,\n"
                "sacred sites and timeless legends.",
                IMAGES["bumthang"],
                ["Myths", "Sacred Places", "Stories"]
            ),

            (
                "Trashigang",
                "Land of vibrant culture and strong\n"
                "traditions, with unique stories of\n"
                "brave people and mystical beings.",
                IMAGES["trashigang"],
                ["Myths", "Creatures", "Stories"]
            ),

            (
                "Trashiyangtse",
                "A region of rivers and mountains,\n"
                "known for its rich folklore and\n"
                "sacred heritage.",
                IMAGES["trashiyangtse"],
                ["Myths", "Sacred Places", "Creatures"]
            ),

            (
                "Mongar",
                "Home to ancient traditions and\n"
                "inspiring legends passed down\n"
                "through generations.",
                IMAGES["mongar"],
                ["Myths", "Stories", "Sacred Places"]
            ),

            (
                "Samdrup Jongkhar",
                "A gateway to the east, filled with\n"
                "cultural diversity, forest spirits\n"
                "and hidden tales.",
                IMAGES["samdrup jongkhar"],
                ["Myths", "Creatures", "Stories"]
            ),

            (
                "Zhemgang",
                "Known for its peaceful valleys\n"
                "and legends of nature, spirits\n"
                "and ancestral wisdom.",
                IMAGES["zhemgang"],
                ["Myths", "Creatures", "Sacred Places"]
            ),

            (
                "Trongsa",
                "The central land of power and\n"
                "history, where royal paths and\n"
                "mystical stories meet.",
                IMAGES["trongsa"],
                ["Myths", "Sacred Places", "Stories"]
            ),

            (
                "Wangdue Phodrang",
                "A land of majestic views and\n"
                "fascinating legends, from ancient\n"
                "kings to sacred rivers.",
                IMAGES["wangdue phodrang"],
                ["Myths", "Creatures", "Stories"]
            )
        ]

        for index, item in enumerate(data):

            dzongkhag_card(
                grid,
                item[0],
                item[1],
                item[2],
                item[3],
                index
            )

            grid.columnconfigure(
                index % 4,
                weight=1
            )

        # Explore more
        more = tk.Frame(
            page,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        more.pack(
            fill="x",
            padx=38,
            pady=(5, 25)
        )

        tk.Label(
            more,
            text="✥",
            bg=CARD,
            fg=GOLD,
            font=("Segoe UI Symbol", 27)
        ).pack(
            side="left",
            padx=18,
            pady=15
        )

        text_box = tk.Frame(
            more,
            bg=CARD
        )

        text_box.pack(
            side="left",
            pady=15
        )

        tk.Label(
            text_box,
            text="Explore More",
            bg=CARD,
            fg=LIGHT_GOLD,
            font=("Georgia", 14, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            text_box,
            text="Discover the myths and legends of all 20 Dzongkhags of Bhutan.",
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(
            anchor="w"
        )

        tk.Button(
            more,
            text="View All Dzongkhags  →",
            command=show_regions,
            bg=BG,
            fg=LIGHT_GOLD,
            activebackground="#1a3444",
            relief="solid",
            bd=1,
            font=("Segoe UI", 9),
            padx=15,
            pady=7
        ).pack(
            side="right",
            padx=18
        )

    # ========================================================
    # MAIN EXPLORE BHUTAN PAGE
    # ========================================================

    # Breadcrumb
    top = tk.Frame(
        page,
        bg=BG
    )

    top.pack(
        fill="x",
        padx=38,
        pady=(20, 4)
    )

    tk.Label(
        top,
        text="Home  ›  Regions",
        bg=BG,
        fg=MUTED,
        font=("Segoe UI", 9)
    ).pack(
        anchor="w"
    )

    # --------------------------------------------------------
    # Hero title
    # --------------------------------------------------------

    hero = tk.Frame(
        page,
        bg=BG,
        height=220
    )

    hero.pack(
        fill="x",
        padx=25,
        pady=(8, 16)
    )

    hero.pack_propagate(False)

    background = load_photo(
        IMAGES["explore_background"],
        (1200, 220)
    )

    if background:

        bg_label = tk.Label(
            hero,
            image=background,
            bg=BG,
            borderwidth=0
        )

        bg_label.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

    title_area = tk.Frame(
        hero,
        bg="#031521"
    )

    title_area.pack(
        side="left",
        padx=25,
        pady=38
    )

    tk.Label(
        title_area,
        text="⌘",
        bg="#031521",
        fg=GOLD,
        font=("Segoe UI Symbol", 28)
    ).pack(
        side="left",
        padx=(0, 12)
    )

    words = tk.Frame(
        title_area,
        bg="#031521"
    )

    words.pack(
        side="left"
    )

    tk.Label(
        words,
        text="Explore Bhutan",
        bg="#031521",
        fg=LIGHT_GOLD,
        font=("Georgia", 29, "bold")
    ).pack(
        anchor="w"
    )

    tk.Label(
        words,
        text="Discover the myths, legends, creatures and sacred stories\n"
             "connected to the 20 Dzongkhags of Bhutan.",
        bg="#031521",
        fg=TEXT,
        font=("Segoe UI", 10)
    ).pack(
        anchor="w",
        pady=(4, 0)
    )

    # ========================================================
    # BODY
    # ========================================================

    body = tk.Frame(
        page,
        bg=BG
    )

    body.pack(
        fill="x",
        padx=25
    )

    body.columnconfigure(
        0,
        weight=3
    )

    body.columnconfigure(
        1,
        weight=2
    )

    # ========================================================
    # LEFT SIDE
    # ========================================================

    left = tk.Frame(
        body,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    left.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=(0, 8)
    )

    # Map
    map_photo = load_photo(
        IMAGES["map"],
        (540, 340)
    )

    if map_photo:

        map_frame = tk.Frame(
            left,
            bg=CARD
        )

        map_frame.pack(
            fill="x",
            padx=12,
            pady=12
        )

        tk.Label(
            map_frame,
            image=map_photo,
            bg=CARD
        ).pack(
            fill="both",
            expand=True
        )

    else:

        map_frame = tk.Frame(
            left,
            bg="#071c29",
            height=340
        )

        map_frame.pack(
            fill="x",
            padx=12,
            pady=12
        )

        map_frame.pack_propagate(False)

        tk.Label(
            map_frame,
            text="BHUTAN MAP IMAGE NOT FOUND",
            bg="#071c29",
            fg=LIGHT_GOLD,
            font=("Georgia", 17, "bold")
        ).pack(
            expand=True
        )

    tk.Label(
        left,
        text="✥  20 Dzongkhags of Bhutan",
        bg=CARD,
        fg=LIGHT_GOLD,
        font=("Georgia", 13, "bold")
    ).pack(
        anchor="w",
        padx=20,
        pady=(2, 4)
    )

    tk.Label(
        left,
        text="Click on a dzongkhag to explore its unique myths,\n"
             "legends and sacred places.",
        bg=CARD,
        fg=MUTED,
        justify="left",
        font=("Segoe UI", 9)
    ).pack(
        anchor="w",
        padx=20,
        pady=(0, 15)
    )

    # ========================================================
    # ALL DZONGKHAGS
    # ========================================================

    section = tk.Frame(
        left,
        bg=CARD
    )

    section.pack(
        fill="x",
        padx=12,
        pady=(0, 18)
    )

    tk.Label(
        section,
        text="✥  All Dzongkhags",
        bg=CARD,
        fg=LIGHT_GOLD,
        font=("Georgia", 13, "bold")
    ).pack(
        anchor="w",
        pady=(5, 8)
    )

    names = [
        "Bumthang",
        "Chukha",
        "Dagana",
        "Gasa",
        "Haa",
        "Lhuentse",
        "Mongar",
        "Paro",
        "Pema Gatshel",
        "Punakha",
        "Samdrup Jongkhar",
        "Samtse",
        "Sarpang",
        "Thimphu",
        "Trashigang",
        "Trashiyangtse",
        "Trongsa",
        "Tsirang",
        "Wangdue Phodrang",
        "Zhemgang"
    ]

    grid = tk.Frame(
        section,
        bg=CARD
    )

    grid.pack(
        fill="x"
    )

    for index, name in enumerate(names):

        button = tk.Button(
            grid,
            text=name,
            command=lambda n=name: open_dzongkhag(n),
            bg=BG,
            fg=TEXT,
            activebackground="#203c4b",
            activeforeground=TEXT,
            relief="solid",
            bd=1,
            font=("Segoe UI", 8),
            padx=8,
            pady=5
        )

        button.grid(
            row=index // 5,
            column=index % 5,
            padx=4,
            pady=4,
            sticky="ew"
        )

    for column in range(5):

        grid.columnconfigure(
            column,
            weight=1
        )

    # ========================================================
    # RIGHT SIDE - FEATURED
    # ========================================================

    right = tk.Frame(
        body,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    right.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=(8, 0)
    )

    tk.Label(
        right,
        text="Featured Dzongkhag",
        bg=CARD,
        fg=LIGHT_GOLD,
        font=("Georgia", 14, "bold")
    ).pack(
        anchor="w",
        padx=18,
        pady=(14, 10)
    )

    paro_photo = load_photo(
        IMAGES["paro"],
        (390, 155)
    )

    if paro_photo:

        tk.Label(
            right,
            image=paro_photo,
            bg=CARD
        ).pack(
            padx=14
        )

    else:

        tk.Label(
            right,
            text="PARO",
            bg="#183344",
            fg=LIGHT_GOLD,
            font=("Georgia", 24, "bold"),
            height=5
        ).pack(
            fill="x",
            padx=14
        )

    tk.Label(
        right,
        text="Paro",
        bg=CARD,
        fg=TEXT,
        font=("Georgia", 16, "bold")
    ).pack(
        anchor="w",
        padx=20,
        pady=(8, 0)
    )

    tk.Label(
        right,
        text="Valley of Legends",
        bg=CARD,
        fg=LIGHT_GOLD,
        font=("Georgia", 11)
    ).pack(
        anchor="w",
        padx=20
    )

    tk.Label(
        right,
        text="Home to ancient monasteries, sacred sites and timeless\n"
             "legends, Paro is where history and mythology meet\n"
             "in the mountains.",
        bg=CARD,
        fg=MUTED,
        justify="left",
        font=("Segoe UI", 9)
    ).pack(
        anchor="w",
        padx=20,
        pady=8
    )

    tk.Frame(
        right,
        bg=BORDER,
        height=1
    ).pack(
        fill="x",
        padx=18,
        pady=5
    )

    tk.Label(
        right,
        text="✥  Popular in Paro",
        bg=CARD,
        fg=LIGHT_GOLD,
        font=("Georgia", 11, "bold")
    ).pack(
        anchor="w",
        padx=18,
        pady=8
    )

    popular = tk.Frame(
        right,
        bg=CARD
    )

    popular.pack(
        fill="x",
        padx=12
    )

    small_card(
        popular,
        IMAGES["paro"],
        "The Tiger's Nest",
        "Myth",
        0
    )

    small_card(
        popular,
        IMAGES["dragon"],
        "Paro Dragon",
        "Creature",
        1
    )

    small_card(
        popular,
        IMAGES["kyichu"],
        "Kyichu Lhakhang",
        "Sacred Place",
        2
    )

    tk.Frame(
        right,
        bg=BORDER,
        height=1
    ).pack(
        fill="x",
        padx=18,
        pady=12
    )

    other_head = tk.Frame(
        right,
        bg=CARD
    )

    other_head.pack(
        fill="x",
        padx=18
    )

    tk.Label(
        other_head,
        text="✥  Other Dzongkhags",
        bg=CARD,
        fg=LIGHT_GOLD,
        font=("Georgia", 11, "bold")
    ).pack(
        side="left"
    )

    tk.Button(
        other_head,
        text="View all →",
        command=show_other_dzongkhags,
        bg=CARD,
        fg=LIGHT_GOLD,
        activebackground=CARD,
        relief="flat",
        bd=0,
        font=("Segoe UI", 8)
    ).pack(
        side="right"
    )

    tk.Label(
        right,
        text="Explore more regions of Bhutan",
        bg=CARD,
        fg=MUTED,
        font=("Segoe UI", 8)
    ).pack(
        anchor="w",
        padx=18,
        pady=(2, 8)
    )

    others = tk.Frame(
        right,
        bg=CARD
    )

    others.pack(
        fill="x",
        padx=12,
        pady=(0, 12)
    )

    for index, name in enumerate([
        "Thimphu",
        "Punakha",
        "Bumthang"
    ]):

        other_card(
            others,
            name,
            index
        )

    # ========================================================
    # BEYOND BHUTAN
    # ========================================================

    beyond = tk.Frame(
        page,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    beyond.pack(
        fill="x",
        padx=25,
        pady=20
    )

    tk.Label(
        beyond,
        text="♧",
        bg=CARD,
        fg=GOLD,
        font=("Segoe UI Symbol", 27)
    ).pack(
        side="left",
        padx=18,
        pady=15
    )

    beyond_text = tk.Frame(
        beyond,
        bg=CARD
    )

    beyond_text.pack(
        side="left",
        pady=15
    )

    tk.Label(
        beyond_text,
        text="Beyond Bhutan",
        bg=CARD,
        fg=LIGHT_GOLD,
        font=("Georgia", 14, "bold")
    ).pack(
        anchor="w"
    )

    tk.Label(
        beyond_text,
        text="Explore mythology from other cultures",
        bg=CARD,
        fg=MUTED,
        font=("Segoe UI", 9)
    ).pack(
        anchor="w"
    )

    for country in [
        "India",
        "Tibet",
        "Nepal",
        "Asia"
    ]:

        create_pill(
            beyond,
            country
        ).pack(
            side="right",
            padx=5,
            pady=25
        )

    parent.update_idletasks()
    canvas.configure(
        scrollregion=canvas.bbox("all")
    )