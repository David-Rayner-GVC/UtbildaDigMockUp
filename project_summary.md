# Project Summary: Eleventy Course Catalog Demo (Updated with Harvesting and UI Navigation Changes)

## Goal

Build a **static, collaborative course catalog** using:

* YAML-based course and topic metadata
* Eleventy (11ty) for site generation
* GitHub Pages for free hosting and collaboration
* External course ingestion via API

The catalog is designed to support both overview browsing and topic-focused exploration, with course content displayed in a way that keeps users oriented within a topic.

---

## Current Architecture

### Tech stack

* **Eleventy (11ty)** static site generator
* **Node.js / npm**
* **GitHub Pages via GitHub Actions**
* **Python** for harvesting and transforming external course data

Templates:

* `.md` -> Markdown + Liquid
* `.njk` -> Nunjucks

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
      SciLifeLab/            # generated courses

    _data/
      topics.yml

    images/
      *.jpg / *.jpeg / *.png

    _includes/
      base.njk
      course.njk

  scripts/
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

Current topic metadata includes:

* `id` -> stable internal identifier
* `name` -> display name
* `visible` -> controls whether topic appears in catalog
* optional descriptive metadata such as summary/image where used by templates

Example:

```yaml
- id: fair-data
  name: FAIR Data
  visible: true
```

Ordering is now defined by file position rather than a separate `order` field.

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

Catalog content now includes both:

* manually curated courses
* automatically harvested courses in provider-specific subfolders

---

## Harvesting Pipeline

### Overview

External course data (currently from SciLifeLab) is:

1. **Fetched** from a JSON API
2. **Transformed** into the internal course schema
3. **Enriched** through topic mapping and image handling
4. **Written** as Markdown files into:

   ```text
   src/courses/SciLifeLab/
   ```
5. Included automatically in the Eleventy build

---

### Pipeline Steps

#### 1. `fetch_courses`

* Uses `requests`
* Retrieves JSON from the API endpoint
* Keeps fetching separate from transformation

#### 2. `transform_course`

* Maps API fields to Eleventy front matter
* Normalizes text (for example line endings)
* Extracts:

  * title
  * provider(s)
  * summary
  * level
  * homepage
* Uses **TopicMapper** to map keywords to internal topic IDs

Courses without mapped topics are filtered out.

#### 3. Topic Mapping

Mapping defined in:

```text
scripts/mappings.json
```

Example structure:

```json
{
  "id": "fair-data",
  "terms": ["FAIR", "data sharing"]
}
```

Handled by a Python class that:

* loads the mapping file
* matches keywords case-insensitively
* returns one or more topic IDs

#### 4. Image Handling

* Checks whether an image already exists locally in `src/images/`
* Downloads if missing
* Avoids repeated downloads in later builds

#### 5. `write_course`

* Writes `.md` files with YAML front matter
* Preserves consistent key ordering
* Uses `yaml.dump(..., sort_keys=False)`
* Outputs generated files into provider-specific course folders

---

## Build Integration

GitHub Actions workflow:

1. Checkout repository
2. Set up Python
3. Run harvesting script
4. Run Eleventy build
5. Deploy `_site/`

---

## Collections

### Topics collection

The topics collection:

* reads `topics.yml`
* filters on `visible`
* matches courses by topic ID
* includes both manual and harvested content

This lets all topic-driven views work off the same underlying course collection.

---

## Front-End Views

### 1. All-topics / all-courses overview page (`topics.md`)

This page shows **all topics**, each followed by a compact set of course cards.

Recent UI changes:

* each course card now acts as a single click target
* clicking a course card links to the corresponding course section on the topic page
* the card no longer links directly to the standalone course page
* the course title is now presented as bold text rather than as a homepage link
* inner scroll behavior has been removed from the compact cards
* images remain on their own row at the top of the card and are left-aligned within their image area

This overview page now works primarily as a navigation layer into the fuller topic-specific descriptions.

### 2. Topic overview page / topic detail pages (`topic-cards-page.njk` / `topic-pages.njk`)

