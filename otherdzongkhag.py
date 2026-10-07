#otherdzongkhag.py code
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk, ImageOps, ImageEnhance


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()
root.title("MythLab - Other Dzongkhags")
root.geometry("1280x800")
root.minsize(1000, 650)
root.configure(bg="#061927")


# =========================================================
# COLORS
# =========================================================

BG = "#061927"
SIDEBAR = "#031522"
CARD = "#0A2638"
CARD_DARK = "#071C2B"
GOLD = "#D8AE4D"
LIGHT_GOLD = "#E6C56B"
TEXT = "#F0EAD8"
MUTED = "#B9B6AC"
BORDER = "#705A32"


# =========================================================
# PROJECT FOLDER
# =========================================================

ROOT = Path(__file__).resolve().parent
IMAGE_FOLDER = ROOT / "assets"


# =========================================================
# KEEP IMAGE REFERENCES
# =========================================================

image_refs = []


# =========================================================
# IMAGE FILES
# =========================================================

DZONGKHAG_IMAGES = {

    "Trashigang": "trashigang.jpg",

    "Trashiyangtse": "trashiyangtse.jpg",

    "Samdrup Jongkhar": "samdrupjongkhar.png",

    "Zhemgang": "zhemgang.jpg",

    "Trongsa": "trongsa.jpg",

    "Wangdue Phodrang": "wangdue_phodrang.jpg"
}


# =========================================================
# FIND IMAGE
# =========================================================

def find_image(name):

    if name in DZONGKHAG_IMAGES:

        path = IMAGE_FOLDER / DZONGKHAG_IMAGES[name]

        if path.exists():

            print("IMAGE FOUND:")
            print(name, "->", path)

            return path

        else:

            print("IMAGE NOT FOUND:")
            print(path)


    search_name = (
        name.lower()
        .replace(" ", "")
        .replace("_", "")
        .replace("-", "")
    )


    try:

        for path in IMAGE_FOLDER.iterdir():

            if not path.is_file():
                continue

            if path.suffix.lower() not in [
                ".jpg",
                ".jpeg",
                ".png",
                ".webp"
            ]:
                continue


            file_name = (
                path.stem.lower()
                .replace(" ", "")
                .replace("_", "")
                .replace("-", "")
            )


            if search_name in file_name:

                print("IMAGE FOUND BY SEARCH:")
                print(name, "->", path)

                return path


    except Exception as e:

        print("ERROR SEARCHING IMAGE FOLDER:")
        print(e)


    print("NO IMAGE FOUND FOR:", name)

    return None


# =========================================================
# LOAD IMAGE
# =========================================================

def load_dzongkhag_image(name, size):

    path = find_image(name)

    if path is None:
        return None


    try:

        img = Image.open(path).convert("RGB")

        img = ImageOps.fit(
            img,
            size,
            method=Image.Resampling.LANCZOS
        )

        photo = ImageTk.PhotoImage(img)

        image_refs.append(photo)

        print("IMAGE LOADED:", name)

        return photo


    except Exception as e:

        print("ERROR LOADING IMAGE:")
        print(path)
        print(e)

        return None


# =========================================================
# SIDEBAR
# =========================================================

sidebar = tk.Frame(
    root,
    bg=SIDEBAR,
    width=210
)

sidebar.pack(
    side="left",
    fill="y"
)

sidebar.pack_propagate(False)


# =========================================================
# LOGO
# =========================================================

logo_frame = tk.Frame(
    sidebar,
    bg=SIDEBAR
)

logo_frame.pack(
    pady=(25, 20)
)


logo_symbol = tk.Label(
    logo_frame,
    text="☯",
    font=("Arial", 40),
    fg=GOLD,
    bg=SIDEBAR
)

logo_symbol.pack()


logo = tk.Label(
    logo_frame,
    text="MythLab",
    font=("Georgia", 23, "bold"),
    fg=LIGHT_GOLD,
    bg=SIDEBAR
)

logo.pack()


