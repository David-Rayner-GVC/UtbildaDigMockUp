const { RenderPlugin } = require("@11ty/eleventy");
const yaml = require("js-yaml");
const fs = require("fs");
const path = require("path");

module.exports = function(eleventyConfig) {
  const isProd = process.env.ELEVENTY_ENV === "production";
  const repoName = "UtbildaDigMockUp";

  eleventyConfig.addPlugin(RenderPlugin);
  eleventyConfig.addPassthroughCopy("src/images");

  eleventyConfig.addCollection("topics", function(collectionApi) {
    const courses = collectionApi.getFilteredByTag("courses");

    const topicsPath = path.join(__dirname, "src", "_data", "topics.yml");
    const topicDefs = yaml.load(fs.readFileSync(topicsPath, "utf8"));

    return topicDefs
      .map((topic) => {
        const topicCourses = courses.filter((course) => {
          const courseTopics = course.data.topics || [];
          return courseTopics.includes(topic.id);
        });

        return {
          id: topic.id,
          slug: topic.id,
          name: topic.name,
          summary: topic.summary,
          image: topic.image,
          order: topic.order || 999,
          courses: topicCourses
        };
      })
      /* .filter((topic) => topic.courses.length > 0) */
      .sort((a, b) => a.order - b.order);
  });

  return {
    pathPrefix: isProd ? `/${repoName}/` : "/",
    dir: {
      input: "src",
      output: "_site"
    }
  };
};