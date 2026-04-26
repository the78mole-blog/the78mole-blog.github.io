<script setup lang="ts">
interface Props {
  adSlot: string
  adFormat?: string
  fullWidthResponsive?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  adFormat: 'auto',
  fullWidthResponsive: true,
})

const consentState = useState<boolean>('consent')
const { public: { adsensePubId } } = useRuntimeConfig()

// Push-AdSense nur wenn Consent vorliegt
onMounted(() => {
  if (consentState.value) {
    pushAd()
  }
})

// Reaktiv auf Consent-Änderung reagieren (z.B. nachträgliches Akzeptieren)
watch(consentState, (granted) => {
  if (granted) {
    nextTick(() => pushAd())
  }
})

function pushAd() {
  try {
    const w = window as typeof window & { adsbygoogle: unknown[] }
    ;(w.adsbygoogle = w.adsbygoogle || []).push({})
  } catch {
    // silently ignore – e.g. adblocker
  }
}
</script>

<template>
  <div v-if="consentState" class="ad-block my-4 text-center">
    <ins
      class="adsbygoogle"
      style="display: block"
      :data-ad-client="adsensePubId"
      :data-ad-slot="adSlot"
      :data-ad-format="adFormat"
      :data-full-width-responsive="fullWidthResponsive ? 'true' : 'false'"
    />
  </div>
  <!-- Kein Consent: Platz freilassen oder leer -->
  <div v-else class="hidden" aria-hidden="true" />
</template>
