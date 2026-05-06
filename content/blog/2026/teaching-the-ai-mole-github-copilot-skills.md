---
title: Teaching the AI Mole – GitHub Copilot Skills for Nuxt Blogs
date: '2026-04-27'
description: 'How I taught GitHub Copilot everything it needs to know about managing a Nuxt-based GitHub Pages blog – using Copilot Skills.'
image: /images/blog/2026/04/mole-skill.jpeg
categories:
  - Dev
  - AI
---

Or: How a Mole Stopped Repeating Itself and Started Teaching Its AI Assistant Instead.

Moles are creatures of habit. We dig the same tunnels, follow the same paths, and every now and then we bump into the same rock *again* – wondering how we forgot it was there.

After migrating this blog from WordPress to Nuxt 4 and spending a few sessions fixing the same class of bugs (hydration mismatches, `@nuxt/content` v3 API changes, a rogue tailwindcss v4 update sneaking in via Renovate), I decided enough was enough. The Mole needed to write things down. Not just for himself – but for his AI assistant, too.

## What Are Copilot Skills?

[GitHub Copilot](https://github.com/features/copilot) supports a concept called **Skills**: small knowledge packages that live in your repo (or in your user profile) as a `SKILL.md` file. When you start a conversation, Copilot reads the skill description and decides whether the knowledge is relevant. If it is, the full skill gets loaded automatically.

Think of it as a sticky note on the tunnel wall – but one that an AI can actually read.

A skill lives in `.github/skills/<name>/SKILL.md` for project-scoped knowledge, or in `~/.copilot/skills/<name>/SKILL.md` for personal knowledge that travels with you across all projects.

## What I Documented

### Repo-Level: the `repo-maintenance` Skill

The project-level skill [`.github/skills/repo-maintenance/SKILL.md`](https://github.com/the78mole-blog/the78mole-blog.github.io/blob/main/.github/skills/repo-maintenance/SKILL.md) captures everything a freshly-summoned AI needs to know about *this specific blog*:

- **Directory structure**: where content lives, what each `pages/` file does
- **Environment variables**: which GitHub Vars and Secrets drive the build, and why the StaticForms key is injected by `sed` in CI rather than stored in the repo
- **CI/CD-Workflow**: trigger conditions, Node version, the PR-preview artifact trick
- **AdSense-Slot-IDs**: all four slots named and mapped to their positions
- **Content-Frontmatter-Templates**: copy-paste ready snippets for new blog posts and pages
- **WordPress-Redirects**: why both `routeRules: '/slug'` *and* `'/slug/'` are needed (spoiler: GitHub Pages has no server to normalize trailing slashes)
- **Common errors**: a quick-lookup table of `no such column`, `queryContent is not defined`, hydration mismatches and their fixes
- **Pre-commit checklist**: seven things to verify before every push

### User-Level: the `nuxt-gh-pages` Skill

The personal skill at `~/.copilot/skills/nuxt-gh-pages/SKILL.md` distills the broader Nuxt-on-GitHub-Pages experience, independent of any single repo:

- The full `@nuxt/content` v2 → v3 migration table (`.find()` → `.all()`, `_path` → `path`, etc.)
- The tailwindcss v3/v4 conflict trap with `@nuxtjs/tailwindcss` – and the one-liner to check if it's finally safe to upgrade
- The three hydration-mismatch patterns (cookie-based components, dynamic dates, ad slots) and their `<ClientOnly>` / `isMounted` fixes
- A GitHub Actions workflow template for new Nuxt SSG projects
- A `content.config.ts` template with Zod schemas (the thing that prevents `no such column: "date"` forever)

## Why Bother?

Because the alternative is explaining the same context from scratch in every new chat session. With skills loaded, the AI already knows that `tailwindcss` must stay on `^3.x`, that `ConsentBanner` belongs inside `<ClientOnly>`, and that new Frontmatter fields need a Zod entry before they become queryable.

Less digging in circles. More actual tunneling.

## A Note on Limits

Skills are not magic. They don't run code, they don't watch your repository for changes, and they don't update themselves. They are *documentation* – the kind that gets read by a language model instead of a human.

That means: keep them honest. When something changes (a new package version, a new CI step, a fixed bug), update the skill too. A stale skill is just a misleading comment with extra ceremony.

Also: the `description` field is the discovery surface. If the trigger phrases aren't in the description, the skill won't be loaded. Use the *"Use for: ..."* pattern and be specific.

## The Bigger Picture

We tend to think of AI assistants as tools that know everything. In practice, they know a lot in general and very little about your specific project. Skills are the bridge. They let you invest a small amount of upfront writing to avoid a large amount of repeated explaining.

The Mole has learned: the best tunnel system isn't the one you dig the fastest. It's the one you can navigate in the dark without bumping into the same rock twice.

---

*Both skills are available in this or the skill repository and will be picked up automatically by GitHub Copilot in VS Code when working on this project.*

Links:

- [Repo-Level Skill `repo-maintenance`](https://github.com/the78mole-blog/the78mole-blog.github.io/blob/main/.github/skills/repo-maintenance/SKILL.md)
- [User-Level Skill `nuxt-gh-pages`](https://github.com/the78mole/skills/tree/main/skills/nuxt-gh-pages)
- [All my user level Skills](https://github.com/the78mole/skills)
