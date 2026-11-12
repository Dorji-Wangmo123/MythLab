
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from PIL import Image, ImageTk, ImageOps, ImageDraw
import sqlite3
import hashlib
import hmac
import os
import re
import sys
import subprocess


# ============================================================
# MYTHLAB - WELCOME, LOGIN AND SIGN UP
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
DB_PATH = BASE_DIR / "mythlab.db"

NAVY = "#031725"
CARD = "#031522"
FIELD = "#061f2d"
GOLD = "#e9b75d"
GOLD_LIGHT = "#ffd27c"
TEXT = "#f6e8cd"
MUTED = "#c1c5ca"
ERROR = "#ff8888"
SUCCESS = "#83d6a0"


# ============================================================
# BACKGROUND IMAGE
# ============================================================

def find_background():
    extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

    for folder in [ASSETS_DIR, BASE_DIR]:
        if not folder.exists():
            continue

        for file in folder.iterdir():
            if (
                file.is_file()
                and file.stem.lower() == "backgr"
                and file.suffix.lower() in extensions
            ):
                return file

    return None


# ============================================================
# DATABASE
# ============================================================

def get_connection():
    return sqlite3.connect(DB_PATH)


def init_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                username TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        """)


def hash_password(password, salt=None, iterations=200000):
    if salt is None:
        salt = os.urandom(16).hex()

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        iterations
    )

    return salt, hashed.hex()


def get_user(identifier):
    with get_connection() as conn:
        return conn.execute("""
            SELECT id, full_name, email, username,
                   password_hash, salt
            FROM users
            WHERE LOWER(username) = LOWER(?)
               OR LOWER(email) = LOWER(?)
        """, (identifier, identifier)).fetchone()


def register_user(name, email, username, password):
    salt, hashed = hash_password(password)

    with get_connection() as conn:
        conn.execute("""
            INSERT INTO users
            (full_name, email, username, password_hash, salt)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, username, hashed, salt))


# ============================================================
# VALIDATION FUNCTIONS
# ============================================================

def validate_name(value):
    if len(value.strip()) < 2:
        return "Enter your full name."
    return ""


def validate_email(value):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.fullmatch(pattern, value):
        return "Enter a valid email address."

    return ""


def validate_username(value):
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{2,19}", value):
        return "3-20 characters; start with a letter. Use letters, numbers or _."

    return ""


def validate_password(value):
    missing = []

    if len(value) < 8:
        missing.append("8+ characters")

    if not re.search(r"[A-Z]", value):
        missing.append("uppercase")

    if not re.search(r"[a-z]", value):
        missing.append("lowercase")

    if not re.search(r"[0-9]", value):
        missing.append("number")

    if not re.search(r"[^A-Za-z0-9]", value):
        missing.append("special character")

    if missing:
        return "Add: " + ", ".join(missing)

    return ""


# ============================================================
# MAIN APPLICATION
# ============================================================

