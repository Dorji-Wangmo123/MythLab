#mythlab_favorites.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps
from pathlib import Path


# ============================================================
# MYTHLAB - MY FAVOURITES
# ============================================================

APP_WIDTH = 1280
APP_HEIGHT = 800

SIDEBAR_WIDTH = 210
MAIN_WIDTH = APP_WIDTH - SIDEBAR_WIDTH

BANNER_HEIGHT = 180


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"


# ============================================================
# COLOURS
# ============================================================

BG = "#031722"
SIDEBAR_BG = "#041b29"
CARD_BG = "#062033"
CARD_BORDER = "#315366"

GOLD = "#f3bd55"
GOLD_LIGHT = "#ffd36b"

WHITE = "#f7f1e4"
MUTED = "#b9c3c9"

RED = "#ff5964"
BUTTON_BG = "#092536"


# ============================================================
# FAVOURITES
# ============================================================

favourites = [

    {
        "type": "Myth",
        "title": "The Legend of the Druk",
        "description": "A tale of the thunder dragon, the protector of Bhutan, who brings peace and prosperity to the land.",
        "region": "Thimphu",
        "image": "legend_druk.jpg"
    },

    {
        "type": "Creature",
        "title": "Druk",
        "description": "The sacred dragon of Bhutan, symbolising strength, protection and good fortune.",
        "region": "Bhutan",
        "image": "druk.jpg"
    },

    {
        "type": "Myth",
        "title": "The Black Necked Crane",
        "description": "A beautiful and sacred bird, believed to be a messenger between the human world and the divine.",
        "region": "Punakha",
        "image": "crane.jpg"
    },

    {
        "type": "Creature",
        "title": "Yeti",
        "description": "A mysterious creature said to live in the high mountains of the Himalayas.",
        "region": "Haa",
        "image": "yeti.jpg"
    },

    {
        "type": "Region",
        "title": "Paro",
        "description": "Known for its peaceful valleys, sacred sites and the presence of many legends.",
        "region": "Paro",
        "image": "paro.jpg"
    },

    {
        "type": "Myth",
        "title": "The Lady of the Lake",
        "description": "A spirit who appears at night by the lake, said to grant wishes but also test the hearts of the kind.",
        "region": "Trongsa",
        "image": "lady_lake.jpg"
    }
]


# ============================================================
# APPLICATION
# ============================================================

