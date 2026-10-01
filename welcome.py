'''
import tkinter as tk
from tkinter import messagebox
import re
import os
import json
import hashlib


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()
root.title("MythLab")
root.geometry("1200x850")
root.minsize(900, 820)
root.configure(bg="#071b2b")


# ==========================================
# COLOURS
# ==========================================

BG = "#071b2b"
CARD = "#102b3d"
FIELD = "#0a2030"
GOLD = "#d6a84f"
GOLD_LT = "#f3d9a8"
GOLD_DIM = "#8a6a3a"
TEXT = "#f5ead0"
LIGHT_TEXT = "#c7c1b3"
ERROR = "#ff7b7b"
OK = "#6fcf97"


# ==========================================
# USER STORAGE (saved next to this file)
# ==========================================

USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")


def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def hash_password(password, salt=None):
    salt = salt or os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 100_000)
    return salt, digest.hex()


# ==========================================
# VALIDATORS  (return "" if OK, else the error message)
# ==========================================

def check_name(v):
    if not v.strip():
        return "Full name is required."
    if not re.fullmatch(r"[A-Za-z][A-Za-z '\-]{1,48}", v.strip()):
        return "Use letters only (at least 2 characters)."
    return ""


def check_email(v):
    if not v.strip():
        return "Email is required."
    if not re.fullmatch(r"[\w.+\-]+@[\w\-]+(\.[\w\-]+)+", v.strip()):
        return "Enter a valid email, e.g. name@example.com."
    if v.strip().lower() in [u["email"] for u in load_users().values()]:
        return "This email is already registered."
    return ""


def check_username(v):
    if not v.strip():
        return "Username is required."
    if not re.fullmatch(r"[A-Za-z0-9_]{4,15}", v.strip()):
        return "4–15 characters: letters, numbers or underscore."
    if v.strip().lower() in load_users():
        return "This username is already taken."
    return ""


def check_password(v):
    if not v:
        return "Password is required."
    if len(v) < 8:
        return "Password must be at least 8 characters."
    if not re.search(r"[A-Z]", v):
        return "Add at least one uppercase letter."
    if not re.search(r"[a-z]", v):
        return "Add at least one lowercase letter."
    if not re.search(r"\d", v):
        return "Add at least one number."
    if not re.search(r"[^A-Za-z0-9]", v):
        return "Add at least one symbol (e.g. ! @ # $)."
    return ""


def check_confirm(v):
    if not v:
        return "Please confirm your password."
    if v != f_pass.get():
        return "Passwords do not match."
    return ""


# ==========================================
# FORM FIELD  (label + entry + red/green message)
# ==========================================

class FormField:
    def __init__(self, parent, label, validator, secret=False,
                 ok_text="✓ Looks good", show_ok=True):
        self.validator = validator
        self.ok_text = ok_text
        self.show_ok = show_ok

        frame = tk.Frame(parent, bg=CARD)
        frame.pack(fill="x", pady=(6, 0))

        tk.Label(frame, text=label, font=("Arial", 10),
                 bg=CARD, fg=LIGHT_TEXT).pack(anchor="w")

        row = tk.Frame(frame, bg=CARD)
        row.pack(fill="x")

        self.var = tk.StringVar()
        self.entry = tk.Entry(
            row, textvariable=self.var, font=("Arial", 12),
            bg=FIELD, fg=TEXT, insertbackground=GOLD, relief="flat",
            show="•" if secret else "",
            highlightthickness=1, highlightbackground=GOLD_DIM, highlightcolor=GOLD
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=6)

        if secret:
            tk.Button(
                row, text="👁", font=("Arial", 10), bg=FIELD, fg=GOLD,
                activebackground=FIELD, activeforeground=GOLD_LT,
                relief="flat", cursor="hand2", command=self.toggle_show
            ).pack(side="left", padx=(4, 0), ipady=2)

        self.message = tk.Label(frame, text="", font=("Arial", 9),
                                bg=CARD, fg=ERROR, anchor="w")
        self.message.pack(fill="x")

        self.entry.bind("<FocusOut>", lambda e: self.validate())
        self.entry.bind("<KeyRelease>", self.on_key)

    def on_key(self, event):
        if event.keysym in ("Tab", "ISO_Left_Tab", "Shift_L", "Shift_R"):
            return
        self.validate()

    def toggle_show(self):
        self.entry.config(show="" if self.entry.cget("show") else "•")

    def get(self):
        return self.var.get()

    def clear(self):
        self.var.set("")
        self.set_status("")

    def set_status(self, error):
        if error:                                   # wrong or missing -> red
            self.message.config(text="✗ " + error, fg=ERROR)
            self.entry.config(highlightbackground=ERROR, highlightcolor=ERROR)
        elif self.show_ok and self.get():           # correct -> green
            self.message.config(text=self.ok_text, fg=OK)
            self.entry.config(highlightbackground=OK, highlightcolor=OK)
        else:                                       # neutral
            self.message.config(text="")
            self.entry.config(highlightbackground=GOLD_DIM, highlightcolor=GOLD)

    def validate(self):
        error = self.validator(self.get())
        self.set_status(error)
        return error == ""


# ==========================================
# SCREEN SWITCHING
# ==========================================

def show_screen(screen):
    for s in (welcome_screen, signup_screen, login_screen):
        s.pack_forget()
    screen.pack(fill="both", expand=True)


# ==========================================
# WELCOME SCREEN
# ==========================================

def lerp(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


welcome_screen = tk.Frame(root, bg=BG)
welcome_canvas = tk.Canvas(welcome_screen, bg=BG, highlightthickness=0)
welcome_canvas.pack(fill="both", expand=True)


def canvas_button(c, cx, cy, w, h, text, filled, command, tag):
    x1, y1, x2, y2 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    r = h / 2
    pts = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y2, x2 - r, y2, x1 + r, y2, x1, y2, x1, y1]
    c.create_polygon(pts, smooth=True, tags=tag,
                     fill=GOLD if filled else "#071b2b", outline=GOLD, width=2)
    c.create_text(cx, cy, text=text, tags=tag,
                  fill="#2b1d05" if filled else GOLD_LT, font=("Georgia", 14))
    c.tag_bind(tag, "<Enter>", lambda e: c.config(cursor="hand2"))
    c.tag_bind(tag, "<Leave>", lambda e: c.config(cursor=""))
    c.tag_bind(tag, "<Button-1>", lambda e: command())


def corner(c, x, y, sx, sy):
    """Gold corner ornament. sx/sy = +1 or -1 to mirror it."""
    c.create_line(x, y + sy * 110, x, y, x + sx * 150, y, fill=GOLD, width=1)
    c.create_oval(x + sx * 14, y + sy * 14, x + sx * 54, y + sy * 54, outline=GOLD, width=1)
    c.create_oval(x + sx * 24, y + sy * 24, x + sx * 44, y + sy * 44, outline=GOLD, width=1)
    c.create_arc(x + sx * 40, y + sy * 8, x + sx * 100, y + sy * 60,
                 start=0, extent=180, style="arc", outline=GOLD)


def draw_welcome(event=None):
    c = welcome_canvas
    c.delete("all")
    w, h = c.winfo_width(), c.winfo_height()
    if w < 50:
        return
    cx = w / 2

    # sky: dark navy on the left, sunset glow on the right
    for y in range(h):
        c.create_line(0, y, w, y, fill=lerp("#0b1626", "#050d17", y / h))
    c.create_oval(w * .70, -h * .25, w * 1.15, h * .30, fill="#6b4040", outline="", stipple="gray25")
    c.create_oval(w * .80, -h * .12, w * 1.05, h * .20, fill="#e0883f", outline="", stipple="gray25")

    # mountains
    c.create_polygon(0, h * .40, w * .07, h * .30, w * .13, h * .36, w * .20, h * .28,
                     w * .30, h * .40, w * .30, h * .70, 0, h * .70, fill="#17233b", outline="")
    c.create_polygon(w * .66, h * .40, w * .76, h * .28, w * .83, h * .35, w * .92, h * .27,
                     w, h * .36, w, h * .70, w * .66, h * .70, fill="#1c2a42", outline="")
    c.create_polygon(0, h * .50, w * .2, h * .44, w * .4, h * .56, w * .6, h * .50, w * .8, h * .56,
                     w, h * .48, w, h, 0, h, fill="#08121c", outline="")

    # dzong silhouette (right side)
    dx, dy = w * .76, h * .43
    for (a, b, cc, d, col) in [(0, 0, 150, 40, "#e6d9c4"), (22, -32, 128, 0, "#d9c9ae"), (45, -56, 105, -32, "#c9b898")]:
        c.create_rectangle(dx + a, dy + b, dx + cc, dy + d, fill=col, outline="")
        c.create_rectangle(dx + a - 6, dy + b - 6, dx + cc + 6, dy + b, fill="#6b3326", outline="")
    c.create_polygon(dx - 40, dy + 40, dx + 190, dy + 40, dx + 150, dy + 110, dx, dy + 110,
                     fill="#0d1a12", outline="")

    # trees
    for tx in range(0, w, 46):
        th = 50 + (tx * 7 % 5) * 14
        if tx < w * .3 or tx > w * .62:
            c.create_polygon(tx, h * .72, tx + 18, h * .72 - th, tx + 36, h * .72,
                             fill="#06100b", outline="")

    # prayer flags
    flag_colors = ["#3b6fd0", "#e8e8e8", "#c0392b", "#2e9e5b", "#e6c229"]
    for i in range(14):
        fx = w * .74 + i * (w * .26 / 14)
        fy = h * .53 + i * 4 + (3 if i % 2 else 0)
        c.create_rectangle(fx, fy, fx + 14, fy + 18, fill=flag_colors[i % 5], outline="")

    # corners + top/bottom knots
    corner(c, 14, 22, 1, 1)
    corner(c, w - 14, 22, -1, 1)
    corner(c, 14, h - 22, 1, -1)
    corner(c, w - 14, h - 22, -1, -1)
    for y in (22, h - 22):
        c.create_line(cx - 140, y, cx - 22, y, fill=GOLD_DIM)
        c.create_line(cx + 22, y, cx + 140, y, fill=GOLD_DIM)
        c.create_text(cx, y, text="❖", fill=GOLD, font=("Arial", 16))

    # centre content
    c.create_text(cx, h * .26, text="🐉", fill=GOLD, font=("Arial", 54))
    c.create_text(cx, h * .39, text="MythLab", fill=GOLD, font=("Georgia", 52))
    c.create_text(cx, h * .48, text="Explore. Learn. Believe.", fill=GOLD_LT, font=("Georgia", 17))
    c.create_line(cx - 160, h * .53, cx - 18, h * .53, fill=GOLD_DIM)
    c.create_line(cx + 18, h * .53, cx + 160, h * .53, fill=GOLD_DIM)
    c.create_text(cx, h * .53, text="❖", fill=GOLD, font=("Arial", 12))
    c.create_text(cx, h * .60,
                  text="Discover the myths, legends and mythical\ncreatures of Bhutan and beyond.",
                  fill=TEXT, font=("Georgia", 13), justify="center")

    canvas_button(c, cx, h * .72, 280, 56, "Get Started  →", True,
                  lambda: show_screen(signup_screen), "btn_start")
    canvas_button(c, cx, h * .80, 280, 46, "Login", False,
                  lambda: show_screen(login_screen), "btn_login")


welcome_canvas.bind("<Configure>", draw_welcome)


# ==========================================
# FORM CARD BUILDER
# ==========================================

def build_form_screen(title, subtitle):
    screen = tk.Frame(root, bg=BG)

    card = tk.Frame(screen, bg=CARD, highlightthickness=1, highlightbackground=GOLD)
    card.place(relx=0.5, rely=0.5, anchor="center")

    inner = tk.Frame(card, bg=CARD)
    inner.pack(padx=45, pady=24)

    tk.Label(inner, text="🐉", font=("Arial", 26), bg=CARD, fg=GOLD).pack()
    tk.Label(inner, text=title, font=("Georgia", 22), bg=CARD, fg=GOLD_LT).pack()
    tk.Label(inner, text=subtitle, font=("Arial", 10), bg=CARD, fg=LIGHT_TEXT).pack(pady=(0, 6))

    body = tk.Frame(inner, bg=CARD, width=360)
    body.pack(fill="x")
    return screen, inner, body


def gold_button(parent, text, command):
    return tk.Button(parent, text=text, font=("Arial", 12, "bold"),
                     bg=GOLD, fg="#2b1d05", activebackground=GOLD_LT,
                     relief="flat", cursor="hand2", pady=8, command=command)


def link_button(parent, text, command):
    return tk.Button(parent, text=text, font=("Arial", 10, "underline"),
                     bg=CARD, fg=GOLD, activebackground=CARD, activeforeground=GOLD_LT,
                     relief="flat", cursor="hand2", command=command)


# ==========================================
# CREATE ACCOUNT SCREEN
# ==========================================

signup_screen, signup_inner, signup_body = build_form_screen(
    "Create Account", "Join MythLab and start exploring."
)

f_name = FormField(signup_body, "Full name", check_name, ok_text="✓ Nice to meet you!")
f_email = FormField(signup_body, "Email", check_email, ok_text="✓ Email looks good")
f_user = FormField(signup_body, "Username", check_username, ok_text="✓ Username is available")
f_pass = FormField(signup_body, "Password", check_password,
                   secret=True, ok_text="✓ Strong password")
f_confirm = FormField(signup_body, "Confirm password", check_confirm,
                      secret=True, ok_text="✓ Passwords match")

# when the password changes, re-check the confirm box too
f_pass.entry.bind("<KeyRelease>",
                  lambda e: (f_pass.on_key(e),
                             f_confirm.validate() if f_confirm.get() else None))


# ---------- Terms checkbox ----------

terms_var = tk.IntVar()
terms_msg = tk.Label(signup_body, text="", font=("Arial", 9), bg=CARD, fg=ERROR, anchor="w")


def terms_changed():
    if terms_var.get():
        terms_msg.config(text="✓ Thanks for agreeing", fg=OK)
    else:
        terms_msg.config(text="✗ You must agree to the Terms of Use.", fg=ERROR)


tk.Checkbutton(
    signup_body, text="I agree to the Terms of Use", variable=terms_var,
    font=("Arial", 10), bg=CARD, fg=TEXT, selectcolor=FIELD,
    activebackground=CARD, activeforeground=GOLD,
    command=terms_changed
).pack(anchor="w", pady=(10, 0))
terms_msg.pack(fill="x")


# ---------- Create account ----------

def create_account():
    # run every validator (don't stop at the first failure)
    results = [f.validate() for f in (f_name, f_email, f_user, f_pass, f_confirm)]

    if not terms_var.get():
        terms_changed()
        results.append(False)

    if not all(results):
        messagebox.showerror("Create Account", "Please fix the fields marked in red.")
        return

    users = load_users()
    salt, hashed = hash_password(f_pass.get())
    users[f_user.get().strip().lower()] = {
        "name": f_name.get().strip(),
        "email": f_email.get().strip().lower(),
        "salt": salt,
        "password": hashed
    }
    save_users(users)

    messagebox.showinfo("Account created",
                        "Welcome to MythLab, " + f_name.get().strip().split()[0] + "!\nYou can now log in.")
    for f in (f_name, f_email, f_user, f_pass, f_confirm):
        f.clear()
    terms_var.set(0)
    terms_msg.config(text="")
    show_screen(login_screen)


gold_button(signup_body, "Create Account", create_account).pack(fill="x", pady=(8, 4))

bottom = tk.Frame(signup_body, bg=CARD)
bottom.pack()
tk.Label(bottom, text="Already have an account?", font=("Arial", 10),
         bg=CARD, fg=LIGHT_TEXT).pack(side="left")
link_button(bottom, "Login", lambda: show_screen(login_screen)).pack(side="left")
link_button(signup_body, "← Back", lambda: show_screen(welcome_screen)).pack()


# ==========================================
# LOGIN SCREEN
# ==========================================

login_screen, login_inner, login_body = build_form_screen(
    "Welcome Back", "Log in to continue your journey."
)

l_user = FormField(login_body, "Username",
                   lambda v: "" if v.strip() else "Username is required.", show_ok=False)
l_pass = FormField(login_body, "Password",
                   lambda v: "" if v else "Password is required.", secret=True, show_ok=False)

login_msg = tk.Label(login_body, text="", font=("Arial", 10), bg=CARD, fg=ERROR)
login_msg.pack(pady=(6, 0))


def login():
    login_msg.config(text="")
    ok_user = l_user.validate()
    ok_pass = l_pass.validate()
    if not (ok_user and ok_pass):
        return

    user = load_users().get(l_user.get().strip().lower())

    if user is None:
        login_msg.config(text="✗ Incorrect username or password.", fg=ERROR)
        return

    _, hashed = hash_password(l_pass.get(), user["salt"])
    if hashed != user["password"]:
        login_msg.config(text="✗ Incorrect username or password.", fg=ERROR)
        return

    login_msg.config(text="✓ Login successful!", fg=OK)
    messagebox.showinfo("Login", "Welcome, " + user["name"] + "!")
    l_user.clear()
    l_pass.clear()
    login_msg.config(text="")
    # TODO: open your Home page here (e.g. root.destroy() then run home.py)


gold_button(login_body, "Login", login).pack(fill="x", pady=(8, 4))

bottom2 = tk.Frame(login_body, bg=CARD)
bottom2.pack()
tk.Label(bottom2, text="New to MythLab?", font=("Arial", 10),
         bg=CARD, fg=LIGHT_TEXT).pack(side="left")
link_button(bottom2, "Create account", lambda: show_screen(signup_screen)).pack(side="left")
link_button(login_body, "← Back", lambda: show_screen(welcome_screen)).pack()

root.bind("<Return>", lambda e: login() if login_screen.winfo_ismapped()
          else create_account() if signup_screen.winfo_ismapped() else None)


# ==========================================
# RUN
# ==========================================

show_screen(welcome_screen)
root.mainloop()'''
import tkinter as tk
from tkinter import messagebox
import re
import os
import sys
import json
import hashlib
import subprocess


