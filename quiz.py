
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from datetime import datetime
import sqlite3

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
IMAGE_DIR = PROJECT_DIR / "assets"
LEGACY_IMAGE_DIR = PROJECT_DIR / "images"

DB_FILE = PROJECT_DIR / "mythlab.db"

quiz_image_refs = []

selected_category = "All Quizzes"
quiz_username = None
quiz_grid_widget = None


# ============================================================
# QUIZ VARIABLES
# ============================================================

quiz_content = None
current_quiz = None
current_question = 0

selected_answers = {}
answered_questions = {}

quiz_score = 0

time_left = 10 * 60
timer_job = None


# ============================================================
# FIND IMAGE
# ============================================================

def find_image(filename):

    path = IMAGE_DIR / filename

    if path.exists():
        return path

    path = PROJECT_DIR / filename

    if path.exists():
        return path

    stem = Path(filename).stem.lower()
    extension = Path(filename).suffix.lower()

    for folder in [IMAGE_DIR, LEGACY_IMAGE_DIR, PROJECT_DIR]:

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
# QUESTION SETS
# ============================================================

# The original Bhutanese questions are preserved.

bhutanese_questions = [

    {
        "question": "Which of the following is a famous sacred site in Bhutan known for its tiger's nest monastery?",
        "options": [
            "Tiger's Nest (Paro Taktsang)",
            "Boudhanath Stupa",
            "Angkor Wat",
            "Mount Fuji"
        ],
        "answer": 0
    },

    {
        "question": "What is the national animal of Bhutan?",
        "options": [
            "Takin",
            "Yak",
            "Snow Leopard",
            "Red Panda"
        ],
        "answer": 0
    },

    {
        "question": "What does the Bhutanese word 'Druk' commonly mean?",
        "options": [
            "Thunder Dragon",
            "Mountain Spirit",
            "Snow Lion",
            "Fire Bird"
        ],
        "answer": 0
    },

    {
        "question": "What is the capital city of Bhutan?",
        "options": [
            "Paro",
            "Punakha",
            "Thimphu",
            "Bumthang"
        ],
        "answer": 2
    },

    {
        "question": "How many Dzongkhags are there in Bhutan?",
        "options": [
            "15",
            "20",
            "25",
            "30"
        ],
        "answer": 1
    },

    {
        "question": "Which mythical creature is strongly associated with Bhutanese mythology?",
        "options": [
            "Druk",
            "Phoenix",
            "Minotaur",
            "Kraken"
        ],
        "answer": 0
    },

    {
        "question": "Which mountain is considered sacred in Bhutan?",
        "options": [
            "Mount Everest",
            "Mount Fuji",
            "Mount Jomolhari",
            "K2"
        ],
        "answer": 2
    },

    {
        "question": "What is Paro Taktsang also known as?",
        "options": [
            "Tiger's Nest",
            "Dragon's Palace",
            "Golden Temple",
            "Mountain Monastery"
        ],
        "answer": 0
    },

    {
        "question": "The Takin is best described as what?",
        "options": [
            "A mythical dragon",
            "A large mountain animal",
            "A bird",
            "A river spirit"
        ],
        "answer": 1
    },

    {
        "question": "Which two countries border Bhutan?",
        "options": [
            "India and China",
            "India and Nepal",
            "China and Nepal",
            "India and Tibet"
        ],
        "answer": 0
    }

]


# ------------------------------------------------------------
# MYTHICAL CREATURES QUIZ
# ------------------------------------------------------------