tagline = tk.Label(
    logo_frame,
    text="Explore. Learn. Believe.",
    font=("Arial", 9),
    fg=TEXT,
    bg=SIDEBAR
)

tagline.pack(
    pady=(2, 0)
)


# =========================================================
# NAVIGATION FUNCTION
# =========================================================

def create_nav(text, icon, active=False):

    if active:
        bg = "#4A4129"
    else:
        bg = SIDEBAR


    frame = tk.Frame(
        sidebar,
        bg=bg,
        height=45
    )

    frame.pack(
        fill="x",
        padx=10,
        pady=2
    )


    icon_label = tk.Label(
        frame,
        text=icon,
        font=("Arial", 19),
        fg=LIGHT_GOLD,
        bg=bg,
        width=3
    )

    icon_label.pack(
        side="left",
        padx=(3, 2)
    )


    text_label = tk.Label(
        frame,
        text=text,
        font=("Arial", 11),
        fg=TEXT,
        bg=bg,
        anchor="w"
    )

    text_label.pack(
        side="left",
        fill="x"
    )


    return frame


# =========================================================
# NAVIGATION ITEMS
# =========================================================

create_nav("Home", "⌂")
create_nav("Myths", "▤")
create_nav("Creatures", "☯")
create_nav("Regions", "◎", True)
create_nav("My Tasks", "▣")
create_nav("Quiz", "?")
create_nav("Favourites", "♡")
create_nav("About", "ⓘ")


# =========================================================
# SIDEBAR BOTTOM
# =========================================================

bottom_frame = tk.Frame(
    sidebar,
    bg=SIDEBAR
)

bottom_frame.pack(
    side="bottom",
    fill="x",
    padx=15,
    pady=20
)


mountains = tk.Label(
    bottom_frame,
    text="⌁⌁⌁",
    font=("Georgia", 35),
    fg="#725525",
    bg=SIDEBAR
)

mountains.pack()


line = tk.Frame(
    bottom_frame,
    height=1,
    bg="#725525"
)

line.pack(
    fill="x",
    pady=12
)


quote = tk.Label(
    bottom_frame,
    text="“Every myth is a door\nto a deeper wisdom.”\n\n— Bhutanese Wisdom",
    font=("Georgia", 10, "italic"),
    fg="#D8BC73",
    bg=SIDEBAR,
    justify="center"
)

quote.pack()


# =========================================================
# MAIN AREA
# =========================================================

main = tk.Frame(
    root,
    bg=BG
)

main.pack(
    side="left",
    fill="both",
    expand=True
)


# =========================================================
# HERO SECTION
# =========================================================

hero = tk.Frame(
    main,
    bg="#0A2535",
    height=200
)

hero.pack(
    fill="x"
)

hero.pack_propagate(False)


# =========================================================
# HERO BACKGROUND IMAGE
# =========================================================

welcome_path = IMAGE_FOLDER / "welcome.png"

if welcome_path.exists():

    try:

        welcome_img = Image.open(
            welcome_path
        ).convert("RGB")


        # Fit image to hero area

        welcome_img = ImageOps.fit(
            welcome_img,
            (1100, 180),
            method=Image.Resampling.LANCZOS
        )


        # Darken image slightly so text is easier to see

        enhancer = ImageEnhance.Brightness(
            welcome_img
        )

        welcome_img = enhancer.enhance(0.55)


        # Convert to Tkinter image

        welcome_photo = ImageTk.PhotoImage(
            welcome_img
        )


        # Keep image reference

        image_refs.append(
            welcome_photo
        )


        # Display background

        hero_background = tk.Label(
            hero,
            image=welcome_photo,
            borderwidth=0
        )

        hero_background.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )


        print("WELCOME IMAGE FOUND:")
        print(welcome_path)


    except Exception as e:

        print("ERROR LOADING welcome.png:")
        print(e)


else:

    print("WELCOME.PNG NOT FOUND:")
    print(welcome_path)


# =========================================================
# BREADCRUMB
# =========================================================

