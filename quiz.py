import tkinter as tk
from tkinter import messagebox
from pathlib import Path

from PIL import Image, ImageTk, ImageOps


# ============================================================
# COLOURS
# ============================================================

BG = "#071b2b"
SIDEBAR_BG = "#061522"
CARD = "#102b3d"
CARD_DARK = "#0b2435"

GOLD = "#d6a84f"
GOLD_LIGHT = "#f5d486"

TEXT = "#f5ead0"
LIGHT_TEXT = "#c7c1b3"
WHITE = "#ffffff"

GREEN = "#55c77a"
BLUE = "#7199d8"
GREY = "#b9bac5"
RED = "#d9535f"


# ============================================================
# PROJECT / IMAGE SETTINGS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent
IMAGE_DIR = PROJECT_DIR / "images"

# Keep images in memory
quiz_image_refs = []


# ============================================================
# QUIZ VARIABLES
# ============================================================

quiz_content = None

current_quiz = None

current_question = 0

selected_answers = {}

answered_questions = {}

quiz_score = 0

# 10 minute timer
time_left = 10 * 60

timer_job = None


# ============================================================
# FIND IMAGE
# ============================================================

def find_image(filename):
    """
    Find an image inside the images folder
    or beside quiz.py.
    """

    # First check images folder
    path = IMAGE_DIR / filename

    if path.exists():
        return path

    # Then check beside quiz.py
    path = PROJECT_DIR / filename

    if path.exists():
        return path

    # Try similar filenames
    stem = Path(filename).stem.lower()
    extension = Path(filename).suffix.lower()

    for folder in [IMAGE_DIR, PROJECT_DIR]:

        if folder.is_dir():

            for item in folder.iterdir():

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


# ============================================================
# LOAD IMAGE
# ============================================================

def load_quiz_image(filename, size):

    path = find_image(filename)

    if path is None:
        return None

    try:

        image = Image.open(path).convert("RGB")

        image = ImageOps.fit(
            image,
            size,
            method=Image.Resampling.LANCZOS
        )

        photo = ImageTk.PhotoImage(image)

        quiz_image_refs.append(photo)

        return photo

    except Exception as error:

        print("Could not load image:", filename)
        print(error)

        return None


# ============================================================
# QUIZ QUESTIONS
# ============================================================

quiz_questions = [

    {
        "question":
            "Which of the following is a famous sacred site "
            "in Bhutan known for its tiger's nest monastery?",

        "options": [
            "Tiger's Nest (Paro Taktsang)",
            "Boudhanath Stupa",
            "Angkor Wat",
            "Mount Fuji"
        ],

        "answer": 0
    },

    {
        "question":
            "What is the national animal of Bhutan?",

        "options": [
            "Takin",
            "Yak",
            "Snow Leopard",
            "Red Panda"
        ],

        "answer": 0
    },

    {
        "question":
            "What does the Bhutanese word 'Druk' commonly mean?",

        "options": [
            "Thunder Dragon",
            "Mountain Spirit",
            "Snow Lion",
            "Fire Bird"
        ],

        "answer": 0
    },

    {
        "question":
            "What is the capital city of Bhutan?",

        "options": [
            "Paro",
            "Punakha",
            "Thimphu",
            "Bumthang"
        ],

        "answer": 2
    },

    {
        "question":
            "How many Dzongkhags are there in Bhutan?",

        "options": [
            "15",
            "20",
            "25",
            "30"
        ],

        "answer": 1
    },

    {
        "question":
            "Which mythical creature is strongly associated "
            "with Bhutanese mythology?",

        "options": [
            "Druk",
            "Phoenix",
            "Minotaur",
            "Kraken"
        ],

        "answer": 0
    },

    {
        "question":
            "Which mountain is considered sacred in Bhutan?",

        "options": [
            "Mount Everest",
            "Mount Fuji",
            "Mount Jomolhari",
            "K2"
        ],

        "answer": 2
    },

    {
        "question":
            "What is Paro Taktsang also known as?",

        "options": [
            "Tiger's Nest",
            "Dragon's Palace",
            "Golden Temple",
            "Mountain Monastery"
        ],

        "answer": 0
    },

    {
        "question":
            "The Takin is best described as what?",

        "options": [
            "A mythical dragon",
            "A large mountain animal",
            "A bird",
            "A river spirit"
        ],

        "answer": 1
    },

    {
        "question":
            "Which two countries border Bhutan?",

        "options": [
            "India and China",
            "India and Nepal",
            "China and Nepal",
            "India and Tibet"
        ],

        "answer": 0
    }

]


# ============================================================
# SHOW QUIZ SELECTION PAGE
# ============================================================

