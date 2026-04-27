<script setup lang="ts">
const route = useRoute()
const { data: page } = await useAsyncData(`page-${route.path}`, () =>
  queryCollection('pages').path(route.path).first()
)

if (!page.value) {
  throw createError({ statusCode: 404, statusMessage: 'Page not found' })
}

useSeoMeta({
  title: () => page.value?.title ?? '',
  description: () => page.value?.description ?? '',
})
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <article v-if="page">
    <header class="mb-10">
      <h1 class="text-3xl font-bold text-white mb-3">{{ page.title }}</h1>
      <p v-if="page.description" class="text-lg text-gray-400">{{ page.description }}</p>
    </header>

    <div class="prose prose-invert prose-amber max-w-none">
      <ContentRenderer :value="page" />
    </div>
    </article>
  </div>
</template>