breadcrumb = tk.Label(
    hero,
    text="Home   ›   Regions   ›   Other Dzongkhags",
    font=("Arial", 10),
    fg="#E5E0D5",
    bg="#0A2535"
)

breadcrumb.place(
    x=38,
    y=20
)


# =========================================================
# TITLE FRAME
# =========================================================

title_frame = tk.Frame(
    hero,
    bg="#0A2535"
)

title_frame.place(
    x=38,
    y=55
)


# =========================================================
# TITLE ICON
# =========================================================

title_icon = tk.Label(
    title_frame,
    text="✥",
    font=("Georgia", 37),
    fg=GOLD,
    bg="#0A2535"
)

title_icon.pack(
    side="left",
    padx=(0, 12)
)


# =========================================================
# TITLE
# =========================================================

title = tk.Label(
    title_frame,
    text="Other Dzongkhags",
    font=("Georgia", 31, "bold"),
    fg="#F3E5C3",
    bg="#0A2535"
)

title.pack(
    side="left"
)


# =========================================================
# DESCRIPTION
# =========================================================

description = tk.Label(
    hero,
    text="Discover the rich myths, legends and sacred stories\n"
         "from the different Dzongkhags of Bhutan.",
    font=("Arial", 11),
    fg="#F0ECE3",
    bg="#0A2535",
    justify="left"
)

description.place(
    x=94,
    y=112
)


# =========================================================
# CONTENT
# =========================================================

content = tk.Frame(
    main,
    bg=BG
)

content.pack(
    fill="both",
    expand=True,
    padx=35,
    pady=18
)


# =========================================================
# SEARCH
# =========================================================

search_frame = tk.Frame(
    content,
    bg=BG
)

search_frame.pack(
    fill="x",
    pady=(0, 18)
)


# Search box container

search_container = tk.Frame(
    search_frame,
    bg="#081F30",
    width=350,
    height=42
)

search_container.pack(
    side="left"
)

search_container.pack_propagate(False)


# Search icon

search_icon = tk.Label(
    search_container,
    text="⌕",
    font=("Arial", 20),
    fg=GOLD,
    bg="#081F30"
)

search_icon.place(
    x=10,
    y=5
)


# Search entry

search_box = tk.Entry(
    search_container,
    font=("Arial", 11),
    bg="#081F30",
    fg="#AAA69C",
    insertbackground="white",
    relief="flat",
    bd=0
)

search_box.place(
    x=42,
    y=9,
    width=295,
    height=25
)


search_box.insert(
    0,
    "Search dzongkhags..."
)


# =========================================================
# FILTER BUTTONS
# =========================================================

filters_frame = tk.Frame(
    search_frame,
    bg=BG
)

filters_frame.pack(
    side="left",
    padx=15
)


def filter_button(text, active=False):

    if active:

        bg = "#F0D071"
        fg = "#172331"

    else:

        bg = "#0B2232"
        fg = TEXT


    button = tk.Button(
        filters_frame,
        text=text,
        font=("Arial", 9),
        bg=bg,
        fg=fg,
        activebackground=GOLD,
        activeforeground="#172331",
        relief="flat",
        bd=0,
        padx=14,
        pady=7
    )

    button.pack(
        side="left",
        padx=3
    )


filter_button("All", True)
filter_button("Myths")
filter_button("Creatures")
filter_button("Sacred Places")
filter_button("Stories")


# =========================================================
# FILTER BUTTONS
# =========================================================

filters_frame = tk.Frame(
    search_frame,
    bg=BG
)

filters_frame.pack(
    side="left",
    padx=15
)


def filter_button(text, active=False):

    if active:

        bg = "#F0D071"
        fg = "#172331"

    else:

        bg = "#0B2232"
        fg = TEXT


    button = tk.Button(
        filters_frame,
        text=text,
        font=("Arial", 9),
        bg=bg,
        fg=fg,
        activebackground=GOLD,
        activeforeground="#172331",
        relief="flat",
        bd=0,
        padx=14,
        pady=7
    )

    button.pack(
        side="left",
        padx=3
    )


