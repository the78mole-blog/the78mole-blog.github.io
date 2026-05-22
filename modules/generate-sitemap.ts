/**
 * Nuxt module: generate-sitemap
 *
 * Generates public/sitemap.xml from all blog posts and content pages before
 * every build (dev, build, generate).  Only real content URLs are included –
 * no redirect stubs, tag/category pages, or year-archive pages.
 *
 * URL structure:
 *   /                           – home (index.vue)
 *   /all                        – full post list (all.vue)
 *   /blog/{year}/{slug}         – blog posts  (content/blog/**)
 *   /pages/{slug}               – content pages (content/pages/*.md)
 */

import { readFileSync, writeFileSync, mkdirSync, readdirSync, statSync } from 'node:fs'
import { join, basename, relative } from 'node:path'
import { defineNuxtModule } from '@nuxt/kit'

const BASE_URL = 'https://the78mole.de'

// ── Helpers ───────────────────────────────────────────────────────────────────

function collectMarkdownFiles(dir: string): string[] {
  const files: string[] = []
  try {
    for (const entry of readdirSync(dir)) {
      const full = join(dir, entry)
      if (statSync(full).isDirectory()) {
        files.push(...collectMarkdownFiles(full))
      } else if (entry.endsWith('.md')) {
        files.push(full)
      }
    }
  } catch {
    // directory may not exist yet – silently skip
  }
  return files
}

/** Extracts the value of a scalar frontmatter field (e.g. `date: '2024-01-15'`). */
function parseFrontmatterField(content: string, key: string): string | null {
  const match = content.match(/^---[ \t]*\n([\s\S]*?)\n---[ \t]*\n/)
  if (!match) return null
  const line = match[1].split('\n').find(l => l.startsWith(`${key}:`))
  if (!line) return null
  return line.replace(`${key}:`, '').trim().replace(/^['"]|['"]$/g, '') || null
}

function xmlEscape(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
}

interface SitemapEntry {
  loc: string
  lastmod?: string
  changefreq?: string
  priority?: string
}

function buildXml(entries: SitemapEntry[]): string {
  const items = entries.map(({ loc, lastmod, changefreq, priority }) => {
    const lines = [`  <url>`, `    <loc>${xmlEscape(loc)}</loc>`]
    if (lastmod) lines.push(`    <lastmod>${lastmod}</lastmod>`)
    if (changefreq) lines.push(`    <changefreq>${changefreq}</changefreq>`)
    if (priority) lines.push(`    <priority>${priority}</priority>`)
    lines.push(`  </url>`)
    return lines.join('\n')
  })

  return [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ...items,
    '</urlset>',
    '',
  ].join('\n')
}

// ── Module ────────────────────────────────────────────────────────────────────

export default defineNuxtModule({
  meta: { name: 'generate-sitemap' },

  setup(_options, nuxt) {
    nuxt.hook('build:before', () => {
      const rootDir = nuxt.options.rootDir
      const publicDir = join(rootDir, 'public')
      const contentDir = join(rootDir, 'content')

      const entries: SitemapEntry[] = []

      // ── Static app routes ─────────────────────────────────────────────────
      entries.push({ loc: `${BASE_URL}/`, changefreq: 'daily', priority: '1.0' })
      entries.push({ loc: `${BASE_URL}/all`, changefreq: 'weekly', priority: '0.8' })

      // ── Blog posts ────────────────────────────────────────────────────────
      const blogDir = join(contentDir, 'blog')
      const blogFiles = collectMarkdownFiles(blogDir).sort()

      for (const file of blogFiles) {
        const rel = relative(blogDir, file) // e.g. "2024/my-post.md"
        const slug = rel.replace(/\.md$/, '') // e.g. "2024/my-post"
        const content = readFileSync(file, 'utf-8')
        const date = parseFrontmatterField(content, 'date')

        entries.push({
          loc: `${BASE_URL}/blog/${slug}`,
          lastmod: date ?? undefined,
          changefreq: 'monthly',
          priority: '0.7',
        })
      }

      // ── Content pages ─────────────────────────────────────────────────────
      // Exclude legal/utility pages that should not be indexed.
      const excludedPages = new Set(['datenschutzerklaerung', 'impressum', 'contact'])
      const pagesDir = join(contentDir, 'pages')
      const pageFiles = collectMarkdownFiles(pagesDir).sort()

      for (const file of pageFiles) {
        const slug = basename(file, '.md')
        if (excludedPages.has(slug)) continue
        const content = readFileSync(file, 'utf-8')
        const date = parseFrontmatterField(content, 'date')

        entries.push({
          loc: `${BASE_URL}/pages/${slug}`,
          lastmod: date ?? undefined,
          changefreq: 'monthly',
          priority: '0.5',
        })
      }

      // ── Write ─────────────────────────────────────────────────────────────
      mkdirSync(publicDir, { recursive: true })
      writeFileSync(join(publicDir, 'sitemap.xml'), buildXml(entries), 'utf-8')

      const blogCount = blogFiles.length
      const pageCount = pageFiles.filter(f => !excludedPages.has(basename(f, '.md'))).length
      console.log(
        `sitemap.xml      → ${blogCount} posts, ${pageCount} pages, ${entries.length} URLs total`,
      )
    })
  },
})
