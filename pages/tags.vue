<script setup lang="ts">
interface PostEntry {
  title: string
  path: string
  date: string
  description: string
  image?: string | null
}

const route = useRoute()
const router = useRouter()

const { data: taxonomy, status } = await useFetch<Record<string, PostEntry[]>>(
  '/tags.json',
  { server: false },
)

const allTags = computed(() =>
  taxonomy.value
    ? Object.keys(taxonomy.value).sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base' }))
    : [],
)

const selected = computed(() => route.query.tag as string | undefined)

/** Convert an arbitrary string to a URL slug (e.g. "TH!NK City" → "thnk-city") */
function toSlug(s: string): string {
  return s
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
}

/** Canonical key in the taxonomy (preserves original casing, e.g. "STM32").
 *  Falls back to slug comparison so that e.g. ?tag=thnk-city matches "TH!NK City". */
const selectedKey = computed(() => {
  if (!selected.value || !taxonomy.value) return undefined
  const lower = selected.value.toLowerCase()
  const slug = toSlug(selected.value)
  return Object.keys(taxonomy.value).find(
    k => k.toLowerCase() === lower || toSlug(k) === slug,
  )
})

const posts = computed(() =>
  selectedKey.value && taxonomy.value ? (taxonomy.value[selectedKey.value] ?? []) : [],
)

function select(tag: string) {
  router.push({ query: selected.value === tag ? {} : { tag } })
}

useSeoMeta({
  title: 'Tags – the78mole Blog',
  description: 'Browse all blog posts by tag.',
})
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-2 text-white">Tags</h1>
    <p class="text-gray-400 mb-6">Browse posts by tag – click one to see the matching articles.</p>

    <div v-if="status === 'pending'" class="text-gray-500 text-sm mb-8">Loading…</div>

    <div v-else class="flex flex-wrap gap-2 mb-8">
      <button
        v-for="tag in allTags"
        :key="tag"
        @click="select(tag)"
        :class="[
          'px-3 py-1 rounded-full text-sm transition-colors cursor-pointer',
          selectedKey === tag
            ? 'bg-amber-400 text-gray-900 font-semibold'
            : 'bg-gray-800 text-gray-300 hover:bg-amber-400/20 hover:text-amber-300',
        ]"
      >
        {{ tag }}
        <span class="opacity-60 text-xs ml-1">({{ taxonomy?.[tag]?.length ?? 0 }})</span>
      </button>
    </div>

    <template v-if="selectedKey">
      <h2 class="text-xl font-semibold text-amber-400 mb-4">
        Posts tagged "{{ selectedKey }}" – {{ posts.length }} article{{ posts.length !== 1 ? 's' : '' }}
      </h2>
      <div class="grid gap-4">
        <NuxtLink
          v-for="post in posts"
          :key="post.path"
          :to="post.path"
          class="block bg-gray-900 rounded-xl p-4 border border-gray-800 hover:border-amber-500 transition-colors"
        >
          <div class="font-semibold text-white hover:text-amber-400 transition-colors">{{ post.title }}</div>
          <p v-if="post.description" class="text-sm text-gray-400 mt-1 line-clamp-2">{{ post.description }}</p>
          <time class="text-xs text-gray-500 mt-1 block">{{ post.date?.slice(0, 10) }}</time>
        </NuxtLink>
      </div>
    </template>

    <p v-else-if="status !== 'pending' && !selected" class="text-gray-500 text-sm">
      Select a tag above to see matching posts.
    </p>
    <p v-else-if="status !== 'pending' && selected && !selectedKey" class="text-gray-500 text-sm">
      No posts found for tag "{{ selected }}".
    </p>
  </div>
</template>
