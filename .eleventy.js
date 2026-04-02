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
      .filter((topic) => {
        // visible defaults to true if omitted
        return ![false, 0, "0", "false"].includes(topic.visible);
      })
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
          visible: topic.visible,
          courses: topicCourses
        };
      });
      /* optionally add:
      .filter((topic) => topic.courses.length > 0)
      */
  });

  return {
    pathPrefix: isProd ? `/${repoName}/` : "/",
    dir: {
      input: "src",
      output: "_site"
    }
  };
};