creature_questions = [

    {
        "question": "Which legendary creature appears on the national flag of Bhutan?",
        "options": [
            "Thunder Dragon (Druk)",
            "Phoenix",
            "Unicorn",
            "Griffin"
        ],
        "answer": 0
    },

    {
        "question": "What is the Yeti commonly described as?",
        "options": [
            "A giant sea creature",
            "A mysterious snow-dwelling being",
            "A fire-breathing bird",
            "A forest fairy"
        ],
        "answer": 1
    },

    {
        "question": "Which mythical creature is often associated with wisdom and protection in Himalayan traditions?",
        "options": [
            "Dragon",
            "Minotaur",
            "Kraken",
            "Cyclops"
        ],
        "answer": 0
    },

    {
        "question": "What is a Naga commonly represented as in South Asian traditions?",
        "options": [
            "A serpent or serpent-like being",
            "A giant eagle",
            "A horse with wings",
            "A forest giant"
        ],
        "answer": 0
    },

    {
        "question": "Which creature is traditionally known as a symbol of purity and strength in Himalayan art?",
        "options": [
            "Snow Lion",
            "Werewolf",
            "Mermaid",
            "Goblin"
        ],
        "answer": 0
    },

    {
        "question": "The Phoenix is traditionally associated with which ability?",
        "options": [
            "Living underwater",
            "Rising again from its ashes",
            "Turning invisible",
            "Controlling earthquakes"
        ],
        "answer": 1
    },

    {
        "question": "The Firebird is a legendary creature most closely associated with which folklore tradition?",
        "options": [
            "Slavic folklore",
            "Bhutanese folklore",
            "Japanese folklore",
            "Greek folklore"
        ],
        "answer": 0
    },

    {
        "question": "Which of these is a real animal rather than a mythical creature?",
        "options": [
            "Dragon",
            "Phoenix",
            "Takin",
            "Griffin"
        ],
        "answer": 2
    },

    {
        "question": "Kurma, the giant tortoise, is associated with which mythology?",
        "options": [
            "Hindu mythology",
            "Norse mythology",
            "Greek mythology",
            "Egyptian mythology"
        ],
        "answer": 0
    },

    {
        "question": "Rangda is a supernatural figure from which cultural tradition?",
        "options": [
            "Balinese tradition",
            "Bhutanese tradition",
            "Norse tradition",
            "Egyptian tradition"
        ],
        "answer": 0
    }

]


# ------------------------------------------------------------
# BHUTAN DZONGKHAGS QUIZ
# ------------------------------------------------------------

region_questions = [

    {
        "question": "How many Dzongkhags (districts) are there in Bhutan?",
        "options": [
            "15",
            "18",
            "20",
            "25"
        ],
        "answer": 2
    },

    {
        "question": "Which Dzongkhag is the capital of Bhutan located in?",
        "options": [
            "Paro",
            "Thimphu",
            "Punakha",
            "Wangdue Phodrang"
        ],
        "answer": 1
    },

    {
        "question": "Paro Taktsang, also known as Tiger's Nest, is located in which Dzongkhag?",
        "options": [
            "Paro",
            "Haa",
            "Bumthang",
            "Trongsa"
        ],
        "answer": 0
    },

    {
        "question": "Punakha Dzong is located at the meeting point of which two rivers?",
        "options": [
            "Mo Chhu and Pho Chhu",
            "Wang Chhu and Paro Chhu",
            "Mangde Chhu and Chamkhar Chhu",
            "Kuri Chhu and Drangme Chhu"
        ],
        "answer": 0
    },

    {
        "question": "Which Dzongkhag is often called the spiritual heartland of Bhutan?",
        "options": [
            "Bumthang",
            "Samtse",
            "Chukha",
            "Sarpang"
        ],
        "answer": 0
    },

    {
        "question": "Trongsa Dzong is especially important because it historically controlled which route?",
        "options": [
            "A major east-west route through Bhutan",
            "A sea route to India",
            "A route to Tibet through Paro",
            "A route to Nepal"
        ],
        "answer": 0
    },

    {
        "question": "Which Dzongkhag is located in the northwestern part of Bhutan and is known for its beautiful valley?",
        "options": [
            "Haa",
            "Pemagatshel",
            "Zhemgang",
            "Samtse"
        ],
        "answer": 0
    },

    {
        "question": "Which Dzongkhag is known for its remote mountain communities and Gasa Dzong?",
        "options": [
            "Gasa",
            "Tsirang",
            "Dagana",
            "Sarpang"
        ],
        "answer": 0
    },

    {
        "question": "Which Dzongkhag is home to the famous Punakha Dzong?",
        "options": [
            "Punakha",
            "Thimphu",
            "Mongar",
            "Lhuentse"
        ],
        "answer": 0
    },

    {
        "question": "Which country lies to the south of Bhutan?",
        "options": [
            "India",
            "China",
            "Nepal",
            "Bangladesh"
        ],
        "answer": 0
    }

]


# ------------------------------------------------------------
# MYTHOLOGY BASICS
# ------------------------------------------------------------