def show_quiz(content):

    global quiz_content
    global timer_job

    quiz_content = content

    # Stop timer if returning from a quiz
    if timer_job is not None:

        try:
            content.after_cancel(timer_job)
        except:
            pass

        timer_job = None

    # Clear current page
    for widget in content.winfo_children():
        widget.destroy()

    # Clear old images
    quiz_image_refs.clear()

    # ========================================================
    # BANNER
    # ========================================================

    banner = tk.Frame(
        content,
        bg=BG,
        height=185
    )

    banner.pack(
        fill="x",
        padx=25,
        pady=(15, 8)
    )

    banner.pack_propagate(False)

    banner_image = load_quiz_image(
        "quiz_banner.png",
        (1050, 185)
    )

    if banner_image:

        tk.Label(
            banner,
            image=banner_image,
            bg=BG,
            bd=0
        ).place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

    # Dark title area
    title_area = tk.Frame(
        banner,
        bg="#071b2b"
    )

    title_area.place(
        x=25,
        y=30
    )

    tk.Label(
        title_area,
        text="?",
        font=("Georgia", 30, "bold"),
        bg="#071b2b",
        fg=GOLD_LIGHT
    ).pack(
        side="left",
        padx=(5, 15)
    )

    title_text = tk.Frame(
        title_area,
        bg="#071b2b"
    )

    title_text.pack(
        side="left"
    )

    tk.Label(
        title_text,
        text="Quiz",
        font=("Georgia", 31, "bold"),
        bg="#071b2b",
        fg=TEXT
    ).pack(
        anchor="w"
    )

    tk.Label(
        title_text,
        text="Test your knowledge of myths, legends and mythical creatures\n"
             "from Bhutan and beyond!",
        font=("Arial", 10),
        bg="#071b2b",
        fg=WHITE,
        justify="left"
    ).pack(
        anchor="w"
    )

    # ========================================================
    # CATEGORY BUTTONS
    # ========================================================

    category_bar = tk.Frame(
        content,
        bg=BG
    )

    category_bar.pack(
        fill="x",
        padx=25,
        pady=(5, 12)
    )

    categories = [
        "All Quizzes",
        "Myths",
        "Creatures",
        "Regions",
        "General Knowledge"
    ]

    for index, category in enumerate(categories):

        if index == 0:

            button_bg = GOLD
            button_fg = BG

        else:

            button_bg = BG
            button_fg = TEXT

        tk.Button(
            category_bar,
            text=category,
            font=("Arial", 9),
            bg=button_bg,
            fg=button_fg,
            activebackground=GOLD,
            activeforeground=BG,
            relief="solid",
            bd=1,
            padx=15,
            pady=7,
            command=lambda c=category: category_selected(c)
        ).pack(
            side="left",
            padx=(0, 8)
        )

    # ========================================================
    # BODY
    # ========================================================

    body = tk.Frame(
        content,
        bg=BG
    )

    body.pack(
        fill="x",
        padx=25
    )

    # Left
    left = tk.Frame(
        body,
        bg=BG
    )

    left.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 12)
    )

    # Right
    right = tk.Frame(
        body,
        bg=BG,
        width=275
    )

    right.pack(
        side="right",
        fill="y"
    )

    right.pack_propagate(False)

    # ========================================================
    # AVAILABLE QUIZZES TITLE
    # ========================================================

    heading = tk.Frame(
        left,
        bg=BG
    )

    heading.pack(
        fill="x",
        pady=(0, 10)
    )

    tk.Label(
        heading,
        text="✥",
        font=("Arial", 20),
        bg=BG,
        fg=GOLD
    ).pack(
        side="left",
        padx=(0, 8)
    )

    tk.Label(
        heading,
        text="Available Quizzes",
        font=("Georgia", 17, "bold"),
        bg=BG,
        fg=GOLD
    ).pack(
        side="left"
    )

    tk.Frame(
        heading,
        bg="#5c4a2b",
        height=1
    ).pack(
        side="left",
        fill="x",
        expand=True,
        padx=(15, 0)
    )

    # ========================================================
    # QUIZ GRID
    # ========================================================

    quiz_grid = tk.Frame(
        left,
        bg=BG
    )

    quiz_grid.pack(
        fill="x"
    )

    quizzes = [

        {
            "category": "Myths",
            "title": "Bhutanese Mythology Quiz",
            "description":
                "Test your knowledge about famous\n"
                "myths and legends from Bhutan.",
            "questions": "10 Questions",
            "difficulty": "Medium",
            "image": "thunder_dragon.png"
        },

        {
            "category": "Creatures",
            "title": "Mythical Creatures Quiz",
            "description":
                "How well do you know Bhutan's\n"
                "mythical creatures and their powers?",
            "questions": "10 Questions",
            "difficulty": "Medium",
            "image": "druk (3).png"
        },

        {
            "category": "Regions",
            "title": "Bhutan Dzongkhags Quiz",
            "description":
                "Explore and test your knowledge\n"
                "of Bhutan's 20 Dzongkhags and legends.",
            "questions": "10 Questions",
            "difficulty": "Easy",
            "image": "paro_taktsang.png"
        },

        {
            "category": "General Knowledge",
            "title": "Mythology Basics",
            "description":
                "A quick quiz to check your general\n"
                "knowledge about myths and folklore.",
            "questions": "10 Questions",
            "difficulty": "Easy",
            "image": "recent_firebird.png"
        },

        {
            "category": "Mixed",
            "title": "Legends & Creatures",
            "description":
                "A mix of myths, creatures and\n"
                "interesting facts from across regions.",
            "questions": "10 Questions",
            "difficulty": "Medium",
            "image": "yeti.png"
        },

        {
            "category": "Challenge",
            "title": "The Ultimate Mythology Challenge",
            "description":
                "Are you a true MythLab explorer?\n"
                "Take this advanced quiz!",
            "questions": "10 Questions",
            "difficulty": "Hard",
            "image": "firebird (1).png"
        }

    ]

    for index, quiz in enumerate(quizzes):

        row = index // 3
        column = index % 3

        create_quiz_card(
            quiz_grid,
            quiz,
            row,
            column
        )

    for column in range(3):

        quiz_grid.grid_columnconfigure(
            column,
            weight=1
        )

    # ========================================================
    # RIGHT SIDE
    # ========================================================

    create_selection_progress(right)

    create_quick_links(right)

    create_selection_quote(right)

    # Bottom spacing

    tk.Frame(
        content,
        bg=BG,
        height=25
    ).pack()


