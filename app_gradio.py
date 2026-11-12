
import gradio as gr
from pathlib import Path
from myths import MYTHS, CATEGORIES, REGIONS

# ============================================================
# MYTHLAB - GRADIO APPLICATION
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent
IMAGE_DIR = PROJECT_DIR / "assets"

BG = "#061b2b"
CARD = "#102b3d"
GOLD = "#d6a84f"
TEXT = "#f5ead0"
LIGHT_TEXT = "#c7c1b3"

COLUMNS = 4
IMAGE_HEIGHT = 220

MAX_CARDS = max(
    COLUMNS,
    ((len(MYTHS) + COLUMNS - 1) // COLUMNS) * COLUMNS
)


# ============================================================
# FIND MYTH IMAGES
# ============================================================

def find_image(filename):

    extensions = [".png", ".jpg", ".jpeg", ".webp"]

    target = "".join(
        c.lower() for c in Path(filename).stem if c.isalnum()
    )

    possible_paths = [
        IMAGE_DIR / filename,
        PROJECT_DIR / filename
    ]

    for path in possible_paths:

        if path.exists() and path.is_file():
            return str(path)

    if IMAGE_DIR.exists():

        for item in IMAGE_DIR.iterdir():

            if not item.is_file():
                continue

            if item.suffix.lower() not in extensions:
                continue

            name = "".join(
                c.lower() for c in item.stem if c.isalnum()
            )

            if (
                name == target
                or name.startswith(target)
                or target.startswith(name)
            ):
                return str(item)

    return None


# ============================================================
# SEARCH AND FILTER MYTHS
# ============================================================

def search_myths(category, region, search):

    results = []

    for myth in MYTHS:

        myth_category, name, description, image, myth_region = myth

        # CATEGORY FILTER
        if category != "All" and myth_category != category:
            continue

        # REGION FILTER
        if region != "All" and myth_region != region:
            continue

        # SEARCH FILTER
        searchable = (
            myth_category + " " + name + " " + description
        ).lower()

        if search and search.lower().strip() not in searchable:
            continue

        # FIND IMAGE
        image_path = find_image(image)

        if image_path:

            results.append(
                (
                    image_path,
                    name,
                    myth_category,
                    myth_region,
                    description
                )
            )

    # CREATE CARD UPDATES

    updates = []

    for i in range(MAX_CARDS):

        if i < len(results):

            image_path, name, myth_category, myth_region, description = results[i]

            updates.extend([

                gr.update(visible=True),

                gr.update(value=image_path),

                gr.update(value=f"### {name}"),

                gr.update(
                    value=f"{myth_category} | {myth_region}"
                ),

                gr.update(value=description)

            ])

        else:

            updates.extend([

                gr.update(visible=False),

                gr.update(value=None),

                gr.update(value=""),

                gr.update(value=""),

                gr.update(value="")

            ])

    message = f"### Found {len(results)} matching stories."

    return (message, *updates)


# ============================================================
# CUSTOM CSS
# ============================================================

CUSTOM_CSS = """

/* MAIN BACKGROUND */

.gradio-container {
    background: #061b2b !important;
    color: #f5ead0 !important;
}

/* MAIN TITLE - LEFT SIDE */

#main-title {
    text-align: left !important;
    margin-left: 0 !important;
}

#main-title h1 {
    color: #d6a84f !important;
    font-size: 38px !important;
    font-weight: bold !important;
    text-align: left !important;
    margin-bottom: 8px !important;
}

#main-title h2 {
    color: #f5ead0 !important;
    font-size: 25px !important;
    text-align: left !important;
    margin-top: 5px !important;
}

/* GENERAL HEADINGS */

.gradio-container h1,
.gradio-container h2,
.gradio-container h3 {
    color: #f5ead0 !important;
}

/* NORMAL TEXT */

.gradio-container p {
    color: #c7c1b3 !important;
    line-height: 1.6 !important;
}

/* LABELS */

.gradio-container label,
.gradio-container label span {
    color: #d6a84f !important;
}

/* INPUT BOXES */

.gradio-container input,
.gradio-container textarea {
    background: #102b3d !important;
    color: #f5ead0 !important;
    border: 1px solid #755d2d !important;
}

/* PLACEHOLDER */

.gradio-container input::placeholder {
    color: #c7c1b3 !important;
}

/* DROPDOWN */

.gradio-container [role="listbox"],
.gradio-container [role="option"] {
    background: #102b3d !important;
    color: #f5ead0 !important;
}

/* SEARCH BUTTON */

#search-button {
    background: #d6a84f !important;
    color: #061b2b !important;
    font-weight: bold !important;
    border: none !important;
}

#search-button:hover {
    background: #e5c875 !important;
}

/* RESULT MESSAGE */

#result-message,
#result-message p,
#result-message h3 {
    color: #d6a84f !important;
}

/* MYTH CARD */

.myth-card {
    background: #102b3d !important;
    border: 1px solid #755d2d !important;
    border-radius: 12px !important;
    padding: 12px !important;
    overflow: hidden !important;
    min-width: 0 !important;
}

/* IMAGE CONTAINER */

.myth-image {
    width: 100% !important;
    height: 220px !important;
    min-height: 220px !important;
    max-height: 220px !important;
    background: #061b2b !important;
    border-radius: 9px !important;
    overflow: hidden !important;
}

/* FIT FULL IMAGE PROPERLY */

.myth-image img {
    width: 100% !important;
    height: 220px !important;
    max-height: 220px !important;
    object-fit: contain !important;
    object-position: center !important;
    display: block !important;
    background: #061b2b !important;
    border-radius: 9px !important;
}

/* MYTH NAME BELOW IMAGE */

.myth-name {
    width: 100% !important;
    margin-top: 10px !important;
    margin-bottom: 5px !important;
    text-align: left !important;
}

.myth-name h3 {
    color: #f5ead0 !important;
    font-size: 18px !important;
    font-weight: bold !important;
    text-align: left !important;
    line-height: 1.4 !important;
    margin: 0 !important;
}

/* CATEGORY AND REGION */

.myth-category {
    width: 100% !important;
    text-align: left !important;
    margin: 5px 0 !important;
}

.myth-category p {
    color: #d6a84f !important;
    font-size: 12px !important;
    font-weight: bold !important;
    text-align: left !important;
    line-height: 1.5 !important;
    margin: 0 !important;
}

/* DESCRIPTION BELOW CATEGORY */

.myth-description {
    width: 100% !important;
    text-align: left !important;
    margin-top: 8px !important;
}

.myth-description p {
    color: #c7c1b3 !important;
    font-size: 13px !important;
    text-align: left !important;
    line-height: 1.7 !important;
    margin: 0 !important;
}

/* CARD HOVER EFFECT */

.myth-card:hover {
    border-color: #d6a84f !important;
    transform: translateY(-3px);
    transition: 0.3s ease;
}

/* GENERAL BLOCKS */

.gradio-container .block {
    border-color: #755d2d !important;
}

/* SCROLLBAR */

* {
    scrollbar-color: #d6a84f #061b2b;
}

"""


# ============================================================
# GRADIO APPLICATION
# ============================================================

with gr.Blocks(
    title="MythLab"
) as app:

    # HEADER

    gr.Markdown(
        """
        # 🐉 MYTHLAB

        ## Discover the Myths
        """,
        elem_id="main-title"
    )

    gr.Markdown(
        "Explore ancient stories, guardian deities, legendary heroes "
        "and mysterious creatures from Bhutan and beyond."
    )

    gr.Markdown("---")

    # FILTERS

    with gr.Row():

        category = gr.Dropdown(
            choices=CATEGORIES,
            value="All",
            label="Category"
        )

        region = gr.Dropdown(
            choices=REGIONS,
            value="All",
            label="Region"
        )

    # SEARCH

    search = gr.Textbox(
        label="Search Myths",
        placeholder="Enter a myth name or keyword..."
    )

    search_button = gr.Button(
        "Search Stories",
        variant="primary",
        elem_id="search-button"
    )

    # RESULT MESSAGE

    message = gr.Markdown(
        elem_id="result-message"
    )

    gr.Markdown("---")

    # ========================================================
    # MYTH IMAGE CARDS
    # ========================================================

    card_outputs = []

    for row_number in range(0, MAX_CARDS, COLUMNS):

        with gr.Row():

            for column_number in range(COLUMNS):

                with gr.Column(
                    visible=False,
                    elem_classes=["myth-card"]
                ) as card:

                    # IMAGE

                    myth_image = gr.Image(
                        label=None,
                        show_label=False,
                        interactive=False,
                        height=IMAGE_HEIGHT,
                        container=False,
                        elem_classes=["myth-image"]
                    )

                    # MYTH NAME

                    myth_name = gr.Markdown(
                        elem_classes=["myth-name"]
                    )

                    # CATEGORY AND REGION

                    myth_category = gr.Markdown(
                        elem_classes=["myth-category"]
                    )

                    # DESCRIPTION

                    myth_description = gr.Markdown(
                        elem_classes=["myth-description"]
                    )

                card_outputs.extend([
                    card,
                    myth_image,
                    myth_name,
                    myth_category,
                    myth_description
                ])

    # ========================================================
    # BUTTON ACTIONS
    # ========================================================

    outputs = [message] + card_outputs

    search_button.click(
        fn=search_myths,
        inputs=[category, region, search],
        outputs=outputs
    )

    search.submit(
        fn=search_myths,
        inputs=[category, region, search],
        outputs=outputs
    )

    category.change(
        fn=search_myths,
        inputs=[category, region, search],
        outputs=outputs
    )

    region.change(
        fn=search_myths,
        inputs=[category, region, search],
        outputs=outputs
    )

    # LOAD STORIES AUTOMATICALLY

    app.load(
        fn=search_myths,
        inputs=[category, region, search],
        outputs=outputs
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.launch(
        server_port=7864,
        theme=gr.themes.Base(
            primary_hue="amber",
            secondary_hue="slate",
            neutral_hue="slate"
        ),
        css=CUSTOM_CSS
    )
