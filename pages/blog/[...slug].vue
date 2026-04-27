<script setup lang="ts">
const route = useRoute()
const { public: { adsenseSlots } } = useRuntimeConfig()

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
  <!-- Dreispaltig: linke Sidebar | Artikel | rechte Sidebar -->
  <!-- Sidebars nur ab xl-Breakpoint sichtbar (≥1280px) -->
  <div class="relative flex gap-6 items-start">

    <!-- Linke Sidebar -->
    <aside class="hidden xl:block w-40 flex-shrink-0 sticky top-6 self-start">
      <AdBlock :key="`left-${route.path}`" :ad-slot="adsenseSlots.left" ad-format="vertical" />
    </aside>

    <!-- Artikel -->
    <article v-if="post" class="min-w-0 flex-1">
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

      <!-- In-Article Ad nach dem Inhalt, vor dem Bottom-Ad -->
      <AdBlock :key="`inArticle-${route.path}`" :ad-slot="adsenseSlots.inArticle" ad-format="fluid" ad-layout="in-article" class="mt-8" />

      <!-- Ad unter Artikel (auf kleinen Screens, wo Sidebars versteckt sind) -->
      <AdBlock :key="`bottom-${route.path}`" :ad-slot="adsenseSlots.bottom" ad-format="auto" class="mt-8 xl:hidden" />

      <footer class="mt-16 pt-8 border-t border-gray-800">
        <NuxtLink to="/" class="text-amber-400 hover:text-amber-300 transition-colors text-sm">
          ← Zurück zum Blog
        </NuxtLink>
      </footer>
    </article>

    <!-- Rechte Sidebar -->
    <aside class="hidden xl:block w-40 flex-shrink-0 sticky top-6 self-start">
      <AdBlock :key="`right-${route.path}`" :ad-slot="adsenseSlots.right" ad-format="vertical" />
    </aside>

  </div>
</template>