# ============================================================
# QUIZ CARD
# ============================================================

def create_quiz_card(parent, quiz, row, column):

    card = tk.Frame(
        parent,
        bg=CARD,
        highlightbackground="#76582c",
        highlightthickness=1
    )

    card.grid(
        row=row,
        column=column,
        sticky="nsew",
        padx=5,
        pady=5
    )

    # --------------------------------------------------------
    # Image
    # --------------------------------------------------------

    image = load_quiz_image(
        quiz["image"],
        (220, 105)
    )

    if image:

        tk.Label(
            card,
            image=image,
            bg=CARD
        ).pack(
            fill="x",
            padx=5,
            pady=5
        )

    else:

        tk.Label(
            card,
            text="MYTHLAB",
            font=("Georgia", 15, "bold"),
            bg="#183b50",
            fg=GOLD,
            height=5
        ).pack(
            fill="x",
            padx=5,
            pady=5
        )

    # --------------------------------------------------------
    # Category
    # --------------------------------------------------------

    tk.Label(
        card,
        text="  " + quiz["category"] + "  ",
        font=("Arial", 8),
        bg="#183b50",
        fg=TEXT
    ).pack(
        anchor="w",
        padx=8
    )

    # --------------------------------------------------------
    # Title
    # --------------------------------------------------------

    tk.Label(
        card,
        text=quiz["title"],
        font=("Georgia", 11, "bold"),
        bg=CARD,
        fg=TEXT,
        wraplength=220,
        justify="left"
    ).pack(
        anchor="w",
        padx=10,
        pady=(7, 2)
    )

    # --------------------------------------------------------
    # Description
    # --------------------------------------------------------

    tk.Label(
        card,
        text=quiz["description"],
        font=("Arial", 8),
        bg=CARD,
        fg=LIGHT_TEXT,
        justify="left"
    ).pack(
        anchor="w",
        padx=10
    )

    # --------------------------------------------------------
    # Info
    # --------------------------------------------------------

    info = tk.Frame(
        card,
        bg=CARD
    )

    info.pack(
        fill="x",
        padx=10,
        pady=(12, 5)
    )

    tk.Label(
        info,
        text="▣  " + quiz["questions"],
        font=("Arial", 8),
        bg=CARD,
        fg=TEXT
    ).pack(
        side="left"
    )

    difficulty = quiz["difficulty"]

    if difficulty == "Easy":

        difficulty_bg = "#164a34"
        difficulty_fg = GREEN

    elif difficulty == "Hard":

        difficulty_bg = "#54212b"
        difficulty_fg = RED

    else:

        difficulty_bg = "#4b411c"
        difficulty_fg = GOLD_LIGHT

    tk.Label(
        info,
        text="  " + difficulty + "  ",
        font=("Arial", 8),
        bg=difficulty_bg,
        fg=difficulty_fg
    ).pack(
        side="right"
    )

    # --------------------------------------------------------
    # START BUTTON
    # --------------------------------------------------------

    tk.Button(
        card,
        text="Start Quiz  →",
        font=("Arial", 9, "bold"),
        bg=CARD_DARK,
        fg=GOLD_LIGHT,
        activebackground=GOLD,
        activeforeground=BG,
        relief="solid",
        bd=1,
        command=lambda q=quiz: start_quiz(q)
    ).pack(
        fill="x",
        padx=10,
        pady=(4, 10)
    )


