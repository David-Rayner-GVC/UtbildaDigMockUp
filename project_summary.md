# Project Summary: Eleventy Course Catalog Demo (Updated)

## Goal

Build a **static, collaborative course catalog** using:

- YAML-based course and topic metadata
- Eleventy (11ty) for site generation
- GitHub Pages for free hosting and collaboration

---

## Current Architecture

### Tech stack

- **Eleventy (11ty)** static site generator
- **Node.js / npm**
- **GitHub Pages via GitHub Actions**

Templates:

- `.md` → Markdown + Liquid
- `.njk` → Nunjucks

---

## Project Structure

```text
project-root/
  src/
    index.md
    topics.md                # topic → course view
    topic-cards-page.njk     # topic card overview (new entry point)
    topic-pages.njk          # one page per topic

    courses/
      *.md                   # one file per course (YAML front matter)

    _data/
      topics.yml             # central topic definitions (NEW)

    images/
      *.jpg / *.jpeg

    _includes/
      base.njk
      course.njk

  .eleventy.js
  package.json
  package-lock.json
  .github/workflows/deploy.yml
```

---

## Data Model

### Topics (NEW: centralized)

Defined in:

```text
src/_data/topics.yml
```

Each topic:

```yaml
- id: fair-data
  name: FAIR Data
  summary: Courses about making research data findable, accessible, interoperable, and reusable.
  image: topic-fair.jpg
  order: 2
```

**Key design decision:**
- `id` is the single source of truth
- `id` is used for:
  - course references
  - URL slug (`/topics/{id}/`)

---

### Courses

Each course file contains:

```yaml
---
layout: course.njk
tags: courses
title: ...
provider: ...
level: ...
topics:
  - fair-data
  - research-data-management
summary: |
  Multi-line markdown
image: filename.jpg
homepage: https://...
permalink: /courses/course-slug/
---
```

**Important change:**
- `topics` now uses **topic IDs**, not names

---

## Collections

### Topics collection (updated)

Defined in `.eleventy.js`

- Reads topic definitions from `topics.yml`
- Matches courses by `topic.id`
- Returns:
  - id
  - name
  - summary
  - image
  - order
  - slug (= id)
  - courses[]

---

## Key Features

### 1. Course system

- One file per course
- Auto-generated:
  - individual course pages
  - course listings

---

### 2. Topic system (refactored)

- Topics defined centrally (not inferred from courses)
- Stable IDs prevent breakage when renaming topics
- Pages:
  - `/topics/` → courses grouped by topic
  - `/topics/{id}/` → per-topic pages

---

### 3. Topic card entry page (NEW)

- `/topic-cards/`
- Displays one card per topic
- Each card includes:
  - image
  - title
  - summary
- Click → topic page

---

### 4. Card-based UI

#### Course cards

- Fixed width (300px)
- Fixed height (~430px)
- Scroll on hover
- Markdown-rendered summaries

#### Topic cards

- Grid layout (max 3 columns)
- Responsive (3 → 2 → 1 columns)

---

## Layout & Styling

### Grid fixes (important lesson)

- Use **consistent sizing between grid and cards**
- Avoid mixing `1fr` with fixed-width cards

### Key solution

```css
.topic-course-grid {
  display: grid;
  grid-template-columns: repeat(3, 300px);
  gap: 20px;
  justify-content: start;
}
```

---

### Critical fix: Nunjucks whitespace control

Using:

```njk
{%- for course in topic.courses -%}
...
{%- endfor -%}
```

Prevents stray whitespace nodes becoming grid items.

**Without this → broken layouts ("checkerboard" behavior).**

---

### Base layout

```njk
{{ content | safe }}
```

- Injects rendered page HTML
- Prevents HTML escaping

---

## GitHub Pages Setup

### Deployment

- GitHub Actions builds `_site/`
- Deploys automatically

### Path handling

```js
pathPrefix: isProd ? "/REPO-NAME/" : "/"
```

All internal links use:

```njk
{{ '/topics/' | url }}
```

---

## Key Lessons / Gotchas (Updated)

### 1. Separate content from structure

- Topics should be defined centrally
- Courses reference topics via IDs

---

### 2. Avoid duplicated identifiers

- Use `id` only (no separate slug needed)

---

### 3. Grid + fixed width must match

- Do not mix `1fr` columns with fixed-width cards

---

### 4. Nunjucks whitespace matters in grids

- Use `{%- -%}` to avoid invisible grid items

---

### 5. Liquid vs Nunjucks syntax

- `.md` → Liquid → `| filter: arg`
- `.njk` → Nunjucks → `| filter(arg)`

---

### 6. `permalink` must NOT use `url` filter

---

### 7. Image handling

- Explicit `image:` field required

---

## Current Status

Working:

- Local dev (`npm start`)
- Production build + deploy
- Topic card entry page
- Topic pages
- Course pages
- Centralized topic system
- Stable topic IDs
- Clean grid layout (fixed + responsive)

---

## Next Steps (Updated Priorities)

### High impact

- Filtering (topic, level, provider)
- Sorting

### Medium

- Improve homepage (highlight topics)
- Add fallback images

### Longer-term

- Contribution workflow
- Lightweight search

---

## One-line description

> Static course catalog built with Eleventy using YAML-driven topics and courses, with topic-based navigation and GitHub Pages deployment.