basics_questions = [

    {
        "question": "What is mythology?",
        "options": [
            "A collection of traditional stories about gods, heroes and supernatural events",
            "A list of scientific experiments",
            "A modern news report",
            "A type of mathematics"
        ],
        "answer": 0
    },

    {
        "question": "What is a legend?",
        "options": [
            "A traditional story often connected with people or places",
            "A computer program",
            "A scientific formula",
            "A weather forecast"
        ],
        "answer": 0
    },

    {
        "question": "What is folklore?",
        "options": [
            "Traditional beliefs, stories and customs shared by a community",
            "A type of machine",
            "A modern business plan",
            "A mathematical theory"
        ],
        "answer": 0
    },

    {
        "question": "What is a creation myth usually about?",
        "options": [
            "How the world or universe began",
            "How computers are made",
            "How mountains are measured",
            "How people build houses"
        ],
        "answer": 0
    },

    {
        "question": "Which of these is commonly found in mythology?",
        "options": [
            "Gods and goddesses",
            "Only modern machines",
            "Only scientific tools",
            "Computer passwords"
        ],
        "answer": 0
    },

    {
        "question": "What is a hero usually known for in traditional stories?",
        "options": [
            "Courage and important deeds",
            "Avoiding every challenge",
            "Destroying every tradition",
            "Never helping others"
        ],
        "answer": 0
    },

    {
        "question": "Why are myths and legends passed from one generation to another?",
        "options": [
            "To preserve culture, beliefs and values",
            "To replace all history books",
            "To teach computer programming",
            "To explain modern technology"
        ],
        "answer": 0
    },

    {
        "question": "What is a symbol in mythology?",
        "options": [
            "An image or object that represents an idea",
            "A type of building material",
            "A modern vehicle",
            "A musical instrument only"
        ],
        "answer": 0
    },

    {
        "question": "Which of the following is an example of an oral tradition?",
        "options": [
            "Stories told by elders to younger generations",
            "A computer file saved on a hard drive",
            "A printed shopping receipt",
            "A television remote control"
        ],
        "answer": 0
    },

    {
        "question": "Why should we learn about mythology from different cultures?",
        "options": [
            "To understand different cultures and traditions",
            "To prove that all cultures are identical",
            "To forget local traditions",
            "To replace cultural history"
        ],
        "answer": 0
    }

]


# ------------------------------------------------------------
# LEGENDS & CREATURES QUIZ
# ------------------------------------------------------------

mixed_questions = [

    {
        "question": "Which legendary creature is strongly connected with Bhutan's national identity?",
        "options": [
            "Druk",
            "Minotaur",
            "Kraken",
            "Unicorn"
        ],
        "answer": 0
    },

    {
        "question": "The Yeti is traditionally associated with which environment?",
        "options": [
            "Himalayan mountains",
            "Desert dunes",
            "Tropical beaches",
            "Deep oceans"
        ],
        "answer": 0
    },

    {
        "question": "Which Greek mythological creature has the body of a lion and the head and wings of an eagle?",
        "options": [
            "Griffin",
            "Naga",
            "Phoenix",
            "Yeti"
        ],
        "answer": 0
    },

    {
        "question": "Which legendary bird is known for being reborn from its ashes?",
        "options": [
            "Phoenix",
            "Griffin",
            "Roc",
            "Garuda"
        ],
        "answer": 0
    },

    {
        "question": "Which Bhutanese site is associated with Guru Rinpoche's meditation?",
        "options": [
            "Paro Taktsang",
            "Punakha Dzong",
            "Trongsa Dzong",
            "Tashichho Dzong"
        ],
        "answer": 0
    },

    {
        "question": "In Greek mythology, who is the king of the gods?",
        "options": [
            "Zeus",
            "Apollo",
            "Hermes",
            "Ares"
        ],
        "answer": 0
    },

    {
        "question": "Which creature is commonly described as half-human and half-fish?",
        "options": [
            "Mermaid",
            "Griffin",
            "Centaur",
            "Minotaur"
        ],
        "answer": 0
    },

    {
        "question": "Which legendary creature is traditionally associated with the sea and enormous tentacles?",
        "options": [
            "Kraken",
            "Phoenix",
            "Snow Lion",
            "Unicorn"
        ],
        "answer": 0
    },

    {
        "question": "What is the Takin?",
        "options": [
            "Bhutan's national animal",
            "A mythical sea monster",
            "A legendary bird",
            "A Greek god"
        ],
        "answer": 0
    },

    {
        "question": "What is one important purpose of traditional legends?",
        "options": [
            "To share cultural beliefs and lessons",
            "To provide exact scientific measurements",
            "To replace every form of education",
            "To describe only modern inventions"
        ],
        "answer": 0
    }

]