All topics are listed in an overview pages as cards, with click-though to a pages with all courses for that topic. Each topic then has its own generated page showing:

* topic title
* topic summary/image where available
* all courses tagged with that topic

Recent UI changes:

* course cards start at a fixed collapsed height
* if content overflows, a **Show more / Show less** control appears
* cards expand inline rather than creating an inner scroll region
* each course card has a stable anchor ID based on the course slug
* if a user arrives via a hash link from the overview page, the corresponding course card expands automatically

This means users can browse the all-courses page, click a compact course card, and land directly on the expanded course description within the topic context.

---

## Navigation Pattern

A key recent change is the shift from page-to-page navigation toward **context-preserving in-page navigation**.

### Previous behavior

* course cards in `topics.md` linked to individual course pages or mixed destinations
* some cards relied on inner scrolling to expose longer content

### Current behavior

* compact course cards in `topics.md` link to anchored course sections in the corresponding topic page
* destination URLs follow the pattern:

  ```text
  /topics/<topic-slug>/#course-<course-slug>
  ```
* the matching course card on the topic page expands automatically on arrival

Benefits:

* users stay oriented within a topic
* navigation is more intuitive
* no nested scrolling regions inside cards
* overview cards remain compact while full descriptions stay accessible

---

## Key Features

### 1. Hybrid course system

* manually curated and harvested courses coexist
* both use the same schema and templates

### 2. External data ingestion

* API-driven course updates
* no manual duplication of source data
* clear separation between source data and transformed site content

### 3. Topic mapping layer

* decouples provider vocabulary from internal taxonomy
* makes it easier to support additional providers later

### 4. Image caching

* avoids repeated downloads
* keeps static assets local

### 5. Topic-centered navigation

* overview cards route into topic pages
* expanded course descriptions are available in context
* interaction is simpler than hover-based or scroll-within-card approaches

---

## GitHub Pages / Eleventy Setup

Important Eleventy configuration:

```js
eleventyConfig.setUseGitIgnore(false);
```

This allows:

* Git to ignore generated files from the python script
* Eleventy to still process them as source content

---

## Key Lessons / Gotchas

### 1. `.gitignore` can affect Eleventy builds

* ignored files may disappear from Eleventy input processing
* this has to be disabled explicitly when generated content should still be built

### 2. Separate responsibilities in the harvesting pipeline

* fetch != transform != write
* downloads and other side effects are easier to manage when isolated

### 3. Stable identifiers matter

Use IDs and slugs rather than display titles for:

* filenames
* anchors
* topic references
* generated links between views

### 4. Normalize external data early

Examples:

* line endings
* provider lists
* missing fields
* formatting inconsistencies in summaries

### 5. UI patterns should avoid nested scroll regions

Inner scroll inside cards created a poor browsing experience.
The current approach is:

* compact cards for overview
* explicit expansion on topic pages
* direct linking to anchored expanded content

### 6. Clickable card design needs valid HTML structure

Making a whole card clickable works best when handled carefully, especially when rendered summary content may itself contain links. This affects both usability and layout stability.

---

## Current Status

Working:

* local development (`npm start`)
* production build and deploy
* topic system with visibility control
* external harvesting pipeline
* topic mapping
* image downloading and caching
* generated courses integrated into collections
* topic overview cards linking into topic detail pages
* automatic expansion of linked course cards on topic pages
* removal of inner-scroll behavior from overview cards

---

## Next Steps

### High impact

* filtering by topic, level, and provider
* search
* refine layout for the compact card overview

### Medium

* improve homepage
* handle missing images gracefully
* decide whether standalone course pages are still needed as a primary navigation route

### Longer-term

* support multiple providers
* scheduled harvesting
* contribution workflow
* smarter topic matching (fuzzy matching / NLP)

---

## One-line description

> Static course catalog built with Eleventy, combining manually curated and automatically harvested courses through a Python ingestion pipeline, with YAML-driven topics, topic-centered navigation, and GitHub Pages deployment.

---
