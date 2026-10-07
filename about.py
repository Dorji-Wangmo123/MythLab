import tkinter as tk
from tkinter import messagebox


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()
root.title("MythLab - About")
root.geometry("1200x900")
root.minsize(900, 650)
root.configure(bg="#071b2b")


# ==========================================
# COLOURS
# ==========================================

BG = "#071b2b"
SIDEBAR = "#061522"
CARD = "#102b3d"
GOLD = "#d6a84f"
TEXT = "#f5ead0"
LIGHT_TEXT = "#c7c1b3"
ACTIVE = "#2b3a3f"
ICON_BG = "#1a3a4d"


# ==========================================
# FUNCTIONS
# ==========================================

def open_page(page):
    if page == "About":
        return
    messagebox.showinfo(
        page,
        page + " page will be added here."
    )


# ==========================================
# SIDEBAR
# ==========================================

sidebar = tk.Frame(root, bg=SIDEBAR, width=210)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)


tk.Label(
    sidebar, text="🐉", font=("Arial", 30),
    bg=SIDEBAR, fg=GOLD
).pack(pady=(25, 0))

tk.Label(
    sidebar, text="MythLab", font=("Georgia", 22, "bold"),
    bg=SIDEBAR, fg=GOLD
).pack()

tk.Label(
    sidebar, text="Explore. Learn. Believe.", font=("Arial", 9),
    bg=SIDEBAR, fg=GOLD
).pack(pady=(0, 25))


menu_items = [
    ("⌂  Home", "Home"),
    ("📖  Myths", "Myths"),
    ("🐉  Creatures", "Creatures"),
    ("🌐  Regions", "Regions"),
    ("✓  My Tasks", "My Tasks"),
    ("?  Quiz", "Quiz"),
    ("♡  Favourites", "Favourites"),
    ("ⓘ  About", "About")
]

for text, page in menu_items:
    is_active = (page == "About")

    tk.Button(
        sidebar,
        text=text,
        font=("Arial", 11),
        bg=ACTIVE if is_active else SIDEBAR,
        fg=GOLD if is_active else TEXT,
        activebackground="#263b47",
        activeforeground=GOLD,
        relief="flat",
        anchor="w",
        padx=20,
        pady=10,
        highlightthickness=1 if is_active else 0,
        highlightbackground=GOLD,
        command=lambda p=page: open_page(p)
    ).pack(fill="x", padx=10, pady=2)


tk.Label(
    sidebar,
    text='“Every myth is a door\nto a deeper wisdom.”\n\n— Bhutanese Wisdom',
    font=("Georgia", 9, "italic"),
    bg=SIDEBAR, fg=GOLD, justify="center"
).pack(side="bottom", pady=25)


# ==========================================
# MAIN AREA
# ==========================================

main_area = tk.Frame(root, bg=BG)
main_area.pack(side="right", fill="both", expand=True)


# ==========================================
# CANVAS + SCROLLBAR
# ==========================================

canvas = tk.Canvas(main_area, bg=BG, highlightthickness=0)
scrollbar = tk.Scrollbar(main_area, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

content = tk.Frame(canvas, bg=BG)
content_window = canvas.create_window((0, 0), window=content, anchor="nw")


def update_scroll_region(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))


def resize_content(event):
    canvas.itemconfig(content_window, width=event.width)


def mouse_scroll(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


content.bind("<Configure>", update_scroll_region)
canvas.bind("<Configure>", resize_content)
canvas.bind_all("<MouseWheel>", mouse_scroll)


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def make_card(parent, icon, title):
    """Gold-outlined card with an icon + title row. Returns the frame."""
    card = tk.Frame(
        parent, bg=CARD,
        highlightthickness=1, highlightbackground=GOLD
    )

    heading = tk.Frame(card, bg=CARD)
    heading.pack(anchor="w", padx=25, pady=(20, 8))

    tk.Label(
        heading, text=icon, font=("Arial", 18),
        bg=CARD, fg=GOLD
    ).pack(side="left")

    tk.Label(
        heading, text=title, font=("Georgia", 16),
        bg=CARD, fg="#f3d9a8"
    ).pack(side="left", padx=12)

    return card


def make_divider(parent):
    row = tk.Frame(parent, bg=CARD)
    tk.Frame(row, bg=GOLD, height=1, width=110).pack(side="left", pady=8)
    tk.Label(row, text="❖", font=("Arial", 11), bg=CARD, fg=GOLD).pack(side="left", padx=8)
    tk.Frame(row, bg=GOLD, height=1, width=110).pack(side="left", pady=8)
    return row


# ==========================================
# PAGE CONTENT
# ==========================================

page = tk.Frame(content, bg=BG)
page.pack(fill="both", expand=True, padx=40, pady=30)


# ---------- Header ----------

header = tk.Frame(page, bg=BG)
header.pack(anchor="w")

tk.Label(
    header, text="ⓘ", font=("Arial", 26),
    bg=BG, fg=GOLD
).pack(side="left")

tk.Label(
    header, text="About", font=("Georgia", 34),
    bg=BG, fg="white"
).pack(side="left", padx=18)

tk.Label(
    page,
    text="MythLab is an interactive learning application that brings myths, legends,\n"
         mythical creatures from Bhutan and around the world together in one place.",
    font=("Arial", 12), bg=BG, fg=TEXT,
    justify="left", anchor="w"
).pack(anchor="w", pady=(10, 25))


# ---------- Two-column layout ----------

columns = tk.Frame(page, bg=BG)
columns.pack(fill="both", expand=True)

columns.columnconfigure(0, weight=3)
columns.columnconfigure(1, weight=2)

left_col = tk.Frame(columns, bg=BG)
left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 18))

