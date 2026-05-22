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
  '/categories.json',
  { server: false },
)

const allCategories = computed(() =>
  taxonomy.value
    ? Object.keys(taxonomy.value).sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base' }))
    : [],
)

const selected = computed(() => route.query.category as string | undefined)

/** Canonical key in the taxonomy (preserves original casing, e.g. "ESPhome") */
const selectedKey = computed(() => {
  if (!selected.value || !taxonomy.value) return undefined
  const lower = selected.value.toLowerCase()
  return Object.keys(taxonomy.value).find(k => k.toLowerCase() === lower)
})

const posts = computed(() =>
  selectedKey.value && taxonomy.value ? (taxonomy.value[selectedKey.value] ?? []) : [],
)

function select(cat: string) {
  router.push({ query: selected.value === cat ? {} : { category: cat } })
}

useSeoMeta({
  title: 'Categories – the78mole Blog',
  description: 'Browse all blog posts by category.',
})
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-2 text-white">Categories</h1>
    <p class="text-gray-400 mb-6">Browse posts by category – click one to see the matching articles.</p>

    <div v-if="status === 'pending'" class="text-gray-500 text-sm mb-8">Loading…</div>

    <div v-else class="flex flex-wrap gap-2 mb-8">
      <button
        v-for="cat in allCategories"
        :key="cat"
        @click="select(cat)"
        :class="[
          'px-3 py-1 rounded-full text-sm transition-colors cursor-pointer',
          selectedKey === cat
            ? 'bg-amber-400 text-gray-900 font-semibold'
            : 'bg-gray-800 text-gray-300 hover:bg-amber-400/20 hover:text-amber-300',
        ]"
      >
        {{ cat }}
        <span class="opacity-60 text-xs ml-1">({{ taxonomy?.[cat]?.length ?? 0 }})</span>
      </button>
    </div>

    <template v-if="selectedKey">
      <h2 class="text-xl font-semibold text-amber-400 mb-4">
        Category "{{ selectedKey }}" – {{ posts.length }} article{{ posts.length !== 1 ? 's' : '' }}
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
      Select a category above to see matching posts.
    </p>
    <p v-else-if="status !== 'pending' && selected && !selectedKey" class="text-gray-500 text-sm">
      No posts found for category "{{ selected }}".
    </p>
  </div>
</template>
