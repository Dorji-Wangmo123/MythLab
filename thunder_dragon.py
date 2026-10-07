#thunder_dragon.py code
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from PIL import Image, ImageTk, ImageOps


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()
root.title("MythLab - The Thunder Dragon")
root.geometry("1280x900")
root.minsize(1050, 700)
root.configure(bg="#061b2b")


# =========================================================
# COLOURS
# =========================================================

BG = "#061b2b"
SIDEBAR = "#071522"
CARD = "#0a2131"
CARD2 = "#0d293b"
GOLD = "#d6a84f"
LIGHT_GOLD = "#e5c875"
TEXT = "#f5ead0"
LIGHT_TEXT = "#c7c1b3"
BORDER = "#755d2d"
DARK = "#071522"


# =========================================================
# IMAGE LOCATION
# =========================================================

IMAGE_DIR = Path(__file__).resolve().parent / "assets"

# Keep all image references
image_refs = []


# =========================================================
# LOAD IMAGE
# =========================================================

def load_image(filename, size):

    path = IMAGE_DIR / filename

    try:

        if not path.exists():

            print("IMAGE NOT FOUND:", path)

            return None

        image = Image.open(path).convert("RGB")

        image = ImageOps.fit(
            image,
            size,
            method=Image.Resampling.LANCZOS
        )

        photo = ImageTk.PhotoImage(image)

        image_refs.append(photo)

        return photo

    except Exception as error:

        print("Could not load image:", path)
        print("Error:", error)

        return None


# =========================================================
# BUTTON FUNCTIONS
# =========================================================

def show_message(title, message):

    messagebox.showinfo(
        title,
        message
    )


def play_video():

    messagebox.showinfo(
        "The Thunder Dragon",
        "The Thunder Dragon – A Bhutanese Legend\n\n"
        "Video player will be connected here."
    )


def open_story():

    messagebox.showinfo(
        "Read More Stories",
        "More Bhutanese myths and stories will be shown here."
    )


def open_creatures():

    messagebox.showinfo(
        "Related Creatures",
        "Related mythical creatures will be shown here."
    )


def open_regions():

    messagebox.showinfo(
        "Bhutan's Regions",
        "Explore the regions connected with Bhutanese myths."
    )


def related_myth(name):

    messagebox.showinfo(
        name,
        "Opening " + name
    )


# =========================================================
# SIDEBAR
# =========================================================

sidebar = tk.Frame(
    root,
    bg=SIDEBAR,
    width=215
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


# =========================================================
# SIDEBAR LOGO
# =========================================================

tk.Label(
    sidebar,
    text="🐉",
    font=("Arial", 34),
    bg=SIDEBAR,
    fg=GOLD
).pack(
    pady=(18, 0)
)


tk.Label(
    sidebar,
    text="MythLab",
    font=("Georgia", 23, "bold"),
    bg=SIDEBAR,
    fg=GOLD
).pack()


tk.Label(
    sidebar,
    text="Explore. Learn. Believe.",
    font=("Arial", 9),
    bg=SIDEBAR,
    fg=GOLD
).pack(
    pady=(0, 30)
)


# =========================================================
# SIDEBAR MENU
# =========================================================

menu_items = [
    ("⌂", "Home"),
    ("▣", "Myths"),
    ("🐉", "Creatures"),
    ("◎", "Regions"),
    ("☑", "My Tasks"),
    ("?", "Quiz"),
    ("♡", "Favourites"),
    ("ⓘ", "About")
]


for icon, name in menu_items:

    button = tk.Button(
        sidebar,
        text=f"{icon}    {name}",
        font=("Arial", 11),
        bg=SIDEBAR,
        fg=TEXT,
        activebackground="#263b47",
        activeforeground=GOLD,
        relief="flat",
        anchor="w",
        padx=18,
        pady=10,
        bd=0,
        command=lambda n=name: show_message(
            n,
            n + " page"
        )
    )

    button.pack(
        fill="x",
        padx=10,
        pady=2
    )

    if name == "Myths":

        button.configure(
            bg="#5a4b2f",
            fg=TEXT
        )


# =========================================================
# SIDEBAR DECORATION
# =========================================================

tk.Label(
    sidebar,
    text="⌁⌁⌁⌁⌁⌁⌁",
    font=("Arial", 14),
    bg=SIDEBAR,
    fg="#5c4929"
).pack(
    side="bottom",
    pady=(0, 5)
)


tk.Label(
    sidebar,
    text='“Every myth is a door\nto a deeper wisdom.”\n\n'
         "— Bhutanese Wisdom",
    font=("Georgia", 10, "italic"),
    bg=SIDEBAR,
    fg=GOLD,
    justify="center"
).pack(
    side="bottom",
    pady=20
)


# =========================================================
# MAIN SCROLL AREA
# =========================================================

main_area = tk.Frame(
    root,
    bg=BG
)

main_area.pack(
    side="right",
    fill="both",
    expand=True
)


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

    canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


canvas.bind_all(
    "<MouseWheel>",
    scroll_canvas
)


# =========================================================
# PAGE CONTENT
# =========================================================

page = tk.Frame(
    content,
    bg=BG
)

page.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=25
)


