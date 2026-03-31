# Project Summary: Eleventy Course Catalog Demo

## Goal

Build a **static, collaborative course catalog** using:

* YAML-based course metadata
* Eleventy (11ty) for site generation
* GitHub Pages for free hosting and collaboration

---

## Current Architecture

### Tech stack

* **Eleventy (11ty)** static site generator
* **Node.js / npm**
* **GitHub Pages via GitHub Actions**
* Templates:

  * `.md` → Markdown + Liquid
  * `.njk` → Nunjucks

---

## Project Structure

```text
project-root/
  src/
    index.md                  # homepage
    topics.md                 # topic overview page
    topic-pages.njk           # generates one page per topic

    courses/
      *.md                    # one file per course (YAML front matter)

    images/
      *.jpg / *.jpeg          # course images

    _includes/
      base.njk                # main layout
      course.njk              # course page layout

  .eleventy.js
  package.json
  package-lock.json
  .github/workflows/deploy.yml
```

---

## Data Model (Course Files)

Each course is a Markdown file with YAML front matter:

```yaml
---
layout: course.njk
tags: courses
title: ...
provider: ...
level: ...
topics:
  - ...
summary: |
  Multi-line text (can include markdown lists)
image: filename.jpg
homepage: https://...
permalink: /courses/course-slug/
---
```

---

## Key Features Implemented

### 1. Course system

* One file per course
* Auto-generated:

  * course pages
  * course listing page (`/courses/`)

### 2. Topic system

* Topics derived dynamically from course metadata
* Custom Eleventy collection (`topics`)
* Pages:

  * `/topics/` → overview
  * `/topics/{slug}/` → per-topic pages

### 3. Card-based UI (Topics page)

* 300px wide cards
* Image (300×200, `object-fit: contain`)
* Title + metadata + summary
* Entire card scrolls on hover
* No overlay (removed for UX consistency)

### 4. Markdown rendering inside templates

* Uses Eleventy Render plugin:

  * Liquid: `| renderContent: "md"`
  * Nunjucks: `| renderContent("md")`

---

## Styling Approach

* Inline CSS (for now, inside templates)
* Flexbox grid layout
* Cards:

  * fixed height (~430px)
  * scrollable on hover
  * subtle hover shadow

---

## GitHub Pages Setup

### Deployment method

* GitHub Actions workflow
* Builds `_site/` and deploys

### Important config

#### `.eleventy.js`

* Uses environment-based `pathPrefix`:

```js
pathPrefix: isProd ? "/REPO-NAME/" : "/"
```

#### Links

* All internal links use Eleventy `url` filter:

```njk
{{ '/topics/' | url }}
```

#### Images

```njk
{{ '/images/' | url }}{{ course.data.image }}
```

---

## Important Lessons / Gotchas

### 1. Liquid vs Nunjucks syntax

* `.md` → Liquid → `| filter: arg`
* `.njk` → Nunjucks → `| filter(arg)`

### 2. `permalink` must NOT use `url` filter

Correct:

```njk
permalink: "/topics/{{ topic.slug }}/index.html"
```

### 3. GitHub Pages path issues

* Must use `pathPrefix` + `url` filter
* Avoid hardcoded `/...` links

### 4. Image handling

* Explicit `image:` field recommended
* Avoid relying on `.jpg` assumptions

### 5. `.gitignore`

```text
_site/
node_modules/
```

Do NOT ignore:

```text
package-lock.json
```

---

## Current Status

Working:

* Local dev (`npm start`)
* Build (`npm run build:prod`)
* GitHub Pages deploy
* Topics + courses + navigation
* Card UI with scroll-on-hover

---

## Possible Next Steps

### UX / UI

* Move CSS to a shared stylesheet
* Add topic badges to cards
* Improve homepage (featured topics or courses)
* Add fallback image handling

### Functionality

* Filters (provider, level, topic)
* Search
* Sorting

### Data model

* Separate `summary` vs `highlights`
* Add duration, format, etc.

---

## Key Files to Share in Future Chat

If debugging:

* `.eleventy.js`
* `topics.md`
* `topic-pages.njk`
* one example course file

---

## One-line description

> Static course catalog built with Eleventy using YAML front matter, topic-based grouping, and GitHub Pages deployment.

