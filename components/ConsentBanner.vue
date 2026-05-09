<script setup lang="ts">
const { gtag } = useGtag()

// Cookie: 365 Tage, SameSite=Lax
const consent = useCookie<boolean | null>('user-consent', {
  maxAge: 60 * 60 * 24 * 365,
  sameSite: 'lax',
  default: () => null,
})

// Sichtbar solange noch keine Entscheidung
const visible = computed(() => consent.value === null)

// Globalen Zustand für AdBlock-Komponenten bereitstellen
const consentState = useState<boolean>('consent', () => false)

// Beim Mount: gespeicherten Consent wiederherstellen
onMounted(() => {
  if (consent.value === true) {
    consentState.value = true
    gtag('consent', 'update', {
      analytics_storage: 'granted',
      ad_storage: 'granted',
    })
  }
})

function acceptAll() {
  consent.value = true
  consentState.value = true
  // Consent Mode v2: Datenerfassung freigeben
  gtag('consent', 'update', {
    analytics_storage:  'granted',
    ad_storage:         'granted',
    ad_user_data:       'granted',
    ad_personalization: 'granted',
  })
}

function denyAll() {
  consent.value = false
  consentState.value = false
}

// Erlaubt Footer-Link, den Banner erneut zu öffnen
function resetConsent() {
  consent.value = null
  consentState.value = false
}

// Expose damit der Footer-Link es aufrufen kann
defineExpose({ resetConsent })
</script>

<template>
  <Transition name="slide-up">
    <div
      v-if="visible"
      class="fixed bottom-0 inset-x-0 z-50 bg-gray-900 border-t border-gray-700 shadow-2xl"
      role="dialog"
      aria-modal="true"
      aria-label="Cookie-Einstellungen"
    >
      <div class="max-w-4xl mx-auto px-4 py-5 flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
        <div class="text-sm text-gray-300 leading-relaxed">
          <p class="font-semibold text-white mb-1">🍪 Diese Seite verwendet Cookies</p>
          <p>
            Ich nutze Google Analytics (GA4) und Google AdSense, um die Nutzung zu analysieren und Werbung zu schalten.
            Weitere Infos in der
            <NuxtLink to="/pages/datenschutzerklaerung" class="text-amber-400 underline hover:text-amber-300">
              Datenschutzerklärung
            </NuxtLink>.
          </p>
        </div>
        <div class="flex gap-3 flex-shrink-0">
          <button
            @click="denyAll"
            class="px-4 py-2 text-sm rounded-lg border border-gray-600 text-gray-300 hover:border-gray-400 hover:text-white transition-colors"
          >
            Nur notwendige
          </button>
          <button
            @click="acceptAll"
            class="px-4 py-2 text-sm rounded-lg bg-amber-500 hover:bg-amber-400 text-gray-950 font-semibold transition-colors"
          >
            Alle akzeptieren
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}
.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>
