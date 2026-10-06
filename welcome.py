import tkinter as tk

from tkinter import messagebox

import re

import os

import sys

import json

import hashlib

import subprocess

from PIL import Image, ImageTk





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

# NEXT PAGE

# ==========================================



NEXT_PAGE = "home.py"





# ==========================================

# USER STORAGE

# ==========================================



USERS_FILE = os.path.join(

    os.path.dirname(os.path.abspath(__file__)),

    "users.json"

)





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



    digest = hashlib.pbkdf2_hmac(

        "sha256",

        password.encode(),

        bytes.fromhex(salt),

        100_000

    )



    return salt, digest.hex()





# ==========================================

# VALIDATORS

# ==========================================



def check_name(v):

    if not v.strip():

        return "Full name is required."



    if not re.fullmatch(

        r"[A-Za-z][A-Za-z '\-]{1,48}",

        v.strip()

    ):

        return "Use letters only (at least 2 characters)."



    return ""





def check_email(v):

    if not v.strip():

        return "Email is required."



    if not re.fullmatch(

        r"[\w.+\-]+@[\w\-]+(\.[\w\-]+)+",

        v.strip()

    ):

        return "Enter a valid email, e.g. name@example.com."



    if v.strip().lower() in [

        u["email"] for u in load_users().values()

    ]:

        return "This email is already registered."



    return ""





def check_username(v):

    if not v.strip():

        return "Username is required."



    if not re.fullmatch(

        r"[A-Za-z0-9_]{4,15}",

        v.strip()

    ):

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

# FORM FIELD

# ==========================================



class FormField:



    def __init__(

        self,

        parent,

        label,

        validator,

        secret=False,

        ok_text="✓ Looks good",

        show_ok=True

    ):



        self.validator = validator

        self.ok_text = ok_text

        self.show_ok = show_ok



        frame = tk.Frame(

            parent,

            bg=CARD

        )



        frame.pack(

            fill="x",

            pady=(6, 0)

        )



        tk.Label(

            frame,

            text=label,

            font=("Arial", 10),

            bg=CARD,

            fg=LIGHT_TEXT

        ).pack(anchor="w")



        row = tk.Frame(

            frame,

            bg=CARD

        )



        row.pack(fill="x")



        self.var = tk.StringVar()



        self.entry = tk.Entry(

            row,

            textvariable=self.var,

            font=("Arial", 12),

            bg=FIELD,

            fg=TEXT,

            insertbackground=GOLD,

            relief="flat",

            show="•" if secret else "",

            highlightthickness=1,

            highlightbackground=GOLD_DIM,

            highlightcolor=GOLD

        )



        self.entry.pack(

            side="left",

            fill="x",

            expand=True,

            ipady=6

        )



        if secret:



            tk.Button(

                row,

                text="👁",

                font=("Arial", 10),

                bg=FIELD,

                fg=GOLD,

                activebackground=FIELD,

                activeforeground=GOLD_LT,

                relief="flat",

                cursor="hand2",

                command=self.toggle_show

            ).pack(

                side="left",

                padx=(4, 0),

                ipady=2

            )



        self.message = tk.Label(

            frame,

            text="",

            font=("Arial", 9),

            bg=CARD,

            fg=ERROR,

            anchor="w"

        )



        self.message.pack(fill="x")



        self.entry.bind(

            "<FocusOut>",

            lambda e: self.validate()

        )



        self.entry.bind(

            "<KeyRelease>",

            self.on_key

        )





    def on_key(self, event):



        if event.keysym in (

            "Tab",

            "ISO_Left_Tab",

            "Shift_L",

            "Shift_R"

        ):

            return



        self.validate()





    def toggle_show(self):



        self.entry.config(

            show="" if self.entry.cget("show") else "•"

        )





    def get(self):

        return self.var.get()





    def clear(self):



        self.var.set("")

        self.set_status("")





    def set_status(self, error):



        if error:



            self.message.config(

                text="✗ " + error,

                fg=ERROR

            )



            self.entry.config(

                highlightbackground=ERROR,

                highlightcolor=ERROR

            )



        elif self.show_ok and self.get():



            self.message.config(

                text=self.ok_text,

                fg=OK

            )



            self.entry.config(

                highlightbackground=OK,

                highlightcolor=OK

            )



        else:



            self.message.config(

                text="",

                fg=ERROR

            )



            self.entry.config(

                highlightbackground=GOLD_DIM,

                highlightcolor=GOLD

            )





    def validate(self):



        error = self.validator(

            self.get()

        )



        self.set_status(error)



        return error == ""





# ==========================================

# SCREEN SWITCHING

# ==========================================



def show_screen(screen):



    for s in (

        welcome_screen,

        signup_screen,

        login_screen

    ):

        s.pack_forget()



    screen.pack(

        fill="both",

        expand=True

    )