# ==========================================
# MAIN WINDOW
# ==========================================

root = tk.Tk()
root.title("MythLab")
root.geometry("1200x850")
root.minsize(900, 820)
root.configure(bg="#071b2b")


# ==========================================
# COLOURS
# ==========================================

BG = "#071b2b"
CARD = "#102b3d"
FIELD = "#0a2030"
GOLD = "#d6a84f"
GOLD_LT = "#f3d9a8"
GOLD_DIM = "#8a6a3a"
TEXT = "#f5ead0"
LIGHT_TEXT = "#c7c1b3"
ERROR = "#ff7b7b"
OK = "#6fcf97"


# ==========================================
# NEXT PAGE  (change this if your file has another name)
# ==========================================

NEXT_PAGE = "home.py"


# ==========================================
# USER STORAGE (saved next to this file)
# ==========================================

USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")


def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def hash_password(password, salt=None):
    salt = salt or os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 100_000)
    return salt, digest.hex()


# ==========================================
# VALIDATORS  (return "" if OK, else the error message)
# ==========================================

def check_name(v):
    if not v.strip():
        return "Full name is required."
    if not re.fullmatch(r"[A-Za-z][A-Za-z '\-]{1,48}", v.strip()):
        return "Use letters only (at least 2 characters)."
    return ""


