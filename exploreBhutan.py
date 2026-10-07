#exploreBhutan.py code
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from PIL import Image, ImageTk, ImageOps


# ============================================================
# MYTHLAB - REGIONS / OTHER DZONGKHAGS
# Tkinter + Pillow
# ============================================================

ROOT = Path(__file__).resolve().parent

# IMPORTANT:
# Your images should be inside:
#
# mythlib/
#     main.py
#     images/
#         welcome.png
#         explore_bhutan.png
#         bhutan map.png
#         thimphu_dzongkha.png
#         punakha.png
#         bumthang.png
#         kyichu lhakhang.png
#         etc.

IMAGE_FOLDER = ROOT / "images"


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

    # Main header
    "hero": "explore_bhutan.png",

    # Explore Bhutan title background
    "explore_background": "welcome.png",

    # Bhutan map
    "map": [
        "bhutan map.png",
        "bhutan_map.png"
    ],

    # Paro
    "paro": [
        "paro_taktsang.png",
        "jomolhari.png",
        "welcome.png"
    ],

    # Dragon
    "dragon": [
        "thunder_dragon.png",
        "druk (3).png",
        "creatures.png"
    ],

    # Bumthang
    "bumthang": [
        "bumthang.png",
        "welcome.png",
        "jomolhari.png"
    ],

    # Trashigang
    "trashigang": [
        "welcome.png",
        "jomolhari.png"
    ],

    # Trashiyangtse
    "trashiyangtse": [
        "jomolhari.png",
        "welcome.png"
    ],

    # Mongar
    "mongar": [
        "welcome.png",
        "jomolhari.png"
    ],

    # Samdrup Jongkhar
    "samdrup jongkhar": [
        "welcome.png",
        "jomolhari.png"
    ],

    # Zhemgang
    "zhemgang": [
        "black_mountain (2).png",
        "welcome.png"
    ],

    # Trongsa
    "trongsa": [
        "jomolhari.png",
        "welcome.png"
    ],

    # Wangdue Phodrang
    "wangdue phodrang": [
        "welcome.png",
        "jomolhari.png"
    ],

    # Thimphu
    "thimphu": [
        "thimphu_dzongkha.png",
        "welcome.png",
        "jomolhari.png"
    ],

    # Punakha
    "punakha": [
        "punakha.png",
        "welcome.png",
        "jomolhari.png"
    ],

    # Kyichu Lhakhang
    "kyichu": [
        "kyichu lhakhang.png",
        "kyichu_lhakhang.png",
        "kyichu.png"
    ]
}


# ============================================================
# MAIN APPLICATION
# ============================================================