class MythLabFavourites:

    def __init__(self, root):

        self.root = root

        self.root.title("MythLab - My Favourites")

        self.root.geometry(
            f"{APP_WIDTH}x{APP_HEIGHT}"
        )

        self.root.resizable(False, False)

        self.root.configure(bg=BG)

        self.current_filter = "All"

        self.search_var = tk.StringVar()

        self.search_var.trace_add(
            "write",
            self.search_changed
        )

        # Keep image references alive
        self.image_references = []

        self.banner_image = None

        self.create_sidebar()

        self.create_main_area()

        self.update_filter_buttons()

        self.refresh_cards()


    # ========================================================
    # SIDEBAR
    # ========================================================

    def create_sidebar(self):

        sidebar = tk.Frame(
            self.root,
            width=SIDEBAR_WIDTH,
            height=APP_HEIGHT,
            bg=SIDEBAR_BG
        )

        sidebar.place(
            x=0,
            y=0
        )


        # Logo

        tk.Label(
            sidebar,
            text="🐉",
            font=("Segoe UI Emoji", 36),
            bg=SIDEBAR_BG,
            fg=GOLD
        ).place(
            x=75,
            y=18
        )


        tk.Label(
            sidebar,
            text="MythLab",
            font=("Georgia", 21, "bold"),
            bg=SIDEBAR_BG,
            fg=GOLD_LIGHT
        ).place(
            x=48,
            y=72
        )


        tk.Label(
            sidebar,
            text="Explore. Learn. Believe.",
            font=("Segoe UI", 9),
            bg=SIDEBAR_BG,
            fg=MUTED
        ).place(
            x=38,
            y=106
        )


        tk.Frame(
            sidebar,
            bg=GOLD,
            width=165,
            height=1
        ).place(
            x=23,
            y=132
        )


        # Menu

        menu_items = [

            ("⌂", "Home"),
            ("▣", "Myths"),
            ("🐉", "Creatures"),
            ("◉", "Regions"),
            ("☷", "My Tasks"),
            ("?", "Quiz"),
            ("♡", "Favourites"),
            ("ⓘ", "About")

        ]


        y = 151


        for icon, name in menu_items:

            active = name == "Favourites"

            row_bg = (
                "#3b3321"
                if active
                else SIDEBAR_BG
            )


            row = tk.Frame(
                sidebar,
                width=190,
                height=42,
                bg=row_bg,
                highlightthickness=1 if active else 0,
                highlightbackground=GOLD
            )

            row.place(
                x=10,
                y=y
            )


            tk.Label(
                row,
                text=icon,
                font=("Segoe UI Symbol", 18),
                bg=row_bg,
                fg=GOLD
            ).place(
                x=14,
                y=7
            )


            label = tk.Label(
                row,
                text=name,
                font=("Segoe UI", 11),
                bg=row_bg,
                fg=WHITE
            )

            label.place(
                x=58,
                y=9
            )


            row.bind(
                "<Button-1>",
                lambda event, n=name:
                self.menu_clicked(n)
            )


            label.bind(
                "<Button-1>",
                lambda event, n=name:
                self.menu_clicked(n)
            )


            y += 45


        # Bottom decoration

        tk.Label(
            sidebar,
            text="△  △  △",
            font=("Georgia", 34),
            bg=SIDEBAR_BG,
            fg="#173847"
        ).place(
            x=39,
            y=680
        )


        tk.Label(
            sidebar,
            text='"Every myth is a door\nto deeper wisdom."',
            font=("Georgia", 10, "italic"),
            justify="center",
            bg=SIDEBAR_BG,
            fg=GOLD_LIGHT
        ).place(
            x=25,
            y=720
        )


        tk.Label(
            sidebar,
            text="— Bhutanese Wisdom",
            font=("Segoe UI", 8),
            bg=SIDEBAR_BG,
            fg=MUTED
        ).place(
            x=62,
            y=765
        )


    # ========================================================
    # SIDEBAR BUTTONS
    # ========================================================

    def menu_clicked(self, name):

        if name == "Favourites":
            return


        messagebox.showinfo(
            "MythLab",
            f"You selected {name}.\n\n"
            "This page is currently the Favourites section."
        )


    # ========================================================
    # MAIN AREA
    # ========================================================

    def create_main_area(self):

        self.main = tk.Frame(
            self.root,
            width=MAIN_WIDTH,
            height=APP_HEIGHT,
            bg=BG
        )

        self.main.place(
            x=SIDEBAR_WIDTH,
            y=0
        )


        self.create_banner()

        self.create_filter_area()


        self.cards_area = tk.Frame(
            self.main,
            width=MAIN_WIDTH,
            height=530,
            bg=BG
        )

        self.cards_area.place(
            x=18,
            y=245
        )


        self.count_label = tk.Label(
            self.main,
            text="",
            font=("Segoe UI", 10),
            bg=BG,
            fg=GOLD_LIGHT
        )

        self.count_label.place(
            x=20,
            y=775
        )


    # ========================================================
    # BANNER
    # ========================================================
    # IMPORTANT:
    # banner.jpg ALREADY contains the title and description.
    # Therefore we DO NOT add text on top of it.
    # ========================================================

    def create_banner(self):

        banner_path = ASSETS_DIR / "banner.jpg"


        print(
            "Banner:",
            banner_path
        )


        self.banner_canvas = tk.Canvas(
            self.main,
            width=MAIN_WIDTH,
            height=BANNER_HEIGHT,
            bg="#071f2e",
            highlightthickness=0
        )

        self.banner_canvas.place(
            x=0,
            y=0
        )


        if banner_path.exists():

            try:

                image = Image.open(
                    banner_path
                ).convert("RGB")


                image = ImageOps.fit(
                    image,
                    (
                        MAIN_WIDTH,
                        BANNER_HEIGHT
                    ),
                    method=Image.Resampling.LANCZOS
                )


                self.banner_image = ImageTk.PhotoImage(
                    image
                )


                self.banner_canvas.create_image(
                    0,
                    0,
                    anchor="nw",
                    image=self.banner_image
                )


            except Exception as error:

                print(
                    "Banner error:",
                    error
                )

        else:

            print(
                "BANNER NOT FOUND:",
                banner_path
            )


            self.banner_canvas.create_text(
                MAIN_WIDTH // 2,
                BANNER_HEIGHT // 2,
                text="Banner image not found",
                fill=WHITE,
                font=("Segoe UI", 16)
            )


    # ========================================================
    # FILTER BUTTONS
    # ========================================================

    def create_filter_area(self):

        y = 194

        self.filter_buttons = {}


        buttons = [

            ("All", 45, 90),
            ("Myths", 150, 90),
            ("Creatures", 265, 125),
            ("Regions", 405, 100)

        ]


        for name, x, width in buttons:

            button = tk.Button(
                self.main,
                text=(
                    "♥  "
                    if name == "All"
                    else ""
                ) + name,
                font=("Segoe UI", 10, "bold"),
                relief="flat",
                bd=0,
                cursor="hand2",
                command=lambda n=name:
                self.set_filter(n)
            )


            button.place(
                x=x,
                y=y,
                width=width,
                height=38
            )


            self.filter_buttons[name] = button


        # Search

        search_frame = tk.Frame(
            self.main,
            bg="#0a2433",
            highlightbackground="#526b78",
            highlightthickness=1
        )


        search_frame.place(
            x=680,
            y=194,
            width=330,
            height=40
        )


        tk.Label(
            search_frame,
            text="⌕",
            font=("Segoe UI Symbol", 21),
            bg="#0a2433",
            fg=GOLD
        ).place(
            x=10,
            y=4
        )


        tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            bg="#0a2433",
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            bd=0
        ).place(
            x=48,
            y=8,
            width=265,
            height=24
        )


    # ========================================================
    # FILTER
    # ========================================================

    def set_filter(self, name):

        self.current_filter = name

        self.update_filter_buttons()

        self.refresh_cards()


    def update_filter_buttons(self):

        for name, button in self.filter_buttons.items():

            if name == self.current_filter:

                button.configure(
                    bg=GOLD_LIGHT,
                    fg="#132330"
                )

            else:

                button.configure(
                    bg=BUTTON_BG,
                    fg=WHITE
                )


    # ========================================================
    # SEARCH
    # ========================================================

    def search_changed(self, *args):

        self.refresh_cards()


    # ========================================================
    # LOAD CARD IMAGE
    # ========================================================

    def load_card_image(self, filename):

        image_path = ASSETS_DIR / filename


        if not image_path.exists():

            print(
                "IMAGE NOT FOUND:",
                image_path
            )

            return None


        try:

            image = Image.open(
                image_path
            ).convert("RGB")


            image = ImageOps.fit(
                image,
                (325, 128),
                method=Image.Resampling.LANCZOS
            )


            return ImageTk.PhotoImage(
                image
            )


        except Exception as error:

            print(
                "Image error:",
                error
            )

            return None


    # ========================================================
    # REFRESH CARDS
    # ========================================================

    def refresh_cards(self):

        for widget in self.cards_area.winfo_children():

            widget.destroy()


        self.image_references = []


        query = (
            self.search_var
            .get()
            .strip()
            .lower()
        )


        results = []


        for item in favourites:

            if self.current_filter == "All":

                type_match = True

            else:

                type_match = (
                    item["type"].lower()
                    ==
                    self.current_filter[:-1].lower()
                )


            search_match = (

                query == ""

                or query in item["title"].lower()

                or query in item["description"].lower()

                or query in item["region"].lower()

                or query in item["type"].lower()

            )


            if type_match and search_match:

                results.append(item)


        for index, item in enumerate(results):

            row = index // 3

            column = index % 3


            x = column * 345

            y = row * 273


            self.create_card(
                item,
                x,
                y
            )


        count = len(results)


        self.count_label.configure(
            text=
            f"✦  You have {count} favourite item"
            +
            (
                ""
                if count == 1
                else "s"
            )
        )


    # ========================================================
    # CREATE CARD
    # ========================================================

    def create_card(
        self,
        item,
        x,
        y
    ):

        CARD_WIDTH = 325
        CARD_HEIGHT = 255


        card = tk.Frame(
            self.cards_area,
            width=CARD_WIDTH,
            height=CARD_HEIGHT,
            bg=CARD_BG,
            highlightbackground=CARD_BORDER,
            highlightthickness=1
        )


        card.place(
            x=x,
            y=y
        )


        # ====================================================
        # IMAGE
        # ====================================================
        # NO EXTRA TYPE LABEL
        # NO EXTRA HEART
        #
        # Your image files already contain those elements.
        # ====================================================

        photo = self.load_card_image(
            item["image"]
        )


        if photo:

            self.image_references.append(
                photo
            )


            tk.Label(
                card,
                image=photo,
                bg=CARD_BG
            ).place(
                x=0,
                y=0,
                width=CARD_WIDTH,
                height=128
            )


        else:

            tk.Label(
                card,
                text="Image not found",
                font=("Georgia", 17, "bold"),
                bg="#12394a",
                fg=GOLD_LIGHT
            ).place(
                x=0,
                y=0,
                width=CARD_WIDTH,
                height=128
            )


        # ====================================================
        # TITLE
        # ====================================================

        tk.Label(
            card,
            text=item["title"],
            font=("Georgia", 12, "bold"),
            bg=CARD_BG,
            fg=WHITE,
            anchor="w"
        ).place(
            x=12,
            y=137,
            width=300,
            height=25
        )


        # ====================================================
        # DESCRIPTION
        # ====================================================

        tk.Label(
            card,
            text=item["description"],
            font=("Segoe UI", 8),
            bg=CARD_BG,
            fg=MUTED,
            justify="left",
            anchor="nw",
            wraplength=295
        ).place(
            x=12,
            y=164,
            width=300,
            height=45
        )


        # ====================================================
        # REGION
        # ====================================================

        tk.Label(
            card,
            text=f"⌖ {item['region']}",
            font=("Segoe UI", 9, "bold"),
            bg=CARD_BG,
            fg=GOLD_LIGHT,
            anchor="w"
        ).place(
            x=12,
            y=216,
            width=150,
            height=24
        )


        # ====================================================
        # VIEW BUTTON
        # ====================================================

        tk.Button(
            card,
            text="◉",
            font=("Segoe UI Symbol", 11),
            bg=CARD_BG,
            fg=WHITE,
            activebackground=CARD_BG,
            activeforeground=GOLD_LIGHT,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda data=item:
            self.view_item(data)
        ).place(
            x=268,
            y=212,
            width=25,
            height=28
        )


        # ====================================================
        # DELETE BUTTON
        # ====================================================

        tk.Button(
            card,
            text="♜",
            font=("Segoe UI Symbol", 11),
            bg=CARD_BG,
            fg=RED,
            activebackground=CARD_BG,
            activeforeground=RED,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=lambda title=item["title"]:
            self.remove_favourite(title)
        ).place(
            x=298,
            y=212,
            width=25,
            height=28
        )


    # ========================================================
    # VIEW
    # ========================================================

    def view_item(self, item):

        messagebox.showinfo(
            item["title"],

            f"{item['title']}\n\n"
            f"Type: {item['type']}\n"
            f"Region: {item['region']}\n\n"
            f"{item['description']}"
        )


    # ========================================================
    # REMOVE
    # ========================================================

    def remove_favourite(self, title):

        answer = messagebox.askyesno(
            "Remove Favourite",

            f"Do you want to remove\n\n"
            f"'{title}'\n\n"
            f"from your favourites?"
        )


        if not answer:
            return


        global favourites


        favourites = [

            item
            for item in favourites

            if item["title"] != title

        ]


        self.refresh_cards()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = MythLabFavourites(root)

    root.mainloop()