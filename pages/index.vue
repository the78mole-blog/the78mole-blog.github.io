<script setup lang="ts">
const { data: posts } = await useAsyncData('blog-index', () =>
  queryCollection('blog')
    .select('title', 'date', 'description', 'image', 'categories', 'tags', 'path')
    .order('date', 'DESC')
    .limit(5)
    .all()
)
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-2 text-white">Blog</h1>
    <p class="text-gray-400 mb-6">Tech, embedded, smart home, and everything in between.</p>
    <YearMonthNav />
    <BlogPostList :posts="posts ?? []" />
  </div>
</template>
