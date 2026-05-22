<script setup lang="ts">
defineProps<{
  posts: Array<{
    path: string
    title: string
    date: string
    description?: string | null
    image?: string | null
    categories?: string[] | null
    tags?: string[] | null
  }>
}>()
</script>

<template>
  <div class="grid gap-6">
    <p v-if="!posts?.length" class="text-gray-500 text-sm">No posts found.</p>
    <article
      v-for="post in posts"
      :key="post.path"
      class="group bg-gray-900 rounded-xl overflow-hidden border border-gray-800 hover:border-amber-500 transition-colors"
    >
      <div class="flex gap-4 p-5">
        <NuxtLink :to="post.path" class="flex-shrink-0 self-center" tabindex="-1" aria-hidden="true">
          <img
            v-if="post.image"
            :src="post.image"
            :alt="post.title"
            class="w-24 h-24 object-cover rounded-lg bg-gray-800"
            loading="lazy"
          />
        </NuxtLink>
        <div class="flex flex-col justify-center min-w-0">
          <div class="flex gap-1.5 mb-1 flex-wrap">
            <NuxtLink
              v-for="cat in post.categories"
              :key="cat"
              :to="`/categories?category=${encodeURIComponent(cat)}`"
              class="text-xs bg-amber-400/10 text-amber-400 px-2 py-0.5 rounded-full hover:bg-amber-400/30 transition-colors"
            >{{ cat }}</NuxtLink>
            <NuxtLink
              v-for="tag in post.tags"
              :key="tag"
              :to="`/tags?tag=${encodeURIComponent(tag)}`"
              class="text-xs bg-gray-700 text-gray-300 px-2 py-0.5 rounded-full hover:bg-gray-600 transition-colors"
            ># {{ tag }}</NuxtLink>
          </div>
          <NuxtLink :to="post.path" class="block">
            <h2 class="font-semibold text-white group-hover:text-amber-400 transition-colors line-clamp-2">
              {{ post.title }}
            </h2>
            <p v-if="post.description" class="text-sm text-gray-400 mt-1 line-clamp-2">
              {{ post.description }}
            </p>
            <time class="text-xs text-gray-500 mt-2 block">{{ post.date?.slice(0, 10) }}</time>
          </NuxtLink>
        </div>
      </div>
    </article>
  </div>
</template>
