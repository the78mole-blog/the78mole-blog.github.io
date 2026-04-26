<script setup lang="ts">
const route = useRoute()
const consentState = useState<boolean>('consent')

// Bei SPA-Navigation: AdSense-Slots auf jeder neuen Seite neu pushen
watch(() => route.fullPath, () => {
  if (!consentState.value) return
  nextTick(() => {
    try {
      const w = window as typeof window & { adsbygoogle: unknown[] }
      ;(w.adsbygoogle = w.adsbygoogle || []).push({})
    } catch {
      // silently ignore
    }
  })
})
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
    <ConsentBanner />
  </NuxtLayout>
</template>