# =========================================================
# BREADCRUMB
# =========================================================

breadcrumb = tk.Frame(
    page,
    bg=BG
)

breadcrumb.pack(
    fill="x",
    pady=(0, 10)
)


tk.Label(
    breadcrumb,
    text="←  Myths",
    font=("Arial", 9),
    bg=BG,
    fg=LIGHT_TEXT
).pack(
    side="left"
)


tk.Label(
    breadcrumb,
    text="  ›  ",
    font=("Arial", 9),
    bg=BG,
    fg="#74684f"
).pack(
    side="left"
)


tk.Label(
    breadcrumb,
    text="The Thunder Dragon",
    font=("Arial", 9, "bold"),
    bg=BG,
    fg=GOLD
).pack(
    side="left"
)


# =========================================================
# HERO AREA
# =========================================================

hero = tk.Frame(
    page,
    bg=BG,
    height=255
)

hero.pack(
    fill="x"
)

hero.pack_propagate(False)


# =========================================================
# HERO TEXT
# =========================================================

hero_text = tk.Frame(
    hero,
    bg=BG
)

hero_text.pack(
    side="left",
    fill="both",
    expand=True
)


tk.Label(
    hero_text,
    text="The Thunder Dragon",
    font=("Georgia", 29, "bold"),
    bg=BG,
    fg=GOLD
).pack(
    anchor="w",
    pady=(5, 8)
)


category_badge = tk.Label(
    hero_text,
    text="  Legendary Beings  ",
    font=("Arial", 9),
    bg="#1b3040",
    fg=TEXT,
    relief="solid",
    bd=1
)

category_badge.pack(
    anchor="w",
    pady=(0, 12)
)


tk.Label(
    hero_text,
    text="A powerful and sacred dragon that\n"
         "brings rain, fertility and protects the kingdom.",
    font=("Arial", 11),
    bg=BG,
    fg=TEXT,
    justify="left"
).pack(
    anchor="w"
)


# =========================================================
# HERO INFORMATION
# =========================================================

info_frame = tk.Frame(
    hero_text,
    bg=BG
)

info_frame.pack(
    anchor="w",
    pady=18
)


# REGION

region_frame = tk.Frame(
    info_frame,
    bg=BG
)

region_frame.pack(
    side="left",
    padx=(0, 25)
)


tk.Label(
    region_frame,
    text="⌖",
    font=("Arial", 22),
    bg=BG,
    fg=GOLD
).pack(
    side="left",
    padx=(0, 8)
)


region_text = tk.Frame(
    region_frame,
    bg=BG
)

region_text.pack(
    side="left"
)


tk.Label(
    region_text,
    text="Region",
    font=("Arial", 8),
    bg=BG,
    fg=LIGHT_TEXT
).pack(
    anchor="w"
)


tk.Label(
    region_text,
    text="Bhutan",
    font=("Arial", 9, "bold"),
    bg=BG,
    fg=TEXT
).pack(
    anchor="w"
)


# DIVIDER

