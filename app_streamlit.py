
import streamlit as st
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
from myths import MYTHS, CATEGORIES, REGIONS

# ============================================================
# MYTHLAB - STREAMLIT APPLICATION
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent
IMAGE_DIR = PROJECT_DIR / "assets"

BG = "#061b2b"
CARD = "#102b3d"
GOLD = "#d6a84f"
TEXT = "#f5ead0"
LIGHT_TEXT = "#c7c1b3"

COLUMNS = 4

# All images will have the same dimensions
IMAGE_WIDTH = 600
IMAGE_HEIGHT = 400


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MythLab",
    page_icon="🐉",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

CUSTOM_CSS = """

/* MAIN BACKGROUND */

.stApp {
    background-color: #061b2b;
    color: #f5ead0;
}

/* MAIN TITLE */

.main-title {
    color: #d6a84f;
    font-size: 40px;
    font-weight: bold;
    text-align: left;
    margin-bottom: 5px;
}

.subtitle {
    color: #f5ead0;
    font-size: 25px;
    text-align: left;
    margin-bottom: 12px;
}

/* GENERAL TEXT */

.stApp p {
    color: #c7c1b3;
    line-height: 1.6;
}

/* LABELS */

.stApp label {
    color: #d6a84f !important;
}

/* TEXT INPUT */

.stTextInput input {
    background-color: #102b3d;
    color: #f5ead0;
    border: 1px solid #755d2d;
}

/* DROPDOWN */

.stSelectbox div[data-baseweb="select"] {
    background-color: #102b3d;
    color: #f5ead0;
}

/* MYTH CARDS */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #102b3d;
    border: 1px solid #755d2d;
    border-radius: 12px;
    padding: 10px;
}

/* MYTH NAME */

.myth-name {
    color: #f5ead0;
    font-size: 18px;
    font-weight: bold;
    text-align: left;
    line-height: 1.4;
    margin-top: 10px;
    margin-bottom: 6px;
}

/* CATEGORY AND REGION */

.myth-category {
    color: #d6a84f;
    font-size: 12px;
    font-weight: bold;
    text-align: left;
    margin-bottom: 8px;
}

/* DESCRIPTION */

.myth-description {
    color: #c7c1b3;
    font-size: 13px;
    line-height: 1.7;
    text-align: left;
}

/* DIVIDER */

hr {
    border-color: #755d2d;
}

"""


st.markdown(
    f"<style>{CUSTOM_CSS}</style>",
    unsafe_allow_html=True
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
            return path

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
                return item

    return None


# ============================================================
# RESIZE IMAGES TO THE SAME SIZE
# ============================================================

@st.cache_data
def prepare_image(image_path):

    with Image.open(image_path) as original:

        # Correct image orientation
        image = ImageOps.exif_transpose(original)

        # Convert image to RGB
        image = image.convert("RGB")

        # Resize while maintaining original proportions
        image = ImageOps.contain(
            image,
            (IMAGE_WIDTH, IMAGE_HEIGHT),
            method=Image.Resampling.LANCZOS
        )

        # Create a fixed-size background
        background = Image.new(
            "RGB",
            (IMAGE_WIDTH, IMAGE_HEIGHT),
            BG
        )

        # Calculate center position
        x = (IMAGE_WIDTH - image.width) // 2
        y = (IMAGE_HEIGHT - image.height) // 2

        # Place image in the centre
        background.paste(image, (x, y))

        return background


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🐉 MYTHLAB</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Discover the Myths</div>',
    unsafe_allow_html=True
)

st.write(
    "Explore ancient stories, guardian deities, legendary heroes "
    "and mysterious creatures from Bhutan and beyond."
)

st.markdown("---")


# ============================================================
# SEARCH AND FILTERS
# ============================================================

st.subheader("Explore Mythology")

col1, col2 = st.columns(2)

category_options = ["All"] + [
    item for item in CATEGORIES if item != "All"
]

region_options = ["All"] + [
    item for item in REGIONS if item != "All"
]

with col1:

    category = st.selectbox(
        "Select Category",
        category_options
    )

with col2:

    region = st.selectbox(
        "Select Region",
        region_options
    )


search = st.text_input(
    "Search Myths",
    placeholder="Enter a myth name or keyword..."
)


# ============================================================
# SEARCH AND FILTER FUNCTION
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
            str(myth_category) + " " +
            str(name) + " " +
            str(description) + " " +
            str(myth_region)
        ).lower()

        if search and search.strip().lower() not in searchable:
            continue

        results.append(myth)

    return results


# ============================================================
# DISPLAY MYTH CARDS
# ============================================================

results = search_myths(
    category,
    region,
    search
)

st.markdown("---")

st.markdown(
    f"<h3 style='color:#d6a84f;'>Found {len(results)} matching stories</h3>",
    unsafe_allow_html=True
)


if results:

    # DISPLAY FOUR CARDS IN EACH ROW

    for start in range(0, len(results), COLUMNS):

        columns = st.columns(COLUMNS)

        row_results = results[start:start + COLUMNS]

        for col, myth in zip(columns, row_results):

            myth_category, name, description, image, myth_region = myth

            image_path = find_image(image)

            with col:

                with st.container(border=True):

                    # IMAGE

                    if image_path:

                        try:

                            display_image = prepare_image(
                                str(image_path)
                            )

                            st.image(
                                display_image,
                                use_container_width=True
                            )

                        except Exception:

                            st.warning(
                                "Unable to display this image."
                            )

                    else:

                        st.info("Image not available")

                    # MYTH NAME

                    st.markdown(
                        f'<div class="myth-name">{name}</div>',
                        unsafe_allow_html=True
                    )

                    # CATEGORY AND REGION

                    st.markdown(
                        f'<div class="myth-category">'
                        f'{myth_category} | {myth_region}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                    # DESCRIPTION

                    st.markdown(
                        f'<div class="myth-description">'
                        f'{description}'
                        f'</div>',
                        unsafe_allow_html=True
                    )

else:

    st.warning(
        "No matching myths found. Try another search or change the filters."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <p style="text-align:center; color:#d6a84f;">
        🐉 MythLab | Discover Stories, Explore Cultures
    </p>
    """,
    unsafe_allow_html=True
)
