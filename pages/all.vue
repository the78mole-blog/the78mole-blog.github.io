<script setup lang="ts">
const { data: posts } = await useAsyncData('blog-all', () =>
  queryCollection('blog')
    .select('title', 'date', 'description', 'image', 'categories', 'path')
    .order('date', 'DESC')
    .all()
)

useSeoMeta({
  title: 'Blog – All Posts',
  description: 'All blog posts in chronological order.',
})
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-2 text-white">All Posts</h1>
    <p class="text-gray-400 mb-6">Every post, newest first.</p>
    <YearMonthNav />
    <BlogPostList :posts="posts ?? []" />
  </div>
</template>