# ==========================================

# OPEN HOME

# ==========================================



def open_home(username):



    page_file = os.path.join(

        os.path.dirname(os.path.abspath(__file__)),

        NEXT_PAGE

    )



    if not os.path.exists(page_file):



        messagebox.showerror(

            "Page not found",

            NEXT_PAGE +

            " was not found in the same folder as welcome.py.\n\n"

            "Create it, or change NEXT_PAGE at the top of this file."

        )



        return



    root.destroy()



    subprocess.Popen([

        sys.executable,

        page_file,

        username

    ])





# ==========================================

# WELCOME SCREEN

# ==========================================



welcome_screen = tk.Frame(

    root,

    bg=BG

)



welcome_canvas = tk.Canvas(

    welcome_screen,

    bg=BG,

    highlightthickness=0

)



welcome_canvas.pack(

    fill="both",

    expand=True

)





# ==========================================

# BACKGROUND IMAGE

# ==========================================



BACKGROUND_FILE = os.path.join(

    os.path.dirname(os.path.abspath(__file__)),

    "welcome.png"

)



background_image = None





def draw_background():



    global background_image



    w = welcome_canvas.winfo_width()

    h = welcome_canvas.winfo_height()



    if w < 50 or h < 50:

        return



    try:



        image = Image.open(

            BACKGROUND_FILE

        )



        image = image.resize(

            (w, h),

            Image.LANCZOS

        )



        background_image = ImageTk.PhotoImage(

            image

        )



        welcome_canvas.create_image(

            0,

            0,

            image=background_image,

            anchor="nw",

            tags="background"

        )



    except Exception:



        welcome_canvas.create_rectangle(

            0,

            0,

            w,

            h,

            fill=BG,

            outline=""

        )





# ==========================================

# BUTTON

# ==========================================



def canvas_button(

    c,

    cx,

    cy,

    w,

    h,

    text,

    filled,

    command,

    tag

):



    x1 = cx - w / 2

    y1 = cy - h / 2

    x2 = cx + w / 2

    y2 = cy + h / 2



    r = h / 2



    pts = [

        x1 + r, y1,

        x2 - r, y1,

        x2, y1,

        x2, y2,

        x2 - r, y2,

        x1 + r, y2,

        x1, y2,

        x1, y1

    ]



    c.create_polygon(

        pts,

        smooth=True,

        tags=tag,

        fill=GOLD if filled else "#071b2b",

        outline=GOLD,

        width=2

    )



    c.create_text(

        cx,

        cy,

        text=text,

        tags=tag,

        fill="#2b1d05" if filled else GOLD_LT,

        font=("Georgia", 14)

    )



    c.tag_bind(

        tag,

        "<Enter>",

        lambda e: c.config(cursor="hand2")

    )



    c.tag_bind(

        tag,

        "<Leave>",

        lambda e: c.config(cursor="")

    )



    c.tag_bind(

        tag,

        "<Button-1>",

        lambda e: command()

    )





# ==========================================

# CORNER DESIGN

# ==========================================



def corner(c, x, y, sx, sy):



    c.create_line(

        x,

        y + sy * 110,

        x,

        y,

        x + sx * 150,

        y,

        fill=GOLD,

        width=1

    )



    c.create_oval(

        x + sx * 14,

        y + sy * 14,

        x + sx * 54,

        y + sy * 54,

        outline=GOLD,

        width=1

    )



    c.create_oval(

        x + sx * 24,

        y + sy * 24,

        x + sx * 44,

        y + sy * 44,

        outline=GOLD,

        width=1

    )





# ==========================================

# DRAW WELCOME

# ==========================================



