import { defineContentConfig, defineCollection, z } from '@nuxt/content'

export default defineContentConfig({
  collections: {
    /**
     * Blog posts under content/blog/**
     *
     * Built-in fields added by the 'page' type (no need to redeclare):
     *   title    – extracted from frontmatter `title:` or the first H1
     *   path     – URL path derived from the file location
     *   stem     – file path without extension
     *   body     – rendered AST
     *
     * The schema below extends the built-in schema with blog-specific fields.
     * Fields without .optional() are REQUIRED – nuxi generate will error if missing.
     */
    blog: defineCollection({
      type: 'page',
      source: 'blog/**/*.md',
      schema: z.object({
        // Required fields – every blog post must provide these in frontmatter
        date:        z.string(),
        description: z.string(),
        // Optional fields
        image:      z.string().optional(),
        categories: z.array(z.string()).optional(),
        tags:       z.array(z.string()).optional(),
      }),
    }),

    /**
     * Static pages under content/pages/
     * These are simpler – only description is part of the extended schema.
     */
    pages: defineCollection({
      type: 'page',
      source: 'pages/**/*.md',
      schema: z.object({
        description: z.string().optional(),
      }),
    }),
  },
})