# ------------------------------------------------------------
# ULTIMATE MYTHOLOGY CHALLENGE
# ------------------------------------------------------------

challenge_questions = [

    {
        "question": "What is the name commonly used for Bhutan's Thunder Dragon?",
        "options": [
            "Druk",
            "Garuda",
            "Naga",
            "Roc"
        ],
        "answer": 0
    },

    {
        "question": "In Hindu mythology, which deity is associated with the preservation of the universe?",
        "options": [
            "Vishnu",
            "Agni",
            "Indra",
            "Yama"
        ],
        "answer": 0
    },

    {
        "question": "Which Greek hero is famous for completing twelve labours?",
        "options": [
            "Heracles",
            "Achilles",
            "Odysseus",
            "Perseus"
        ],
        "answer": 0
    },

    {
        "question": "In Norse mythology, what is the name of the world tree connecting the nine worlds?",
        "options": [
            "Yggdrasil",
            "Asgard",
            "Midgard",
            "Valhalla"
        ],
        "answer": 0
    },

    {
        "question": "Which Hindu mythological figure is known as the half-man, half-lion avatar of Vishnu?",
        "options": [
            "Narasimha",
            "Hanuman",
            "Garuda",
            "Ganesha"
        ],
        "answer": 0
    },

    {
        "question": "Which creature in Greek mythology guarded the entrance to the Underworld?",
        "options": [
            "Cerberus",
            "Pegasus",
            "Chimera",
            "Hydra"
        ],
        "answer": 0
    },

    {
        "question": "In Egyptian mythology, which god is commonly associated with the afterlife and mummification?",
        "options": [
            "Anubis",
            "Ra",
            "Horus",
            "Thoth"
        ],
        "answer": 0
    },

    {
        "question": "Which legendary bird is associated with the Hindu deity Vishnu as his mount?",
        "options": [
            "Garuda",
            "Phoenix",
            "Roc",
            "Griffin"
        ],
        "answer": 0
    },

    {
        "question": "What is the main purpose of comparing myths from different cultures?",
        "options": [
            "To understand similarities and differences between traditions",
            "To prove that one culture is superior",
            "To remove local cultural beliefs",
            "To show that all stories are historically identical"
        ],
        "answer": 0
    },

    {
        "question": "Which term describes a traditional story that explains a natural event or cultural belief?",
        "options": [
            "Myth",
            "Invoice",
            "Algorithm",
            "Biography"
        ],
        "answer": 0
    }

]


# Connect each quiz title to its own question list.

QUIZ_QUESTION_SETS = {

    "Bhutanese Mythology Quiz": bhutanese_questions,

    "Mythical Creatures Quiz": creature_questions,

    "Bhutan Dzongkhags Quiz": region_questions,

    "Mythology Basics": basics_questions,

    "Legends & Creatures": mixed_questions,

    "The Ultimate Mythology Challenge": challenge_questions

}


# Keep the original variable name for the rest of the quiz functions.
quiz_questions = bhutanese_questions


# ============================================================
# SHOW QUIZ SELECTION PAGE
# ============================================================

