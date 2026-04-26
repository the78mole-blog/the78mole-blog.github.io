<script setup lang="ts">
useSeoMeta({
  title: 'Kontakt – the78mole',
  description: 'Schreib mir – Fragen, Anmerkungen oder einfach Hallo.',
})

const form = reactive({
  name: '',
  email: '',
  subject: '',
  message: '',
})

const submitted = ref(false)
const error = ref(false)

async function handleSubmit(e: Event) {
  const target = e.target as HTMLFormElement
  const data = new FormData(target)
  try {
    const res = await fetch('https://api.staticforms.xyz/submit', {
      method: 'POST',
      body: data,
    })
    if (res.ok) {
      submitted.value = true
    } else {
      error.value = true
    }
  } catch {
    error.value = true
  }
}
</script>

<template>
  <div>
    <h1 class="text-3xl font-bold text-white mb-2">Kontakt</h1>
    <p class="text-gray-400 mb-10">Fragen, Anmerkungen oder einfach Hallo – schreib mir!</p>

    <div class="grid sm:grid-cols-2 gap-6 mb-12">
      <a href="mailto:me@the78mole.de"
         class="flex items-center gap-3 bg-gray-900 border border-gray-800 hover:border-amber-500 rounded-xl p-4 transition-colors">
        <span class="text-2xl">✉️</span>
        <div>
          <div class="text-xs text-gray-500 uppercase tracking-wide">E-Mail</div>
          <div class="text-white">me@the78mole.de</div>
        </div>
      </a>
      <a href="https://github.com/the78mole" target="_blank" rel="noopener"
         class="flex items-center gap-3 bg-gray-900 border border-gray-800 hover:border-amber-500 rounded-xl p-4 transition-colors">
        <span class="text-2xl">🐙</span>
        <div>
          <div class="text-xs text-gray-500 uppercase tracking-wide">GitHub</div>
          <div class="text-white">the78mole</div>
        </div>
      </a>
    </div>

    <div v-if="submitted" class="bg-green-900/30 border border-green-700 text-green-300 rounded-xl p-6 mb-8">
      Danke für deine Nachricht! Ich melde mich so bald wie möglich.
    </div>

    <div v-else-if="error" class="bg-red-900/30 border border-red-700 text-red-300 rounded-xl p-6 mb-8">
      Leider ist etwas schiefgelaufen. Schreib mir direkt per E-Mail.
    </div>

    <template v-else>
      <h2 class="text-xl font-semibold text-white mb-6">Formular</h2>
      <form @submit.prevent="handleSubmit" class="space-y-5">
        <!-- StaticForms – API-Key eintragen -->
        <input type="hidden" name="apiKey" value="YOUR_STATICFORMS_API_KEY" />
        <input type="hidden" name="redirectTo" value="" />
        <!-- Honeypot gegen Spam -->
        <input type="text" name="honeypot" class="hidden" tabindex="-1" autocomplete="off" />

        <div class="grid sm:grid-cols-2 gap-5">
          <div>
            <label for="name" class="block text-sm text-gray-400 mb-1">Name *</label>
            <input
              id="name" v-model="form.name" type="text" name="name" required
              class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-600 focus:outline-none focus:border-amber-500 transition-colors"
            />
          </div>
          <div>
            <label for="email" class="block text-sm text-gray-400 mb-1">E-Mail *</label>
            <input
              id="email" v-model="form.email" type="email" name="email" required
              class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-600 focus:outline-none focus:border-amber-500 transition-colors"
            />
          </div>
        </div>

        <div>
          <label for="subject" class="block text-sm text-gray-400 mb-1">Betreff</label>
          <input
            id="subject" v-model="form.subject" type="text" name="subject"
            placeholder="z. B. Frage zu einem Artikel, Kooperation, ..."
            class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-600 focus:outline-none focus:border-amber-500 transition-colors"
          />
        </div>

        <div>
          <label for="message" class="block text-sm text-gray-400 mb-1">Nachricht *</label>
          <textarea
            id="message" v-model="form.message" name="message" rows="6" required
            class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 text-white placeholder-gray-600 focus:outline-none focus:border-amber-500 transition-colors resize-none"
          ></textarea>
        </div>

        <button
          type="submit"
          class="bg-amber-500 hover:bg-amber-400 text-gray-950 font-semibold px-6 py-2 rounded-lg transition-colors"
        >
          Nachricht senden
        </button>
      </form>

      <p class="mt-4 text-xs text-gray-600">
        Das Formular nutzt <a href="https://www.staticforms.xyz" target="_blank" rel="noopener" class="underline hover:text-gray-400">Static Forms</a>.
        Weitere Infos in der <NuxtLink to="/pages/datenschutzerklaerung" class="underline hover:text-gray-400">Datenschutzerklärung</NuxtLink>.
      </p>
    </template>
  </div>
</template>
