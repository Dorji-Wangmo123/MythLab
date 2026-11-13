
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import sqlite3

import customtkinter as ctk
from PIL import Image, ImageTk, ImageOps


# ============================================================
# MYTHLAB - FAVOURITES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
DB_FILE = BASE_DIR / "mythlab.db"

BG = "#031722"
CARD_BG = "#062033"
CARD_BORDER = "#315366"

GOLD = "#f3bd55"
GOLD_LIGHT = "#ffd36b"

WHITE = "#f7f1e4"
MUTED = "#b9c3c9"
RED = "#ff5964"
BUTTON_BG = "#092536"

ctk.set_appearance_mode("dark")


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    return sqlite3.connect(DB_FILE)


def get_user_id(username):

    if not username:
        return None

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE LOWER(username) = LOWER(?)",
            (username.strip(),)
        )

        result = cursor.fetchone()

        return result[0] if result else None

    finally:
        conn.close()


def prepare_favourites_table():

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favourites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                item_type TEXT NOT NULL,
                item_id INTEGER,
                title TEXT,
                description TEXT,
                region TEXT,
                image TEXT
            )
        """)

        existing_columns = {
            row[1] for row in cursor.execute(
                "PRAGMA table_info(favourites)"
            ).fetchall()
        }

        required_columns = {
            "title": "TEXT",
            "description": "TEXT",
            "region": "TEXT",
            "image": "TEXT"
        }

        for name, column_type in required_columns.items():

            if name not in existing_columns:
                cursor.execute(
                    f"ALTER TABLE favourites ADD COLUMN {name} {column_type}"
                )

        conn.commit()

    finally:
        conn.close()


# ============================================================
# APPLICATION
# ============================================================

class MythLabFavourites:

    def __init__(self, parent, username=None):

        self.root = parent
        self.username = username
        self.user_id = None

        prepare_favourites_table()

        if username:
            self.user_id = get_user_id(username)

        self.favourites = []

        self.current_filter = "All"
        self.search_var = tk.StringVar()

        self.image_references = []
        self.banner_image = None
        self.banner_source = None

        self.load_favourites()
        self.create_main_area()

        self.search_var.trace_add(
            "write",
            self.search_changed
        )

        self.update_filter_buttons()
        self.refresh_cards()

    # ========================================================
    # LOAD FAVOURITES
    # ========================================================

    def load_favourites(self):

        self.favourites = []

        if not self.user_id:
            return

        conn = get_connection()

        try:
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

        finally:
            conn.close()

        for row in rows:

            self.favourites.append({
                "id": row[0],
                "type": row[1] or "",
                "item_id": row[2],
                "title": row[3] or "",
                "description": row[4] or "",
                "region": row[5] or "",
                "image": row[6] or ""
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

        self.create_banner()
        self.create_filter_area()

        # Cards canvas
        self.cards_canvas = tk.Canvas(
            self.main,
            bg=BG,
            highlightthickness=0,
            bd=0
        )

        self.cards_canvas.place(
            x=18,
            y=245,
            relwidth=1,
            width=-36,
            height=450
        )

        self.cards_scrollbar = tk.Scrollbar(
            self.main,
            orient="vertical",
            command=self.cards_canvas.yview
        )

        self.cards_scrollbar.place(
            relx=1,
            x=-8,
            y=245,
            width=10,
            height=450,
            anchor="ne"
        )

        self.cards_canvas.configure(
            yscrollcommand=self.cards_scrollbar.set
        )

        self.cards_area = tk.Frame(
            self.cards_canvas,
            bg=BG
        )

        self.cards_window = self.cards_canvas.create_window(
            (0, 0),
            window=self.cards_area,
            anchor="nw"
        )

        self.cards_area.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.cards_canvas.bind(
            "<Configure>",
            self.resize_cards_area
        )

        self.cards_canvas.bind(
            "<Enter>",
            self.enable_mousewheel
        )

        self.cards_canvas.bind(
            "<Leave>",
            self.disable_mousewheel
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
            y=715
        )

    # ========================================================
    # BANNER - RESPONSIVE IMAGE
    # ========================================================

    def create_banner(self):

        self.banner_canvas = tk.Canvas(
            self.main,
            height=180,
            bg="#071f2e",
            highlightthickness=0
        )

        self.banner_canvas.place(
            x=0,
            y=0,
            relwidth=1
        )

        banner_path = ASSETS_DIR / "banner.jpg"

        if banner_path.exists():

            try:
                self.banner_source = Image.open(
                    banner_path
                ).convert("RGB")

            except Exception as error:
                print("Banner error:", error)

        self.banner_canvas.bind(
            "<Configure>",
            self.resize_banner
        )

    def resize_banner(self, event):

        if event.width < 2:
            return

        self.banner_canvas.delete("all")

        if self.banner_source:

            try:
                image = ImageOps.fit(
                    self.banner_source,
                    (event.width, 180),
                    method=Image.Resampling.LANCZOS
                )

                self.banner_image = ImageTk.PhotoImage(image)

                self.banner_canvas.create_image(
                    0,
                    0,
                    anchor="nw",
                    image=self.banner_image
                )

            except Exception as error:
                print("Banner resize error:", error)

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
    # ROUNDED FILTERS AND SEARCH
    # ========================================================

    def create_filter_area(self):

        self.filter_buttons = {}

        buttons = [
            ("All", 45, 90),
            ("Myths", 150, 90),
            ("Creatures", 255, 125),
            ("Regions", 395, 100)
        ]

        for name, x, width in buttons:

            button = ctk.CTkButton(
                self.main,
                text=("♥  " if name == "All" else "") + name,
                width=width,
                height=38,
                corner_radius=14,
                font=("Segoe UI", 10, "bold"),
                fg_color=BUTTON_BG,
                hover_color="#183c50",
                text_color=WHITE,
                command=lambda n=name: self.set_filter(n)
            )

            button.place(
                x=x,
                y=194
            )

            self.filter_buttons[name] = button

        # Rounded search box. Icon and input stay inside the frame.
        self.search_frame = ctk.CTkFrame(
            self.main,
            width=330,
            height=40,
            corner_radius=14,
            fg_color="#0a2433",
            border_width=1,
            border_color="#526b78"
        )
        self.search_frame.place(relx=1, x=-25, y=194, anchor="ne")
        self.search_frame.pack_propagate(False)

        self.search_icon = tk.Label(
            self.search_frame,
            text="⌕",
            font=("Segoe UI Symbol", 21),
            bg="#0a2433",
            fg=GOLD
        )
        self.search_icon.pack(side="left", padx=(12, 5))

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            textvariable=self.search_var,
            height=30,
            corner_radius=10,
            border_width=0,
            fg_color="#0a2433",
            text_color=WHITE,
            placeholder_text="Search favourites...",
            placeholder_text_color=MUTED,
            font=("Segoe UI", 10)
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=5)

        # On narrow windows move the search below the category buttons.
        self.main.bind("<Configure>", self.layout_search)

    def layout_search(self, event=None):
        width = self.main.winfo_width()
        if width < 2:
            return
        if width < 850:
            search_y = 242
            cards_y = 294
        else:
            search_y = 194
            cards_y = 245
        self.search_frame.place_configure(y=search_y, width=min(330, max(170, width - 50)))
        if hasattr(self, "cards_canvas"):
            self.cards_canvas.place_configure(y=cards_y)
            self.cards_scrollbar.place_configure(y=cards_y)

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
                    fg_color=GOLD_LIGHT,
                    text_color="#132330",
                    hover_color=GOLD
                )

            else:

                button.configure(
                    fg_color=BUTTON_BG,
                    text_color=WHITE,
                    hover_color="#183c50"
                )

    # ========================================================
    # SEARCH
    # ========================================================

    def search_changed(self, *args):
        self.refresh_cards()

    # ========================================================
    # CARD IMAGE
    # ========================================================

    def load_card_image(self, filename):
        """Load saved images even if the file extension differs."""
        if not filename:
            return None

        requested = Path(str(filename)).name
        candidate = ASSETS_DIR / requested

        if not candidate.is_file():
            # The Myths page may save .png while the actual asset is .jpg.
            # Match the image stem without changing existing saved favourites.
            def normalise(value):
                return "".join(ch.lower() for ch in value if ch.isalnum())

            stem = normalise(Path(requested).stem)
            candidate = None
            if ASSETS_DIR.is_dir():
                for path in ASSETS_DIR.iterdir():
                    if (path.is_file()
                            and path.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")
                            and normalise(path.stem) == stem):
                        candidate = path
                        break

        if candidate is None or not candidate.is_file():
            print("IMAGE NOT FOUND:", requested)
            return None

        try:
            with Image.open(candidate) as source:
                image = ImageOps.fit(
                    source.convert("RGB"),
                    (290, 128),
                    method=Image.Resampling.LANCZOS
                )
            return ImageTk.PhotoImage(image)
        except Exception as error:
            print("Image error:", candidate, error)
            return None

    # ========================================================
    # REFRESH CARDS
    # ========================================================

    def refresh_cards(self):

        for widget in self.cards_area.winfo_children():
            widget.destroy()

        self.image_references = []

        query = self.search_var.get().strip().lower()

        results = []

        for item in self.favourites:

            if self.current_filter == "All":
                type_match = True

            else:
                type_match = (
                    item["type"].lower()
                    == self.current_filter[:-1].lower()
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

        # Three cards fit inside the main content area.
        card_width = 290
        card_height = 255
        gap_x = 15
        gap_y = 18
        cards_per_row = 3

        for index, item in enumerate(results):

            row = index // cards_per_row
            column = index % cards_per_row

            x = column * (card_width + gap_x)
            y = row * (card_height + gap_y)

            self.create_card(item, x, y)

        if results:

            rows = (
                len(results) + cards_per_row - 1
            ) // cards_per_row

            content_height = (
                rows * card_height
                + (rows - 1) * gap_y
            )

        else:

            content_height = 230

            tk.Label(
                self.cards_area,
                text="♡",
                font=("Segoe UI Symbol", 42),
                bg=BG,
                fg=GOLD
            ).place(
                x=0,
                y=35,
                relwidth=1
            )

            tk.Label(
                self.cards_area,
                text="No favourites yet",
                font=("Georgia", 19, "bold"),
                bg=BG,
                fg=WHITE
            ).place(
                x=0,
                y=105,
                relwidth=1
            )

            tk.Label(
                self.cards_area,
                text=(
                    "Explore myths, creatures and regions, "
                    "then add them to your favourites."
                ),
                font=("Segoe UI", 10),
                bg=BG,
                fg=MUTED,
                wraplength=600
            ).place(
                x=0,
                y=145,
                relwidth=1
            )

        self.cards_area.configure(
            height=content_height
        )

        self.cards_canvas.configure(
            scrollregion=(0, 0, self.cards_canvas.winfo_width(), content_height)
        )

        self.cards_canvas.yview_moveto(0)

        count = len(results)

        self.count_label.configure(
            text=(
                f"✦  You have {count} favourite item"
                + ("" if count == 1 else "s")
            )
        )

    # ========================================================
    # CREATE CARD
    # ========================================================

    def create_card(self, item, x, y):

        card = tk.Frame(
            self.cards_area,
            width=290,
            height=255,
            bg=CARD_BG,
            highlightbackground=CARD_BORDER,
            highlightthickness=1
        )

        card.place(x=x, y=y)

        photo = self.load_card_image(item["image"])

        if photo:

            self.image_references.append(photo)

            tk.Label(
                card,
                image=photo,
                bg=CARD_BG
            ).place(
                x=0,
                y=0,
                width=290,
                height=128
            )

        else:

            tk.Label(
                card,
                text="Image not found",
                font=("Georgia", 15, "bold"),
                bg="#12394a",
                fg=GOLD_LIGHT
            ).place(
                x=0,
                y=0,
                width=290,
                height=128
            )

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
            width=265,
            height=25
        )

        tk.Label(
            card,
            text=item["description"],
            font=("Segoe UI", 8),
            bg=CARD_BG,
            fg=MUTED,
            justify="left",
            anchor="nw",
            wraplength=260
        ).place(
            x=12,
            y=164,
            width=265,
            height=45
        )

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
            width=140,
            height=24
        )

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
            command=lambda data=item: self.view_item(data)
        ).place(
            x=232,
            y=212,
            width=25,
            height=28
        )

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
            command=lambda data=item: self.remove_favourite(data)
        ).place(
            x=262,
            y=212,
            width=25,
            height=28
        )

        # Make the card clickable
        def open_item(event=None):
            self.view_item(item)

        def make_clickable(widget):

            if isinstance(widget, tk.Button):
                return

            widget.bind("<Button-1>", open_item)
            widget.configure(cursor="hand2")

            for child in widget.winfo_children():
                make_clickable(child)

        def highlight(event=None):
            card.configure(highlightbackground=GOLD_LIGHT)

        def unhighlight(event=None):

            px, py = card.winfo_pointerxy()
            under_pointer = card.winfo_containing(px, py)

            if (
                under_pointer is not None
                and str(under_pointer).startswith(str(card))
            ):
                return

            card.configure(highlightbackground=CARD_BORDER)

        make_clickable(card)

        card.bind("<Enter>", highlight)
        card.bind("<Leave>", unhighlight)

    # ========================================================
    # VIEW ITEM
    # ========================================================

    def view_item(self, item):
        """Open the selected favourite's story, not the general Myths page."""
        item_type = str(item.get("type", "")).strip().lower()
        title = str(item.get("title", "")).strip()

        if item_type in ("myth", "myths"):
            open_detail = getattr(self.root, "open_favourite_detail", None)
            if callable(open_detail) and title:
                # The detail page handles its own Back button to Favourites.
                detail_titles = {
                    "the legend of paro taktsang": "Paro Taktsang",
                    "jomo (aum jomo)": "Jomo",
                }
                open_detail(detail_titles.get(title.casefold(), title))
                return

        # Other favourite types retain their existing navigation.
        open_page = getattr(self.root, "open_mythlab_page", None)
        if callable(open_page):
            if item_type in ("creature", "creatures"):
                open_page("Creatures")
                return
            if item_type in ("region", "regions"):
                open_page("Regions")
                return

        self.show_item_information(item)

    def show_item_information(self, item):

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

        try:
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM favourites
                WHERE id = ? AND user_id = ?
            """, (
                item["id"],
                self.user_id
            ))

            conn.commit()

        finally:
            conn.close()

        self.load_favourites()
        self.refresh_cards()

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

        self.cards_canvas.unbind_all("<MouseWheel>")
        self.cards_canvas.unbind_all("<Button-4>")
        self.cards_canvas.unbind_all("<Button-5>")

    def scroll_mousewheel(self, event):

        self.cards_canvas.yview_scroll(
            int(-event.delta / 120),
            "units"
        )

    def scroll_up_linux(self, event):
        self.cards_canvas.yview_scroll(-3, "units")

    def scroll_down_linux(self, event):
        self.cards_canvas.yview_scroll(3, "units")


# ============================================================
# RUN DIRECTLY FOR TESTING
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()
    root.title("MythLab - Favourites")
    root.geometry("1200x900")

    app = MythLabFavourites(root)

    root.mainloop()