def show_quiz(content, category_filter="All Quizzes"):

    global quiz_content
    global timer_job
    global quiz_grid_widget
    global selected_category

    quiz_content = content
    selected_category = category_filter

    if timer_job is not None:

        try:
            content.after_cancel(timer_job)
        except:
            pass

        timer_job = None

    for widget in content.winfo_children():
        widget.destroy()

    quiz_image_refs.clear()

    # BANNER

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
        "banner.jpg",
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

        banner_canvas = tk.Canvas(
            banner,
            bg=BG,
            highlightthickness=0,
            bd=0
        )

        banner_canvas.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        banner_canvas.create_image(
            0, 0,
            image=banner_image,
            anchor="nw"
        )

        banner_canvas.create_text(
            35, 58,
            text="?",
            anchor="w",
            font=("Georgia", 30, "bold"),
            fill=GOLD_LIGHT
        )

        banner_canvas.create_text(
            85, 50,
            text="Quiz",
            anchor="w",
            font=("Georgia", 31, "bold"),
            fill=TEXT
        )

        banner_canvas.create_text(
            85, 95,
            text="Test your knowledge of myths, legends and mythical creatures\nfrom Bhutan and beyond!",
            anchor="w",
            font=("Arial", 10),
            fill=WHITE
        )

    # CATEGORY BUTTONS

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
        "General Knowledge",
        "Mixed",
        "Challenge"
    ]

    for category in categories:

        if category == selected_category:
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
            cursor="hand2",
            command=lambda c=category: category_selected(c)
        ).pack(
            side="left",
            padx=(0, 8)
        )

    # BODY

    body = tk.Frame(
        content,
        bg=BG
    )

    body.pack(
        fill="x",
        padx=25
    )

    left = tk.Frame(
        body,
        bg=BG
    )

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

    left.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(0, 12)
    )

    # AVAILABLE QUIZZES TITLE

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

    # QUIZ GRID

    quiz_grid = tk.Frame(
        left,
        bg=BG
    )

    quiz_grid.pack(
        fill="x"
    )

    quiz_grid_widget = quiz_grid

    quizzes = [

        {
            "category": "Myths",
            "title": "Bhutanese Mythology Quiz",
            "description": "Test your knowledge about famous\nmyths and legends from Bhutan.",
            "questions": "10 Questions",
            "difficulty": "Medium",
            "image": "thunder_dragon.png"
        },

        {
            "category": "Creatures",
            "title": "Mythical Creatures Quiz",
            "description": "How well do you know Bhutan's\nmythical creatures and their powers?",
            "questions": "10 Questions",
            "difficulty": "Medium",
            "image": "druk (3).png"
        },

        {
            "category": "Regions",
            "title": "Bhutan Dzongkhags Quiz",
            "description": "Explore and test your knowledge\nof Bhutan's 20 Dzongkhags and legends.",
            "questions": "10 Questions",
            "difficulty": "Easy",
            "image": "paro_taktsang.png"
        },

        {
            "category": "General Knowledge",
            "title": "Mythology Basics",
            "description": "A quick quiz to check your general\nknowledge about myths and folklore.",
            "questions": "10 Questions",
            "difficulty": "Easy",
            "image": "recent_firebird.png"
        },

        {
            "category": "Mixed",
            "title": "Legends & Creatures",
            "description": "A mix of myths, creatures and\ninteresting facts from across regions.",
            "questions": "10 Questions",
            "difficulty": "Medium",
            "image": "yeti.png"
        },

        {
            "category": "Challenge",
            "title": "The Ultimate Mythology Challenge",
            "description": "Are you a true MythLab explorer?\nTake this advanced quiz!",
            "questions": "10 Questions",
            "difficulty": "Hard",
            "image": "firebird (1).png"
        }

    ]

    visible_quizzes = [
        q for q in quizzes
        if selected_category == "All Quizzes"
        or q["category"] == selected_category
    ]

    if not visible_quizzes:

        tk.Label(
            quiz_grid,
            text="No quizzes in this category yet.",
            font=("Georgia", 12, "italic"),
            bg=BG,
            fg=LIGHT_TEXT
        ).pack(
            pady=30
        )

    for index, quiz in enumerate(visible_quizzes):

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

    create_selection_progress(right)
    create_quick_links(right)
    create_selection_quote(right)

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

    image = load_quiz_image(
        quiz["image"],
        (190, 95)
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

    title_label = tk.Label(
        card,
        text=quiz["title"],
        font=("Georgia", 11, "bold"),
        bg=CARD,
        fg=TEXT,
        wraplength=170,
        justify="left"
    )

    title_label.pack(
        anchor="w",
        padx=10,
        pady=(7, 2)
    )

    description_label = tk.Label(
        card,
        text=quiz["description"],
        font=("Arial", 8),
        bg=CARD,
        fg=LIGHT_TEXT,
        wraplength=170,
        justify="left"
    )

    description_label.pack(
        anchor="w",
        padx=10
    )

    def fit_text(event):

        width = max(event.width - 30, 100)

        title_label.configure(wraplength=width)
        description_label.configure(wraplength=width)

    card.bind("<Configure>", fit_text)

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

    donut.create_oval(
        12, 12, 93, 93,
        outline="#284b63",
        width=11
    )

    donut.create_arc(
        12, 12, 93, 93,
        start=90,
        extent=-180,
        style="arc",
        outline=GOLD_LIGHT,
        width=11
    )

    donut.create_text(
        52, 43,
        text="3/6",
        font=("Arial", 13, "bold"),
        fill=TEXT
    )

    donut.create_text(
        52, 62,
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

    selection_legend(legend, GREEN, "Completed", "3")
    selection_legend(legend, BLUE, "In Progress", "1")
    selection_legend(legend, GREY, "Not Started", "2")

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
    ).pack(side="left")

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
    ).pack(side="right")


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
        ("▣", "View All Quizzes", "Browse all available quizzes", view_all_quizzes),
        ("▤", "Your Results", "Check your past quiz scores", show_results_page),
        ("♜", "Leaderboard", "See how you rank", show_leaderboard_page)
    ]

    for icon, title, description, link_command in links:

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
        ).pack(anchor="w")

        tk.Label(
            text_frame,
            text=description,
            font=("Arial", 7),
            bg=CARD,
            fg=LIGHT_TEXT
        ).pack(anchor="w")

        tk.Label(
            row,
            text="›",
            font=("Arial", 20),
            bg=CARD,
            fg=GOLD
        ).pack(side="right")

        make_clickable(row, link_command)

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
# QUICK LINK HELPERS
# ============================================================