# ============================================================
# SELECTION PAGE PROGRESS
# ============================================================

def create_selection_progress(parent):

    frame = tk.Frame(
        parent,
        bg=CARD,
        highlightbackground="#76582c",
        highlightthickness=1
    )

    frame.pack(
        fill="x",
        pady=(0, 12)
    )

    tk.Label(
        frame,
        text="✥  Your Quiz Progress",
        font=("Georgia", 12, "bold"),
        bg=CARD,
        fg=GOLD
    ).pack(
        anchor="w",
        padx=12,
        pady=(12, 5)
    )

    progress_area = tk.Frame(
        frame,
        bg=CARD
    )

    progress_area.pack(
        fill="x",
        padx=8
    )

    donut = tk.Canvas(
        progress_area,
        width=105,
        height=105,
        bg=CARD,
        highlightthickness=0
    )

    donut.pack(
        side="left"
    )

    # Circle

    donut.create_oval(
        12,
        12,
        93,
        93,
        outline="#284b63",
        width=11
    )

    # Completed section

    donut.create_arc(
        12,
        12,
        93,
        93,
        start=90,
        extent=-180,
        style="arc",
        outline=GOLD_LIGHT,
        width=11
    )

    donut.create_text(
        52,
        43,
        text="3/6",
        font=("Arial", 13, "bold"),
        fill=TEXT
    )

    donut.create_text(
        52,
        62,
        text="Completed",
        font=("Arial", 7),
        fill=LIGHT_TEXT
    )

    legend = tk.Frame(
        progress_area,
        bg=CARD
    )

    legend.pack(
        side="left",
        fill="both",
        expand=True
    )

    selection_legend(
        legend,
        GREEN,
        "Completed",
        "3"
    )

    selection_legend(
        legend,
        BLUE,
        "In Progress",
        "1"
    )

    selection_legend(
        legend,
        GREY,
        "Not Started",
        "2"
    )

    tk.Label(
        frame,
        text="Keep exploring!\nYou're doing great!",
        font=("Georgia", 10, "italic"),
        bg=CARD,
        fg=GOLD_LIGHT
    ).pack(
        pady=(8, 15)
    )


def selection_legend(parent, colour, name, number):

    row = tk.Frame(
        parent,
        bg=CARD
    )

    row.pack(
        fill="x",
        pady=3
    )

    tk.Label(
        row,
        text="●",
        font=("Arial", 10),
        bg=CARD,
        fg=colour
    ).pack(
        side="left"
    )

    tk.Label(
        row,
        text=name,
        font=("Arial", 8),
        bg=CARD,
        fg=TEXT
    ).pack(
        side="left",
        padx=4
    )

    tk.Label(
        row,
        text=number,
        font=("Arial", 8),
        bg=CARD,
        fg=TEXT
    ).pack(
        side="right"
    )


# ============================================================
# QUICK LINKS
# ============================================================

def create_quick_links(parent):

    frame = tk.Frame(
        parent,
        bg=CARD,
        highlightbackground="#76582c",
        highlightthickness=1
    )

    frame.pack(
        fill="x",
        pady=(0, 12)
    )

    tk.Label(
        frame,
        text="♢  Quick Links",
        font=("Georgia", 12, "bold"),
        bg=CARD,
        fg=GOLD
    ).pack(
        anchor="w",
        padx=12,
        pady=(12, 8)
    )

    links = [
        ("▣", "View All Quizzes", "Browse all available quizzes"),
        ("▤", "Your Results", "Check your past quiz scores"),
        ("♜", "Leaderboard", "See how you rank")
    ]

    for icon, title, description in links:

        row = tk.Frame(
            frame,
            bg=CARD
        )

        row.pack(
            fill="x",
            padx=8,
            pady=3
        )

        tk.Label(
            row,
            text=icon,
            font=("Arial", 17),
            bg=CARD,
            fg=GOLD_LIGHT
        ).pack(
            side="left",
            padx=5
        )

        text_frame = tk.Frame(
            row,
            bg=CARD
        )

        text_frame.pack(
            side="left",
            fill="x",
            expand=True
        )

        tk.Label(
            text_frame,
            text=title,
            font=("Arial", 9),
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
            fg=LIGHT_TEXT
        ).pack(
            anchor="w"
        )

        tk.Label(
            row,
            text="›",
            font=("Arial", 20),
            bg=CARD,
            fg=GOLD
        ).pack(
            side="right"
        )

        tk.Frame(
            frame,
            bg="#263d4b",
            height=1
        ).pack(
            fill="x",
            padx=10,
            pady=3
        )