tk.Frame(
    info_frame,
    bg="#39414a",
    width=1,
    height=38
).pack(
    side="left",
    padx=15
)


# TYPE

type_frame = tk.Frame(
    info_frame,
    bg=BG
)

type_frame.pack(
    side="left",
    padx=15
)


tk.Label(
    type_frame,
    text="🐉",
    font=("Arial", 18),
    bg=BG,
    fg=GOLD
).pack(
    side="left",
    padx=(0, 8)
)


type_text = tk.Frame(
    type_frame,
    bg=BG
)

type_text.pack(
    side="left"
)


tk.Label(
    type_text,
    text="Type",
    font=("Arial", 8),
    bg=BG,
    fg=LIGHT_TEXT
).pack(
    anchor="w"
)


tk.Label(
    type_text,
    text="Dragon",
    font=("Arial", 9, "bold"),
    bg=BG,
    fg=TEXT
).pack(
    anchor="w"
)


# DIVIDER

tk.Frame(
    info_frame,
    bg="#39414a",
    width=1,
    height=38
).pack(
    side="left",
    padx=15
)


# ASSOCIATED WITH

associated_frame = tk.Frame(
    info_frame,
    bg=BG
)

associated_frame.pack(
    side="left",
    padx=15
)


tk.Label(
    associated_frame,
    text="♢",
    font=("Arial", 20),
    bg=BG,
    fg=GOLD
).pack(
    side="left",
    padx=(0, 8)
)


associated_text = tk.Frame(
    associated_frame,
    bg=BG
)

associated_text.pack(
    side="left"
)


tk.Label(
    associated_text,
    text="Associated with",
    font=("Arial", 8),
    bg=BG,
    fg=LIGHT_TEXT
).pack(
    anchor="w"
)


tk.Label(
    associated_text,
    text="Rain & Fertility",
    font=("Arial", 9, "bold"),
    bg=BG,
    fg=TEXT
).pack(
    anchor="w"
)


# =========================================================
# HERO IMAGE
# =========================================================

hero_photo = load_image(
    "thunder_dragon.png",
    (600, 255)
)


if hero_photo:

    hero_image = tk.Label(
        hero,
        image=hero_photo,
        bg=BG
    )

    hero_image.pack(
        side="right"
    )

else:

    tk.Label(
        hero,
        text="Thunder Dragon Image\n\n"
             "Please check:\n"
             "thunder_dragon.png",
        font=("Arial", 12),
        bg=CARD,
        fg=LIGHT_TEXT,
        justify="center"
    ).pack(
        side="right",
        fill="both",
        expand=True
    )


# =========================================================
# TABS
# =========================================================

tabs = tk.Frame(
    page,
    bg="#0b2535"
)

tabs.pack(
    fill="x",
    pady=(0, 12)
)


tab_names = [
    "Overview",
    "Story",
    "Symbolism",
    "Related Myths"
]


for i, tab in enumerate(tab_names):

    tk.Button(
        tabs,
        text=tab,
        font=("Arial", 9, "bold" if i == 0 else "normal"),
        bg=GOLD if i == 0 else "#0b2535",
        fg=BG if i == 0 else TEXT,
        activebackground=GOLD,
        activeforeground=BG,
        relief="flat",
        padx=20,
        pady=8,
        command=lambda t=tab: show_message(
            t,
            t + " section"
        )
    ).pack(
        side="left"
    )


# =========================================================
# TWO COLUMN AREA
# =========================================================

columns = tk.Frame(
    page,
    bg=BG
)

columns.pack(
    fill="x"
)


left_column = tk.Frame(
    columns,
    bg=BG
)

left_column.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 12)
)


right_column = tk.Frame(
    columns,
    bg=BG,
    width=360
)

right_column.pack(
    side="right",
    fill="y"
)

right_column.pack_propagate(False)


# =========================================================
# THE LEGEND CARD
# =========================================================

legend_card = tk.Frame(
    left_column,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)

legend_card.pack(
    fill="x",
    pady=(0, 15)
)


legend_title = tk.Frame(
    legend_card,
    bg=CARD
)

legend_title.pack(
    fill="x",
    padx=20,
    pady=(16, 8)
)


