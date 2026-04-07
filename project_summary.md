# Project Summary: Eleventy Course Catalog Demo (Updated with Harvesting)

## Goal

Build a **static, collaborative course catalog** using:

* YAML-based course and topic metadata
* Eleventy (11ty) for site generation
* GitHub Pages for free hosting and collaboration
* External course ingestion via API (NEW)

---

## Current Architecture

### Tech stack

* **Eleventy (11ty)** static site generator
* **Node.js / npm**
* **GitHub Pages via GitHub Actions**
* **Python (NEW)** for harvesting and transforming external course data

Templates:

* `.md` → Markdown + Liquid
* `.njk` → Nunjucks

---

## Project Structure

```text
project-root/
  src/
    index.md
    topics.md
    topic-cards-page.njk
    topic-pages.njk
    courses.md               # only used for troubleshooting

    courses/
      *.md                   # manually curated courses
      SciLifeLab/            # generated courses (NEW)

    _data/
      topics.yml

    images/
      *.jpg / *.jpeg / *.png

    _includes/
      base.njk
      course.njk

  scripts/                  # NEW
    import_scilifelab.py
    TopicMapper.py
    defaults.py

    _data/
      mappings.json

  .eleventy.js
  package.json
  .github/workflows/deploy.yml
```

---

## Data Model

### Topics

Defined in:

```text
src/_data/topics.yml
```

Changes:

* `order` field removed → ordering now defined by file position
* `visible` field added → controls whether topic appears in catalog

```yaml
- id: fair-data
  name: FAIR Data
  visible: true
```

---

### Courses

Still one file per course:

```yaml
---
layout: course.njk
tags: courses
title: ...
provider: ...
level: ...
topics:
  - fair-data
summary: |
  ...
image: filename.jpg
homepage: https://...
permalink: /courses/course-slug/
---
```

Now includes both:

* manually curated courses
* automatically harvested courses (NEW) in subfolders

---

## NEW: Harvesting Pipeline

### Overview

External course data (currently from SciLifeLab) is:

1. **Fetched** from a JSON API
2. **Transformed** into the internal course schema
3. **Enriched** (topics mapped, images can be downloaded, though not currently used)
4. **Written** as Markdown files into:

   ```text
   src/courses/SciLifeLab/
   ```
5. Included automatically in Eleventy build

---

### Pipeline Steps

#### 1. fetch_courses

* Uses `requests`
* Retrieves JSON from API endpoint
* Minimal logic (no transformation)

#### 2. transform_course

* Maps API fields → Eleventy front matter
* Normalizes text (e.g. line endings)
* Extracts:

  * title
  * provider(s)
  * summary
  * level
  * homepage
* Uses **TopicMapper** to map keywords → topic IDs

Courses without mapped topics are filtered out

---

#### 3. Topic Mapping (NEW)

Mapping defined in:

```text
scripts/mappings.json
```

Structure:

```json
{
  "id": "fair-data",
  "terms": ["FAIR", "data sharing"]
}
```

Handled by a Python class:

* Loads mapping file
* Matches keywords (case-insensitive)
* Returns list of topic IDs

---

#### 4. Image Handling (NEW)

* Checks if image exists locally (`src/images/`)
* Downloads if missing
* Avoids re-downloading on subsequent builds

---

#### 5. write_course

* Writes `.md` files with YAML front matter
* Ensures consistent key ordering
* Uses `yaml.dump(..., sort_keys=False)`
* Outputs to:

  ```text
  src/courses/SciLifeLab/
  ```

---

### Build Integration

GitHub Actions workflow:

1. Checkout repo
2. Setup Python
3. Run harvesting script
4. Run Eleventy build
5. Deploy `_site/`

---

## Collections

### Topics collection

* Reads `topics.yml`
* Filters on `visible`
* Matches courses by topic ID
* Includes both manual and harvested courses

---

## Key Features (Updated)

### 1. Hybrid course system

* Manual + auto-generated courses coexist
* Same schema and templates

---

### 2. External data ingestion

* API-driven content updates
* No manual duplication
* Clean separation between:

  * source data
  * transformed content

---

### 3. Topic mapping layer

* Decouples external vocabularies from internal taxonomy
* Easily extensible for new providers

---

### 4. Image caching (not currently used)

* Avoids repeated downloads
* Keeps static assets local

---

## GitHub Pages Setup

### Important update

Eleventy now ignores `.gitignore`:

```js
eleventyConfig.setUseGitIgnore(false);
```

This allows:

* Git to ignore generated files
* Eleventy to still process them

---

## Key Lessons / Gotchas (Updated)

### 1. Git ignore affects Eleventy

* `.gitignore` can hide source files from Eleventy
* Must disable via config when generating content

---

### 2. Separate pipeline responsibilities

* Fetch ≠ transform ≠ write
* Keep side effects (downloads) isolated

---

### 3. Stable identifiers matter

* Use IDs (not titles) for:

  * slugs
  * filenames
  * topic references

---

### 4. Normalize external data early

* Line endings
* provider lists
* missing fields

---

### 5. Filter aggressively

* Exclude courses without valid topic mappings
* Keeps catalog clean

---

## Current Status

Working:

* Local dev (`npm start`)
* Production build + deploy
* Topic system with visibility control
* External harvesting pipeline
* Topic mapping
* Image downloading + caching
* Generated courses integrated into collections

---

## Next Steps (Updated)

### High impact

* Filtering (topic, level, provider)
* Search

### Medium

* Improve homepage
* Handle missing images gracefully

### Longer-term

* Support multiple providers
* Scheduled harvesting
* Contribution workflow
* Smarter topic matching (fuzzy / NLP)

---

## One-line description

> Static course catalog built with Eleventy, combining manually curated and automatically harvested courses via a Python ingestion pipeline, with YAML-driven topics and GitHub Pages deployment.

---

