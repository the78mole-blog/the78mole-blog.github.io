/**
 * Nuxt module: generate-taxonomy
 *
 * Automatically generates public/tags.json and public/categories.json from
 * blog post frontmatter before every build (dev, build, generate).
 *
 * The JSON maps each tag / category name to the list of matching posts:
 *   { "ESP32": [{ title, path, date, description, image }, ...], ... }
 */

import {
  readFileSync,
  writeFileSync,
  mkdirSync,
  readdirSync,
  statSync,
} from 'node:fs'
import { join, relative } from 'node:path'
import { defineNuxtModule } from '@nuxt/kit'

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

/**
 * Minimal YAML frontmatter parser that covers all field types used in this
 * blog (strings and string arrays).  A full YAML library is not needed.
 */
function parseFrontmatter(content: string): Record<string, unknown> {
  const match = content.match(/^---[ \t]*\n([\s\S]*?)\n---[ \t]*\n/)
  if (!match) return {}

  const result: Record<string, unknown> = {}
  let currentKey: string | null = null
  let currentArray: string[] = []

  const flush = () => {
    if (currentKey !== null) {
      result[currentKey] = currentArray
      currentKey = null
      currentArray = []
    }
  }

  for (const line of match[1].split('\n')) {
    // Array item under current key
    const arrayItem = line.match(/^[ \t]*-[ \t]+(.+)$/)
    if (currentKey !== null && arrayItem) {
      currentArray.push(arrayItem[1].trim().replace(/^['"]|['"]$/g, ''))
      continue
    }

    flush()

    // Key: value pair
    const kv = line.match(/^([\w]+):[ \t]*(.*)$/)
    if (!kv) continue

    const [, key, raw] = kv
    const val = raw.trim()

    if (val === '[]') {
      result[key] = []
    } else if (val === '') {
      // Next lines may be array items
      currentKey = key
      currentArray = []
    } else {
      result[key] = val.replace(/^['"]|['"]$/g, '')
    }
  }

  flush()
  return result
}

// ── Module ────────────────────────────────────────────────────────────────────

export default defineNuxtModule({
  meta: { name: 'generate-taxonomy', version: '1.0.0' },

  setup(_options, nuxt) {
    nuxt.hook('build:before', () => {
      const root = nuxt.options.rootDir
      const contentDir = join(root, 'content', 'blog')
      const publicDir = join(root, 'public')

      const files = collectMarkdownFiles(contentDir).sort().reverse()

      const tags: Record<string, object[]> = {}
      const categories: Record<string, object[]> = {}

      for (const file of files) {
        const fm = parseFrontmatter(readFileSync(file, 'utf-8'))

        const title = String(fm.title ?? '').trim()
        if (!title) continue

        // content/blog/2024/post.md → /blog/2024/post
        const rel = relative(join(root, 'content'), file)
        const path = '/' + rel.replace(/\\/g, '/').replace(/\.md$/, '')

        const entry = {
          title,
          path,
          date: String(fm.date ?? '').trim(),
          description: String(fm.description ?? '').trim(),
          image: (fm.image as string | undefined) ?? null,
        }

        for (const tag of (fm.tags as string[] | undefined) ?? []) {
          const t = String(tag).trim()
          if (t) (tags[t] ??= []).push(entry)
        }
        for (const cat of (fm.categories as string[] | undefined) ?? []) {
          const c = String(cat).trim()
          if (c) (categories[c] ??= []).push(entry)
        }
      }

      mkdirSync(publicDir, { recursive: true })
      writeFileSync(join(publicDir, 'tags.json'), JSON.stringify(tags, null, 2), 'utf-8')
      writeFileSync(join(publicDir, 'categories.json'), JSON.stringify(categories, null, 2), 'utf-8')

      const tc = Object.keys(tags).length
      const cc = Object.keys(categories).length
      console.log(`[taxonomy] tags.json: ${tc} tags | categories.json: ${cc} categories`)
    })
  },
})