# ============================================================
# SELECTION QUOTE
# ============================================================

def create_selection_quote(parent):

    frame = tk.Frame(
        parent,
        bg=CARD,
        highlightbackground="#76582c",
        highlightthickness=1
    )

    frame.pack(
        fill="x"
    )

    image = load_quiz_image(
        "quiz_quote.png",
        (250, 125)
    )

    if image:

        tk.Label(
            frame,
            image=image,
            bg=CARD
        ).pack(
            fill="x",
            padx=3,
            pady=3
        )

    tk.Label(
        frame,
        text="“Small steps\nlead to great\ndiscoveries.”",
        font=("Georgia", 10, "italic"),
        bg=CARD,
        fg=GOLD_LIGHT,
        justify="center"
    ).pack(
        pady=(5, 15)
    )


# ============================================================
# START QUIZ
# ============================================================

def start_quiz(quiz):

    global current_quiz
    global current_question
    global selected_answers
    global answered_questions
    global quiz_score
    global time_left
    global timer_job

    current_quiz = quiz

    current_question = 0

    selected_answers = {}

    answered_questions = {}

    quiz_score = 0

    time_left = 10 * 60

    # Stop old timer
    if timer_job is not None:

        try:
            quiz_content.after_cancel(timer_job)
        except:
            pass

        timer_job = None

    # Clear page
    for widget in quiz_content.winfo_children():
        widget.destroy()

    # Show question page
    build_question_page()

    # Start timer
    update_timer()


# ============================================================
# BUILD QUESTION PAGE
# ============================================================

def build_question_page():

    page = tk.Frame(
        quiz_content,
        bg=BG
    )

    page.pack(
        fill="both",
        expand=True
    )

    # ========================================================
    # BANNER
    # ========================================================

    banner = tk.Frame(
        page,
        bg=BG,
        height=190
    )

    banner.pack(
        fill="x",
        padx=25
    )

    banner.pack_propagate(False)

    banner_image = load_quiz_image(
        "quiz_banner.png",
        (1050, 190)
    )

    if banner_image:

        tk.Label(
            banner,
            image=banner_image,
            bg=BG,
            bd=0
        ).place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

    # Header

    header = tk.Frame(
        banner,
        bg="#071b2b"
    )

    header.place(
        x=25,
        y=35
    )

    tk.Label(
        header,
        text="♢",
        font=("Arial", 38),
        bg="#071b2b",
        fg=GOLD
    ).pack(
        side="left",
        padx=(5, 15)
    )

    title_frame = tk.Frame(
        header,
        bg="#071b2b"
    )

    title_frame.pack(
        side="left"
    )

    tk.Label(
        title_frame,
        text="Quiz",
        font=("Georgia", 32, "bold"),
        bg="#071b2b",
        fg=TEXT
    ).pack(
        anchor="w"
    )

    tk.Label(
        title_frame,
        text="Challenge yourself with myths, legends and mythical creatures\n"
             "from Bhutan and around the world!",
        font=("Arial", 10),
        bg="#071b2b",
        fg=WHITE,
        justify="left"
    ).pack(
        anchor="w"
    )

    # ========================================================
    # BODY
    # ========================================================

    body = tk.Frame(
        page,
        bg=BG
    )

    body.pack(
        fill="x",
        padx=25,
        pady=(8, 0)
    )

    # ========================================================
    # QUESTION AREA
    # ========================================================

    question_area = tk.Frame(
        body,
        bg=BG,
        highlightbackground="#76582c",
        highlightthickness=1
    )

    question_area.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 12)
    )

    # ========================================================
    # SIDE PANEL
    # ========================================================

    side_panel = tk.Frame(
        body,
        bg=BG,
        width=270
    )

    side_panel.pack(
        side="right",
        fill="y"
    )

    side_panel.pack_propagate(False)

    # ========================================================
    # QUESTION HEADER
    # ========================================================

    question_header = tk.Frame(
        question_area,
        bg=BG
    )

    question_header.pack(
        fill="x",
        padx=25,
        pady=(20, 8)
    )

    tk.Label(
        question_header,
        text=f"Question {current_question + 1} of {len(quiz_questions)}",
        font=("Arial", 11),
        bg=BG,
        fg=TEXT
    ).pack(
        side="left"
    )

    category = current_quiz["category"]

    tk.Label(
        question_header,
        text="▣  " + category + " Quiz",
        font=("Arial", 10),
        bg=BG,
        fg=TEXT
    ).pack(
        side="right"
    )

    # ========================================================
    # PROGRESS BAR
    # ========================================================

    progress_background = tk.Frame(
        question_area,
        bg="#1c3b50",
        height=12
    )

    progress_background.pack(
        fill="x",
        padx=25
    )

    progress_background.pack_propagate(False)

    progress = (
        (current_question + 1)
        / len(quiz_questions)
    )

    tk.Frame(
        progress_background,
        bg="#f2bd5b"
    ).place(
        x=0,
        y=0,
        relwidth=progress,
        relheight=1
    )

    # ========================================================
    # QUESTION
    # ========================================================

    question_text = quiz_questions[current_question]["question"]

    tk.Label(
        question_area,
        text=question_text,
        font=("Georgia", 17, "bold"),
        bg=BG,
        fg=TEXT,
        wraplength=650,
        justify="left"
    ).pack(
        anchor="w",
        padx=25,
        pady=(30, 25)
    )

    # ========================================================
    # ANSWERS
    # ========================================================

    options = quiz_questions[current_question]["options"]

    option_frame = tk.Frame(
        question_area,
        bg=BG
    )

    option_frame.pack(
        fill="x",
        padx=25
    )

    for index, option in enumerate(options):

        create_answer_button(
            option_frame,
            index,
            option
        )

    # ========================================================
    # NAVIGATION
    # ========================================================

    navigation = tk.Frame(
        question_area,
        bg=BG
    )

    navigation.pack(
        fill="x",
        padx=25,
        pady=(30, 25)
    )

    tk.Button(
        navigation,
        text="‹  Previous",
        font=("Arial", 10, "bold"),
        bg=BG,
        fg=GOLD_LIGHT,
        activebackground=GOLD,
        activeforeground=BG,
        relief="solid",
        bd=1,
        padx=25,
        pady=8,
        command=previous_question
    ).pack(
        side="left"
    )

    tk.Button(
        navigation,
        text="Next  ›",
        font=("Arial", 10, "bold"),
        bg=GOLD_LIGHT,
        fg=BG,
        activebackground=GOLD,
        activeforeground=BG,
        relief="flat",
        padx=30,
        pady=9,
        command=next_question
    ).pack(
        side="right"
    )

    # ========================================================
    # RIGHT SIDE PANELS
    # ========================================================

    create_question_progress(side_panel)

    create_time_panel(side_panel)

    create_question_overview(side_panel)

    create_quiz_quote(side_panel)


