<script setup lang="ts">
const route = useRoute()
const { data: post } = await useAsyncData(`post-${route.path}`, () =>
  queryContent(route.path).findOne()
)

if (!post.value) {
  throw createError({ statusCode: 404, statusMessage: 'Post not found' })
}

useSeoMeta({
  title: () => post.value?.title ?? '',
  description: () => post.value?.description ?? '',
  ogImage: () => post.value?.image ?? '',
})
</script>

<template>
  <article v-if="post">
    <header class="mb-10">
      <div class="flex gap-2 mb-3 flex-wrap">
        <span
          v-for="cat in post.categories"
          :key="cat"
          class="text-xs bg-amber-400/10 text-amber-400 px-2 py-0.5 rounded-full"
        >{{ cat }}</span>
      </div>
      <h1 class="text-3xl font-bold text-white mb-3">{{ post.title }}</h1>
      <p v-if="post.description" class="text-lg text-gray-400 mb-4">{{ post.description }}</p>
      <time class="text-sm text-gray-500">{{ post.date?.slice(0, 10) }}</time>
      <img
        v-if="post.image"
        :src="post.image"
        :alt="post.title"
        class="mt-6 w-full max-h-80 object-cover rounded-xl"
      />
    </header>

    <div class="prose prose-invert prose-amber max-w-none">
      <ContentRenderer :value="post" />
    </div>

    <footer class="mt-16 pt-8 border-t border-gray-800">
      <NuxtLink to="/" class="text-amber-400 hover:text-amber-300 transition-colors text-sm">
        ← Zurück zum Blog
      </NuxtLink>
    </footer>
  </article>
</template>
