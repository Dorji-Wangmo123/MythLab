
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from PIL import Image, ImageTk, ImageOps


# ============================================================
# MYTHLAB - REGIONS
# Embedded page for main.py
# ============================================================

ROOT = Path(__file__).resolve().parent
IMAGE_FOLDER = ROOT / "assets"

# Keep PhotoImage references alive
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
    "hero": "banner.jpg",
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
        "trashigang.jpg",
        "trashigang.png",
        "welcome.png",
        "jomolhari.png"
    ],

    "trashiyangtse": [
        "trashiyangtse.jpg",
        "trashiyangtse.png",
        "jomolhari.png",
        "welcome.png"
    ],

    "mongar": [
        "mongar.jpg",
        "mongar.png",
        "welcome.png",
        "jomolhari.png"
    ],

    "samdrup jongkhar": [
        "samdrupjongkhar.png",
        "samdrup_jongkhar.png",
        "welcome.png",
        "jomolhari.png"
    ],

    "zhemgang": [
        "zhemgang.jpg",
        "zhemgang.png",
        "black_mountain (2).png",
        "welcome.png"
    ],

    "trongsa": [
        "trongsa.jpg",
        "trongsa.png",
        "jomolhari.png",
        "welcome.png"
    ],

    "wangdue phodrang": [
        "wangdue_phodrang.jpg",
        "wangdue_phodrang.png",
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
# FIND IMAGE
# ============================================================

def find_image(names):

    if isinstance(names, str):
        names = [names]

    # Check assets folder and project folder first
    for name in names:

        path = IMAGE_FOLDER / name

        if path.is_file():
            return path

        path = ROOT / name

        if path.is_file():
            return path

    # Search recursively using exact filename
    for name in names:

        target = Path(name).name.lower()

        try:
            for path in ROOT.rglob("*"):

                if (
                    path.is_file()
                    and path.suffix.lower() in {
                        ".png", ".jpg", ".jpeg", ".webp"
                    }
                    and path.name.lower() == target
                ):
                    return path

        except Exception as error:
            print("IMAGE SEARCH ERROR:", error)

    # Search recursively using flexible filename matching
    for name in names:

        target = Path(name).stem.lower()
        target = (
            target.replace("_", "")
            .replace("-", "")
            .replace(" ", "")
        )

        try:
            for path in ROOT.rglob("*"):

                if not path.is_file():
                    continue

                if path.suffix.lower() not in {
                    ".png", ".jpg", ".jpeg", ".webp"
                }:
                    continue

                current = path.stem.lower()
                current = (
                    current.replace("_", "")
                    .replace("-", "")
                    .replace(" ", "")
                )

                if current == target:
                    return path

        except Exception as error:
            print("FLEXIBLE IMAGE SEARCH ERROR:", error)

    print("IMAGE NOT FOUND:", names)
    return None


# ============================================================
# LOAD IMAGE
# ============================================================

def load_photo(names, size, mode="contain", background=CARD):

    path = find_image(names)

    if path is None:
        return None

    try:

        img = Image.open(path).convert("RGB")

        if mode == "cover":

            # Fill the complete area.
            # Some cropping may occur.
            img = ImageOps.fit(
                img,
                size,
                method=Image.Resampling.LANCZOS
            )

        else:

            # Preserve the complete image without cropping.
            img.thumbnail(
                size,
                Image.Resampling.LANCZOS
            )

            canvas = Image.new(
                "RGB",
                size,
                background
            )

            x = (size[0] - img.width) // 2
            y = (size[1] - img.height) // 2

            canvas.paste(img, (x, y))
            img = canvas

        photo = ImageTk.PhotoImage(img)
        image_refs.append(photo)

        print("IMAGE LOADED:", path)
        return photo

    except Exception as error:

        print("IMAGE ERROR:", path)
        print(error)
        return None


# ============================================================
# MAIN REGIONS PAGE
# ============================================================

def show_regions(parent):

    # Clear the existing page
    for widget in parent.winfo_children():
        widget.destroy()

    image_refs.clear()

    # --------------------------------------------------------
    # SCROLLABLE PAGE
    # --------------------------------------------------------

    holder = tk.Frame(parent, bg=BG)
    holder.pack(fill="both", expand=True)

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

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    page = tk.Frame(canvas, bg=BG)

    window = canvas.create_window(
        (0, 0),
        window=page,
        anchor="nw"
    )

    def update_scrollregion(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def resize_page(event):
        canvas.itemconfigure(
            window,
            width=event.width
        )

    page.bind("<Configure>", update_scrollregion)
    canvas.bind("<Configure>", resize_page)

    def mousewheel(event):
        canvas.yview_scroll(
            -int(event.delta / 120),
            "units"
        )

    canvas.bind_all("<MouseWheel>", mousewheel)

    # ========================================================
    # COMMON HELPERS
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

    # ========================================================
    # OTHER DZONGKHAGS CARD
    # ========================================================

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
            highlightthickness=1,
            height=225
        )

        box.grid(
            row=index // 4,
            column=index % 4,
            padx=7,
            pady=8,
            sticky="nsew"
        )

        box.grid_propagate(False)

        # Image area
        image_area = tk.Frame(
            box,
            bg="#173547",
            height=105
        )

        image_area.pack(fill="x")
        image_area.pack_propagate(False)

        photo = load_photo(
            image_names,
            (260, 105),
            mode="cover",
            background="#173547"
        )

        if photo:

            tk.Label(
                image_area,
                image=photo,
                bg="#173547",
                borderwidth=0
            ).pack(fill="both", expand=True)

        else:

            tk.Label(
                image_area,
                text=name,
                bg="#173547",
                fg=LIGHT_GOLD,
                font=("Georgia", 15, "bold")
            ).pack(fill="both", expand=True)

        # Card body
        body = tk.Frame(box, bg=CARD)

        body.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=7
        )

        tk.Label(
            body,
            text=f"⌖  {name}",
            bg=CARD,
            fg=LIGHT_GOLD,
            font=("Georgia", 11, "bold"),
            anchor="w"
        ).pack(fill="x")

        tk.Label(
            body,
            text=description,
            bg=CARD,
            fg=TEXT,
            justify="left",
            anchor="w",
            font=("Segoe UI", 8)
        ).pack(
            fill="x",
            pady=(5, 4)
        )

        bottom = tk.Frame(body, bg=CARD)
        bottom.pack(side="bottom", fill="x")

        for tag in tags:

            tk.Label(
                bottom,
                text=tag,
                font=("Segoe UI", 7),
                fg="#E4D9C2",
                bg="#102D3D",
                padx=5,
                pady=3
            ).pack(side="left", padx=(0, 3))

        tk.Button(
            bottom,
            text="→",
            command=lambda n=name: open_dzongkhag(n),
            bg=CARD,
            fg=LIGHT_GOLD,
            activebackground="#1a3444",
            relief="flat",
            bd=0,
            font=("Segoe UI", 13)
        ).pack(side="right")

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
        title_box = tk.Frame(page, bg=BG)

        title_box.pack(
            fill="x",
            padx=38,
            pady=(8, 16)
        )

        tk.Label(
            title_box,
            text="✥",
            bg=BG,
            fg=GOLD,
            font=("Georgia", 30)
        ).pack(side="left", padx=(0, 12))

        title_words = tk.Frame(title_box, bg=BG)
        title_words.pack(side="left")

        tk.Label(
            title_words,
            text="Other Dzongkhags",
            bg=BG,
            fg=LIGHT_GOLD,
            font=("Georgia", 29, "bold")
        ).pack(anchor="w")

        tk.Label(
            title_words,
            text="Explore the unique myths, legends and sacred stories "
                 "from Bhutan's other Dzongkhags.",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(4, 0))

        # Header image
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

        photo = load_photo(
            IMAGES["hero"],
            (1100, 180),
            mode="cover",
            background="#082333"
        )

        if photo:

            tk.Label(
                header,
                image=photo,
                bg="#082333",
                borderwidth=0
            ).pack(fill="both", expand=True)

        else:

            tk.Label(
                header,
                text="BHUTAN  •  MYTHS  •  LEGENDS",
                bg="#082333",
                fg=LIGHT_GOLD,
                font=("Georgia", 24, "bold")
            ).pack(expand=True)

        # Search and filters
        controls = tk.Frame(page, bg=BG)

        controls.pack(
            fill="x",
            padx=38,
            pady=(0, 18)
        )

        search = tk.Entry(
            controls,
            bg="#081F30",
            fg=TEXT,
            insertbackground=TEXT,
            relief="solid",
            bd=1,
            font=("Segoe UI", 10)
        )

        search.insert(0, "Search dzongkhags...")

        search.pack(
            side="left",
            ipady=8,
            ipadx=12,
            fill="x",
            expand=True
        )

        def clear_search(event):

            if search.get() == "Search dzongkhags...":
                search.delete(0, "end")

        search.bind("<FocusIn>", clear_search)

        # Section title
        section = tk.Frame(page, bg=BG)

        section.pack(
            fill="x",
            padx=38
        )

        tk.Label(
            section,
            text="✥  Other Dzongkhags",
            bg=BG,
            fg=LIGHT_GOLD,
            font=("Georgia", 15, "bold")
        ).pack(side="left")

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

        # Dzongkhag data
        
        data = [
    ("Bumthang", "The spiritual heart of Bhutan, home to ancient temples and sacred legends.", IMAGES["bumthang"], ["Myths", "Sacred Places"]),
    ("Chukha", "A southern region rich in cultural heritage, rivers and traditional stories.", ["chukha.jpg", "chukha.png", "welcome.png"], ["Myths", "Stories"]),
    ("Dagana", "A peaceful region with traditional villages and stories passed through generations.", ["dagana.jpg", "dagana.png", "welcome.png"], ["Folklore", "Stories"]),
    ("Gasa", "Known for its mountain landscapes, hot springs and Himalayan traditions.", ["gasa.jpg", "gasa.png", "jomolhari.png"], ["Myths", "Nature"]),

    ("Haa", "A beautiful valley with ancient traditions, sacred places and local legends.", ["haa.jpg", "haa.png", "welcome.png"], ["Myths", "Sacred Places"]),
    ("Lhuentse", "A region known for its rich cultural heritage, ancestral traditions and legends.", ["lhuentse.jpg", "lhuentse.png", "welcome.png"], ["Folklore", "Stories"]),
    ("Mongar", "Home to ancient traditions and inspiring legends passed down through generations.", IMAGES["mongar"], ["Myths", "Stories"]),
    ("Paro", "A valley of ancient monasteries, sacred sites and timeless legends.", IMAGES["paro"], ["Myths", "Sacred Places"]),

    ("Pema Gatshel", "A region of eastern Bhutan known for its traditions and cultural heritage.", ["pemagatshel.jpg", "pema_gatshel.png", "welcome.png"], ["Folklore", "Stories"]),
    ("Punakha", "A historic valley known for its majestic dzong and sacred stories.", IMAGES["punakha"], ["Myths", "Sacred Places"]),
    ("Samdrup Jongkhar", "A gateway to the east, filled with cultural diversity and hidden tales.", IMAGES["samdrup jongkhar"], ["Myths", "Creatures"]),
    ("Samtse", "A southern region with diverse communities, traditions and local folklore.", ["samtse.jpg", "samtse.png", "welcome.png"], ["Folklore", "Stories"]),

    ("Sarpang", "A southern region with rich natural surroundings and cultural traditions.", ["sarpang.jpg", "sarpang.png", "welcome.png"], ["Nature", "Stories"]),
    ("Thimphu", "The capital region, where modern Bhutan meets ancient traditions and sacred heritage.", IMAGES["thimphu"], ["Myths", "Sacred Places"]),
    ("Trashigang", "Land of vibrant culture and strong traditions, with stories of brave people and mystical beings.", IMAGES["trashigang"], ["Myths", "Creatures"]),
    ("Trashiyangtse", "A region of rivers and mountains, known for its rich folklore and sacred heritage.", IMAGES["trashiyangtse"], ["Myths", "Sacred Places"]),

    ("Trongsa", "The central land of power and history, where royal paths and mystical stories meet.", IMAGES["trongsa"], ["Myths", "Sacred Places"]),
    ("Tsirang", "A region of beautiful landscapes, diverse communities and traditional stories.", ["tsirang.jpg", "tsirang.png", "welcome.png"], ["Folklore", "Stories"]),
    ("Wangdue Phodrang", "A land of majestic views and fascinating legends, from ancient kings to sacred rivers.", IMAGES["wangdue phodrang"], ["Myths", "Creatures"]),
    ("Zhemgang", "Known for its peaceful valleys and legends of nature, spirits and ancestral wisdom.", IMAGES["zhemgang"], ["Myths", "Creatures"])
    ]


        grid = tk.Frame(page, bg=BG)

        grid.pack(
            fill="x",
            padx=30,
            pady=15
        )

        for column in range(4):
            grid.columnconfigure(column, weight=1)

        for index, item in enumerate(data):

            dzongkhag_card(
                grid,
                item[0],
                item[1],
                item[2],
                item[3],
                index
            )

        # Explore more section
        more = tk.Frame(
            page,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1,
            height=75
        )

        more.pack(
            fill="x",
            padx=38,
            pady=(5, 25)
        )

        more.pack_propagate(False)

        tk.Label(
            more,
            text="✥",
            bg=CARD,
            fg=GOLD,
            font=("Georgia", 27)
        ).pack(
            side="left",
            padx=18
        )

        text_box = tk.Frame(more, bg=CARD)
        text_box.pack(side="left", pady=15)

        tk.Label(
            text_box,
            text="Explore More",
            bg=CARD,
            fg=LIGHT_GOLD,
            font=("Georgia", 14, "bold")
        ).pack(anchor="w")

        tk.Label(
            text_box,
            text="Discover the myths and legends of all 20 Dzongkhags of Bhutan.",
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w")

        tk.Button(
            more,
            text="Back to Regions  →",
            command=show_main_regions,
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

        canvas.yview_moveto(0)

    # ========================================================
    # MAIN EXPLORE BHUTAN PAGE
    # ========================================================

    def show_main_regions():

        for widget in page.winfo_children():
            widget.destroy()

        image_refs.clear()

        # Breadcrumb
        top = tk.Frame(page, bg=BG)

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
        ).pack(anchor="w")

        # Hero section
        
        # Hero section
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

        # Use the same banner image as the other pages
        banner_photo = load_photo(
            IMAGES["hero"],
            (1200, 220),
            mode="cover",
            background=BG
        )

        if banner_photo:

            tk.Label(
                hero,
                image=banner_photo,
                bg=BG,
                borderwidth=0
            ).place(
                x=0,
                y=0,
                relwidth=1,
                relheight=1
            )

        # Title and description without a background box
        title_area = tk.Frame(
            hero,
            bg=BG
        )

        title_area.pack(
            side="left",
            padx=25,
            pady=38
        )

        tk.Label(
            title_area,
            text="✥",
            bg=BG,
            fg=GOLD,
            font=("Georgia", 28)
        ).pack(side="left", padx=(0, 12))

        words = tk.Frame(
            title_area,
            bg=BG
        )

        words.pack(side="left")

        tk.Label(
            words,
            text="Explore Bhutan",
            bg=BG,
            fg=LIGHT_GOLD,
            font=("Georgia", 29, "bold")
        ).pack(anchor="w")

        tk.Label(
            words,
            text="Discover the myths, legends, creatures and sacred stories\n"
                 "connected to the 20 Dzongkhags of Bhutan.",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 10),
            justify="left"
        ).pack(anchor="w", pady=(4, 0))


        # Body layout
        body = tk.Frame(page, bg=BG)

        body.pack(
            fill="x",
            padx=25
        )

        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)

        # ----------------------------------------------------
        # LEFT SIDE
        # ----------------------------------------------------

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

        # Bhutan map
        map_photo = load_photo(
            IMAGES["map"],
            (540, 340),
            mode="contain",
            background=CARD
        )

        map_frame = tk.Frame(
            left,
            bg=CARD,
            height=340
        )

        map_frame.pack(
            fill="x",
            padx=12,
            pady=12
        )

        map_frame.pack_propagate(False)

        if map_photo:

            tk.Label(
                map_frame,
                image=map_photo,
                bg=CARD
            ).pack(
                fill="both",
                expand=True
            )

        else:

            tk.Label(
                map_frame,
                text="BHUTAN MAP IMAGE NOT FOUND",
                bg="#071c29",
                fg=LIGHT_GOLD,
                font=("Georgia", 17, "bold")
            ).pack(
                fill="both",
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

        # All Dzongkhags
        section = tk.Frame(left, bg=CARD)

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

        name_grid = tk.Frame(section, bg=CARD)
        name_grid.pack(fill="x")

        for index, name in enumerate(names):

            tk.Button(
                name_grid,
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
            ).grid(
                row=index // 5,
                column=index % 5,
                padx=4,
                pady=4,
                sticky="ew"
            )

        for column in range(5):
            name_grid.columnconfigure(column, weight=1)

        # ----------------------------------------------------
        # RIGHT SIDE - FEATURED
        # ----------------------------------------------------

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
            (390, 155),
            mode="cover",
            background=CARD
        )

        if paro_photo:

            tk.Label(
                right,
                image=paro_photo,
                bg=CARD
            ).pack(padx=14)

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

        popular = tk.Frame(right, bg=CARD)

        popular.pack(
            fill="x",
            padx=12
        )

        # Popular cards
        popular_items = [
            (IMAGES["paro"], "The Tiger's Nest", "Myth"),
            (IMAGES["dragon"], "Paro Dragon", "Creature"),
            (IMAGES["kyichu"], "Kyichu Lhakhang", "Sacred Place")
        ]

        for index, item in enumerate(popular_items):

            box = tk.Frame(
                popular,
                bg=CARD2,
                highlightbackground=BORDER,
                highlightthickness=1
            )

            box.grid(
                row=0,
                column=index,
                padx=3,
                sticky="nsew"
            )

            popular_photo = load_photo(
                item[0],
                (120, 85),
                mode="cover",
                background=CARD2
            )

            if popular_photo:

                tk.Label(
                    box,
                    image=popular_photo,
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
                text=item[1],
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
                text=item[2],
                bg=CARD2,
                fg=LIGHT_GOLD,
                font=("Segoe UI", 7)
            ).pack(
                anchor="w",
                padx=6,
                pady=(0, 5)
            )

            popular.columnconfigure(index, weight=1)

        tk.Frame(
            right,
            bg=BORDER,
            height=1
        ).pack(
            fill="x",
            padx=18,
            pady=12
        )

        # Other Dzongkhags link
        other_head = tk.Frame(right, bg=CARD)

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
        ).pack(side="left")

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
        ).pack(side="right")

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

        others = tk.Frame(right, bg=CARD)

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

            box = tk.Frame(
                others,
                bg=CARD2,
                highlightbackground=BORDER,
                highlightthickness=1
            )

            box.grid(
                row=0,
                column=index,
                padx=3,
                sticky="nsew"
            )

            photo = load_photo(
                IMAGES[name.lower()],
                (120, 85),
                mode="cover",
                background=CARD2
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
            ).pack(pady=6)

            others.columnconfigure(index, weight=1)

        # ----------------------------------------------------
        # BEYOND BHUTAN
        # ----------------------------------------------------

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
            font=("Georgia", 27)
        ).pack(
            side="left",
            padx=18,
            pady=15
        )

        beyond_text = tk.Frame(beyond, bg=CARD)
        beyond_text.pack(side="left", pady=15)

        tk.Label(
            beyond_text,
            text="Beyond Bhutan",
            bg=CARD,
            fg=LIGHT_GOLD,
            font=("Georgia", 14, "bold")
        ).pack(anchor="w")

        tk.Label(
            beyond_text,
            text="Explore mythology from other cultures",
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w")

        for country in ["India", "Tibet", "Nepal", "Asia"]:

            create_pill(
                beyond,
                country
            ).pack(
                side="right",
                padx=5,
                pady=25
            )

        canvas.yview_moveto(0)

    # Show the main Regions page when opened
    show_main_regions()

    parent.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