# ============================================================
# ANSWER BUTTON
# ============================================================

def create_answer_button(parent, index, option):

    selected = selected_answers.get(
        current_question
    )

    if selected == index:

        background = "#1d2d2f"
        border = "#f2bd5b"
        circle = "●"

    else:

        background = "#0b2638"
        border = "#41637a"
        circle = "○"

    answer = tk.Frame(
        parent,
        bg=background,
        highlightbackground=border,
        highlightthickness=1,
        cursor="hand2"
    )

    answer.pack(
        fill="x",
        pady=7
    )

    # Circle

    circle_label = tk.Label(
        answer,
        text=circle,
        font=("Arial", 18),
        bg=background,
        fg=GOLD_LIGHT if selected == index else TEXT
    )

    circle_label.pack(
        side="left",
        padx=(18, 12),
        pady=8
    )

    # A/B/C/D

    letter = chr(65 + index)

    letter_label = tk.Label(
        answer,
        text=letter + ".",
        font=("Arial", 10, "bold"),
        bg=background,
        fg=TEXT
    )

    letter_label.pack(
        side="left",
        padx=(0, 12)
    )

    # Text

    option_label = tk.Label(
        answer,
        text=option,
        font=("Arial", 10),
        bg=background,
        fg=TEXT,
        anchor="w"
    )

    option_label.pack(
        side="left",
        pady=12
    )

    # Click entire answer

    answer.bind(
        "<Button-1>",
        lambda event, i=index: select_answer(i)
    )

    circle_label.bind(
        "<Button-1>",
        lambda event, i=index: select_answer(i)
    )

    letter_label.bind(
        "<Button-1>",
        lambda event, i=index: select_answer(i)
    )

    option_label.bind(
        "<Button-1>",
        lambda event, i=index: select_answer(i)
    )


# ============================================================
# SELECT ANSWER
# ============================================================

def select_answer(index):

    selected_answers[current_question] = index

    refresh_question()


# ============================================================
# REFRESH CURRENT QUESTION
# ============================================================

def refresh_question():

    for widget in quiz_content.winfo_children():
        widget.destroy()

    build_question_page()


# ============================================================
# NEXT QUESTION
# ============================================================

