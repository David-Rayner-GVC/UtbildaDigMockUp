const { RenderPlugin } = require("@11ty/eleventy");

module.exports = function(eleventyConfig) {
  eleventyConfig.addPlugin(RenderPlugin);

  eleventyConfig.addPassthroughCopy("src/images");

  eleventyConfig.addCollection("topics", function(collectionApi) {
    const courses = collectionApi.getFilteredByTag("courses");
    const topicsMap = new Map();

    for (const course of courses) {
      const topics = course.data.topics || [];

      for (const topic of topics) {
        if (!topicsMap.has(topic)) {
          topicsMap.set(topic, []);
        }
        topicsMap.get(topic).push(course);
      }
    }

    return Array.from(topicsMap.entries())
      .map(([name, courses]) => ({
        name,
        slug: name
          .toLowerCase()
          .replace(/[^a-z0-9]+/g, "-")
          .replace(/^-|-$/g, ""),
        courses
      }))
      .sort((a, b) => a.name.localeCompare(b.name));
  });

  return {
    dir: {
      input: "src",
      output: "_site"
    }
  };
};
