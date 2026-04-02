import defaults
from TopicMapper import *
import requests
import json

import os
from urllib.parse import urlparse

import yaml

HARVEST_URL = "https://training.scilifelab.se/events.json"
USE_PROVIDER = -1



def clean_text(text):
    if not isinstance(text, str):
        return text
    return text.replace("\r\n", "\n").replace("\r", "\n").strip()

def ensure_image(raw):
    # raw is raw json
    # which provider to use? 

    try:
      image_name = raw["content_providers"][USE_PROVIDER]["image_file_name"]
    except:
      return defaults.course_image

    filepath = defaults.IMAGES_DIR / image_name
    if filepath.exists():
        return image_name

    id = str(raw["content_providers"][USE_PROVIDER]["id"])
    
    image_url = "https://training.scilifelab.se/system/content_providers/images/000/000/" + \
    id.zfill(3) + "/original/" + image_name

    response = requests.get(image_url, timeout=10)
    try:
      response.raise_for_status()
    except:
      return defaults.course_image

    with open(filepath, "wb") as f:
        f.write(response.content)

    return image_name

def fetch_courses(url):
  # Get the 
  response = requests.get(url)
  response.raise_for_status()
  return response.json()

def transform_course(harvest_data):
    mapper = TopicMapper(defaults.TOPIC_MAPPINGS_FILE)

    course_data = {}
    course_data["topics"] = mapper.map(harvest_data["keywords"])
    course_data["title"] = harvest_data["title"]

    providers = harvest_data.get("content_providers", [])

    course_data["provider"] = ", ".join(
        p.get("title", "").strip()
        for p in providers
        if p.get("title")
    )

    target_audience = harvest_data.get("target_audience", [])

    course_data["level"] = ", ".join(
        t.strip()
        for t in target_audience
    )

    course_data["summary"] = clean_text(harvest_data["description"])

    course_data["permalink"] = "/courses/" + harvest_data["slug"] + "/"

    course_data["homepage"] = harvest_data["url"]

    return course_data, harvest_data["slug"]

def write_course(course, filepath):
    course["layout"]="course.njk"
    course["tags"]="courses"

    key_order = [
        'layout',
        'tags',
        'title',
        'image',
        'provider',
        'level',
        'topics',
        'summary',
        'permalink',
        'homepage',
    ]

    ordered_course = {key: course[key] for key in key_order if key in course}
    ordered_course.update({key: value for key, value in course.items() if key not in ordered_course})

    txt = yaml.dump(
        ordered_course,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False
    )   

    txt = "\n".join(("---",txt.rstrip(),"---","","Harvested from SciLifeLab\n"))

    with open(filepath, "w") as f:
       f.write(txt)
  
def main():
    raw_courses = fetch_courses(HARVEST_URL)

    transformed = []

    for raw in raw_courses:
        course, slug = transform_course(raw)

        if not course.get("topics"):
            continue
        
        #course["image"] = ensure_image(raw)
        course["image"] = "SciLifeLab_Logotype_Green.png"

        transformed.append(course)

        filename = slug + ".md"
        filepath = defaults.COURSES_DIR / filename
        write_course(course, filepath)

if __name__ == "__main__":
    main()
