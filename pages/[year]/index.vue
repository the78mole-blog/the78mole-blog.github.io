<script setup lang="ts">
const route = useRoute()
const year = route.params.year as string

if (!/^\d{4}$/.test(year)) {
  throw createError({ statusCode: 404, statusMessage: 'Not found' })
}

const { data: posts } = await useAsyncData(`blog-year-${year}`, () =>
  queryCollection('blog')
    .select('title', 'date', 'description', 'image', 'categories', 'tags', 'path')
    .where('date', 'LIKE', `${year}-%`)
    .order('date', 'DESC')
    .all()
)

useSeoMeta({
  title: `Blog ${year}`,
  description: `All posts from ${year}.`,
})
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-2 text-white">Blog {{ year }}</h1>
    <p class="text-gray-400 mb-6">All posts from {{ year }}.</p>
    <YearMonthNav :selected-year="year" />
    <BlogPostList :posts="posts ?? []" />
  </div>
</template>