filter_button("All", True)
filter_button("Myths")
filter_button("Creatures")
filter_button("Sacred Places")
filter_button("Stories")


# =========================================================
# SECTION TITLE
# =========================================================

section = tk.Frame(
    content,
    bg=BG
)

section.pack(
    fill="x",
    pady=(0, 12)
)


section_icon = tk.Label(
    section,
    text="☯",
    font=("Arial", 22),
    fg=GOLD,
    bg=BG
)

section_icon.pack(
    side="left"
)


section_title = tk.Label(
    section,
    text="Other Dzongkhags",
    font=("Georgia", 16, "bold"),
    fg=TEXT,
    bg=BG
)

section_title.pack(
    side="left",
    padx=10
)


line_frame = tk.Frame(
    section,
    bg="#66552F",
    height=1
)

line_frame.pack(
    side="left",
    fill="x",
    expand=True,
    padx=12
)


view_all = tk.Label(
    section,
    text="View all →",
    font=("Arial", 9),
    fg="#E3C35D",
    bg=BG
)

view_all.pack(
    side="right"
)


# =========================================================
# DZONGKHAG DATA
# =========================================================

dzongkhags = [

    (
        "Bumthang",
        "Known as the spiritual heart of Bhutan,\n"
        "Bumthang is home to ancient temples,\n"
        "sacred sites and timeless legends.",
        ["Myths", "Sacred Places", "Stories"]
    ),

    (
        "Trashigang",
        "Land of vibrant culture and strong\n"
        "traditions, with unique stories of\n"
        "brave people and mystical beings.",
        ["Myths", "Creatures", "Stories"]
    ),

    (
        "Trashiyangtse",
        "A region of rivers and mountains,\n"
        "known for its rich folklore and\n"
        "sacred heritage.",
        ["Myths", "Sacred Places", "Creatures"]
    ),

    (
        "Mongar",
        "Home to ancient traditions and\n"
        "inspiring legends passed down\n"
        "through generations.",
        ["Myths", "Stories", "Sacred Places"]
    ),

    (
        "Samdrup Jongkhar",
        "A gateway to the east, filled with\n"
        "cultural diversity, forest spirits\n"
        "and hidden tales.",
        ["Myths", "Creatures", "Stories"]
    ),

    (
        "Zhemgang",
        "Known for its peaceful valleys\n"
        "and legends of nature, spirits\n"
        "and ancestral wisdom.",
        ["Myths", "Creatures", "Sacred Places"]
    ),

    (
        "Trongsa",
        "The central land of power and\n"
        "history, where royal paths and\n"
        "mystical stories meet.",
        ["Myths", "Sacred Places", "Stories"]
    ),

    (
        "Wangdue Phodrang",
        "A land of majestic views and\n"
        "fascinating legends, from ancient\n"
        "kings to sacred rivers.",
        ["Myths", "Creatures", "Stories"]
    )
]


# =========================================================
# CARDS FRAME
# =========================================================

cards_frame = tk.Frame(
    content,
    bg=BG
)

cards_frame.pack(
    fill="both",
    expand=True
)


# =========================================================
# CARD FUNCTION
# =========================================================

