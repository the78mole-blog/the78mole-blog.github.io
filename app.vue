<script setup lang="ts">
const consentState = useState<boolean>('consent')
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
    <ClientOnly>
      <ConsentBanner />
    </ClientOnly>
  </NuxtLayout>
</template>
