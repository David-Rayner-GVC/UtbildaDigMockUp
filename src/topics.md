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
  height: 430px;
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow-y: hidden;
  overflow-x: hidden;
  display: block;
  background: white;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.course-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
  overflow-y: auto;
}

.course-card img {
  display: block;
  width: 300px;
  height: 200px;
  object-fit: contain;
  background-color: #eee;
}
.course-content {
  padding: 0.75rem 1rem 1rem 1rem;
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
}

.course-summary ul,
.course-summary ol {
  padding-left: 1.25rem;
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

       <div class="course-content">  
        <p><a href="{{ course.data.homepage }}"><strong>{{ course.data.title }}</strong></a></p>
        {{ course.data.summary | renderContent: "md" }}
        <p><em>Provider:</em> {{ course.data.provider }}<br></p>
        <p><em>Level:</em> {{ course.data.level }}</p>
       </div>
      </div>
    {% endfor %}
   </div> 
  </section>
  <hr>
{% endfor %}