def create_card(
    parent,
    name,
    description,
    tags,
    row,
    column
):

    card = tk.Frame(
        parent,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1,
        width=240,
        height=225
    )

    card.grid(
        row=row,
        column=column,
        padx=8,
        pady=8,
        sticky="nsew"
    )

    card.grid_propagate(False)


    # =====================================================
    # IMAGE AREA
    # =====================================================

    image = tk.Frame(
        card,
        bg="#31566A",
        height=95
    )

    image.pack(
        fill="x"
    )

    image.pack_propagate(False)


    # Load Dzongkhag image

    card_image = load_dzongkhag_image(
        name,
        (240, 95)
    )


    # =====================================================
    # DISPLAY IMAGE
    # =====================================================

    if card_image is not None:

        image_label = tk.Label(
            image,
            image=card_image,
            bg="#31566A",
            borderwidth=0
        )

        image_label.pack(
            fill="both",
            expand=True
        )

    else:

        mountain_text = tk.Label(
            image,
            text="     /\\       /\\       /\\\n"
                 "    /  \\  /\\ /  \\  /\\\n"
                 "___/____\\/__V____\\/__\\___",
            font=("Arial", 16),
            fg="#B8C8C5",
            bg="#31566A",
            justify="center"
        )

        mountain_text.pack(
            expand=True
        )


    # =====================================================
    # CARD BODY
    # =====================================================

    body = tk.Frame(
        card,
        bg=CARD
    )

    body.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=7
    )


    # Dzongkhag name

    name_label = tk.Label(
        body,
        text="⌖  " + name,
        font=("Georgia", 12, "bold"),
        fg="#EEE0BB",
        bg=CARD,
        anchor="w"
    )

    name_label.pack(
        fill="x"
    )


    # Description

    desc = tk.Label(
        body,
        text=description,
        font=("Arial", 8),
        fg="#D0CEC8",
        bg=CARD,
        justify="left",
        anchor="w"
    )

    desc.pack(
        fill="x",
        pady=(5, 4)
    )


    # Bottom section

    bottom = tk.Frame(
        body,
        bg=CARD
    )

    bottom.pack(
        fill="x",
        side="bottom"
    )


    # Tags

    for tag in tags:

        tag_label = tk.Label(
            bottom,
            text=tag,
            font=("Arial", 7),
            fg="#E4D9C2",
            bg="#102D3D",
            padx=5,
            pady=3
        )

        tag_label.pack(
            side="left",
            padx=(0, 3)
        )


    # Arrow

    arrow = tk.Label(
        bottom,
        text="→",
        font=("Arial", 14),
        fg="#E0BB50",
        bg=CARD
    )

    arrow.pack(
        side="right"
    )


# =========================================================
# CARD GRID
# =========================================================

for i in range(4):

    cards_frame.grid_columnconfigure(
        i,
        weight=1
    )


# =========================================================
# CREATE 8 CARDS
# =========================================================

for i, data in enumerate(dzongkhags):

    row = i // 4
    column = i % 4

    create_card(
        cards_frame,
        data[0],
        data[1],
        data[2],
        row,
        column
    )


# =========================================================
# EXPLORE MORE
# =========================================================

explore = tk.Frame(
    content,
    bg="#0A2535",
    highlightbackground=BORDER,
    highlightthickness=1,
    height=75
)

explore.pack(
    fill="x",
    pady=(12, 0)
)

explore.pack_propagate(False)


explore_icon = tk.Label(
    explore,
    text="✥",
    font=("Georgia", 30),
    fg=GOLD,
    bg="#0A2535"
)

explore_icon.pack(
    side="left",
    padx=25
)


explore_text = tk.Frame(
    explore,
    bg="#0A2535"
)

explore_text.pack(
    side="left",
    expand=True,
    anchor="w"
)


explore_title = tk.Label(
    explore_text,
    text="Explore More",
    font=("Georgia", 13, "bold"),
    fg=TEXT,
    bg="#0A2535"
)

explore_title.pack(
    anchor="w"
)


explore_description = tk.Label(
    explore_text,
    text="Discover the myths and legends of all 20 Dzongkhags of Bhutan.",
    font=("Arial", 8),
    fg="#C7C4BB",
    bg="#0A2535"
)

explore_description.pack(
    anchor="w"
)


explore_button = tk.Button(
    explore,
    text="View All Dzongkhags  →",
    font=("Arial", 9),
    fg="#E2C15B",
    bg="#0A2535",
    activebackground=GOLD,
    activeforeground="#172331",
    relief="solid",
    bd=1,
    padx=15,
    pady=7
)

explore_button.pack(
    side="right",
    padx=25
)


# =========================================================
# RUN PROGRAM
# =========================================================

root.mainloop()