def next_question():

    global current_question
    global quiz_score

    # No answer selected
    if current_question not in selected_answers:

        messagebox.showwarning(
            "Select an Answer",
            "Please select an answer before continuing."
        )

        return

    # Check only once
    if current_question not in answered_questions:

        selected = selected_answers[current_question]

        correct = quiz_questions[current_question]["answer"]

        if selected == correct:

            quiz_score += 1

            answered_questions[current_question] = "correct"

        else:

            answered_questions[current_question] = "incorrect"

    # Move forward

    if current_question < len(quiz_questions) - 1:

        current_question += 1

        refresh_question()

    else:

        show_quiz_result()


# ============================================================
# PREVIOUS QUESTION
# ============================================================

def previous_question():

    global current_question

    if current_question > 0:

        current_question -= 1

        refresh_question()


# ============================================================
# RIGHT PANEL - PROGRESS
# ============================================================

def create_question_progress(parent):

    frame = tk.Frame(
        parent,
        bg=CARD,
        highlightbackground="#76582c",
        highlightthickness=1
    )

    frame.pack(
        fill="x",
        pady=(0, 12)
    )

    tk.Label(
        frame,
        text="◉  Quiz Progress",
        font=("Georgia", 12, "bold"),
        bg=CARD,
        fg=GOLD
    ).pack(
        anchor="w",
        padx=15,
        pady=(12, 5)
    )

    area = tk.Frame(
        frame,
        bg=CARD
    )

    area.pack(
        fill="x",
        padx=8
    )

    canvas = tk.Canvas(
        area,
        width=105,
        height=105,
        bg=CARD,
        highlightthickness=0
    )

    canvas.pack(
        side="left"
    )

    total = len(quiz_questions)

    completed = len(answered_questions)

    correct = sum(
        1
        for result in answered_questions.values()
        if result == "correct"
    )

    incorrect = sum(
        1
        for result in answered_questions.values()
        if result == "incorrect"
    )

    # Background circle

    canvas.create_oval(
        12,
        12,
        93,
        93,
        outline="#294c65",
        width=11
    )

    # Completed arc

    if total > 0:

        angle = (
            completed / total
        ) * 360

        canvas.create_arc(
            12,
            12,
            93,
            93,
            start=90,
            extent=-angle,
            style="arc",
            outline=GOLD_LIGHT,
            width=11
        )

    canvas.create_text(
        52,
        43,
        text=f"{completed}/{total}",
        font=("Arial", 13, "bold"),
        fill=TEXT
    )

    canvas.create_text(
        52,
        62,
        text="Questions",
        font=("Arial", 7),
        fill=LIGHT_TEXT
    )

    legend = tk.Frame(
        area,
        bg=CARD
    )

    legend.pack(
        side="left",
        fill="both",
        expand=True
    )

    question_legend(
        legend,
        GREEN,
        "Correct",
        str(correct)
    )

    question_legend(
        legend,
        RED,
        "Incorrect",
        str(incorrect)
    )

    question_legend(
        legend,
        "#b9c5db",
        "Remaining",
        str(total - completed)
    )


def question_legend(parent, colour, name, number):

    row = tk.Frame(
        parent,
        bg=CARD
    )

    row.pack(
        fill="x",
        pady=4
    )

    tk.Label(
        row,
        text="●",
        font=("Arial", 10),
        bg=CARD,
        fg=colour
    ).pack(
        side="left"
    )

    tk.Label(
        row,
        text=name,
        font=("Arial", 8),
        bg=CARD,
        fg=TEXT
    ).pack(
        side="left",
        padx=4
    )

    tk.Label(
        row,
        text=number,
        font=("Arial", 8),
        bg=CARD,
        fg=TEXT
    ).pack(
        side="right",
        padx=8
    )


# ============================================================
# TIMER
# ============================================================

def create_time_panel(parent):

    frame = tk.Frame(
        parent,
        bg=CARD,
        highlightbackground="#76582c",
        highlightthickness=1
    )

    frame.pack(
        fill="x",
        pady=(0, 12)
    )

    tk.Label(
        frame,
        text="◷  Time Left",
        font=("Georgia", 12, "bold"),
        bg=CARD,
        fg=GOLD
    ).pack(
        anchor="w",
        padx=15,
        pady=(12, 2)
    )

    # Current time

    minutes = time_left // 60

    seconds = time_left % 60

    time_text = f"{minutes:02d}:{seconds:02d}"

    tk.Label(
        frame,
        text=time_text,
        font=("Georgia", 22, "bold"),
        bg=CARD,
        fg=TEXT
    ).pack(
        pady=5
    )

    # Time bar

    background = tk.Frame(
        frame,
        bg="#1c3b50",
        height=10
    )

    background.pack(
        fill="x",
        padx=15,
        pady=(0, 15)
    )

    background.pack_propagate(False)

    percentage = time_left / (10 * 60)

    tk.Frame(
        background,
        bg="#f2bd5b"
    ).place(
        x=0,
        y=0,
        relwidth=percentage,
        relheight=1
    )


