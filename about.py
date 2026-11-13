"""MythLab About page. Replace your existing about.py with this file."""
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageDraw

BG = '#061b2b'
CARD = '#0d293a'
CARD_ALT = '#102f42'
GOLD = '#d6a84f'
GOLD_LIGHT = '#efce86'
TEXT = '#f5ead0'
MUTED = '#bac8d0'
BORDER = '#315064'
PROJECT_DIR = Path(__file__).resolve().parent
IMAGE_DIRS = [PROJECT_DIR / 'assets', PROJECT_DIR / 'images', PROJECT_DIR]


def find_image(name):
    for folder in IMAGE_DIRS:
        path = folder / name
        if path.is_file():
            return path
    return None


def label(parent, text, size=11, color=TEXT, bold=False, font='Arial', **kwargs):
    return tk.Label(parent, text=text, bg=kwargs.pop('bg', parent.cget('bg')),
                    fg=color, font=(font, size, 'bold' if bold else 'normal'),
                    justify='left', anchor='w', **kwargs)


def section(parent, heading, number=None):
    wrapper = tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
    header = tk.Frame(wrapper, bg=CARD)
    header.pack(fill='x', padx=23, pady=(21, 12))
    if number:
        label(header, number, 10, GOLD, True, bg=CARD).pack(side='left', padx=(0, 12))
    label(header, heading, 18, GOLD_LIGHT, True, 'Georgia', bg=CARD).pack(side='left')
    tk.Frame(wrapper, bg=BORDER, height=1).pack(fill='x', padx=23)
    return wrapper


def paragraph(parent, text, width=600):
    item = label(parent, text, 11, MUTED, wraplength=width, bg=CARD)
    item.pack(anchor='w', fill='x', padx=23, pady=(15, 22))
    return item