def make_clickable(row, command):

    def set_background(widget, colour):

        try:
            widget.configure(bg=colour)
        except tk.TclError:
            pass

        for child in widget.winfo_children():
            set_background(child, colour)

    def bind_all_children(widget):

        widget.bind(
            "<Button-1>",
            lambda event: command()
        )

        widget.configure(cursor="hand2")

        for child in widget.winfo_children():
            bind_all_children(child)

    row.bind(
        "<Enter>",
        lambda event: set_background(row, CARD_DARK)
    )

    row.bind(
        "<Leave>",
        lambda event: set_background(row, CARD)
    )

    bind_all_children(row)


def scroll_quiz_page(fraction=0.0):

    try:

        quiz_content.update_idletasks()

        canvas = quiz_content.master

        if hasattr(canvas, "yview_moveto"):
            canvas.yview_moveto(fraction)

    except tk.TclError:
        pass


def view_all_quizzes():

    show_quiz(quiz_content)

    try:

        quiz_content.update_idletasks()

        total = max(quiz_content.winfo_height(), 1)

        top = (
            quiz_grid_widget.winfo_rooty()
            - quiz_content.winfo_rooty()
            - 20
        )

        scroll_quiz_page(max(top, 0) / total)

    except (tk.TclError, AttributeError):
        pass


# ============================================================
# SAVED RESULTS (SQLite)
# ============================================================

def get_db():

    conn = sqlite3.connect(DB_FILE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            quiz_title TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            taken_at TEXT NOT NULL
        )
    """)

    return conn


def set_quiz_user(username):

    global quiz_username

    quiz_username = username.strip() if username else None


def player_name():

    return quiz_username or "Guest"


def save_quiz_result():

    title = (
        current_quiz["title"]
        if isinstance(current_quiz, dict)
        else "Quiz"
    )

    try:

        conn = get_db()

        conn.execute(
            """
            INSERT INTO quiz_results
                (username, quiz_title, score, total, taken_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                player_name(),
                title,
                quiz_score,
                len(quiz_questions),
                datetime.now().strftime("%d %b %Y, %H:%M")
            )
        )

        conn.commit()
        conn.close()

    except Exception as error:

        print("Could not save quiz result:", error)


# ============================================================
# RESULTS + LEADERBOARD PAGES
# ============================================================

def show_table_page(title, subtitle, headers, rows, empty_text,
                    widths, highlight_row=None):

    for widget in quiz_content.winfo_children():
        widget.destroy()

    page = tk.Frame(
        quiz_content,
        bg=BG
    )

    page.pack(
        fill="both",
        expand=True,
        padx=40,
        pady=25
    )

    tk.Button(
        page,
        text="←  Back to Quizzes",
        font=("Arial", 10, "bold"),
        bg=GOLD_LIGHT,
        fg=BG,
        relief="flat",
        padx=18,
        pady=8,
        cursor="hand2",
        command=lambda: show_quiz(quiz_content)
    ).pack(anchor="w")

    tk.Label(
        page,
        text=title,
        font=("Georgia", 26, "bold"),
        bg=BG,
        fg=GOLD
    ).pack(
        anchor="w",
        pady=(18, 2)
    )

    tk.Label(
        page,
        text=subtitle,
        font=("Arial", 10),
        bg=BG,
        fg=LIGHT_TEXT
    ).pack(
        anchor="w",
        pady=(0, 15)
    )

    table = tk.Frame(
        page,
        bg=CARD,
        highlightbackground="#76582c",
        highlightthickness=1
    )

    table.pack(fill="x")

    if not rows:

        tk.Label(
            table,
            text=empty_text,
            font=("Georgia", 12, "italic"),
            bg=CARD,
            fg=LIGHT_TEXT,
            pady=40
        ).pack()

    else:

        for column, header in enumerate(headers):

            tk.Label(
                table,
                text=header,
                font=("Arial", 10, "bold"),
                bg=CARD_DARK,
                fg=GOLD,
                anchor="w",
                width=widths[column],
                padx=12,
                pady=10
            ).grid(
                row=0,
                column=column,
                sticky="nsew"
            )

        for row_number, values in enumerate(rows, start=1):

            is_mine = (row_number - 1) == highlight_row

            for column, value in enumerate(values):

                tk.Label(
                    table,
                    text=str(value),
                    font=("Arial", 10, "bold" if is_mine else "normal"),
                    bg=CARD,
                    fg=GOLD_LIGHT if is_mine else TEXT,
                    anchor="w",
                    width=widths[column],
                    padx=12,
                    pady=9
                ).grid(
                    row=row_number,
                    column=column,
                    sticky="nsew"
                )

    scroll_quiz_page(0)


