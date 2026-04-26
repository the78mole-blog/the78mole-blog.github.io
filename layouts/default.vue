<script setup lang="ts">
const consent = useCookie<boolean | null>('user-consent')
function resetConsent() {
  consent.value = null
}
</script>

<template>
  <div class="min-h-screen bg-gray-950 text-gray-100">
    <header class="border-b border-gray-800 bg-gray-900">
      <div class="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
        <NuxtLink to="/" class="text-xl font-bold text-amber-400 hover:text-amber-300 transition-colors">
          the78mole
        </NuxtLink>
        <nav class="flex gap-6 text-sm text-gray-400">
          <NuxtLink to="/" class="hover:text-white transition-colors">Blog</NuxtLink>
          <NuxtLink to="/pages/projects" class="hover:text-white transition-colors">Projects</NuxtLink>
          <NuxtLink to="/pages/tutorials" class="hover:text-white transition-colors">HowTos</NuxtLink>
          <NuxtLink to="/pages/links" class="hover:text-white transition-colors">Links</NuxtLink>
          <NuxtLink to="/pages/about" class="hover:text-white transition-colors">About</NuxtLink>
          <NuxtLink to="/pages/contact" class="hover:text-white transition-colors">Kontakt</NuxtLink>
          <a href="https://github.com/the78mole" target="_blank" rel="noopener" class="hover:text-white transition-colors">GitHub</a>
        </nav>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-10">
      <slot />
    </main>

    <footer class="border-t border-gray-800 mt-20">
      <div class="max-w-4xl mx-auto px-4 py-6 text-center text-sm text-gray-500 space-x-4">
        <span>© {{ new Date().getFullYear() }} the78mole</span>
        <span>·</span>
        <NuxtLink to="/pages/impressum" class="hover:text-gray-300 transition-colors">Impressum</NuxtLink>
        <span>·</span>
        <NuxtLink to="/pages/datenschutzerklaerung" class="hover:text-gray-300 transition-colors">Datenschutz</NuxtLink>
        <span>·</span>
        <button @click="resetConsent" class="hover:text-gray-300 transition-colors">Datenschutzeinstellungen</button>
        <span>·</span>
        <span>Built with <a href="https://nuxt.com" target="_blank" class="text-amber-400 hover:text-amber-300">Nuxt</a></span>
      </div>
    </footer>
  </div>
</template>
