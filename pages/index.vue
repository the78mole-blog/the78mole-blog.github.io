<script setup lang="ts">
const { data: posts } = await useAsyncData('blog-index', () =>
  queryContent('blog')
    .only(['title', 'date', 'description', 'image', 'categories', '_path'])
    .sort({ date: -1 })
    .find()
)
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-2 text-white">Blog</h1>
    <p class="text-gray-400 mb-10">Technik, Embedded, Smart Home und alles dazwischen.</p>

    <div class="grid gap-6">
      <article
        v-for="post in posts"
        :key="post._path"
        class="group bg-gray-900 rounded-xl overflow-hidden border border-gray-800 hover:border-amber-500 transition-colors"
      >
        <NuxtLink :to="post._path" class="flex gap-4 p-5">
          <img
            v-if="post.image"
            :src="post.image"
            :alt="post.title"
            class="w-24 h-24 object-cover rounded-lg flex-shrink-0 bg-gray-800"
            loading="lazy"
          />
          <div class="flex flex-col justify-center min-w-0">
            <div class="flex gap-2 mb-1 flex-wrap">
              <span
                v-for="cat in post.categories"
                :key="cat"
                class="text-xs bg-amber-400/10 text-amber-400 px-2 py-0.5 rounded-full"
              >{{ cat }}</span>
            </div>
            <h2 class="font-semibold text-white group-hover:text-amber-400 transition-colors line-clamp-2">
              {{ post.title }}
            </h2>
            <p v-if="post.description" class="text-sm text-gray-400 mt-1 line-clamp-2">
              {{ post.description }}
            </p>
            <time class="text-xs text-gray-500 mt-2">{{ post.date?.slice(0, 10) }}</time>
          </div>
        </NuxtLink>
      </article>
    </div>
  </div>
</template>
