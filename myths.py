# myths.py

import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from PIL import Image, ImageTk, ImageOps

# ==================================================
# COLOURS
# ==================================================

BG = "#061b2b"
SIDEBAR = "#071522"
CARD = "#092333"
GOLD = "#d6a84f"
TEXT = "#f5ead0"
LIGHT_TEXT = "#c7c1b3"

# ==================================================
# IMAGE LOCATION
# ==================================================

PROJECT_DIR = Path(__file__).resolve().parent
IMAGE_DIR = PROJECT_DIR / "assets"

# Keep image objects in memory so Tkinter does not remove them.
image_refs = []

def show_myths(parent, open_detail=None):
    """
    Display the Myths page inside the main MythLab window.

    The page is built inside the parent frame instead of creating
    another Tk() window. This keeps MythLab as one application.
    """

    # Clear anything currently inside the page area.
    for widget in parent.winfo_children():
        widget.destroy()

    def find_image(filename):

        path = IMAGE_DIR / filename

        if path.exists():
            print("FOUND IMAGE:", path)
            return path

        path = PROJECT_DIR / filename

        if path.exists():
            print("FOUND IMAGE:", path)
            return path

        stem = Path(filename).stem.lower()
        extension = Path(filename).suffix.lower()

        if IMAGE_DIR.is_dir():

            for item in IMAGE_DIR.iterdir():

                if (
                    item.is_file()
                    and item.suffix.lower() == extension
                ):

                    item_stem = item.stem.lower()

                    if (
                        item_stem.startswith(stem)
                        or stem.startswith(item_stem)
                    ):

                        return item

        return None

    def load_image(filename, size):

        path = find_image(filename)

        if path is None:

            print("IMAGE NOT FOUND:", filename)
            print("Looking inside:", IMAGE_DIR)

            return None

        try:

            image = Image.open(path).convert("RGB")

            image = ImageOps.fit(
                image,
                size,
                method=Image.Resampling.LANCZOS
            )

            photo = ImageTk.PhotoImage(image)

            image_refs.append(photo)

            print(
                "IMAGE LOADED:",
                filename,
                photo
            )

            return photo

        except Exception as error:

            print("Could not load:", filename)
            print("Error:", error)

            return None

    def create_image(parent_widget, filename, size):

        photo = load_image(
            filename,
            size
        )

        print(
            "CREATE IMAGE:",
            filename,
            "PHOTO:",
            photo
        )

        if photo:

            label = tk.Label(
                parent_widget,
                image=photo,
                bg=CARD
            )

        else:

            label = tk.Label(
                parent_widget,
                text="IMAGE NOT FOUND",
                font=("Arial", 8),
                bg="#183b50",
                fg=LIGHT_TEXT
            )

        label.pack(
            fill="x",
            padx=5,
            pady=5
        )

        return label

    # Current filter / search / page.
    state = {
        "region": "All",
        "category": "All",
        "search": "",
        "page": 1
    }

    # Filter buttons, kept so the selected one can be highlighted.
    region_buttons = {}
    category_buttons = {}


    def highlight(buttons, selected):

        for label, button in buttons.items():

            if label == selected:
                button.configure(bg=GOLD, fg=BG)
            else:
                button.configure(bg=BG, fg=TEXT)


    def search_myth(event=None):

        state["search"] = search_entry.get().strip().lower()
        state["page"] = 1

        render_cards()


    def read_more(name):

        # Open the selected myth inside MythLab's main content area.
        if open_detail is not None:
            open_detail(name)
        else:
            messagebox.showinfo(
                name,
                "The detail page for this myth is not connected yet."
            )


    def favourite(name):

        messagebox.showinfo(
            "Favourite",
            name + " added to your favourites."
        )


    def filter_region(region):

        state["region"] = region
        state["page"] = 1

        highlight(region_buttons, region)

        render_cards()


    def filter_category(category):

        state["category"] = category
        state["page"] = 1

        highlight(category_buttons, category)

        render_cards()


    def go_to_page(number):

        state["page"] = number

        render_cards()

        canvas.yview_moveto(0)


    # ==================================================
    # MAIN AREA
    # ==================================================

    main_area = tk.Frame(
        parent,
        bg=BG
    )

    main_area.pack(
        side="right",
        fill="both",
        expand=True
    )

    # ==================================================
    # SCROLLABLE CANVAS
    # ==================================================

    canvas = tk.Canvas(
        main_area,
        bg=BG,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        main_area,
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

    content = tk.Frame(
        canvas,
        bg=BG
    )

    content_window = canvas.create_window(
        (0, 0),
        window=content,
        anchor="nw"
    )

    def update_scroll(event=None):

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    def resize_content(event):

        canvas.itemconfig(
            content_window,
            width=event.width
        )

    content.bind(
        "<Configure>",
        update_scroll
    )

    canvas.bind(
        "<Configure>",
        resize_content
    )

    def scroll_canvas(event):

        if getattr(event, "num", None) == 4:
            direction = -1
        elif getattr(event, "num", None) == 5:
            direction = 1
        else:
            direction = -1 if event.delta > 0 else 1

        canvas.yview_scroll(
            direction,
            "units"
        )

    canvas.bind_all("<MouseWheel>", scroll_canvas)
    canvas.bind_all("<Button-4>", scroll_canvas)
    canvas.bind_all("<Button-5>", scroll_canvas)

    # ==================================================
    # HERO SECTION
    # ==================================================
    #
    # Only this section has been changed.
    #
    # The old Frame + blue hero_text box has been replaced
    # with a Canvas so the text sits directly on the image.
    #

    hero = tk.Canvas(
        content,
        bg="#183b50",
        height=250,
        highlightthickness=0,
        bd=0
    )

    hero.pack(
        fill="x",
        padx=30,
        pady=(0, 15)
    )

    # ==================================================
    # HERO IMAGE
    # ==================================================

    hero_image_ref = [None]

    def update_hero(event=None):

        width = hero.winfo_width()
        height = hero.winfo_height()

        # If Tkinter has not calculated the size yet,
        # use a safe default.
        if width <= 1:
            width = 1050

        if height <= 1:
            height = 250

        hero_path = find_image(
            "welcome.png"
        )

        if hero_path is None:

            hero.delete("all")

            hero.create_text(
                width / 2,
                height / 2,
                text="Welcome to MythLab",
                font=("Georgia", 24, "bold"),
                fill=TEXT
            )

            return

        try:

            image = Image.open(
                hero_path
            ).convert("RGB")

            # Fit the image exactly to the hero area.
            image = ImageOps.fit(
                image,
                (width, height),
                method=Image.Resampling.LANCZOS
            )

            photo = ImageTk.PhotoImage(
                image
            )

            hero_image_ref[0] = photo

            # Keep reference globally as well.
            image_refs.append(photo)

            hero.delete("all")

            # --------------------------------------------------
            # IMAGE
            # --------------------------------------------------

            hero.create_image(
                0,
                0,
                image=photo,
                anchor="nw"
            )

            # --------------------------------------------------
            # TEXT SHADOW
            # --------------------------------------------------
            # Very subtle shadow only.
            # There is NO background rectangle.
            # --------------------------------------------------

            hero.create_text(
                48,
                48,
                text="Myths",
                anchor="w",
                font=("Arial", 10),
                fill="#071522"
            )

            hero.create_text(
                48,
                83,
                text="✥  Discover the Myths",
                anchor="w",
                font=("Georgia", 25, "bold"),
                fill="#071522"
            )

            hero.create_text(
                48,
                132,
                text=(
                    "Discover ancient stories, legendary heroes, "
                    "and magical beings\n"
                    "from Bhutan and cultures around the world."
                ),
                anchor="w",
                font=("Arial", 10),
                fill="#071522",
                justify="left"
            )

            # --------------------------------------------------
            # MAIN TEXT
            # --------------------------------------------------

            hero.create_text(
                45,
                45,
                text="Myths",
                anchor="w",
                font=("Arial", 10),
                fill=GOLD
            )

            hero.create_text(
                45,
                80,
                text="✥  Discover the Myths",
                anchor="w",
                font=("Georgia", 25, "bold"),
                fill=TEXT
            )

            hero.create_text(
                45,
                129,
                text=(
                    "Discover ancient stories, legendary heroes, "
                    "and magical beings\n"
                    "from Bhutan and cultures around the world."
                ),
                anchor="w",
                font=("Arial", 10),
                fill=LIGHT_TEXT,
                justify="left"
            )

        except Exception as error:

            print(
                "Hero image error:",
                error
            )

    hero.bind(
        "<Configure>",
        update_hero
    )

    # Force initial drawing.
    hero.update_idletasks()
    update_hero()

    # ==================================================
    # SEARCH BAR
    # ==================================================

    search_frame = tk.Frame(
        content,
        bg=BG
    )

    search_frame.pack(
        fill="x",
        padx=30,
        pady=(0, 15)
    )

    search_entry = tk.Entry(
        search_frame,
        font=("Arial", 11),
        bg="#102b3d",
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat"
    )

    search_entry.pack(
        side="left",
        fill="x",
        expand=True,
        ipady=10,
        padx=(0, 10)
    )

    search_entry.bind("<Return>", search_myth)

    tk.Button(
        search_frame,
        text="🔍",
        font=("Arial", 12),
        bg=GOLD,
        fg=BG,
        relief="flat",
        padx=15,
        pady=6,
        command=search_myth
    ).pack(
        side="right"
    )

    # ==================================================
    # FILTERS
    # ==================================================

    filter_frame = tk.Frame(
        content,
        bg=BG
    )

    filter_frame.pack(
        fill="x",
        padx=30,
        pady=(0, 18)
    )

    tk.Label(
        filter_frame,
        text="📍 Region:",
        font=("Arial", 9, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        side="left",
        padx=(0, 8)
    )

    regions = [
        "All",
        "Bhutan",
        "Asia",
        "Europe",
        "Other"
    ]

    for region in regions:

        region_button = tk.Button(
            filter_frame,
            text=region,
            font=("Arial", 8),
            bg=GOLD if region == "All" else BG,
            fg=BG if region == "All" else TEXT,
            activebackground=GOLD,
            activeforeground=BG,
            relief="solid",
            bd=1,
            cursor="hand2",
            command=lambda r=region: filter_region(r)
        )

        region_button.pack(
            side="left",
            padx=3,
            ipadx=7
        )

        region_buttons[region] = region_button

    tk.Label(
        filter_frame,
        text="   Categories:",
        font=("Arial", 9, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        side="left",
        padx=(15, 5)
    )

    categories = [
        "All",
        "Legendary Beings",
        "Heroic Tales",
        "Creation Myths",
        "Folk Tales"
    ]

    for category in categories:

        category_button = tk.Button(
            filter_frame,
            text=category,
            font=("Arial", 7),
            bg=GOLD if category == "All" else BG,
            fg=BG if category == "All" else TEXT,
            activebackground=GOLD,
            activeforeground=BG,
            relief="solid",
            bd=1,
            cursor="hand2",
            command=lambda c=category: filter_category(c)
        )

        category_button.pack(
            side="left",
            padx=2,
            ipadx=5
        )

        category_buttons[category] = category_button

    # ==================================================
    # MYTH DATA
    # ==================================================

    myths = [

        (
            "Legendary Beings",
            "The Thunder Dragon",
            "A powerful and sacred dragon that\n"
            "brings rain, fertility and protects the\n"
            "kingdom.",
            "thunder_dragon.png"
        ),

        (
            "Heroic Tales",
            "The Story of King Gesar",
            "The legendary hero who fought against\n"
            "evil and brought peace to the land.",
            "heroes.png"
        ),

        (
            "Creation Myths",
            "The Yeti",
            "A mysterious being said to live in the\n"
            "high mountains of Bhutan and the\n"
            "Himalayas.",
            "yeti.png"
        ),

        (
            "Folk Tales",
            "The Firebird",
            "A magical bird that symbolizes\n"
            "rebirth, hope and the eternal cycle\n"
            "of life.",
            "firebird (1).png"
        ),

        (
            "Legendary Beings",
            "The Black Mountain",
            "A sacred mountain with hidden\n"
            "powers and ancient secrets.",
            "black_mountain (2).png"
        ),

        (
            "Folk Tales",
            "The Snow Lion",
            "A mythical creature symbolizing\n"
            "strength, purity and good fortune.",
            "snow_lion.png"
        ),

        (
            "Heroic Tales",
            "The Legend of Paro Taktsang",
            "The story of Guru Rinpoche and the\n"
            "sacred monastery built in a cliff.",
            "paro_taktsang.png"
        ),

        (
            "Creation Myths",
            "The Birth of the Universe",
            "How the world, its beings and\n"
            "humanity came into existence.",
            "gods.png"
        )
    ]

    # ==================================================
    # MYTH CARDS
    # ==================================================

    # Which region each myth belongs to (used by the Region filter).
    myth_regions = {
        "The Thunder Dragon": "Bhutan",
        "The Story of King Gesar": "Asia",
        "The Yeti": "Bhutan",
        "The Firebird": "Asia",
        "The Black Mountain": "Bhutan",
        "The Snow Lion": "Asia",
        "The Legend of Paro Taktsang": "Bhutan",
        "The Birth of the Universe": "Other"
    }

    PAGE_SIZE = 8

    card_area = tk.Frame(
        content,
        bg=BG
    )

    card_area.pack(
        fill="x",
        padx=30
    )

    page_frame = tk.Frame(
        content,
        bg=BG
    )

    page_frame.pack(
        pady=25
    )


    def matching_myths():

        """Myths that match the region, category and search text."""

        found = []

        for myth in myths:

            category_name, name, description = myth[0], myth[1], myth[2]

            if (
                state["region"] != "All"
                and myth_regions.get(name, "Other") != state["region"]
            ):
                continue

            if (
                state["category"] != "All"
                and category_name != state["category"]
            ):
                continue

            text = (
                name + " " + description + " " + category_name
            ).lower().replace("\n", " ")

            if state["search"] and state["search"] not in text:
                continue

            found.append(myth)

        return found


    def render_cards():

        for widget in card_area.winfo_children():
            widget.destroy()

        matches = matching_myths()

        total_pages = max(1, -(-len(matches) // PAGE_SIZE))

        state["page"] = min(state["page"], total_pages)

        first = (state["page"] - 1) * PAGE_SIZE

        page_items = matches[first:first + PAGE_SIZE]

        if not page_items:

            tk.Label(
                card_area,
                text="No myths found.\nTry another region, category or search.",
                font=("Georgia", 13, "italic"),
                bg=BG,
                fg=LIGHT_TEXT,
                pady=60
            ).pack()

        row = None

        for index, myth in enumerate(page_items):

            category = myth[0]
            name = myth[1]
            description = myth[2]
            image_file = myth[3]

            if index % 4 == 0:

                row = tk.Frame(
                    card_area,
                    bg=BG
                )

                row.pack(
                    fill="x",
                    pady=5
                )

                for column in range(4):

                    row.grid_columnconfigure(
                        column,
                        weight=1,
                        uniform="myth_cards"
                    )

            card = tk.Frame(
                row,
                bg=CARD,
                height=250
            )

            card.grid(
                row=0,
                column=index % 4,
                sticky="nsew",
                padx=5
            )

            card.pack_propagate(False)

            create_image(
                card,
                image_file,
                (235, 125)
            )

            tk.Label(
                card,
                text=category,
                font=("Arial", 7),
                bg=CARD,
                fg=GOLD
            ).pack(
                anchor="w",
                padx=10,
                pady=(2, 0)
            )

            tk.Label(
                card,
                text=name,
                font=("Georgia", 11, "bold"),
                bg=CARD,
                fg=TEXT
            ).pack(
                anchor="w",
                padx=10,
                pady=(3, 0)
            )

            tk.Label(
                card,
                text=description,
                font=("Arial", 7),
                bg=CARD,
                fg=LIGHT_TEXT,
                justify="left"
            ).pack(
                anchor="w",
                padx=10,
                pady=(2, 0)
            )

            button_frame = tk.Frame(
                card,
                bg=CARD
            )

            button_frame.pack(
                fill="x",
                padx=10,
                pady=7
            )

            tk.Button(
                button_frame,
                text="Read More →",
                font=("Arial", 7),
                bg=BG,
                fg=GOLD,
                activebackground=GOLD,
                activeforeground=BG,
                relief="solid",
                bd=1,
                command=lambda n=name: read_more(n)
            ).pack(
                side="left"
            )

            tk.Button(
                button_frame,
                text="♡",
                font=("Arial", 11),
                bg=CARD,
                fg=GOLD,
                activebackground=CARD,
                activeforeground=GOLD,
                relief="flat",
                command=lambda n=name: favourite(n)
            ).pack(
                side="right"
            )

        render_pagination(total_pages)


    # ==================================================
    # PAGE NUMBERS
    # ==================================================

    def render_pagination(total_pages):

        for widget in page_frame.winfo_children():
            widget.destroy()

        # Nothing to page through.
        if total_pages <= 1:
            return

        current = state["page"]

        tk.Button(
            page_frame,
            text="←",
            font=("Arial", 11),
            bg=BG,
            fg=GOLD,
            relief="solid",
            bd=1,
            cursor="hand2",
            state="normal" if current > 1 else "disabled",
            command=lambda: go_to_page(current - 1)
        ).pack(
            side="left",
            padx=8
        )

        for number in range(1, total_pages + 1):

            tk.Button(
                page_frame,
                text=str(number),
                font=("Arial", 9, "bold"),
                bg=GOLD if number == current else BG,
                fg=BG if number == current else TEXT,
                activebackground=GOLD,
                activeforeground=BG,
                relief="solid",
                bd=1,
                width=3,
                cursor="hand2",
                command=lambda n=number: go_to_page(n)
            ).pack(
                side="left",
                padx=3
            )

        tk.Button(
            page_frame,
            text="→",
            font=("Arial", 11),
            bg=BG,
            fg=GOLD,
            relief="solid",
            bd=1,
            cursor="hand2",
            state="normal" if current < total_pages else "disabled",
            command=lambda: go_to_page(current + 1)
        ).pack(
            side="left",
            padx=8
        )


    # Draw the first page.
    render_cards()


# ==================================================
# OPTIONAL STANDALONE TEST
# ==================================================

if __name__ == "__main__":

    test_root = tk.Tk()

    test_root.title(
        "MythLab - Myths"
    )

    test_root.geometry(
        "1280x900"
    )

    test_root.minsize(
        1000,
        700
    )

    test_root.configure(
        bg=BG
    )

    show_myths(
        test_root
    )

    test_root.mainloop()