def check_email(v):
    if not v.strip():
        return "Email is required."
    if not re.fullmatch(r"[\w.+\-]+@[\w\-]+(\.[\w\-]+)+", v.strip()):
        return "Enter a valid email, e.g. name@example.com."
    if v.strip().lower() in [u["email"] for u in load_users().values()]:
        return "This email is already registered."
    return ""


def check_username(v):
    if not v.strip():
        return "Username is required."
    if not re.fullmatch(r"[A-Za-z0-9_]{4,15}", v.strip()):
        return "4–15 characters: letters, numbers or underscore."
    if v.strip().lower() in load_users():
        return "This username is already taken."
    return ""


def check_password(v):
    if not v:
        return "Password is required."
    if len(v) < 8:
        return "Password must be at least 8 characters."
    if not re.search(r"[A-Z]", v):
        return "Add at least one uppercase letter."
    if not re.search(r"[a-z]", v):
        return "Add at least one lowercase letter."
    if not re.search(r"\d", v):
        return "Add at least one number."
    if not re.search(r"[^A-Za-z0-9]", v):
        return "Add at least one symbol (e.g. ! @ # $)."
    return ""


def check_confirm(v):
    if not v:
        return "Please confirm your password."
    if v != f_pass.get():
        return "Passwords do not match."
    return ""