tk.Label(
    legend_title,
    text="❖",
    font=("Arial", 19),
    bg=CARD,
    fg=GOLD
).pack(
    side="left",
    padx=(0, 10)
)


tk.Label(
    legend_title,
    text="The Legend",
    font=("Georgia", 15, "bold"),
    bg=CARD,
    fg=GOLD
).pack(
    side="left"
)


legend_text = (
    "The Thunder Dragon, known as Druk in Bhutan, is a sacred and powerful\n"
    "creature believed to control the weather. It is said to live in the high mountains\n"
    "and deep within the clouds, appearing during storms with flashes of lightning\n"
    "and thunder. The dragon is a symbol of strength, protection and good fortune,\n"
    "bringing much-needed rain for crops and the people of Bhutan.\n\n"
    "According to legend, the Thunder Dragon protects the kingdom and its people.\n"
    "When it is angry, it can cause floods, storms, and destruction. When it is happy,\n"
    "it brings rain, fertile land and prosperity."
)


tk.Label(
    legend_card,
    text=legend_text,
    font=("Arial", 10),
    bg=CARD,
    fg=TEXT,
    justify="left"
).pack(
    anchor="w",
    padx=50,
    pady=5
)


tk.Label(
    legend_card,
    text="────────────── ❖ ──────────────",
    font=("Arial", 10),
    bg=CARD,
    fg="#796337"
).pack(
    pady=8
)


tk.Label(
    legend_card,
    text="“When the Thunder Dragon roars,\n"
         "the mountains echo and the land comes alive.”",
    font=("Georgia", 11, "italic"),
    bg=CARD,
    fg=LIGHT_GOLD,
    justify="center"
).pack(
    pady=(0, 18)
)


# =========================================================
# KEY FACTS
# =========================================================

facts_card = tk.Frame(
    left_column,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)

facts_card.pack(
    fill="x",
    pady=(0, 15)
)


tk.Label(
    facts_card,
    text="Key Facts",
    font=("Georgia", 14, "bold"),
    bg=CARD,
    fg=GOLD
).pack(
    anchor="w",
    padx=20,
    pady=(14, 10)
)


# =========================================================
# KEY FACTS WITH ACTUAL IMAGES
# =========================================================

facts = [
    (
        "thunder_dragon.png",
        "Also Known As",
        "Druk"
    ),
    (
        "jomolhari.png",
        "Main Element",
        "Water / Storm"
    ),
    (
        "black_mountain (2).png",
        "Habitat",
        "Mountains & Clouds"
    ),
    (
        "yeti.png",
        "Symbolises",
        "Protection & Prosperity"
    )
]


facts_row = tk.Frame(
    facts_card,
    bg=CARD
)

facts_row.pack(
    fill="x",
    padx=10,
    pady=(0, 18)
)


for index, fact in enumerate(facts):

    image_file, title, value = fact


    # Divider
    if index > 0:

        tk.Frame(
            facts_row,
            bg="#39414a",
            width=1,
            height=115
        ).pack(
            side="left",
            padx=5
        )


    fact_box = tk.Frame(
        facts_row,
        bg=CARD
    )

    fact_box.pack(
        side="left",
        fill="both",
        expand=True
    )


    # Load actual image
    fact_photo = load_image(
        image_file,
        (75, 55)
    )


    # Display image
    if fact_photo:

        fact_image = tk.Label(
            fact_box,
            image=fact_photo,
            bg=CARD
        )

        fact_image.pack(
            pady=(3, 6)
        )

    else:

        tk.Label(
            fact_box,
            text="Image\nnot found",
            font=("Arial", 7),
            bg="#183b50",
            fg=LIGHT_TEXT,
            width=10,
            height=4
        ).pack(
            pady=(3, 6)
        )


    # Fact title
    tk.Label(
        fact_box,
        text=title,
        font=("Arial", 8),
        bg=CARD,
        fg=LIGHT_TEXT
    ).pack()


    # Fact value
    tk.Label(
        fact_box,
        text=value,
        font=("Arial", 9, "bold"),
        bg=CARD,
        fg=TEXT
    ).pack(
        pady=(3, 0)
    )


