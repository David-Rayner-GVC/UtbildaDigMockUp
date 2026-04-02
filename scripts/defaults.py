from pathlib import Path
import json

# defaults here should be genericly-useful for harvesting 
# from different sites

# Get project root (two levels up from this file)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Key src directories
SRC_DIR = PROJECT_ROOT / "src"
SRC_DATA_DIR = SRC_DIR / "_data"
COURSES_DIR = SRC_DIR / "courses"
GENERATED_DIR = COURSES_DIR / "generated" / "scilifelab"
IMAGES_DIR = SRC_DIR / "images"

# Harvesting 
HARVEST_DATA  = PROJECT_ROOT / "scripts" / "_data"
TOPIC_MAPPINGS_FILE = HARVEST_DATA / "mappings.json"

# other useful
course_image = "generic_course.png"