class MythLab(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title("MythLab - Regions")
        self.geometry("1280x910")
        self.minsize(1100, 760)
        self.configure(bg=BG)

        # Keep PhotoImage objects alive
        self.image_refs = []

        # Build sidebar
        self.build_sidebar()

        # Main content
        self.content = tk.Frame(
            self,
            bg=BG
        )

        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Show regions page
        self.show_regions()


    # ========================================================
    # IMAGE HELPERS
    # ========================================================

    def find_image(self, names):

        if isinstance(names, str):
            names = [names]

        # ----------------------------------------------------
        # 1. Check exact filename
        # ----------------------------------------------------

        for name in names:

            path = IMAGE_FOLDER / name

            if path.is_file():
                print("IMAGE FOUND:", path)
                return path

            path = ROOT / name

            if path.is_file():
                print("IMAGE FOUND:", path)
                return path


        # ----------------------------------------------------
        # 2. Search recursively - case insensitive
        # ----------------------------------------------------

        for name in names:

            target = Path(name).name.lower()

            try:

                for path in ROOT.rglob("*"):

                    if path.is_file():

                        if path.name.lower() == target:

                            print("IMAGE FOUND:", path)

                            return path

            except Exception:
                pass


        # ----------------------------------------------------
        # 3. Flexible search
        #    Spaces and underscores are treated the same
        # ----------------------------------------------------

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

                    if path.suffix.lower() not in [
                        ".png",
                        ".jpg",
                        ".jpeg",
                        ".webp"
                    ]:
                        continue

                    current = path.stem.lower()

                    current = (
                        current
                        .replace("_", " ")
                        .replace("-", " ")
                        .strip()
                    )

                    if current == target:

                        print("IMAGE FOUND:", path)

                        return path

            except Exception:
                pass


        print("IMAGE NOT FOUND:", names)
        print("Project folder:", ROOT)
        print("Image folder:", IMAGE_FOLDER)

        return None


    def photo(self, names, size):

        path = self.find_image(names)

        if not path:

            print("IMAGE NOT FOUND:", names)
            print("Looking inside:", IMAGE_FOLDER)

            return None

        try:

            img = Image.open(path).convert("RGB")

            img = ImageOps.fit(
                img,
                size,
                method=Image.Resampling.LANCZOS
            )

            p = ImageTk.PhotoImage(img)

            self.image_refs.append(p)

            return p

        except Exception as e:

            print("IMAGE ERROR:", path)
            print(e)

            return None


    # ========================================================
    # SIDEBAR
    # ========================================================

    def build_sidebar(self):

        side = tk.Frame(
            self,
            bg=SIDEBAR,
            width=208
        )

        side.pack(
            side="left",
            fill="y"
        )

        side.pack_propagate(False)


        # Dragon icon
        tk.Label(
            side,
            text="🐉",
            bg=SIDEBAR,
            fg=GOLD,
            font=("Segoe UI Symbol", 28)
        ).pack(
            pady=(15, 0)
        )


        # Application name
        tk.Label(
            side,
            text="MythLab",
            bg=SIDEBAR,
            fg=LIGHT_GOLD,
            font=("Georgia", 22, "bold")
        ).pack()


        tk.Label(
            side,
            text="Explore. Learn. Believe.",
            bg=SIDEBAR,
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(
            pady=(0, 24)
        )


        # Menu
        menu = [

            ("⌂", "Home", self.home),

            ("▤", "Myths", self.placeholder),

            ("🐉", "Creatures", self.placeholder),

            ("◎", "Regions", self.show_regions),

            ("▣", "My Tasks", self.placeholder),

            ("?", "Quiz", self.placeholder),

            ("♡", "Favourites", self.placeholder),

            ("ⓘ", "About", self.placeholder),

        ]


        for icon, name, command in menu:

            active = name == "Regions"

            row_bg = "#5b4a2d" if active else SIDEBAR

            row = tk.Frame(
                side,
                bg=row_bg,
                height=43
            )

            row.pack(
                fill="x",
                padx=10,
                pady=3
            )

            row.pack_propagate(False)


            tk.Label(
                row,
                text=icon,
                width=3,
                bg=row_bg,
                fg=LIGHT_GOLD if active else TEXT,
                font=("Segoe UI Symbol", 15)
            ).pack(
                side="left"
            )


            tk.Button(
                row,
                text=name,
                command=command,
                anchor="w",
                relief="flat",
                bd=0,
                bg=row_bg,
                fg=LIGHT_GOLD if active else TEXT,
                activebackground=row_bg,
                activeforeground=LIGHT_GOLD,
                font=("Segoe UI", 10)
            ).pack(
                side="left",
                fill="both",
                expand=True
            )


        # Bottom decoration
        tk.Label(
            side,
            text="╱╲╱╲╱╲",
            bg=SIDEBAR,
            fg="#2b4658",
            font=("Georgia", 25)
        ).pack(
            side="bottom",
            pady=(0, 18)
        )


        tk.Label(
            side,
            text="Every myth is a door\nto a deeper wisdom.",
            bg=SIDEBAR,
            fg=LIGHT_GOLD,
            justify="left",
            font=("Georgia", 10, "italic")
        ).pack(
            side="bottom",
            pady=4
        )


        tk.Label(
            side,
            text="— Bhutanese Wisdom",
            bg=SIDEBAR,
            fg=MUTED,
            font=("Segoe UI", 8)
        ).pack(
            side="bottom"
        )


    # ========================================================
    # CLEAR CONTENT
    # ========================================================

    def clear(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        self.image_refs.clear()


    # ========================================================
    # SCROLL PAGE
    # ========================================================

    def scroll_page(self):

        holder = tk.Frame(
            self.content,
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


        bar = tk.Scrollbar(
            holder,
            orient="vertical",
            command=canvas.yview
        )


        canvas.configure(
            yscrollcommand=bar.set
        )


        bar.pack(
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
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )


        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfigure(
                window,
                width=e.width
            )
        )


        def wheel(event):

            canvas.yview_scroll(
                -int(event.delta / 120),
                "units"
            )


        canvas.bind_all(
            "<MouseWheel>",
            wheel
        )


        return page


    # ========================================================
    # TITLE BLOCK
    # ========================================================

    def title_block(self, parent, title, subtitle):

        # ----------------------------------------------------
        # Explore Bhutan title with welcome.png background
        # ----------------------------------------------------

        if title == "Explore Bhutan":

            box = tk.Frame(
                parent,
                bg=BG,
                height=220
            )

            box.pack(
                fill="x",
                padx=25,
                pady=(22, 16)
            )

            box.pack_propagate(False)


            # ------------------------------------------------
            # Background image
            # ------------------------------------------------

            background = self.photo(
                IMAGES["explore_background"],
                (1200, 220)
            )


            if background:

                bg_label = tk.Label(
                    box,
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


            # ------------------------------------------------
            # Title area
            # ------------------------------------------------

            title_area = tk.Frame(
                box,
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
                text=title,
                bg="#031521",
                fg=LIGHT_GOLD,
                font=("Georgia", 29, "bold")
            ).pack(
                anchor="w"
            )


            tk.Label(
                words,
                text=subtitle,
                bg="#031521",
                fg=TEXT,
                font=("Segoe UI", 10)
            ).pack(
                anchor="w",
                pady=(4, 0)
            )


            return box


        # ----------------------------------------------------
        # Original title block for all other pages
        # ----------------------------------------------------

        box = tk.Frame(
            parent,
            bg=BG
        )

        box.pack(
            fill="x",
            padx=38,
            pady=(22, 16)
        )


        tk.Label(
            box,
            text="⌘",
            bg=BG,
            fg=GOLD,
            font=("Segoe UI Symbol", 28)
        ).pack(
            side="left",
            padx=(0, 12)
        )


        words = tk.Frame(
            box,
            bg=BG
        )


        words.pack(
            side="left"
        )


        tk.Label(
            words,
            text=title,
            bg=BG,
            fg=LIGHT_GOLD,
            font=("Georgia", 29, "bold")
        ).pack(
            anchor="w"
        )


        tk.Label(
            words,
            text=subtitle,
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            pady=(4, 0)
        )


        return box


    # ========================================================
    # HEADER IMAGE
    # ========================================================

    def header_image(self, parent):

        p = self.photo(
            IMAGES["hero"],
            (1050, 180)
        )


        frame = tk.Frame(
            parent,
            bg="#082333",
            height=180
        )


        frame.pack(
            fill="x",
            padx=25,
            pady=(0, 15)
        )


        frame.pack_propagate(False)


        if p:

            tk.Label(
                frame,
                image=p,
                bg="#082333"
            ).pack(
                fill="both",
                expand=True
            )

        else:

            tk.Label(
                frame,
                text="BHUTAN • MYTHS • LEGENDS",
                bg="#082333",
                fg=LIGHT_GOLD,
                font=("Georgia", 24, "bold")
            ).pack(
                expand=True
            )


    # ========================================================
    # PILL
    # ========================================================

    def pill(self, parent, text):

        return tk.Button(
            parent,
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
    # PAGE 1 - EXPLORE BHUTAN
    # ========================================================

    def show_regions(self):

        self.clear()

        page = self.scroll_page()


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


        # Title
        self.title_block(
            page,
            "Explore Bhutan",
            "Discover the myths, legends, creatures and sacred stories\n"
            "connected to the 20 Dzongkhags of Bhutan."
        )


        # Body
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


        # ====================================================
        # LEFT - MAP
        # ====================================================

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
        map_photo = self.photo(
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
                map_frame,
                text="Please place:\n\n"
                     "bhutan map.png\n\n"
                     "inside the images folder.",
                bg="#071c29",
                fg=MUTED,
                font=("Segoe UI", 9),
                justify="center"
            ).pack(
                expand=True
            )


        # Map description
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


        # ====================================================
        # ALL DZONGKHAGS
        # ====================================================

        sec = tk.Frame(
            left,
            bg=CARD
        )


        sec.pack(
            fill="x",
            padx=12,
            pady=(0, 18)
        )


        tk.Label(
            sec,
            text="✥  All Dzongkhags",
            bg=CARD,
            fg=LIGHT_GOLD,
            font=("Georgia", 13, "bold")
        ).pack(
            anchor="w",
            pady=(5, 8)
        )


        # Complete 20 Dzongkhags
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
            sec,
            bg=CARD
        )


        grid.pack(
            fill="x"
        )


        for i, name in enumerate(names):

            b = tk.Button(
                grid,
                text=name,
                command=lambda n=name:
                self.open_dzongkhag(n),

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


            b.grid(
                row=i // 5,
                column=i % 5,
                padx=4,
                pady=4,
                sticky="ew"
            )


        for c in range(5):

            grid.columnconfigure(
                c,
                weight=1
            )


        # ====================================================
        # RIGHT - FEATURED
        # ====================================================

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


        fp = self.photo(
            IMAGES["paro"],
            (390, 155)
        )


        if fp:

            tk.Label(
                right,
                image=fp,
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


        self.small_card(
            popular,
            IMAGES["paro"],
            "The Tiger's Nest",
            "Myth",
            0
        )


        self.small_card(
            popular,
            IMAGES["dragon"],
            "Paro Dragon",
            "Creature",
            1
        )


        self.small_card(
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
            command=self.show_other_dzongkhags,
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


        for i, name in enumerate(
            ["Thimphu", "Punakha", "Bumthang"]
        ):

            self.other_card(
                others,
                name,
                i
            )


        # ====================================================
        # BEYOND BHUTAN
        # ====================================================

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


        text = tk.Frame(
            beyond,
            bg=CARD
        )


        text.pack(
            side="left",
            pady=15
        )


        tk.Label(
            text,
            text="Beyond Bhutan",
            bg=CARD,
            fg=LIGHT_GOLD,
            font=("Georgia", 14, "bold")
        ).pack(
            anchor="w"
        )


        tk.Label(
            text,
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

            self.pill(
                beyond,
                country
            ).pack(
                side="right",
                padx=5,
                pady=25
            )


    # ========================================================
    # SMALL CARD
    # ========================================================

    def small_card(
        self,
        parent,
        names,
        title,
        tag,
        col
    ):

        box = tk.Frame(
            parent,
            bg=CARD2,
            highlightbackground=BORDER,
            highlightthickness=1
        )


        box.grid(
            row=0,
            column=col,
            padx=3,
            sticky="nsew"
        )


        # Equal image size for Popular in Paro
        p = self.photo(
            names,
            (120, 85)
        )


        if p:

            tk.Label(
                box,
                image=p,
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


        parent.columnconfigure(
            col,
            weight=1
        )


    # ========================================================
    # OTHER CARD
    # ========================================================

    def other_card(
        self,
        parent,
        name,
        col
    ):

        box = tk.Frame(
            parent,
            bg=CARD2,
            highlightbackground=BORDER,
            highlightthickness=1
        )


        box.grid(
            row=0,
            column=col,
            padx=4,
            sticky="nsew"
        )


        key = name.lower()


        if key in IMAGES:

            image_names = IMAGES[key]

        else:

            image_names = IMAGES["hero"]


        # Equal image size for Thimphu, Punakha and Bumthang
        p = self.photo(
            image_names,
            (120, 85)
        )


        if p:

            tk.Label(
                box,
                image=p,
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


        parent.columnconfigure(
            col,
            weight=1
        )


    # ========================================================
    # PAGE 2 - OTHER DZONGKHAGS
    # ========================================================

    def show_other_dzongkhags(self):

        self.clear()

        page = self.scroll_page()


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
        self.title_block(
            page,
            "Other Dzongkhags",
            "Explore the unique myths, legends and sacred stories from\n"
            "Bhutan's other Dzongkhags."
        )


        # Header image
        self.header_image(page)


        # ====================================================
        # SEARCH AND FILTERS
        # ====================================================

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
            highlightbackground=BORDER,
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


        search.bind(
            "<FocusIn>",
            lambda e:
            search.delete(0, "end")
            if search.get().startswith("🔍")
            else None
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
                relief="solid",
                bd=1,
                font=("Segoe UI", 8),
                padx=13,
                pady=7
            ).pack(
                side="left",
                padx=4
            )


        # ====================================================
        # SECTION TITLE
        # ====================================================

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


        # ====================================================
        # DZONGKHAG GRID
        # ====================================================

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


        for i, (
            name,
            desc,
            imgs,
            tags
        ) in enumerate(data):

            self.dzongkhag_card(
                grid,
                name,
                desc,
                imgs,
                tags,
                i
            )


            grid.columnconfigure(
                i % 4,
                weight=1
            )


        # ====================================================
        # EXPLORE MORE
        # ====================================================

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


        txt = tk.Frame(
            more,
            bg=CARD
        )


        txt.pack(
            side="left",
            pady=15
        )


        tk.Label(
            txt,
            text="Explore More",
            bg=CARD,
            fg=LIGHT_GOLD,
            font=("Georgia", 14, "bold")
        ).pack(
            anchor="w"
        )


        tk.Label(
            txt,
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
            command=self.show_regions,
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
    # DZONGKHAG CARD
    # ========================================================

    def dzongkhag_card(
        self,
        parent,
        name,
        desc,
        imgs,
        tags,
        index
    ):

        box = tk.Frame(
            parent,
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


        p = self.photo(
            imgs,
            (260, 115)
        )


        if p:

            tk.Label(
                box,
                image=p,
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
            text=desc,
            bg=CARD,
            fg=TEXT,
            justify="left",
            font=("Segoe UI", 8)
        ).pack(
            anchor="w",
            padx=12
        )


        tagrow = tk.Frame(
            box,
            bg=CARD
        )


        tagrow.pack(
            fill="x",
            padx=9,
            pady=10
        )


        for tag in tags:

            self.pill(
                tagrow,
                tag
            ).pack(
                side="left",
                padx=2
            )


        tk.Button(
            tagrow,
            text="→",
            command=lambda n=name:
            self.open_dzongkhag(n),

            bg=BG,
            fg=LIGHT_GOLD,
            relief="solid",
            bd=1,
            font=("Segoe UI", 11)
        ).pack(
            side="right"
        )


        parent.rowconfigure(
            index // 4,
            weight=1
        )


    # ========================================================
    # NAVIGATION
    # ========================================================

    def open_dzongkhag(self, name):

        messagebox.showinfo(
            "MythLab",
            f"Opening {name}\n\n"
            f"You can connect this button to your "
            f"{name} detail page."
        )


    def home(self):

        messagebox.showinfo(
            "MythLab",
            "Home page"
        )


    def placeholder(self):

        messagebox.showinfo(
            "MythLab",
            "This page can be connected later."
        )


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":

    app = MythLab()

    app.mainloop()