def show_results_page():

    rows = []

    try:

        conn = get_db()

        data = conn.execute(
            """
            SELECT quiz_title, score, total, taken_at
            FROM quiz_results
            WHERE LOWER(username) = LOWER(?)
            ORDER BY id DESC
            LIMIT 50
            """,
            (player_name(),)
        ).fetchall()

        conn.close()

        for quiz_title, score, total, taken_at in data:

            percent = round(score / total * 100) if total else 0

            rows.append((
                quiz_title,
                f"{score} / {total}",
                f"{percent}%",
                taken_at
            ))

    except Exception as error:

        print("Could not read results:", error)

    show_table_page(
        "Your Results",
        f"Quiz scores for {player_name()}",
        ["Quiz", "Score", "Percent", "Date"],
        rows,
        "No results yet.\nFinish a quiz and your score will appear here.",
        [34, 10, 10, 20]
    )


def show_leaderboard_page():

    players = {}

    try:

        conn = get_db()

        data = conn.execute(
            "SELECT username, score, total FROM quiz_results"
        ).fetchall()

        conn.close()

        for username, score, total in data:

            percent = round(score / total * 100) if total else 0

            entry = players.setdefault(
                username,
                {"best": 0, "attempts": 0}
            )

            entry["best"] = max(entry["best"], percent)
            entry["attempts"] += 1

    except Exception as error:

        print("Could not read leaderboard:", error)

    ranking = sorted(
        players.items(),
        key=lambda item: (-item[1]["best"], item[0].lower())
    )[:10]

    rows = []
    highlight = None

    for position, (username, entry) in enumerate(ranking, start=1):

        rows.append((
            f"#{position}",
            username,
            f"{entry['best']}%",
            entry["attempts"]
        ))

        if username.lower() == player_name().lower():
            highlight = position - 1

    show_table_page(
        "Leaderboard",
        "Top explorers ranked by their best quiz score",
        ["Rank", "Player", "Best Score", "Quizzes Taken"],
        rows,
        "The leaderboard is empty.\nBe the first to finish a quiz!",
        [8, 30, 14, 16],
        highlight_row=highlight
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

    frame.pack(fill="x")

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
    ).pack(pady=(5, 15))


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
    global quiz_questions

    current_quiz = quiz

    # IMPORTANT: Load the question set belonging to this card.
    quiz_questions = QUIZ_QUESTION_SETS.get(
        quiz["title"],
        bhutanese_questions
    )

    current_question = 0

    selected_answers = {}
    answered_questions = {}

    quiz_score = 0
    time_left = 10 * 60

    if timer_job is not None:

        try:
            quiz_content.after_cancel(timer_job)
        except:
            pass

        timer_job = None

    for widget in quiz_content.winfo_children():
        widget.destroy()

    build_question_page()

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

    # BANNER

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
        "banner.jpg",
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

        banner_canvas = tk.Canvas(
            banner,
            bg=BG,
            highlightthickness=0,
            bd=0
        )

        banner_canvas.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        banner_canvas.create_image(
            0, 0,
            image=banner_image,
            anchor="nw"
        )

        banner_canvas.create_text(
            35, 62,
            text="♢",
            anchor="w",
            font=("Arial", 38),
            fill=GOLD
        )

        banner_canvas.create_text(
            95, 52,
            text="Quiz",
            anchor="w",
            font=("Georgia", 32, "bold"),
            fill=TEXT
        )

        banner_canvas.create_text(
            95, 98,
            text="Challenge yourself with myths, legends and mythical creatures\nfrom Bhutan and around the world!",
            anchor="w",
            font=("Arial", 10),
            fill=WHITE
        )

    # BODY

    body = tk.Frame(
        page,
        bg=BG
    )

    body.pack(
        fill="x",
        padx=25,
        pady=(8, 0)
    )

    # QUESTION AREA

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

    # SIDE PANEL

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

    # QUESTION HEADER

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
    ).pack(side="left")

    category = current_quiz["category"]

    tk.Label(
        question_header,
        text="▣  " + category + " Quiz",
        font=("Arial", 10),
        bg=BG,
        fg=TEXT
    ).pack(side="right")

    # PROGRESS BAR

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

    # QUESTION

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

    # ANSWERS

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

    # NAVIGATION

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
    ).pack(side="left")

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
    ).pack(side="right")

    create_question_progress(side_panel)
    create_time_panel(side_panel)
    create_question_overview(side_panel)
    create_quiz_quote(side_panel)


