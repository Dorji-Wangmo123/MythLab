# about.py

import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk, ImageOps


# ============================================================
# MYTHLAB - ABOUT PAGE
# ============================================================

# ============================================================
# COLOURS
# ============================================================

BG = "#071b2b"
CARD = "#102b3d"

GOLD = "#d6a84f"
TEXT = "#f5ead0"
LIGHT_TEXT = "#c7c1b3"

ICON_BG = "#1a3a4d"

# Project / image settings
PROJECT_DIR = Path(__file__).resolve().parent
IMAGE_DIRS = [
    PROJECT_DIR / "assets",
    PROJECT_DIR / "images",
    PROJECT_DIR
]

about_image_refs = []


# ============================================================
# IMAGE HELPER
# ============================================================

def find_image(filename):
    """Find an image in assets, images, or beside about.py."""

    for folder in IMAGE_DIRS:
        path = folder / filename

        if path.exists():
            return path

    return None


def load_banner_image(filename, size):
    """Load and crop the banner image to the requested size."""

    path = find_image(filename)

    if path is None:
        print("Could not find image:", filename)
        return None

    try:
        image = Image.open(path).convert("RGB")

        image = ImageOps.fit(
            image,
            size,
            method=Image.Resampling.LANCZOS
        )

        photo = ImageTk.PhotoImage(image)

        about_image_refs.append(photo)

        return photo

    except Exception as error:
        print("Could not load image:", filename)
        print(error)
        return None


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def make_card(parent, icon, title):

    card = tk.Frame(
        parent,
        bg=CARD,
        highlightthickness=1,
        highlightbackground=GOLD
    )

    heading = tk.Frame(
        card,
        bg=CARD
    )

    heading.pack(
        anchor="w",
        padx=25,
        pady=(20, 8)
    )

    tk.Label(
        heading,
        text=icon,
        font=("Arial", 18),
        bg=CARD,
        fg=GOLD
    ).pack(
        side="left"
    )

    tk.Label(
        heading,
        text=title,
        font=("Georgia", 16),
        bg=CARD,
        fg="#f3d9a8"
    ).pack(
        side="left",
        padx=12
    )

    return card


def make_divider(parent):

    row = tk.Frame(
        parent,
        bg=CARD
    )

    tk.Frame(
        row,
        bg=GOLD,
        height=1,
        width=110
    ).pack(
        side="left",
        pady=8
    )

    tk.Label(
        row,
        text="❖",
        font=("Arial", 11),
        bg=CARD,
        fg=GOLD
    ).pack(
        side="left",
        padx=8
    )

    tk.Frame(
        row,
        bg=GOLD,
        height=1,
        width=110
    ).pack(
        side="left",
        pady=8
    )

    return row


# ============================================================
# SHOW ABOUT PAGE
# ============================================================