right_col = tk.Frame(columns, bg=BG)
right_col.grid(row=0, column=1, sticky="nsew")


# ---------- Our Purpose ----------

purpose = make_card(left_col, "📖", "Our Purpose")
purpose.pack(fill="x", pady=(0, 18))

tk.Label(
    purpose,
    text="We created MythLab to bring the rich stories and cultural "
         "heritage of Bhutan and the world to life. Our goal is to "
         "inspire curiosity, encourage learning, and keep these "
         "myths and legends alive for future generations.",
    font=("Arial", 11), bg=CARD, fg=TEXT,
    wraplength=420, justify="left"
).pack(anchor="w", padx=25)

trio = tk.Frame(purpose, bg=CARD)
trio.pack(fill="x", padx=25, pady=(22, 25))

for i in range(3):
    trio.columnconfigure(i, weight=1)

trio_items = [
    ("⛰", "Explore", "Discover fascinating\nmyths and creatures."),
    ("💡", "Learn", "Build your knowledge\nand understanding."),
    ("♡", "Believe", "Keep the magic\nalive.")
]

for i, (icon, title, desc) in enumerate(trio_items):
    box = tk.Frame(trio, bg=CARD)
    box.grid(row=0, column=i)

    tk.Label(
        box, text=icon, font=("Arial", 18),
        bg=ICON_BG, fg=GOLD, width=3, height=1
    ).pack(pady=(0, 8))

    tk.Label(
        box, text=title, font=("Arial", 12, "bold"),
        bg=CARD, fg=TEXT
    ).pack()

    tk.Label(
        box, text=desc, font=("Arial", 9),
        bg=CARD, fg=LIGHT_TEXT, justify="center"
    ).pack(pady=(3, 0))


# ---------- Our Inspiration ----------

inspiration = make_card(left_col, "⛰", "Our Inspiration")
inspiration.pack(fill="x")

tk.Label(
    inspiration,
    text="Bhutan’s landscapes, traditions and people have given us "
         "stories that are both magical and meaningful. MythLab "
         "is inspired by this rich heritage — and by the belief that "
         "stories have the power to teach, connect and inspire.",
    font=("Arial", 11), bg=CARD, fg=TEXT,
    wraplength=420, justify="left"
).pack(anchor="w", padx=25)

make_divider(inspiration).pack(pady=(18, 0))

tk.Label(
    inspiration,
    text="“Small steps lead to great discoveries.”",
    font=("Georgia", 12, "italic"), bg=CARD, fg=GOLD
).pack(pady=4)

make_divider(inspiration).pack(pady=(0, 18))


# ---------- Key Features ----------

features = make_card(right_col, "★", "Key Features")
features.pack(fill="both", expand=True)

feature_items = [
    ("📖", "Myths", "Read and explore timeless stories\nfrom Bhutan and around the world."),
    ("🐉", "Creatures", "Discover mythical beings, from the\nlegendary to the mysterious."),
    ("📖", "Regions", "Explore the 20 Dzongkhags of Bhutan\nand their unique legends."),
    ("✓", "My Tasks", "Complete learning tasks and track\nyour progress."),
    ("?", "Quiz", "Test your knowledge and challenge\nyourself with fun quizzes."),
    ("♡", "Favourites", "Save your favourite myths, creatures\nand stories for later.")
]

for icon, title, desc in feature_items:
    row = tk.Frame(features, bg=CARD)
    row.pack(fill="x", padx=25, pady=9)

    tk.Label(
        row, text=icon, font=("Arial", 16),
        bg=ICON_BG, fg=GOLD, width=3, height=1
    ).pack(side="left")

    text_box = tk.Frame(row, bg=CARD)
    text_box.pack(side="left", padx=15)

    tk.Label(
        text_box, text=title, font=("Arial", 11, "bold"),
        bg=CARD, fg="#f3d9a8"
    ).pack(anchor="w")

    tk.Label(
        text_box, text=desc, font=("Arial", 9),
        bg=CARD, fg=LIGHT_TEXT, justify="left"
    ).pack(anchor="w")

tk.Frame(features, bg=CARD, height=12).pack()


# ---------- Thank you ----------

footer = tk.Frame(page, bg=BG)
footer.pack(anchor="e", pady=(25, 0))

tk.Label(
    footer, text="Thank you", font=("Georgia", 20, "italic"),
    bg=BG, fg=GOLD
).pack()

tk.Label(
    footer, text="for exploring the world of\nMythLab!",
    font=("Arial", 10), bg=BG, fg=LIGHT_TEXT, justify="center"
).pack()

tk.Label(
    footer, text="Version 1.0",
    font=("Arial", 8),
    bg=BG, fg="#7f8c95"
).pack(pady=(8, 0))
# ==========================================
# RUN
# ==========================================

root.mainloop()