# ============================================================
# ANSWER BUTTON
# ============================================================

def create_answer_button(parent, index, option):

    selected = selected_answers.get(current_question)

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

    if current_question not in selected_answers:

        messagebox.showwarning(
            "Select an Answer",
            "Please select an answer before continuing."
        )

        return

    # Recalculate the current answer so changing an earlier
    # answer does not leave an outdated score.

    selected = selected_answers[current_question]
    correct = quiz_questions[current_question]["answer"]

    if selected == correct:
        answered_questions[current_question] = "correct"
    else:
        answered_questions[current_question] = "incorrect"

    quiz_score = sum(
        1
        for question_number, answer_index in selected_answers.items()
        if answer_index == quiz_questions[question_number]["answer"]
    )

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

    canvas.pack(side="left")

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

    canvas.create_oval(
        12, 12, 93, 93,
        outline="#294c65",
        width=11
    )

    if total > 0:

        angle = (completed / total) * 360

        canvas.create_arc(
            12, 12, 93, 93,
            start=90,
            extent=-angle,
            style="arc",
            outline=GOLD_LIGHT,
            width=11
        )

    canvas.create_text(
        52, 43,
        text=f"{completed}/{total}",
        font=("Arial", 13, "bold"),
        fill=TEXT
    )

    canvas.create_text(
        52, 62,
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

    question_legend(legend, GREEN, "Correct", str(correct))
    question_legend(legend, RED, "Incorrect", str(incorrect))
    question_legend(legend, "#b9c5db", "Remaining", str(total - completed))


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
    ).pack(side="left")

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

    minutes = time_left // 60
    seconds = time_left % 60

    time_text = f"{minutes:02d}:{seconds:02d}"

    tk.Label(
        frame,
        text=time_text,
        font=("Georgia", 22, "bold"),
        bg=CARD,
        fg=TEXT
    ).pack(pady=5)

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

    percentage = max(time_left / (10 * 60), 0)

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

    if time_left <= 0:

        show_quiz_result()

        return

    time_left -= 1

    timer_job = quiz_content.after(
        1000,
        update_timer
    )


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

    frame.pack(fill="x")

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
    ).pack(pady=12)


# ============================================================
# QUIZ RESULT
# ============================================================

def show_quiz_result():

    global timer_job
    global quiz_score

    # Calculate final score using all selected answers.
    quiz_score = sum(
        1
        for question_number, answer_index in selected_answers.items()
        if answer_index == quiz_questions[question_number]["answer"]
    )

    if timer_job is not None:

        try:
            quiz_content.after_cancel(timer_job)
        except:
            pass

        timer_job = None

    save_quiz_result()

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
    ).pack(pady=10)

    tk.Label(
        result,
        text=f"You scored {quiz_score} out of {len(quiz_questions)}",
        font=("Arial", 15),
        bg=BG,
        fg=LIGHT_TEXT
    ).pack(pady=10)

    percentage = (
        quiz_score / len(quiz_questions)
    ) * 100

    tk.Label(
        result,
        text=f"{percentage:.0f}%",
        font=("Georgia", 32, "bold"),
        bg=BG,
        fg=GOLD_LIGHT
    ).pack(pady=10)

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
    ).pack(pady=20)


# ============================================================
# CATEGORY BUTTON
# ============================================================

def category_selected(category):

    show_quiz(quiz_content, category)