def show_about(parent):

    # Clear previous content
    for widget in parent.winfo_children():
        widget.destroy()

    # Keep only current page images in memory
    about_image_refs.clear()

    # ========================================================
    # MAIN SCROLLING AREA
    # ========================================================

    canvas = tk.Canvas(
        parent,
        bg=BG,
        highlightthickness=0
    )

    scrollbar = tk.Scrollbar(
        parent,
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

    # ========================================================
    # SCROLLING
    # ========================================================

    def update_scroll_region(event=None):

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    def resize_content(event):

        canvas.itemconfigure(
            content_window,
            width=event.width
        )

    def mouse_scroll(event):

        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    content.bind(
        "<Configure>",
        update_scroll_region
    )

    canvas.bind(
        "<Configure>",
        resize_content
    )

    canvas.bind(
        "<Enter>",
        lambda event: canvas.bind_all(
            "<MouseWheel>",
            mouse_scroll
        )
    )

    canvas.bind(
        "<Leave>",
        lambda event: canvas.unbind_all(
            "<MouseWheel>"
        )
    )

    # ========================================================
    # PAGE
    # ========================================================

    page = tk.Frame(
        content,
        bg=BG
    )

    page.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=(20, 30)
    )

    # ========================================================
    # HEADER IMAGE
    # ========================================================

    # The image is drawn directly on a Canvas so the title
    # appears ON TOP of banner.jpg instead of having a solid
    # rectangle behind it.

    header_width = 1050
    header_height = 190

    header_canvas = tk.Canvas(
        page,
        height=header_height,
        bg=BG,
        highlightthickness=0,
        bd=0
    )

    header_canvas.pack(
        fill="x",
        pady=(0, 20)
    )

    def draw_header(event=None):

        width = max(header_canvas.winfo_width(), 1)

        image = load_banner_image(
            "banner.jpg",
            (width, header_height)
        )

        header_canvas.delete("all")

        if image:
            header_canvas.create_image(
                0,
                0,
                image=image,
                anchor="nw"
            )
        else:
            # Fallback if banner.jpg is not found
            header_canvas.create_rectangle(
                0,
                0,
                width,
                header_height,
                fill=BG,
                outline=""
            )

        # Header icon
        header_canvas.create_text(
            35,
            55,
            text="ⓘ",
            font=("Arial", 28),
            fill=GOLD,
            anchor="w"
        )

        # Header title
        header_canvas.create_text(
            88,
            52,
            text="About",
            font=("Georgia", 34),
            fill="white",
            anchor="w"
        )

        # Subtitle on the image
        header_canvas.create_text(
            90,
            105,
            text=(
                "Discover the story behind MythLab — "
                "our purpose, inspiration and features."
            ),
            font=("Arial", 10),
            fill=TEXT,
            anchor="w"
        )

    header_canvas.bind(
        "<Configure>",
        draw_header
    )

    # ========================================================
    # INTRODUCTION
    # ========================================================

    tk.Label(
        page,
        text=(
            "MythLab is your gateway to the enchanting world of myths,\n"
            "legends, and mythical creatures — with a special focus on\n"
            "Bhutan and beyond."
        ),
        font=("Arial", 12),
        bg=BG,
        fg=TEXT,
        justify="left",
        anchor="w"
    ).pack(
        anchor="w",
        pady=(0, 25)
    )

    # ========================================================
    # TWO COLUMN LAYOUT
    # ========================================================

    columns = tk.Frame(
        page,
        bg=BG
    )

    columns.pack(
        fill="both",
        expand=True
    )

    columns.columnconfigure(
        0,
        weight=3
    )

    columns.columnconfigure(
        1,
        weight=2
    )

    left_col = tk.Frame(
        columns,
        bg=BG
    )

    left_col.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=(0, 18)
    )

    right_col = tk.Frame(
        columns,
        bg=BG
    )

    right_col.grid(
        row=0,
        column=1,
        sticky="nsew"
    )

    # ========================================================
    # OUR PURPOSE
    # ========================================================

    purpose = make_card(
        left_col,
        "📖",
        "Our Purpose"
    )

    purpose.pack(
        fill="x",
        pady=(0, 18)
    )

    tk.Label(
        purpose,
        text=(
            "We created MythLab to bring the rich stories and cultural "
            "heritage of Bhutan and the world to life. Our goal is to "
            "inspire curiosity, encourage learning, and keep these "
            "myths and legends alive for future generations."
        ),
        font=("Arial", 11),
        bg=CARD,
        fg=TEXT,
        wraplength=420,
        justify="left"
    ).pack(
        anchor="w",
        padx=25
    )

    trio = tk.Frame(
        purpose,
        bg=CARD
    )

    trio.pack(
        fill="x",
        padx=25,
        pady=(22, 25)
    )

    for i in range(3):

        trio.columnconfigure(
            i,
            weight=1
        )

    trio_items = [

        (
            "⛰",
            "Explore",
            "Discover fascinating\nmyths and creatures."
        ),

        (
            "💡",
            "Learn",
            "Build your knowledge\nand understanding."
        ),

        (
            "♡",
            "Believe",
            "Keep the magic\nalive."
        )

    ]

    for i, (icon, title, desc) in enumerate(trio_items):

        box = tk.Frame(
            trio,
            bg=CARD
        )

        box.grid(
            row=0,
            column=i
        )

        tk.Label(
            box,
            text=icon,
            font=("Arial", 18),
            bg=ICON_BG,
            fg=GOLD,
            width=3,
            height=1
        ).pack(
            pady=(0, 8)
        )

        tk.Label(
            box,
            text=title,
            font=("Arial", 12, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack()

        tk.Label(
            box,
            text=desc,
            font=("Arial", 9),
            bg=CARD,
            fg=LIGHT_TEXT,
            justify="center"
        ).pack(
            pady=(3, 0)
        )

    # ========================================================
    # OUR INSPIRATION
    # ========================================================

    inspiration = make_card(
        left_col,
        "⛰",
        "Our Inspiration"
    )

    inspiration.pack(
        fill="x"
    )

    tk.Label(
        inspiration,
        text=(
            "Bhutan’s landscapes, traditions and people have given us "
            "stories that are both magical and meaningful. MythLab "
            "is inspired by this rich heritage — and by the belief that "
            "stories have the power to teach, connect and inspire."
        ),
        font=("Arial", 11),
        bg=CARD,
        fg=TEXT,
        wraplength=420,
        justify="left"
    ).pack(
        anchor="w",
        padx=25
    )

    make_divider(
        inspiration
    ).pack(
        pady=(18, 0)
    )

    tk.Label(
        inspiration,
        text="“Small steps lead to great discoveries.”",
        font=("Georgia", 12, "italic"),
        bg=CARD,
        fg=GOLD
    ).pack(
        pady=4
    )

    make_divider(
        inspiration
    ).pack(
        pady=(0, 18)
    )

    # ========================================================
    # KEY FEATURES
    # ========================================================

    features = make_card(
        right_col,
        "★",
        "Key Features"
    )

    features.pack(
        fill="both",
        expand=True
    )

    feature_items = [

        (
            "📖",
            "Myths",
            "Read and explore timeless stories\n"
            "from Bhutan and around the world."
        ),

        (
            "🐉",
            "Creatures",
            "Discover mythical beings, from the\n"
            "legendary to the mysterious."
        ),

        (
            "📖",
            "Regions",
            "Explore the 20 Dzongkhags of Bhutan\n"
            "and their unique legends."
        ),

        (
            "✓",
            "My Tasks",
            "Complete learning tasks and track\n"
            "your progress."
        ),

        (
            "?",
            "Quiz",
            "Test your knowledge and challenge\n"
            "yourself with fun quizzes."
        ),

        (
            "♡",
            "Favourites",
            "Save your favourite myths, creatures\n"
            "and stories for later."
        )

    ]

    for icon, title, desc in feature_items:

        row = tk.Frame(
            features,
            bg=CARD
        )

        row.pack(
            fill="x",
            padx=25,
            pady=9
        )

        tk.Label(
            row,
            text=icon,
            font=("Arial", 16),
            bg=ICON_BG,
            fg=GOLD,
            width=3,
            height=1
        ).pack(
            side="left"
        )

        text_box = tk.Frame(
            row,
            bg=CARD
        )

        text_box.pack(
            side="left",
            padx=15
        )

        tk.Label(
            text_box,
            text=title,
            font=("Arial", 11, "bold"),
            bg=CARD,
            fg="#f3d9a8"
        ).pack(
            anchor="w"
        )

        tk.Label(
            text_box,
            text=desc,
            font=("Arial", 9),
            bg=CARD,
            fg=LIGHT_TEXT,
            justify="left"
        ).pack(
            anchor="w"
        )

    tk.Frame(
        features,
        bg=CARD,
        height=12
    ).pack()

    # ========================================================
    # THANK YOU
    # ========================================================

    footer = tk.Frame(
        page,
        bg=BG
    )

    footer.pack(
        anchor="e",
        pady=(25, 0)
    )

    tk.Label(
        footer,
        text="Thank you",
        font=("Georgia", 20, "italic"),
        bg=BG,
        fg=GOLD
    ).pack()

    tk.Label(
        footer,
        text="for exploring the world of\nMythLab!",
        font=("Arial", 10),
        bg=BG,
        fg=LIGHT_TEXT,
        justify="center"
    ).pack()

    tk.Label(
        footer,
        text="Version 1.0",
        font=("Arial", 8),
        bg=BG,
        fg="#7f8c95"
    ).pack(
        pady=(8, 0)
    )

    # Update scroll region after everything is created
    parent.update_idletasks()

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )
