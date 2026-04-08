---
title: Topics
layout: base.njk
permalink: /topics/
---

# Utbilda dig!
Here you will find a selection of courses about research data management and related topics.
<hr>
 
<style>
.topic-course-grid {
  display: grid;
  grid-template-columns: repeat(3, 300px);
  gap: 20px;
  margin-bottom: 2rem;
  justify-content: start;
}

.topic-course-grid_flex {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: flex-start;
}

.course-card {
  width: 100%;
  height: 430px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
  display: block;
  background: white;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
  cursor: pointer;
}

.course-card:hover,
.course-card:focus {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}


/* Image on the left */
.course-card img {
  display: block;
  width: 100%;                 /* fixed width */
  height: 100px;
  object-fit: contain;
  object-position: left center; /* keeps image anchored left inside box */
  background-color: #eee;
    /* flex-shrink: 0;  */             /* prevents squishing */
  /* margin: 0.75rem 0 0 0.75rem;  */  /* gives it some breathing room */
  padding: 0.5rem;
  box-sizing: border-box;
}


/* Content fills remaining space */
.course-content {
  padding: 0.75rem 1rem 1rem 1rem;
  flex: 1;                      /* take remaining width */
  min-width: 0;                 /* prevents overflow issues */
  overflow: hidden;
}
.course-content h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.course-content h3 a {
  text-decoration: none;
  color: inherit;
}

.course-content p {
  margin: 0 0 0.5rem 0;
}

.course-summary {
  font-size: 0.95rem;
  overflow: hidden;
}
/* this next one is important if the summary contains links */
.course-summary a {
  pointer-events: none;
  color: inherit;
  text-decoration: none;
}
.course-summary ul,
.course-summary ol {
  padding-left: 1.25rem;
}
@media (max-width: 1000px) {
  .topic-course-grid {
    grid-template-columns: repeat(2, 300px);
    justify-content: start;
  }
}

@media (max-width: 650px) {
  .topic-course-grid {
    grid-template-columns: 1fr;
    justify-content: start;
  }

  .course-card {
    width: 100%;
  }
}
</style>
{% for topic in collections.topics %}
  <section>
    <h2><a href="{{ '/topics/' | url }}{{ topic.slug }}/">{{ topic.name }}</a></h2>

    <div class="topic-course-grid">
    {%- for course in topic.courses -%}
      
      <div
        class="course-card js-clickable-card"
        data-href="{{ '/topics/' | append: topic.slug | append: '/' | url }}#course-{{ course.fileSlug }}"
        tabindex="0"
        role="link"
        aria-label="Go to {{ course.data.title }}"
      >
        <img
          src="{{ '/images/' | url }}{{ course.data.image }}"
          alt="{{ course.data.title }}"
        >

        <div class="course-content">
          <p><strong>{{ course.data.title }}</strong></p>

          <div class="course-summary">
            {{ course.data.summary | renderContent: "md" }}
          </div>

          <p><em>Provider:</em> {{ course.data.provider }}</p>
          <p><em>Level:</em> {{ course.data.level }}</p>
        </div>
      </div>

    {%- endfor -%}
    </div>
  </section>
  <hr>
{% endfor %}

<script>
document.addEventListener("DOMContentLoaded", function () {
  const cards = document.querySelectorAll(".js-clickable-card");

  cards.forEach(function (card) {
    card.addEventListener("click", function (event) {
      if (event.target.closest("a")) return;
      window.location.href = card.dataset.href;
    });

    card.addEventListener("keydown", function (event) {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        window.location.href = card.dataset.href;
      }
    });
  });
});
</script>