---
title: Courses
layout: base.njk
permalink: /courses/
---

# Courses

<ul>
{% for course in collections.courses %}
  <li>
    <a href="{{ course.url | url}}"><strong>{{ course.data.title }}</strong></a><br>
    {{ course.data.summary }}<br>
    <em>Provider:</em> {{ course.data.provider }}<br>
    <em>Topics:</em> {{ course.data.topics | join: ", " }}
  </li>
{% endfor %}
</ul>