# =========================================================
# EXPLORE MORE
# =========================================================

tk.Label(
    left_column,
    text="♧  Explore More",
    font=("Georgia", 14, "bold"),
    bg=BG,
    fg=GOLD
).pack(
    anchor="w",
    pady=(2, 8)
)


explore_frame = tk.Frame(
    left_column,
    bg=BG
)

explore_frame.pack(
    fill="x"
)


def explore_button(parent, icon, text, command):

    button = tk.Button(
        parent,
        text=icon + "  " + text + "  →",
        font=("Arial", 9, "bold"),
        bg=BG,
        fg=TEXT,
        activebackground="#263b47",
        activeforeground=GOLD,
        relief="solid",
        bd=1,
        highlightbackground=BORDER,
        padx=12,
        pady=10,
        command=command
    )

    button.pack(
        side="left",
        fill="x",
        expand=True,
        padx=4
    )


explore_button(
    explore_frame,
    "▣",
    "Read More Stories",
    open_story
)


explore_button(
    explore_frame,
    "🐉",
    "View Related Creatures",
    open_creatures
)


explore_button(
    explore_frame,
    "◎",
    "Explore Bhutan's Regions",
    open_regions
)


# =========================================================
# VIDEO CARD
# =========================================================

video_card = tk.Frame(
    right_column,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)

video_card.pack(
    fill="x",
    pady=(0, 15)
)


video_photo = load_image(
    "thunder_dragon.png",
    (335, 125)
)


video_image_frame = tk.Frame(
    video_card,
    bg=CARD
)

video_image_frame.pack(
    fill="x",
    padx=8,
    pady=8
)


if video_photo:

    video_label = tk.Label(
        video_image_frame,
        image=video_photo,
        bg=CARD
    )

    video_label.pack()

else:

    tk.Label(
        video_image_frame,
        text="Thunder Dragon Image\n"
             "thunder_dragon.png",
        font=("Arial", 10),
        bg="#183b50",
        fg=LIGHT_TEXT,
        height=6
    ).pack(
        fill="x"
    )


tk.Button(
    video_image_frame,
    text="▶",
    font=("Arial", 18),
    bg=GOLD,
    fg=BG,
    activebackground=LIGHT_GOLD,
    activeforeground=BG,
    relief="flat",
    command=play_video
).place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)


tk.Label(
    video_card,
    text="The Thunder Dragon – A Bhutanese Legend",
    font=("Arial", 9, "bold"),
    bg=CARD,
    fg=TEXT
).pack(
    anchor="w",
    padx=12
)


tk.Label(
    video_card,
    text="(2:45 min)",
    font=("Arial", 8),
    bg=CARD,
    fg=LIGHT_TEXT
).pack(
    anchor="w",
    padx=12,
    pady=(2, 12)
)


# =========================================================
# RELATED MYTHS
# =========================================================

related_card = tk.Frame(
    right_column,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)

related_card.pack(
    fill="x",
    pady=(0, 15)
)


related_header = tk.Frame(
    related_card,
    bg=CARD
)

related_header.pack(
    fill="x",
    padx=12,
    pady=12
)


tk.Label(
    related_header,
    text="❖  Related Myths",
    font=("Georgia", 13, "bold"),
    bg=CARD,
    fg=GOLD
).pack(
    side="left"
)


tk.Button(
    related_header,
    text="View all →",
    font=("Arial", 7),
    bg=CARD,
    fg=LIGHT_TEXT,
    relief="flat",
    command=lambda: show_message(
        "Related Myths",
        "View all related myths"
    )
).pack(
    side="right"
)


related_myths = [
    (
        "yeti.png",
        "The Yeti",
        "A mysterious being said to live\n"
        "in the Himalayas."
    ),
    (
        "firebird (1).png",
        "The Firebird",
        "A magical bird that symbolizes rebirth,\n"
        "hope and the eternal cycle of life."
    ),
    (
        "black_mountain (2).png",
        "The Black Mountain",
        "A sacred mountain with hidden\n"
        "powers and ancient secrets."
    )
]


