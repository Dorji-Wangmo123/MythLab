# about.py

import tkinter as tk


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
        lambda event:
        canvas.bind_all(
            "<MouseWheel>",
            mouse_scroll
        )
    )


    canvas.bind(
        "<Leave>",
        lambda event:
        canvas.unbind_all(
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
        pady=30
    )


    # ========================================================
    # HEADER
    # ========================================================

    header = tk.Frame(
        page,
        bg=BG
    )


    header.pack(
        anchor="w"
    )


    tk.Label(
        header,
        text="ⓘ",
        font=("Arial", 26),
        bg=BG,
        fg=GOLD
    ).pack(
        side="left"
    )


    tk.Label(
        header,
        text="About",
        font=("Georgia", 34),
        bg=BG,
        fg="white"
    ).pack(
        side="left",
        padx=18
    )


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
        pady=(10, 25)
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