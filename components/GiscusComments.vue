<script setup lang="ts">
import Giscus from '@giscus/vue'

const { public: { giscus } } = useRuntimeConfig()
</script>

<template>
  <ClientOnly>
    <div class="mt-16 pt-8 border-t border-gray-800">
      <Giscus
        :repo="giscus.repo"
        :repo-id="giscus.repoId"
        :category="giscus.category"
        :category-id="giscus.categoryId"
        mapping="pathname"
        strict="0"
        reactions-enabled="1"
        emit-metadata="0"
        input-position="top"
        theme="transparent_dark"
        lang="de"
        loading="lazy"
      />
    </div>
  </ClientOnly>
</template>