for image_file, name, description in related_myths:

    item = tk.Frame(
        related_card,
        bg=CARD
    )

    item.pack(
        fill="x",
        padx=10,
        pady=5
    )


    photo = load_image(
        image_file,
        (90, 60)
    )


    if photo:

        image_label = tk.Label(
            item,
            image=photo,
            bg=CARD
        )

        image_label.pack(
            side="left"
        )

    else:

        tk.Label(
            item,
            text="Image\n" + image_file,
            bg="#183b50",
            fg=LIGHT_TEXT,
            width=12,
            height=4,
            font=("Arial", 7)
        ).pack(
            side="left"
        )


    text_frame = tk.Frame(
        item,
        bg=CARD
    )

    text_frame.pack(
        side="left",
        fill="both",
        expand=True,
        padx=10
    )


    tk.Label(
        text_frame,
        text=name,
        font=("Arial", 9, "bold"),
        bg=CARD,
        fg=TEXT
    ).pack(
        anchor="w"
    )


    tk.Label(
        text_frame,
        text=description,
        font=("Arial", 7),
        bg=CARD,
        fg=LIGHT_TEXT,
        justify="left"
    ).pack(
        anchor="w",
        pady=(2, 0)
    )


    tk.Button(
        item,
        text="›",
        font=("Arial", 17),
        bg=CARD,
        fg=GOLD,
        relief="flat",
        command=lambda n=name: related_myth(n)
    ).pack(
        side="right"
    )


# =========================================================
# RELATED REGIONS
# =========================================================

regions_card = tk.Frame(
    right_column,
    bg=CARD,
    highlightbackground=BORDER,
    highlightthickness=1
)

regions_card.pack(
    fill="x"
)


region_header = tk.Frame(
    regions_card,
    bg=CARD
)

region_header.pack(
    fill="x",
    padx=12,
    pady=12
)


tk.Label(
    region_header,
    text="❖  Related Regions",
    font=("Georgia", 13, "bold"),
    bg=CARD,
    fg=GOLD
).pack(
    side="left"
)


tk.Button(
    region_header,
    text="View all →",
    font=("Arial", 7),
    bg=CARD,
    fg=LIGHT_TEXT,
    relief="flat",
    command=lambda: show_message(
        "Regions",
        "View all related regions"
    )
).pack(
    side="right"
)


region_item = tk.Frame(
    regions_card,
    bg=CARD
)

region_item.pack(
    fill="x",
    padx=10,
    pady=(0, 12)
)


region_photo = load_image(
    "jomolhari.png",
    (95, 60)
)


if region_photo:

    region_image_label = tk.Label(
        region_item,
        image=region_photo,
        bg=CARD
    )

    region_image_label.pack(
        side="left"
    )

else:

    tk.Label(
        region_item,
        text="Bhutan\njomolhari.png",
        bg="#183b50",
        fg=LIGHT_TEXT,
        width=12,
        height=4,
        font=("Arial", 7)
    ).pack(
        side="left"
    )


region_info = tk.Frame(
    region_item,
    bg=CARD
)

region_info.pack(
    side="left",
    fill="both",
    expand=True,
    padx=10
)


tk.Label(
    region_info,
    text="Bhutan",
    font=("Arial", 9, "bold"),
    bg=CARD,
    fg=TEXT
).pack(
    anchor="w"
)


tk.Label(
    region_info,
    text="Land of the Thunder Dragon",
    font=("Arial", 7),
    bg=CARD,
    fg=LIGHT_TEXT
).pack(
    anchor="w",
    pady=(3, 0)
)


tk.Button(
    region_item,
    text="›",
    font=("Arial", 17),
    bg=CARD,
    fg=GOLD,
    relief="flat",
    command=lambda: show_message(
        "Bhutan",
        "Explore Bhutan - Land of the Thunder Dragon"
    )
).pack(
    side="right"
)


# =========================================================
# FOOTER SPACE
# =========================================================

tk.Frame(
    content,
    height=30,
    bg=BG
).pack()


# =========================================================
# START PROGRAM
# =========================================================

root.mainloop()