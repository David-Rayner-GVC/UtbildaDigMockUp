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
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 2rem;
}

.course-card {
  width: 300px;
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  display: flex;
  flex-direction: column;
}

.course-card img {
  display: block;
  width: 300px;
  height: 200px;
  object-fit: contain;
  background-color: #eee; /* optional, fills empty space */
}

/* overlay */
.course-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  color: white;
  padding: 1rem;
  opacity: 0;
  transition: opacity 0.2s ease-in-out;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  overflow-y: auto;
  box-sizing: border-box;
}

.course-card:hover .course-overlay {
  opacity: 1;
}

.course-overlay h3 {
  margin-top: 0;
}

.course-overlay {
  overflow-y: auto;
}

.course-title {
  padding: 0.75rem 1rem;
}

.course-title a {
  color: #5af4ff; /* Light blue for contrast */
  text-decoration: underline; /* Always underline */
  font-weight: bold; /* Optional: adds extra visibility */
}

.course-overlay a {
  color: #5af4ff; /* Light blue for contrast */
  text-decoration: underline; /* Always underline */
  font-weight: bold; /* Optional: adds extra visibility */
}

.course-overlay a:hover {
  color: #ffffff; /* White on hover for high contrast */
  text-decoration: none; /* Remove underline on hover if preferred */
}

.course-overlay a:visited {
  color: #ceb3f2; /* A lighter or distinct purple-blue */
}

.course-content {
  padding: 0.75rem 1rem 1rem 1rem;
}

.course-content h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.course-content a {
  text-decoration: none;
  color: inherit;
}

.course-summary {
  font-size: 0.9rem;
  color: #555;
  margin: 0;
}
</style>

{% for topic in collections.topics %}
  <section>
    <h2><a href="{{ '/topics/' | url }}{{ topic.slug }}/">{{ topic.name }}</a></h2>
    <!-- <p>{{ topic.courses.length }} course{% if topic.courses.length != 1 %}s{% endif %}</p> -->

    <div class="topic-course-grid">
    {% for course in topic.courses %}
      <div class="course-card">
      <a href="{{ course.url | url }}">
        <img
          src="{{ '/images/' | url }}{{ course.data.image }}"
          alt="{{ course.data.title }}"
        >
      </a>

      <div class="course-overlay">
        <h3><a href="{{ course.data.homepage }}">{{ course.data.title }}</a></h3>
        <p><strong>Provider:</strong> {{ course.data.provider }}</p>
        <p><strong>Level:</strong> {{ course.data.level }}</p>
        <p>{{ course.data.summary}}</p>
        <p><strong><a href="{{ course.data.homepage }}">Link to Course Homepage</a></strong></p>
      </div>
      <div class="course-content">
       <h3>
        <a href="{{ course.url | url }}">{{ course.data.title }}</a>
       </h3>
       <p class="course-summary">
       {{ course.data.summary | truncate: 120 }}
       </p>
     </div>
     </div>
    {% endfor %}
    
  </section>
  <hr>
{% endfor %}