def draw_welcome(event=None):



    c = welcome_canvas



    c.delete("all")



    w = c.winfo_width()

    h = c.winfo_height()



    if w < 50:

        return



    cx = w / 2



    # --------------------------------------

    # BACKGROUND IMAGE

    # --------------------------------------



    draw_background()



    # --------------------------------------

    # DARK OVERLAY

    # --------------------------------------



    c.create_rectangle(

        0,

        0,

        w,

        h,

        fill="#071b2b",

        stipple="gray50",

        outline=""

    )



    # --------------------------------------

    # DECORATION

    # --------------------------------------



    corner(c, 14, 22, 1, 1)

    corner(c, w - 14, 22, -1, 1)



    corner(c, 14, h - 22, 1, -1)

    corner(c, w - 14, h - 22, -1, -1)



    for y in (22, h - 22):



        c.create_line(

            cx - 140,

            y,

            cx - 22,

            y,

            fill=GOLD_DIM

        )



        c.create_line(

            cx + 22,

            y,

            cx + 140,

            y,

            fill=GOLD_DIM

        )



        c.create_text(

            cx,

            y,

            text="❖",

            fill=GOLD,

            font=("Arial", 16)

        )



    # --------------------------------------

    # MAIN CONTENT

    # --------------------------------------



    c.create_text(

        cx,

        h * .26,

        text="🐉",

        fill=GOLD,

        font=("Arial", 54)

    )



    c.create_text(

        cx,

        h * .39,

        text="MythLab",

        fill=GOLD,

        font=("Georgia", 52)

    )



    c.create_text(

        cx,

        h * .48,

        text="Explore. Learn. Believe.",

        fill=GOLD_LT,

        font=("Georgia", 17)

    )



    c.create_line(

        cx - 160,

        h * .53,

        cx - 18,

        h * .53,

        fill=GOLD_DIM

    )



    c.create_line(

        cx + 18,

        h * .53,

        cx + 160,

        h * .53,

        fill=GOLD_DIM

    )



    c.create_text(

        cx,

        h * .53,

        text="❖",

        fill=GOLD,

        font=("Arial", 12)

    )



    c.create_text(

        cx,

        h * .60,

        text="Discover the myths, legends and mythical\n"

             "creatures of Bhutan and beyond.",

        fill=TEXT,

        font=("Georgia", 13),

        justify="center"

    )



    # --------------------------------------

    # BUTTONS

    # --------------------------------------



    canvas_button(

        c,

        cx,

        h * .72,

        280,

        56,

        "Get Started  →",

        True,

        lambda: show_screen(signup_screen),

        "btn_start"

    )



    canvas_button(

        c,

        cx,

        h * .80,

        280,

        46,

        "Login",

        False,

        lambda: show_screen(login_screen),

        "btn_login"

    )





welcome_canvas.bind(

    "<Configure>",

    draw_welcome

)





# ==========================================

# FORM CARD BUILDER

# ==========================================



def build_form_screen(title, subtitle):



    screen = tk.Frame(

        root,

        bg=BG

    )



    card = tk.Frame(

        screen,

        bg=CARD,

        highlightthickness=1,

        highlightbackground=GOLD

    )



    card.place(

        relx=0.5,

        rely=0.5,

        anchor="center"

    )



    inner = tk.Frame(

        card,

        bg=CARD

    )



    inner.pack(

        padx=45,

        pady=24

    )



    tk.Label(

        inner,

        text="🐉",

        font=("Arial", 26),

        bg=CARD,

        fg=GOLD

    ).pack()



    tk.Label(

        inner,

        text=title,

        font=("Georgia", 22),

        bg=CARD,

        fg=GOLD_LT

    ).pack()



    tk.Label(

        inner,

        text=subtitle,

        font=("Arial", 10),

        bg=CARD,

        fg=LIGHT_TEXT

    ).pack(

        pady=(0, 6)

    )



    body = tk.Frame(

        inner,

        bg=CARD,

        width=360

    )



    body.pack(

        fill="x"

    )



    return screen, inner, body





# ==========================================

# BUTTONS

# ==========================================



def gold_button(parent, text, command):



    return tk.Button(

        parent,

        text=text,

        font=("Arial", 12, "bold"),

        bg=GOLD,

        fg="#2b1d05",

        activebackground=GOLD_LT,

        relief="flat",

        cursor="hand2",

        pady=8,

        command=command

    )





def link_button(parent, text, command):



    return tk.Button(

        parent,

        text=text,

        font=("Arial", 10, "underline"),

        bg=CARD,

        fg=GOLD,

        activebackground=CARD,

        activeforeground=GOLD_LT,

        relief="flat",

        cursor="hand2",

        command=command

    )





# ==========================================

# CREATE ACCOUNT

# ==========================================



signup_screen, signup_inner, signup_body = build_form_screen(

    "Create Account",

    "Join MythLab and start exploring."

)



f_name = FormField(

    signup_body,

    "Full name",

    check_name,

    ok_text="✓ Nice to meet you!"

)



f_email = FormField(

    signup_body,

    "Email",

    check_email,

    ok_text="✓ Email looks good"

)



f_user = FormField(

    signup_body,

    "Username",

    check_username,

    ok_text="✓ Username is available"

)



f_pass = FormField(

    signup_body,

    "Password",

    check_password,

    secret=True,

    ok_text="✓ Strong password"

)



f_confirm = FormField(

    signup_body,

    "Confirm password",

    check_confirm,

    secret=True,

    ok_text="✓ Passwords match"

)





f_pass.entry.bind(

    "<KeyRelease>",

    lambda e: (

        f_pass.on_key(e),

        f_confirm.validate() if f_confirm.get() else None

    )

)





# ==========================================

# TERMS

# ==========================================



terms_var = tk.IntVar()



terms_msg = tk.Label(

    signup_body,

    text="",

    font=("Arial", 9),

    bg=CARD,

    fg=ERROR,

    anchor="w"

)