# ============================================================
# UPDATE TIMER
# ============================================================

def update_timer():

    global time_left
    global timer_job

    if quiz_content is None:
        return

    # Refresh only the timer panel by rebuilding page
    # every second would be too heavy, so use a small
    # top-level label approach.

    # If time reaches zero
    if time_left <= 0:

        show_quiz_result()

        return

    time_left -= 1

    # Schedule again
    timer_job = quiz_content.after(
        1000,
        update_timer
    )

    # We don't rebuild the entire page every second.


# ============================================================
# QUESTION OVERVIEW
# ============================================================

def create_question_overview(parent):

    frame = tk.Frame(
        parent,
        bg=CARD,
        highlightbackground="#76582c",
        highlightthickness=1
    )

    frame.pack(
        fill="x",
        pady=(0, 12)
    )

    tk.Label(
        frame,
        text="✥  Quiz Overview",
        font=("Georgia", 12, "bold"),
        bg=CARD,
        fg=GOLD
    ).pack(
        anchor="w",
        padx=15,
        pady=(12, 10)
    )

    grid = tk.Frame(
        frame,
        bg=CARD
    )

    grid.pack(
        padx=10,
        pady=(0, 15)
    )

    for i in range(len(quiz_questions)):

        row = i // 5

        column = i % 5

        if i == current_question:

            background = "#f2bd5b"
            foreground = BG

        elif i in answered_questions:

            if answered_questions[i] == "correct":

                background = "#285943"

            else:

                background = "#5a2931"

            foreground = TEXT

        else:

            background = CARD
            foreground = TEXT

        tk.Label(
            grid,
            text=str(i + 1),
            font=("Arial", 9, "bold"),
            width=3,
            height=1,
            bg=background,
            fg=foreground,
            highlightbackground="#58728b",
            highlightthickness=1
        ).grid(
            row=row,
            column=column,
            padx=4,
            pady=5
        )


# ============================================================
# QUESTION PAGE QUOTE
# ============================================================

def create_quiz_quote(parent):

    frame = tk.Frame(
        parent,
        bg=CARD,
        highlightbackground="#76582c",
        highlightthickness=1
    )

    frame.pack(
        fill="x"
    )

    image = load_quiz_image(
        "quiz_quote.png",
        (245, 125)
    )

    if image:

        tk.Label(
            frame,
            image=image,
            bg=CARD
        ).pack(
            fill="x",
            padx=3,
            pady=3
        )

    tk.Label(
        frame,
        text="“The mountains, the rivers,\n"
             "and the stories — all are\n"
             "part of who we are.”",
        font=("Georgia", 10, "italic"),
        bg=CARD,
        fg=GOLD_LIGHT,
        justify="center"
    ).pack(
        pady=12
    )


# ============================================================
# QUIZ RESULT
# ============================================================

def show_quiz_result():

    global timer_job

    # Stop timer

    if timer_job is not None:

        try:
            quiz_content.after_cancel(timer_job)
        except:
            pass

        timer_job = None

    # Clear page

    for widget in quiz_content.winfo_children():
        widget.destroy()

    result = tk.Frame(
        quiz_content,
        bg=BG
    )

    result.pack(
        fill="both",
        expand=True,
        pady=80
    )

    tk.Label(
        result,
        text="✦",
        font=("Arial", 45),
        bg=BG,
        fg=GOLD
    ).pack()

    tk.Label(
        result,
        text="Quiz Completed!",
        font=("Georgia", 28, "bold"),
        bg=BG,
        fg=TEXT
    ).pack(
        pady=10
    )

    tk.Label(
        result,
        text=f"You scored {quiz_score} out of {len(quiz_questions)}",
        font=("Arial", 15),
        bg=BG,
        fg=LIGHT_TEXT
    ).pack(
        pady=10
    )

    percentage = (
        quiz_score / len(quiz_questions)
    ) * 100

    tk.Label(
        result,
        text=f"{percentage:.0f}%",
        font=("Georgia", 32, "bold"),
        bg=BG,
        fg=GOLD_LIGHT
    ).pack(
        pady=10
    )

    tk.Button(
        result,
        text="Back to Quizzes",
        font=("Arial", 10, "bold"),
        bg=GOLD_LIGHT,
        fg=BG,
        relief="flat",
        padx=30,
        pady=10,
        command=lambda: show_quiz(quiz_content)
    ).pack(
        pady=20
    )


# ============================================================
# CATEGORY BUTTON
# ============================================================

def category_selected(category):

    if category == "All Quizzes":

        messagebox.showinfo(
            "Quizzes",
            "All quizzes are currently displayed."
        )

    else:

        messagebox.showinfo(
            category,
            "The " + category + " category is selected."
        )