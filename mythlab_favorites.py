# mythlab_favorites.py

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps
from pathlib import Path
import sqlite3


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
DB_FILE = BASE_DIR / "mythlab.db"


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    return sqlite3.connect(DB_FILE)


def get_user_id(username):

    if not username:
        return None

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE LOWER(username) = LOWER(?)",
        (username,)
    )

    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None


def prepare_favourites_table():

    conn = get_connection()
    cursor = conn.cursor()

    columns = [
        ("title", "TEXT"),
        ("description", "TEXT"),
        ("region", "TEXT"),
        ("image", "TEXT")
    ]

    for column_name, column_type in columns:

        try:

            cursor.execute(
                f"ALTER TABLE favourites ADD COLUMN "
                f"{column_name} {column_type}"
            )

        except sqlite3.OperationalError:
            pass

    conn.commit()
    conn.close()


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
# APPLICATION
# ============================================================

class MythLabFavourites:

    def __init__(self, parent, username=None):

        self.root = parent

        self.username = username
        self.user_id = None

        # Prepare database table
        prepare_favourites_table()

        # Get logged-in user's ID
        if self.username:
            self.user_id = get_user_id(self.username)

        # Load favourites from database
        self.load_favourites()

        # Add the original six favourites for a new user
        if self.user_id and not self.favourites:
            self.seed_default_favourites()

        self.current_filter = "All"

        self.search_var = tk.StringVar()

        self.search_var.trace_add(
            "write",
            self.search_changed
        )

        # Keep images alive
        self.image_references = []

        self.banner_image = None

        self.create_main_area()

        self.update_filter_buttons()

        self.refresh_cards()


    # ========================================================
    # SEED DEFAULT FAVOURITES
    # ========================================================

    def seed_default_favourites(self):

        default_favourites = [

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

        conn = get_connection()
        cursor = conn.cursor()

        for item in default_favourites:

            cursor.execute("""
                INSERT INTO favourites
                (
                    user_id,
                    item_type,
                    item_id,
                    title,
                    description,
                    region,
                    image
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                self.user_id,
                item["type"],
                0,
                item["title"],
                item["description"],
                item["region"],
                item["image"]
            ))

        conn.commit()
        conn.close()

        self.load_favourites()


    # ========================================================
    # LOAD FAVOURITES
    # ========================================================

    def load_favourites(self):

        self.favourites = []

        if not self.user_id:
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                item_type,
                item_id,
                title,
                description,
                region,
                image
            FROM favourites
            WHERE user_id = ?
            ORDER BY id DESC
        """, (self.user_id,))

        rows = cursor.fetchall()

        conn.close()

        for row in rows:

            (
                favourite_id,
                item_type,
                item_id,
                title,
                description,
                region,
                image
            ) = row

            self.favourites.append({
                "id": favourite_id,
                "type": item_type,
                "item_id": item_id,
                "title": title or "",
                "description": description or "",
                "region": region or "",
                "image": image or ""
            })


    # ========================================================
    # MAIN AREA
    # ========================================================

    def create_main_area(self):

        self.main = tk.Frame(
            self.root,
            bg=BG
        )

        self.main.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------------
        # Banner
        # ----------------------------------------------------

        self.create_banner()

        # ----------------------------------------------------
        # Filters
        # ----------------------------------------------------

        self.create_filter_area()

        # ----------------------------------------------------
        # Cards Canvas
        # ----------------------------------------------------

        self.cards_canvas = tk.Canvas(
            self.main,
            bg=BG,
            highlightthickness=0,
            bd=0
        )

        self.cards_canvas.place(
            x=18,
            y=245,
            relwidth=1.0,
            width=-36,
            height=450
        )

        # ----------------------------------------------------
        # Scrollbar
        # ----------------------------------------------------

        self.cards_scrollbar = tk.Scrollbar(
            self.main,
            orient="vertical",
            command=self.cards_canvas.yview
        )

        self.cards_scrollbar.place(
            relx=1.0,
            x=-8,
            y=245,
            width=10,
            height=450,
            anchor="ne"
        )

        self.cards_canvas.configure(
            yscrollcommand=self.cards_scrollbar.set
        )

        # ----------------------------------------------------
        # Cards Area
        # ----------------------------------------------------

        self.cards_area = tk.Frame(
            self.cards_canvas,
            bg=BG
        )

        self.cards_window = self.cards_canvas.create_window(
            (0, 0),
            window=self.cards_area,
            anchor="nw"
        )

        # ----------------------------------------------------
        # Update Scroll Region
        # ----------------------------------------------------

        self.cards_area.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.cards_canvas.bind(
            "<Configure>",
            self.resize_cards_area
        )

        # ----------------------------------------------------
        # Mouse Wheel
        # ----------------------------------------------------

        self.cards_canvas.bind(
            "<Enter>",
            self.enable_mousewheel
        )

        self.cards_canvas.bind(
            "<Leave>",
            self.disable_mousewheel
        )

        # ----------------------------------------------------
        # Count Label
        # ----------------------------------------------------

        self.count_label = tk.Label(
            self.main,
            text="",
            font=("Segoe UI", 10),
            bg=BG,
            fg=GOLD_LIGHT
        )

        self.count_label.place(
            x=20,
            y=715
        )


    # ========================================================
    # SCROLLING
    # ========================================================

    def update_scroll_region(self, event=None):

        self.cards_canvas.configure(
            scrollregion=self.cards_canvas.bbox("all")
        )


    def resize_cards_area(self, event):

        self.cards_canvas.itemconfigure(
            self.cards_window,
            width=event.width
        )


    def enable_mousewheel(self, event=None):

        self.cards_canvas.bind_all(
            "<MouseWheel>",
            self.scroll_mousewheel
        )

        self.cards_canvas.bind_all(
            "<Button-4>",
            self.scroll_up_linux
        )

        self.cards_canvas.bind_all(
            "<Button-5>",
            self.scroll_down_linux
        )


    def disable_mousewheel(self, event=None):

        self.cards_canvas.unbind_all(
            "<MouseWheel>"
        )

        self.cards_canvas.unbind_all(
            "<Button-4>"
        )

        self.cards_canvas.unbind_all(
            "<Button-5>"
        )


    def scroll_mousewheel(self, event):

        if event.delta:

            self.cards_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )


    def scroll_up_linux(self, event):

        self.cards_canvas.yview_scroll(
            -3,
            "units"
        )


    def scroll_down_linux(self, event):

        self.cards_canvas.yview_scroll(
            3,
            "units"
        )


    # ========================================================
    # BANNER
    # ========================================================

    def create_banner(self):

        banner_path = ASSETS_DIR / "banner.jpg"

        self.main.update_idletasks()

        banner_width = self.main.winfo_width()

        if banner_width <= 1:
            banner_width = MAIN_WIDTH

        self.banner_canvas = tk.Canvas(
            self.main,
            width=banner_width,
            height=BANNER_HEIGHT,
            bg="#071f2e",
            highlightthickness=0
        )

        self.banner_canvas.place(
            x=0,
            y=0,
            relwidth=1.0
        )

        if banner_path.exists():

            try:

                image = Image.open(
                    banner_path
                ).convert("RGB")

                image = ImageOps.fit(
                    image,
                    (
                        banner_width,
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

        # ----------------------------------------------------
        # Header Text
        # ----------------------------------------------------

        self.banner_canvas.create_text(
            45,
            65,
            anchor="w",
            text="My Favourites",
            fill=WHITE,
            font=("Segoe UI", 28, "bold")
        )

        self.banner_canvas.create_text(
            45,
            108,
            anchor="w",
            text="Your favourite myths, creatures, and regions",
            fill=MUTED,
            font=("Segoe UI", 12)
        )


    # ========================================================
    # FILTER AREA
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

        # ----------------------------------------------------
        # Search Box
        # ----------------------------------------------------

        search_frame = tk.Frame(
            self.main,
            bg="#0a2433",
            highlightbackground="#526b78",
            highlightthickness=1
        )

        search_frame.place(
            relx=1.0,
            x=-25,
            y=y,
            width=330,
            height=40,
            anchor="ne"
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

        # Remove old cards

        for widget in self.cards_area.winfo_children():

            widget.destroy()

        # Clear image references

        self.image_references = []

        # Search text

        query = (
            self.search_var
            .get()
            .strip()
            .lower()
        )

        results = []

        # ----------------------------------------------------
        # Filter favourites
        # ----------------------------------------------------

        for item in self.favourites:

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

        # ====================================================
        # CARD SIZE
        # ====================================================

        CARD_WIDTH = 325
        CARD_HEIGHT = 255

        CARD_GAP_X = 20
        CARD_GAP_Y = 18

        cards_per_row = 3

        # ----------------------------------------------------
        # Create Cards
        # ----------------------------------------------------

        for index, item in enumerate(results):

            row = index // cards_per_row

            column = index % cards_per_row

            x = column * (
                CARD_WIDTH + CARD_GAP_X
            )

            y = row * (
                CARD_HEIGHT + CARD_GAP_Y
            )

            self.create_card(
                item,
                x,
                y
            )

        # ====================================================
        # CONTENT SIZE
        # ====================================================

        if len(results) == 0:

            rows = 1

        else:

            rows = (
                len(results)
                + cards_per_row
                - 1
            ) // cards_per_row

        content_width = (

            cards_per_row
            * CARD_WIDTH

            +

            (cards_per_row - 1)
            * CARD_GAP_X
        )

        content_height = (

            rows
            * CARD_HEIGHT

            +

            (rows - 1)
            * CARD_GAP_Y
        )

        # ----------------------------------------------------
        # Force the area to the correct size
        # ----------------------------------------------------

        self.cards_area.configure(
            width=content_width,
            height=content_height
        )

        # ----------------------------------------------------
        # Set scroll region
        # ----------------------------------------------------

        self.cards_canvas.configure(
            scrollregion=(
                0,
                0,
                content_width,
                content_height
            )
        )

        # Always return to top

        self.cards_canvas.yview_moveto(0)

        # ====================================================
        # COUNT
        # ====================================================

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
            command=lambda data=item:
            self.remove_favourite(data)
        ).place(
            x=298,
            y=212,
            width=25,
            height=28
        )


    # ========================================================
    # VIEW ITEM
    # ========================================================

    def view_item(self, item):

        if hasattr(self.root, "open_mythlab_page"):

            item_type = item["type"].lower()

            if item_type == "myth":
                self.root.open_mythlab_page("Myths")

            elif item_type == "creature":
                self.root.open_mythlab_page("Creatures")

            elif item_type == "region":
                self.root.open_mythlab_page("Regions")

            else:
                messagebox.showinfo(
                    item["title"],
                    f"{item['title']}\n\n"
                    f"Type: {item['type']}\n"
                    f"Region: {item['region']}\n\n"
                    f"{item['description']}"
                )

        else:

            messagebox.showinfo(
                item["title"],
                f"{item['title']}\n\n"
                f"Type: {item['type']}\n"
                f"Region: {item['region']}\n\n"
                f"{item['description']}"
            )

    # ========================================================
    # REMOVE FAVOURITE
    # ========================================================

    def remove_favourite(self, item):

        answer = messagebox.askyesno(

            "Remove Favourite",

            f"Do you want to remove\n\n"
            f"'{item['title']}'\n\n"
            f"from your favourites?"
        )

        if not answer:
            return

        if not self.user_id:
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM favourites
            WHERE id = ? AND user_id = ?
        """, (
            item["id"],
            self.user_id
        ))

        conn.commit()
        conn.close()

        self.load_favourites()
        self.refresh_cards()


# ============================================================
# RUN DIRECTLY
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    root.title("MythLab - Favourites")

    root.geometry("1200x900")

    # Direct testing without a logged-in user
    # The actual application passes the username from main.py.
    app = MythLabFavourites(root)

    root.mainloop()