def terms_changed():



    if terms_var.get():



        terms_msg.config(

            text="✓ Thanks for agreeing",

            fg=OK

        )



    else:



        terms_msg.config(

            text="✗ You must agree to the Terms of Use.",

            fg=ERROR

        )





tk.Checkbutton(

    signup_body,

    text="I agree to the Terms of Use",

    variable=terms_var,

    font=("Arial", 10),

    bg=CARD,

    fg=TEXT,

    selectcolor=FIELD,

    activebackground=CARD,

    activeforeground=GOLD,

    command=terms_changed

).pack(

    anchor="w",

    pady=(10, 0)

)



terms_msg.pack(

    fill="x"

)





# ==========================================

# CREATE ACCOUNT

# ==========================================



def create_account():



    results = [

        f.validate()

        for f in (

            f_name,

            f_email,

            f_user,

            f_pass,

            f_confirm

        )

    ]



    if not terms_var.get():



        terms_changed()

        results.append(False)



    if not all(results):



        messagebox.showerror(

            "Create Account",

            "Please fix the fields marked in red."

        )



        return



    users = load_users()



    salt, hashed = hash_password(

        f_pass.get()

    )



    users[f_user.get().strip().lower()] = {

        "name": f_name.get().strip(),

        "email": f_email.get().strip().lower(),

        "salt": salt,

        "password": hashed

    }



    save_users(users)



    messagebox.showinfo(

        "Account created",

        "Welcome to MythLab " +

        f_name.get().strip().split()[0] +

        "!\nYou can now log in."

    )



    for f in (

        f_name,

        f_email,

        f_user,

        f_pass,

        f_confirm

    ):

        f.clear()



    terms_var.set(0)

    terms_msg.config(text="")



    show_screen(login_screen)





gold_button(

    signup_body,

    "Create Account",

    create_account

).pack(

    fill="x",

    pady=(8, 4)

)





bottom = tk.Frame(

    signup_body,

    bg=CARD

)



bottom.pack()



tk.Label(

    bottom,

    text="Already have an account?",

    font=("Arial", 10),

    bg=CARD,

    fg=LIGHT_TEXT

).pack(side="left")



link_button(

    bottom,

    "Login",

    lambda: show_screen(login_screen)

).pack(side="left")





link_button(

    signup_body,

    "← Back",

    lambda: show_screen(welcome_screen)

).pack()





# ==========================================

# LOGIN SCREEN

# ==========================================



login_screen, login_inner, login_body = build_form_screen(

    "Welcome Back",

    "Log in to continue your journey."

)





l_user = FormField(

    login_body,

    "Username",

    lambda v: "" if v.strip()

    else "Username is required.",

    show_ok=False

)



l_pass = FormField(

    login_body,

    "Password",

    lambda v: "" if v

    else "Password is required.",

    secret=True,

    show_ok=False

)





login_msg = tk.Label(

    login_body,

    text="",

    font=("Arial", 10),

    bg=CARD,

    fg=ERROR

)



login_msg.pack(

    pady=(6, 0)

)





# ==========================================

# LOGIN

# ==========================================



def login():



    login_msg.config(text="")



    ok_user = l_user.validate()

    ok_pass = l_pass.validate()



    if not (ok_user and ok_pass):

        return



    username = l_user.get().strip().lower()



    user = load_users().get(username)



    if user is None:



        login_msg.config(

            text="✗ Incorrect username or password.",

            fg=ERROR

        )



        return



    _, hashed = hash_password(

        l_pass.get(),

        user["salt"]

    )



    if hashed != user["password"]:



        login_msg.config(

            text="✗ Incorrect username or password.",

            fg=ERROR

        )



        return



    login_msg.config(

        text="✓ Login successful!",

        fg=OK

    )



    messagebox.showinfo(

        "Login",

        "Welcome, " + user["name"] + "!"

    )



    l_user.clear()

    l_pass.clear()



    login_msg.config(text="")



    open_home(username)





gold_button(

    login_body,

    "Login",

    login

).pack(

    fill="x",

    pady=(8, 4)

)





bottom2 = tk.Frame(

    login_body,

    bg=CARD

)



bottom2.pack()



tk.Label(

    bottom2,

    text="New to MythLab?",

    font=("Arial", 10),

    bg=CARD,

    fg=LIGHT_TEXT

).pack(side="left")



link_button(

    bottom2,

    "Create account",

    lambda: show_screen(signup_screen)

).pack(side="left")





link_button(

    login_body,

    "← Back",

    lambda: show_screen(welcome_screen)

).pack()





# ==========================================

# ENTER KEY

# ==========================================



root.bind(

    "<Return>",

    lambda e:

    login()

    if login_screen.winfo_ismapped()

    else create_account()

    if signup_screen.winfo_ismapped()

    else None

)





# ==========================================

# RUN

# ==========================================



show_screen(welcome_screen)



root.mainloop()