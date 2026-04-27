<script setup lang="ts">
interface Props {
  adSlot: string
  adFormat?: string
  adLayout?: string
  fullWidthResponsive?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  adFormat: 'auto',
  adLayout: undefined,
  fullWidthResponsive: true,
})

const consentState = useState<boolean>('consent')
const { public: { adsensePubId } } = useRuntimeConfig()
const route = useRoute()

// Interner Key: erzwingt neues <ins>-Element nach SPA-Navigation
const insKey = ref(0)

// Initialer Mount
onMounted(() => {
  if (consentState.value) {
    pushAd()
  }
})

// Bei SPA-Navigation: <ins> neu erstellen und pushen
watch(() => route.path, () => {
  if (!consentState.value) return
  insKey.value++
  nextTick(() => pushAd())
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
      :key="insKey"
      class="adsbygoogle"
      style="display: block"
      :data-ad-client="adsensePubId"
      :data-ad-slot="adSlot"
      :data-ad-format="adFormat"
      :data-ad-layout="adLayout ?? undefined"
      :data-full-width-responsive="fullWidthResponsive ? 'true' : 'false'"
    />
  </div>
  <!-- Kein Consent: Platz freilassen oder leer -->
  <div v-else class="hidden" aria-hidden="true" />
</template>