# ==========================================
# FORM FIELD  (label + entry + red/green message)
# ==========================================

class FormField:
    def __init__(self, parent, label, validator, secret=False,
                 ok_text="✓ Looks good", show_ok=True):
        self.validator = validator
        self.ok_text = ok_text
        self.show_ok = show_ok

        frame = tk.Frame(parent, bg=CARD)
        frame.pack(fill="x", pady=(6, 0))

        tk.Label(frame, text=label, font=("Arial", 10),
                 bg=CARD, fg=LIGHT_TEXT).pack(anchor="w")

        row = tk.Frame(frame, bg=CARD)
        row.pack(fill="x")

        self.var = tk.StringVar()
        self.entry = tk.Entry(
            row, textvariable=self.var, font=("Arial", 12),
            bg=FIELD, fg=TEXT, insertbackground=GOLD, relief="flat",
            show="•" if secret else "",
            highlightthickness=1, highlightbackground=GOLD_DIM, highlightcolor=GOLD
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=6)

        if secret:
            tk.Button(
                row, text="👁", font=("Arial", 10), bg=FIELD, fg=GOLD,
                activebackground=FIELD, activeforeground=GOLD_LT,
                relief="flat", cursor="hand2", command=self.toggle_show
            ).pack(side="left", padx=(4, 0), ipady=2)

        self.message = tk.Label(frame, text="", font=("Arial", 9),
                                bg=CARD, fg=ERROR, anchor="w")
        self.message.pack(fill="x")

        self.entry.bind("<FocusOut>", lambda e: self.validate())
        self.entry.bind("<KeyRelease>", self.on_key)

    def on_key(self, event):
        if event.keysym in ("Tab", "ISO_Left_Tab", "Shift_L", "Shift_R"):
            return
        self.validate()

    def toggle_show(self):
        self.entry.config(show="" if self.entry.cget("show") else "•")

    def get(self):
        return self.var.get()

    def clear(self):
        self.var.set("")
        self.set_status("")

    def set_status(self, error):
        if error:                                   # wrong or missing -> red
            self.message.config(text="✗ " + error, fg=ERROR)
            self.entry.config(highlightbackground=ERROR, highlightcolor=ERROR)
        elif self.show_ok and self.get():           # correct -> green
            self.message.config(text=self.ok_text, fg=OK)
            self.entry.config(highlightbackground=OK, highlightcolor=OK)
        else:                                       # neutral
            self.message.config(text="")
            self.entry.config(highlightbackground=GOLD_DIM, highlightcolor=GOLD)

    def validate(self):
        error = self.validator(self.get())
        self.set_status(error)
        return error == ""


