<script setup lang="ts">
defineProps<{
  code?: string
  language?: string
  filename?: string
  highlights?: number[]
  meta?: string
}>()

const copied = ref(false)
const containerRef = ref<HTMLElement | null>(null)

async function copyCode() {
  const codeEl = containerRef.value?.querySelector('code')
  const text = codeEl?.innerText ?? ''
  await navigator.clipboard.writeText(text)
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
}
</script>

<template>
  <div ref="containerRef" class="relative group my-4">
    <button
      class="
        absolute right-2 top-2 z-10
        opacity-0 group-hover:opacity-100
        transition-opacity duration-150
        bg-gray-700 hover:bg-gray-600
        text-gray-300 hover:text-white
        text-xs font-mono
        px-2 py-1 rounded
        select-none
      "
      :aria-label="copied ? 'Copied!' : 'Copy code'"
      @click="copyCode"
    >
      {{ copied ? '✓ Copied' : 'Copy' }}
    </button>

    <pre class="!my-0"><slot /></pre>
  </div>
</template>
