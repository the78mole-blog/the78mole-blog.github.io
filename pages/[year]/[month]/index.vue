<script setup lang="ts">
const route = useRoute()
const year = route.params.year as string
const month = route.params.month as string

if (!/^\d{4}$/.test(year) || !/^\d{2}$/.test(month)) {
  throw createError({ statusCode: 404, statusMessage: 'Not found' })
}

const MONTH_LONG = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
]
const monthName = MONTH_LONG[parseInt(month, 10) - 1] ?? month

const { data: posts } = await useAsyncData(`blog-${year}-${month}`, () =>
  queryCollection('blog')
    .select('title', 'date', 'description', 'image', 'categories', 'tags', 'path')
    .where('date', 'LIKE', `${year}-${month}-%`)
    .order('date', 'DESC')
    .all()
)

useSeoMeta({
  title: `Blog ${monthName} ${year}`,
  description: `All posts from ${monthName} ${year}.`,
})
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-2 text-white">Blog {{ monthName }} {{ year }}</h1>
    <p class="text-gray-400 mb-6">All posts from {{ monthName }} {{ year }}.</p>
    <YearMonthNav :selected-year="year" :selected-month="month" />
    <BlogPostList :posts="posts ?? []" />
  </div>
</template>