def show_about(parent):
    for widget in parent.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(parent, bg=BG, highlightthickness=0)
    scrollbar = tk.Scrollbar(parent, orient='vertical', command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')
    canvas.pack(side='left', fill='both', expand=True)
    content = tk.Frame(canvas, bg=BG)
    window = canvas.create_window((0, 0), window=content, anchor='nw')
    content.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    canvas.bind('<Configure>', lambda e: canvas.itemconfigure(window, width=e.width))

    def wheel(event):
        if event.delta:
            canvas.yview_scroll(-1 if event.delta > 0 else 1, 'units')
    def bind_wheel(event):
        canvas.bind_all('<MouseWheel>', wheel)
    def unbind_wheel(event):
        canvas.unbind_all('<MouseWheel>')
    canvas.bind('<Enter>', bind_wheel)
    canvas.bind('<Leave>', unbind_wheel)

    page = tk.Frame(content, bg=BG)
    page.pack(fill='both', expand=True, padx=32, pady=(25, 36))

    # Hero uses banner.jpg if present; a designed gradient otherwise.
    hero = tk.Canvas(page, height=245, bg='#112e40', highlightthickness=0)
    hero.pack(fill='x', pady=(0, 24))
    hero.photo = None
    def draw_hero(event=None):
        w = max(hero.winfo_width(), 350)
        h = 245
        path = find_image('banner.jpg') or find_image('welcome.png')
        if path:
            try:
                im = ImageOps.fit(Image.open(path).convert('RGB'), (w, h), method=Image.Resampling.LANCZOS)
                im = ImageEnhance.Brightness(im).enhance(.56)
            except Exception:
                path = None
        if not path:
            im = Image.new('RGB', (w, h))
            pixels = im.load()
            for y in range(h):
                for x in range(w):
                    t = x / max(w, 1)
                    pixels[x, y] = (int(7 + 10*t), int(30 + 25*t), int(47 + 24*t))
        # Dark left overlay for legible typography.
        overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        for x in range(w):
            alpha = int(125 * (1 - x / w))
            draw.line([(x, 0), (x, h)], fill=(3, 15, 25, alpha))
        im = Image.alpha_composite(im.convert('RGBA'), overlay).convert('RGB')
        hero.photo = ImageTk.PhotoImage(im)
        hero.delete('all')
        hero.create_image(0, 0, image=hero.photo, anchor='nw')
        hero.create_text(35, 38, text='THE WORLD OF MYTHLAB', fill=GOLD_LIGHT,
                         font=('Arial', 10, 'bold'), anchor='w')
        hero.create_text(35, 92, text='Stories that connect us', fill=TEXT,
                         font=('Georgia', 29, 'bold'), anchor='w')
        hero.create_text(35, 140, text='Explore the legends, cultural traditions and mythical beings\n'
                                         'of Bhutan and beyond.', fill='#e1e7e9',
                         font=('Arial', 12), anchor='nw', width=max(250, w-75))
        hero.create_line(35, 205, min(w-35, 245), 205, fill=GOLD, width=3)
    hero.bind('<Configure>', draw_hero)

    intro = tk.Frame(page, bg=BG)
    intro.pack(fill='x', pady=(0, 24))
    label(intro, 'ABOUT MYTHLAB', 10, GOLD, True).pack(anchor='w', pady=(0, 8))
    label(intro, 'Preserving stories. Inspiring curiosity.', 23, TEXT, True, 'Georgia').pack(anchor='w')
    label(intro,
          'MythLab is a digital space for discovering myths, legends and mythical creatures. '
          'With a special focus on Bhutanese cultural heritage, it brings together stories '
          'from different regions and traditions in an engaging and accessible way.',
          12, MUTED, wraplength=850).pack(anchor='w', fill='x', pady=(11, 0))

    # Two-column arrangement with proportionate content.
    columns = tk.Frame(page, bg=BG)
    columns.pack(fill='x')
    columns.columnconfigure(0, weight=3, uniform='about')
    columns.columnconfigure(1, weight=2, uniform='about')
    left = tk.Frame(columns, bg=BG)
    right = tk.Frame(columns, bg=BG)
    left.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
    right.grid(row=0, column=1, sticky='nsew', padx=(10, 0))

    purpose = section(left, 'Our Purpose', '01')
    purpose.pack(fill='x', pady=(0, 18))
    paragraph(purpose,
              'Our purpose is to make traditional stories easier to discover and appreciate. '
              'Through MythLab, readers can learn about guardian deities, legendary heroes, '
              'folk tales and mysterious creatures while exploring the cultural values and '
              'beliefs associated with them.', 510)

    inspiration = section(left, 'Our Inspiration', '02')
    inspiration.pack(fill='x', pady=(0, 18))
    paragraph(inspiration,
              'Bhutan is rich in oral traditions, sacred places and stories passed down through '
              'generations. These traditions inspired MythLab. We believe that presenting '
              'stories in a digital format can encourage younger readers to explore their '
              'heritage and discover connections with stories from other cultures.', 510)

    journey = section(left, 'What You Can Discover', '03')
    journey.pack(fill='x')
    paragraph(journey,
              'Explore Bhutanese myths and legends, learn about mythical creatures, discover '
              'stories linked to different regions, save your favourites, complete learning '
              'tasks and test your knowledge through quizzes.', 510)

    features = section(right, 'Explore MythLab', '✦')
    features.pack(fill='x')
    items = [
        ('01', 'Myths', 'Read stories of deities, heroes and local traditions.'),
        ('02', 'Creatures', 'Meet legendary beings and explore their cultural meanings.'),
        ('03', 'Regions', 'Discover stories connected with Bhutan’s 20 dzongkhags.'),
        ('04', 'My Tasks', 'Complete activities and follow your learning.'),
        ('05', 'Quiz', 'Challenge yourself with questions about the stories.'),
        ('06', 'Favourites', 'Keep the stories you want to revisit.'),
    ]
    for index, (num, title, description) in enumerate(items):
        item = tk.Frame(features, bg=CARD)
        item.pack(fill='x', padx=22, pady=(13, 4 if index < len(items)-1 else 20))
        tk.Label(item, text=num, bg=CARD_ALT, fg=GOLD, font=('Arial', 10, 'bold'),
                 width=3, height=2).pack(side='left', anchor='n', padx=(0, 12))
        details = tk.Frame(item, bg=CARD)
        details.pack(side='left', fill='x', expand=True)
        label(details, title, 11, TEXT, True, bg=CARD).pack(anchor='w')
        label(details, description, 9, MUTED, wraplength=225, bg=CARD).pack(anchor='w', pady=(3, 0))

    footer = tk.Frame(page, bg=BG)
    footer.pack(fill='x', pady=(28, 0))
    tk.Frame(footer, bg=BORDER, height=1).pack(fill='x', pady=(0, 19))
    label(footer, 'Every legend has a story worth discovering.', 17, GOLD_LIGHT,
          False, 'Georgia').pack(anchor='center')
    label(footer, 'Thank you for exploring MythLab.', 10, MUTED).pack(anchor='center', pady=(8, 0))
    label(footer, 'MYTHLAB  •  VERSION 1.0', 9, GOLD).pack(anchor='center', pady=(13, 0))

    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'))


if __name__ == '__main__':
    root = tk.Tk()
    root.title('MythLab — About')
    root.geometry('1100x850')
    show_about(root)
    root.mainloop()