# ==========================================
# SCREEN SWITCHING
# ==========================================

def show_screen(screen):
    for s in (welcome_screen, signup_screen, login_screen):
        s.pack_forget()
    screen.pack(fill="both", expand=True)


# ==========================================
# OPEN NEXT PAGE AFTER LOGIN
# ==========================================

def open_home(username):
    page_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), NEXT_PAGE)

    if not os.path.exists(page_file):
        messagebox.showerror(
            "Page not found",
            NEXT_PAGE + " was not found in the same folder as welcome.py.\n\n"
            "Create it, or change NEXT_PAGE at the top of this file."
        )
        return

    root.destroy()                                        # close login window
    subprocess.Popen([sys.executable, page_file, username])  # open next page


# ==========================================
# WELCOME SCREEN
# ==========================================

def lerp(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


welcome_screen = tk.Frame(root, bg=BG)
welcome_canvas = tk.Canvas(welcome_screen, bg=BG, highlightthickness=0)
welcome_canvas.pack(fill="both", expand=True)


def canvas_button(c, cx, cy, w, h, text, filled, command, tag):
    x1, y1, x2, y2 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    r = h / 2
    pts = [x1 + r, y1, x2 - r, y1, x2, y1, x2, y2, x2 - r, y2, x1 + r, y2, x1, y2, x1, y1]
    c.create_polygon(pts, smooth=True, tags=tag,
                     fill=GOLD if filled else "#071b2b", outline=GOLD, width=2)
    c.create_text(cx, cy, text=text, tags=tag,
                  fill="#2b1d05" if filled else GOLD_LT, font=("Georgia", 14))
    c.tag_bind(tag, "<Enter>", lambda e: c.config(cursor="hand2"))
    c.tag_bind(tag, "<Leave>", lambda e: c.config(cursor=""))
    c.tag_bind(tag, "<Button-1>", lambda e: command())


def corner(c, x, y, sx, sy):
    """Gold corner ornament. sx/sy = +1 or -1 to mirror it."""
    c.create_line(x, y + sy * 110, x, y, x + sx * 150, y, fill=GOLD, width=1)
    c.create_oval(x + sx * 14, y + sy * 14, x + sx * 54, y + sy * 54, outline=GOLD, width=1)
    c.create_oval(x + sx * 24, y + sy * 24, x + sx * 44, y + sy * 44, outline=GOLD, width=1)
    c.create_arc(x + sx * 40, y + sy * 8, x + sx * 100, y + sy * 60,
                 start=0, extent=180, style="arc", outline=GOLD)


def draw_welcome(event=None):
    c = welcome_canvas
    c.delete("all")
    w, h = c.winfo_width(), c.winfo_height()
    if w < 50:
        return
    cx = w / 2

    # sky: dark navy on the left, sunset glow on the right
    for y in range(h):
        c.create_line(0, y, w, y, fill=lerp("#0b1626", "#050d17", y / h))
    c.create_oval(w * .70, -h * .25, w * 1.15, h * .30, fill="#6b4040", outline="", stipple="gray25")
    c.create_oval(w * .80, -h * .12, w * 1.05, h * .20, fill="#e0883f", outline="", stipple="gray25")

    # mountains
    c.create_polygon(0, h * .40, w * .07, h * .30, w * .13, h * .36, w * .20, h * .28,
                     w * .30, h * .40, w * .30, h * .70, 0, h * .70, fill="#17233b", outline="")
    c.create_polygon(w * .66, h * .40, w * .76, h * .28, w * .83, h * .35, w * .92, h * .27,
                     w, h * .36, w, h * .70, w * .66, h * .70, fill="#1c2a42", outline="")
    c.create_polygon(0, h * .50, w * .2, h * .44, w * .4, h * .56, w * .6, h * .50, w * .8, h * .56,
                     w, h * .48, w, h, 0, h, fill="#08121c", outline="")

    # dzong silhouette (right side)
    dx, dy = w * .76, h * .43
    for (a, b, cc, d, col) in [(0, 0, 150, 40, "#e6d9c4"), (22, -32, 128, 0, "#d9c9ae"), (45, -56, 105, -32, "#c9b898")]:
        c.create_rectangle(dx + a, dy + b, dx + cc, dy + d, fill=col, outline="")
        c.create_rectangle(dx + a - 6, dy + b - 6, dx + cc + 6, dy + b, fill="#6b3326", outline="")
    c.create_polygon(dx - 40, dy + 40, dx + 190, dy + 40, dx + 150, dy + 110, dx, dy + 110,
                     fill="#0d1a12", outline="")

    # trees
    for tx in range(0, w, 46):
        th = 50 + (tx * 7 % 5) * 14
        if tx < w * .3 or tx > w * .62:
            c.create_polygon(tx, h * .72, tx + 18, h * .72 - th, tx + 36, h * .72,
                             fill="#06100b", outline="")

    # prayer flags
    flag_colors = ["#3b6fd0", "#e8e8e8", "#c0392b", "#2e9e5b", "#e6c229"]
    for i in range(14):
        fx = w * .74 + i * (w * .26 / 14)
        fy = h * .53 + i * 4 + (3 if i % 2 else 0)
        c.create_rectangle(fx, fy, fx + 14, fy + 18, fill=flag_colors[i % 5], outline="")

    # corners + top/bottom knots
    corner(c, 14, 22, 1, 1)
    corner(c, w - 14, 22, -1, 1)
    corner(c, 14, h - 22, 1, -1)
    corner(c, w - 14, h - 22, -1, -1)
    for y in (22, h - 22):
        c.create_line(cx - 140, y, cx - 22, y, fill=GOLD_DIM)
        c.create_line(cx + 22, y, cx + 140, y, fill=GOLD_DIM)
        c.create_text(cx, y, text="❖", fill=GOLD, font=("Arial", 16))

    # centre content
    c.create_text(cx, h * .26, text="🐉", fill=GOLD, font=("Arial", 54))
    c.create_text(cx, h * .39, text="MythLab", fill=GOLD, font=("Georgia", 52))
    c.create_text(cx, h * .48, text="Explore. Learn. Believe.", fill=GOLD_LT, font=("Georgia", 17))
    c.create_line(cx - 160, h * .53, cx - 18, h * .53, fill=GOLD_DIM)
    c.create_line(cx + 18, h * .53, cx + 160, h * .53, fill=GOLD_DIM)
    c.create_text(cx, h * .53, text="❖", fill=GOLD, font=("Arial", 12))
    c.create_text(cx, h * .60,
                  text="Discover the myths, legends and mythical\ncreatures of Bhutan and beyond.",
                  fill=TEXT, font=("Georgia", 13), justify="center")

    canvas_button(c, cx, h * .72, 280, 56, "Get Started  →", True,
                  lambda: show_screen(signup_screen), "btn_start")
    canvas_button(c, cx, h * .80, 280, 46, "Login", False,
                  lambda: show_screen(login_screen), "btn_login")


welcome_canvas.bind("<Configure>", draw_welcome)


# ==========================================
# FORM CARD BUILDER
# ==========================================

def build_form_screen(title, subtitle):
    screen = tk.Frame(root, bg=BG)

    card = tk.Frame(screen, bg=CARD, highlightthickness=1, highlightbackground=GOLD)
    card.place(relx=0.5, rely=0.5, anchor="center")

    inner = tk.Frame(card, bg=CARD)
    inner.pack(padx=45, pady=24)

    tk.Label(inner, text="🐉", font=("Arial", 26), bg=CARD, fg=GOLD).pack()
    tk.Label(inner, text=title, font=("Georgia", 22), bg=CARD, fg=GOLD_LT).pack()
    tk.Label(inner, text=subtitle, font=("Arial", 10), bg=CARD, fg=LIGHT_TEXT).pack(pady=(0, 6))

    body = tk.Frame(inner, bg=CARD, width=360)
    body.pack(fill="x")
    return screen, inner, body


def gold_button(parent, text, command):
    return tk.Button(parent, text=text, font=("Arial", 12, "bold"),
                     bg=GOLD, fg="#2b1d05", activebackground=GOLD_LT,
                     relief="flat", cursor="hand2", pady=8, command=command)


def link_button(parent, text, command):
    return tk.Button(parent, text=text, font=("Arial", 10, "underline"),
                     bg=CARD, fg=GOLD, activebackground=CARD, activeforeground=GOLD_LT,
                     relief="flat", cursor="hand2", command=command)


# ==========================================
# CREATE ACCOUNT SCREEN
# ==========================================

signup_screen, signup_inner, signup_body = build_form_screen(
    "Create Account", "Join MythLab and start exploring."
)

f_name = FormField(signup_body, "Full name", check_name, ok_text="✓ Nice to meet you!")
f_email = FormField(signup_body, "Email", check_email, ok_text="✓ Email looks good")
f_user = FormField(signup_body, "Username", check_username, ok_text="✓ Username is available")
f_pass = FormField(signup_body, "Password", check_password,
                   secret=True, ok_text="✓ Strong password")
f_confirm = FormField(signup_body, "Confirm password", check_confirm,
                      secret=True, ok_text="✓ Passwords match")

# when the password changes, re-check the confirm box too
f_pass.entry.bind("<KeyRelease>",
                  lambda e: (f_pass.on_key(e),
                             f_confirm.validate() if f_confirm.get() else None))


# ---------- Terms checkbox ----------

terms_var = tk.IntVar()
terms_msg = tk.Label(signup_body, text="", font=("Arial", 9), bg=CARD, fg=ERROR, anchor="w")


def terms_changed():
    if terms_var.get():
        terms_msg.config(text="✓ Thanks for agreeing", fg=OK)
    else:
        terms_msg.config(text="✗ You must agree to the Terms of Use.", fg=ERROR)


tk.Checkbutton(
    signup_body, text="I agree to the Terms of Use", variable=terms_var,
    font=("Arial", 10), bg=CARD, fg=TEXT, selectcolor=FIELD,
    activebackground=CARD, activeforeground=GOLD,
    command=terms_changed
).pack(anchor="w", pady=(10, 0))
terms_msg.pack(fill="x")


# ---------- Create account ----------

def create_account():
    # run every validator (don't stop at the first failure)
    results = [f.validate() for f in (f_name, f_email, f_user, f_pass, f_confirm)]

    if not terms_var.get():
        terms_changed()
        results.append(False)

    if not all(results):
        messagebox.showerror("Create Account", "Please fix the fields marked in red.")
        return

    users = load_users()
    salt, hashed = hash_password(f_pass.get())
    users[f_user.get().strip().lower()] = {
        "name": f_name.get().strip(),
        "email": f_email.get().strip().lower(),
        "salt": salt,
        "password": hashed
    }
    save_users(users)

    messagebox.showinfo("Account created",
                        "Welcome to MythLab, " + f_name.get().strip().split()[0] + "!\nYou can now log in.")
    for f in (f_name, f_email, f_user, f_pass, f_confirm):
        f.clear()
    terms_var.set(0)
    terms_msg.config(text="")
    show_screen(login_screen)


gold_button(signup_body, "Create Account", create_account).pack(fill="x", pady=(8, 4))

bottom = tk.Frame(signup_body, bg=CARD)
bottom.pack()
tk.Label(bottom, text="Already have an account?", font=("Arial", 10),
         bg=CARD, fg=LIGHT_TEXT).pack(side="left")
link_button(bottom, "Login", lambda: show_screen(login_screen)).pack(side="left")
link_button(signup_body, "← Back", lambda: show_screen(welcome_screen)).pack()


# ==========================================
# LOGIN SCREEN
# ==========================================

login_screen, login_inner, login_body = build_form_screen(
    "Welcome Back", "Log in to continue your journey."
)

l_user = FormField(login_body, "Username",
                   lambda v: "" if v.strip() else "Username is required.", show_ok=False)
l_pass = FormField(login_body, "Password",
                   lambda v: "" if v else "Password is required.", secret=True, show_ok=False)

login_msg = tk.Label(login_body, text="", font=("Arial", 10), bg=CARD, fg=ERROR)
login_msg.pack(pady=(6, 0))


def login():
    login_msg.config(text="")
    ok_user = l_user.validate()
    ok_pass = l_pass.validate()
    if not (ok_user and ok_pass):
        return

    username = l_user.get().strip().lower()
    user = load_users().get(username)

    if user is None:
        login_msg.config(text="✗ Incorrect username or password.", fg=ERROR)
        return

    _, hashed = hash_password(l_pass.get(), user["salt"])
    if hashed != user["password"]:
        login_msg.config(text="✗ Incorrect username or password.", fg=ERROR)
        return

    # success -> go to the next page
    login_msg.config(text="✓ Login successful!", fg=OK)
    messagebox.showinfo("Login", "Welcome, " + user["name"] + "!")

    l_user.clear()
    l_pass.clear()
    login_msg.config(text="")

    open_home(username)


gold_button(login_body, "Login", login).pack(fill="x", pady=(8, 4))

bottom2 = tk.Frame(login_body, bg=CARD)
bottom2.pack()
tk.Label(bottom2, text="New to MythLab?", font=("Arial", 10),
         bg=CARD, fg=LIGHT_TEXT).pack(side="left")
link_button(bottom2, "Create account", lambda: show_screen(signup_screen)).pack(side="left")
link_button(login_body, "← Back", lambda: show_screen(welcome_screen)).pack()

root.bind("<Return>", lambda e: login() if login_screen.winfo_ismapped()
          else create_account() if signup_screen.winfo_ismapped() else None)


# ==========================================
# RUN
# ==========================================

show_screen(welcome_screen)
root.mainloop()