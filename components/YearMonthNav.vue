<script setup lang="ts">
const props = defineProps<{
  selectedYear?: string
  selectedMonth?: string
}>()

// Alle Post-Datumsfelder – derselbe Key dedupliziert über alle Seiten hinweg
const { data: allDates } = await useAsyncData('nav-years-months', () =>
  queryCollection('blog').select('date').all()
)

const years = computed(() => {
  if (!allDates.value) return []
  const ys = [...new Set(allDates.value.map(p => p.date.slice(0, 4)))]
  return ys.sort((a, b) => b.localeCompare(a))
})

// Monate des gewählten Jahres (null-padded, z.B. '07')
const months = computed(() => {
  if (!props.selectedYear || !allDates.value) return []
  const ms = [...new Set(
    allDates.value
      .filter(p => p.date.startsWith(props.selectedYear!))
      .map(p => p.date.slice(5, 7))
  )]
  return ms.sort()
})

const MONTH_SHORT = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

function monthLabel(mm: string): string {
  return MONTH_SHORT[parseInt(mm, 10) - 1] ?? mm
}

const route = useRoute()
const isAllPage = computed(() => route.path === '/all')
const isLatestActive = computed(() => !isAllPage.value && !props.selectedYear)
</script>

<template>
  <div class="mb-8 space-y-3">
    <!-- Jahres-Buttons -->
    <div class="flex flex-wrap gap-2">
      <NuxtLink
        to="/"
        class="px-3 py-1 rounded-full text-sm font-medium transition-colors"
        :class="isLatestActive
          ? 'bg-amber-400 text-gray-900'
          : 'bg-gray-800 text-gray-300 hover:bg-gray-700 hover:text-white'"
      >• Latest</NuxtLink>
      <NuxtLink
        to="/all"
        class="px-3 py-1 rounded-full text-sm font-medium transition-colors"
        :class="isAllPage
          ? 'bg-amber-400 text-gray-900'
          : 'bg-gray-800 text-gray-300 hover:bg-gray-700 hover:text-white'"
      >All</NuxtLink>
      <NuxtLink
        v-for="year in years"
        :key="year"
        :to="`/${year}`"
        class="px-3 py-1 rounded-full text-sm font-medium transition-colors"
        :class="selectedYear === year
          ? 'bg-amber-400 text-gray-900'
          : 'bg-gray-800 text-gray-300 hover:bg-gray-700 hover:text-white'"
      >{{ year }}</NuxtLink>
    </div>

    <!-- Monats-Buttons (nur wenn ein Jahr gewählt ist) -->
    <div v-if="selectedYear && months.length" class="flex flex-wrap gap-2">
      <NuxtLink
        :to="`/${selectedYear}`"
        class="px-3 py-1 rounded-full text-sm font-medium transition-colors"
        :class="!selectedMonth
          ? 'bg-amber-400/80 text-gray-900'
          : 'bg-gray-800 text-gray-300 hover:bg-gray-700 hover:text-white'"
      >All Months</NuxtLink>
      <NuxtLink
        v-for="mm in months"
        :key="mm"
        :to="`/${selectedYear}/${mm}`"
        class="px-3 py-1 rounded-full text-sm font-medium transition-colors"
        :class="selectedMonth === mm
          ? 'bg-amber-400/80 text-gray-900'
          : 'bg-gray-800 text-gray-300 hover:bg-gray-700 hover:text-white'"
      >{{ monthLabel(mm) }}</NuxtLink>
    </div>
  </div>
</template>