class MythLabApp:

    def __init__(self, root):
        self.root = root

        self.root.title("MythLab | Explore. Learn. Believe.")
        self.root.geometry("1280x800")
        self.root.minsize(1000, 720)
        self.root.configure(bg=NAVY)

        self.screen = "welcome"
        self.bg_source = None
        self.bg_photo = None
        self.resize_job = None

        path = find_background()

        if path:
            try:
                self.bg_source = Image.open(path).convert("RGB")
                print("Background loaded:", path)
            except Exception as error:
                print("Background error:", error)
        else:
            print("Background not found in:", ASSETS_DIR)

        self.root.bind("<Configure>", self.on_resize)
        self.root.bind("<Return>", self.handle_enter)

        self.draw_screen()

    # ========================================================
    # BACKGROUND RESIZING - FIXED
    # ========================================================

    def on_resize(self, event):
        if event.widget != self.root:
            return

        if self.resize_job is not None:
            self.root.after_cancel(self.resize_job)

        self.resize_job = self.root.after(
            100, self.update_layout
        )

    def update_layout(self):
        self.resize_job = None
        self.paint_background()
        self.position_card()

    def paint_background(self):
        if self.bg_source is None:
            return

        if not hasattr(self, "bg_label"):
            return

        w = self.root.winfo_width()
        h = self.root.winfo_height()

        if w < 10 or h < 10:
            return

        source = self.bg_source

        if source.width < 1 or source.height < 1:
            return

        image = ImageOps.fit(
            source,
            (w, h),
            method=Image.Resampling.LANCZOS
        )

        overlay = Image.new(
            "RGBA",
            (w, h),
            (0, 12, 22, 45)
        )

        image = Image.alpha_composite(
            image.convert("RGBA"),
            overlay
        ).convert("RGB")

        self.bg_photo = ImageTk.PhotoImage(image)

        self.bg_label.configure(image=self.bg_photo)
        self.bg_label.lower()

    # ========================================================
    # SCREEN MANAGEMENT
    # ========================================================

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_screen(self, screen):
        self.screen = screen
        self.draw_screen()

    def position_card(self):
        if not hasattr(self, "card"):
            return

        w = max(1000, self.root.winfo_width())
        h = max(720, self.root.winfo_height())

        card_width = 470

        if self.screen == "signup":
            card_height = 640
        else:
            card_height = 590

        x = max(120, int(w * 0.115))
        y = max(40, (h - card_height) // 2)

        self.card.place(
            x=x,
            y=y,
            width=card_width,
            height=card_height
        )

    def draw_screen(self):
        self.clear_screen()

        self.bg_label = tk.Label(
            self.root,
            bg=NAVY,
            bd=0
        )
        self.bg_label.place(
            x=0, y=0,
            relwidth=1,
            relheight=1
        )

        self.root.after_idle(self.paint_background)

        # Decorative borders
        tk.Frame(
            self.root,
            bg=GOLD,
            height=2
        ).place(
            relx=0.015,
            rely=0.025,
            relwidth=0.97
        )

        tk.Frame(
            self.root,
            bg=GOLD,
            height=2
        ).place(
            relx=0.015,
            rely=0.973,
            relwidth=0.97
        )

        # Back arrow
        if self.screen != "welcome":
            tk.Button(
                self.root,
                text="←",
                font=("Arial", 25, "bold"),
                bg=NAVY,
                fg=GOLD,
                activebackground=NAVY,
                activeforeground=GOLD_LIGHT,
                bd=0,
                cursor="hand2",
                command=lambda: self.show_screen("welcome")
            ).place(
                relx=0.035,
                rely=0.07,
                width=60,
                height=45
            )

        self.card = tk.Frame(
            self.root,
            bg=CARD,
            highlightbackground="#9d7841",
            highlightthickness=1
        )

        self.position_card()

        body = tk.Frame(self.card, bg=CARD)
        body.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=8
        )

        # Dragon logo
        tk.Label(
            body,
            text="🐉",
            font=("Segoe UI Emoji", 22),
            bg=CARD,
            fg=GOLD
        ).pack(pady=(0, 0))

        tk.Label(
            body,
            text="MythLab",
            font=("Georgia", 27, "bold"),
            bg=CARD,
            fg=GOLD_LIGHT
        ).pack()

        tk.Label(
            body,
            text="Explore. Learn. Believe.",
            font=("Georgia", 10),
            bg=CARD,
            fg=GOLD
        ).pack(pady=(0, 5))

        tk.Frame(
            body,
            bg="#846439",
            height=1
        ).pack(fill="x", pady=(0, 8))

        if self.screen == "welcome":
            self.welcome_page(body)

        elif self.screen == "login":
            self.login_page(body)

        elif self.screen == "signup":
            self.signup_page(body)

    # ========================================================
    # BUTTONS
    # ========================================================

    def make_button(self, parent, text, command, filled=True):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Georgia", 12, "bold"),
            bg=GOLD if filled else CARD,
            fg=NAVY if filled else GOLD,
            activebackground=GOLD_LIGHT,
            activeforeground=NAVY,
            cursor="hand2",
            relief="solid",
            bd=1,
            highlightbackground=GOLD
        )

    # ========================================================
    # LANDING PAGE
    # ========================================================

    def welcome_page(self, parent):
        tk.Label(
            parent,
            text="Welcome to MythLab",
            font=("Arial", 18, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(pady=(22, 12))

        tk.Label(
            parent,
            text=(
                "Discover Bhutanese myths, legends and stories\n"
                "through an interactive learning experience."
            ),
            font=("Arial", 10),
            bg=CARD,
            fg=MUTED,
            justify="center"
        ).pack(pady=(0, 30))

        self.make_button(
            parent,
            "Login  →",
            lambda: self.show_screen("login")
        ).pack(fill="x", ipady=12, pady=8)

        self.make_button(
            parent,
            "Create Account",
            lambda: self.show_screen("signup"),
            False
        ).pack(fill="x", ipady=12, pady=8)

        tk.Label(
            parent,
            text="──────────  OR  ──────────",
            bg=CARD,
            fg=MUTED
        ).pack(pady=15)

        self.make_button(
            parent,
            "Continue as Guest",
            self.guest,
            False
        ).pack(fill="x", ipady=10)

    # ========================================================
    # INPUT FIELD HELPER
    # ========================================================

    def create_field(self, parent, title, secret=False):
        tk.Label(
            parent,
            text=title,
            font=("Arial", 10),
            bg=CARD,
            fg=GOLD,
            anchor="w"
        ).pack(fill="x", pady=(5, 2))

        entry = tk.Entry(
            parent,
            font=("Arial", 11),
            bg=FIELD,
            fg=TEXT,
            insertbackground=GOLD,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground="#9d7841",
            show="●" if secret else ""
        )

        entry.pack(fill="x", ipady=5)

        return entry

    # ========================================================
    # LOGIN PAGE
    # ========================================================

    def login_page(self, parent):
        tk.Label(
            parent,
            text="Login to Continue",
            font=("Arial", 17, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(anchor="w", pady=(12, 6))

        tk.Label(
            parent,
            text="Welcome back! Enter your details to access MythLab.",
            font=("Arial", 10),
            bg=CARD,
            fg=MUTED
        ).pack(anchor="w", pady=(0, 12))

        self.l_user = self.create_field(
            parent, "Username or Email"
        )

        self.l_pass = self.create_field(
            parent, "Password", True
        )

        self.login_msg = tk.Label(
            parent,
            text="",
            font=("Arial", 9),
            bg=CARD,
            fg=ERROR
        )
        self.login_msg.pack(pady=8)

        self.make_button(
            parent,
            "Login  →",
            self.login
        ).pack(fill="x", ipady=10, pady=10)

        tk.Label(
            parent,
            text="──────────  OR  ──────────",
            bg=CARD,
            fg=MUTED
        ).pack(pady=8)

        self.make_button(
            parent,
            "Continue as Guest",
            self.guest,
            False
        ).pack(fill="x", ipady=9)

        tk.Button(
            parent,
            text="New to MythLab? Create Account",
            font=("Arial", 10),
            bg=CARD,
            fg=GOLD,
            bd=0,
            cursor="hand2",
            command=lambda: self.show_screen("signup")
        ).pack(pady=12)

    # ========================================================
    # SIGN UP PAGE
    # ========================================================

    def signup_page(self, parent):
        tk.Label(
            parent,
            text="Create Your Account",
            font=("Arial", 15, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(anchor="w", pady=(0, 2))

        tk.Label(
            parent,
            text="Join MythLab and start exploring.",
            font=("Arial", 9),
            bg=CARD,
            fg=MUTED
        ).pack(anchor="w", pady=(0, 3))

        self.entries = {}
        self.hints = {}

        self.add_signup_field(parent, "Full Name", "name")
        self.add_signup_field(parent, "Email Address", "email")
        self.add_signup_field(parent, "Username", "username")
        self.add_signup_field(parent, "Password", "password", True)
        self.add_signup_field(
            parent, "Confirm Password", "confirm", True
        )

        self.signup_msg = tk.Label(
            parent,
            text="",
            bg=CARD,
            fg=ERROR,
            font=("Arial", 9)
        )
        self.signup_msg.pack(pady=(2, 0))

        # Always visible inside the card
        self.make_button(
            parent,
            "Create Account  →",
            self.signup
        ).pack(
            fill="x",
            ipady=7,
            pady=(3, 3)
        )

        tk.Button(
            parent,
            text="Already have an account? Login",
            font=("Arial", 9),
            bg=CARD,
            fg=GOLD,
            bd=0,
            cursor="hand2",
            command=lambda: self.show_screen("login")
        ).pack(pady=(1, 0))

    # ========================================================
    # SIGN UP FIELDS AND LIVE VALIDATION
    # ========================================================

    def add_signup_field(self, parent, title, key, secret=False):
        tk.Label(
            parent,
            text=title,
            font=("Arial", 9),
            bg=CARD,
            fg=GOLD,
            anchor="w"
        ).pack(fill="x", pady=(3, 1))

        entry = tk.Entry(
            parent,
            font=("Arial", 11),
            bg=FIELD,
            fg=TEXT,
            insertbackground=GOLD,
            show="●" if secret else "",
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground="#9d7841"
        )

        entry.pack(fill="x", ipady=4)

        hint = tk.Label(
            parent,
            text="",
            font=("Arial", 8),
            bg=CARD,
            fg=MUTED,
            anchor="w",
            height=1
        )

        hint.pack(fill="x")

        self.entries[key] = entry
        self.hints[key] = hint

        entry.bind(
            "<KeyRelease>",
            lambda event, k=key: self.live_validate(k)
        )

        entry.bind(
            "<FocusOut>",
            lambda event, k=key: self.live_validate(k)
        )

    def live_validate(self, key):
        value = self.entries[key].get()

        if not value:
            self.hints[key].config(text="")
            return

        error = ""

        if key == "name":
            error = validate_name(value)

        elif key == "email":
            error = validate_email(value)

        elif key == "username":
            error = validate_username(value)

        elif key == "password":
            error = validate_password(value)

        elif key == "confirm":
            password = self.entries["password"].get()

            if value != password:
                error = "Passwords do not match."

        if error:
            self.hints[key].config(
                text="✗ " + error,
                fg=ERROR
            )
        else:
            self.hints[key].config(
                text="✓ Looks good",
                fg=SUCCESS
            )

        if key == "password":
            if self.entries["confirm"].get():
                self.live_validate("confirm")

    # ========================================================
    # CREATE ACCOUNT
    # ========================================================

    def signup(self):
        name = self.entries["name"].get().strip()
        email = self.entries["email"].get().strip().lower()
        username = self.entries["username"].get().strip().lower()
        password = self.entries["password"].get()
        confirm = self.entries["confirm"].get()

        if not all([name, email, username, password, confirm]):
            self.signup_msg.config(
                text="✗ Please fill in all fields."
            )
            return

        checks = [
            ("name", validate_name(name)),
            ("email", validate_email(email)),
            ("username", validate_username(username)),
            ("password", validate_password(password))
        ]

        if password != confirm:
            checks.append(
                ("confirm", "Passwords do not match.")
            )

        for key, error in checks:
            if error:
                self.hints[key].config(
                    text="✗ " + error,
                    fg=ERROR
                )
                self.signup_msg.config(
                    text="✗ Please correct the highlighted fields."
                )
                return

        try:
            register_user(
                name, email, username, password
            )

        except sqlite3.IntegrityError:
            self.signup_msg.config(
                text="✗ Username or email already registered."
            )
            return

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )
            return

        messagebox.showinfo(
            "Account Created Successfully",
            "Welcome to MythLab, " + name + "!\n\n"
            "Your account has been created successfully.\n"
            "Please log in to continue."
        )

        self.show_screen("login")

    # ========================================================
    # LOGIN VALIDATION
    # ========================================================

    def login(self):
        username = self.l_user.get().strip()
        password = self.l_pass.get()

        if not username or not password:
            self.login_msg.config(
                text="Please enter username and password."
            )
            return

        try:
            user = get_user(username)

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )
            return

        if user is None:
            self.login_msg.config(
                text="✗ Incorrect username or password."
            )
            return

        user_id, name, email, db_username, stored_hash, salt = user

        # Supports accounts created by both the earlier
        # 100,000-iteration and newer 200,000-iteration versions.
        try:
            valid = False

            for iterations in (200000, 100000):
                _, entered_hash = hash_password(
                    password, salt, iterations
                )

                if hmac.compare_digest(
                    entered_hash, stored_hash
                ):
                    valid = True
                    break

        except (ValueError, TypeError):
            valid = False

        if not valid:
            self.login_msg.config(
                text="✗ Incorrect username or password."
            )
            return

        messagebox.showinfo(
            "Login Successful",
            "Welcome, " + (name or db_username) + "!"
        )

        self.open_home(db_username)

    # ========================================================
    # GUEST ACCESS
    # ========================================================

    def guest(self):
        self.open_home(None)

    # ========================================================
    # OPEN MAIN MYTHLAB APPLICATION
    # ========================================================

    def open_home(self, username):
        main_file = BASE_DIR / "main.py"

        if not main_file.exists():
            messagebox.showwarning(
                "Main Application",
                "Your account is ready, but the MythLab dashboard "
                "file main.py was not found.\n\n"
                "Please connect your actual dashboard main.py."
            )
            return

        try:
            subprocess.Popen(
                [
                    sys.executable,
                    str(main_file),
                    username or ""
                ],
                cwd=str(BASE_DIR)
            )

            self.root.destroy()

        except OSError as error:
            messagebox.showerror(
                "Unable to Open MythLab",
                str(error)
            )

    # ========================================================
    # ENTER KEY EVENT HANDLING
    # ========================================================

    def handle_enter(self, event=None):
        if self.screen == "login":
            self.login()

        elif self.screen == "signup":
            self.signup()


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    init_database()

    root = tk.Tk()
    app = MythLabApp(root)

    root.mainloop()
