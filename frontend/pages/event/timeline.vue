<template>
  <Layout narrow>
    <template #append>
      <Bottomnav>
        <template #activator="{ on }">
          <button class="flex items-center text-white px-4 hover:bg-primary-400 h-full" v-on="on">
            <feather type="plus" size="18" />
            <span class="hidden sm:block ml-1">Hinzufügen</span>
          </button>
        </template>
        <div class="bg-white">
          <nuxt-link to="/event/new" class="flex items-center p-4 h-full hover:bg-gray-200">
            <feather type="plus" size="18" />
            <span class="ml-1">Hinzufügen</span>
          </nuxt-link>
          <hr />
          <nuxt-link class="flex items-center p-4 h-full hover:bg-gray-200" :to="{ name: 'import' }">
            <feather type="upload" size="18" />
            <span class="ml-1">Import</span>
          </nuxt-link>
        </div>
      </Bottomnav>
      <button class="flex items-center text-white px-4 hover:bg-primary-400 h-full" @click="filterDrawer = true">
        <feather type="filter" size="18" />
        <span class="hidden sm:block ml-1">Filter</span>
      </button>
    </template>
    <MonthSelector :value="monthFilter" class="fixed z-10" @input="setTimelineTime" />
    <Timeline
      ref="timeline"
      :events="events"
      class="timeline"
      @rangechanged="setMonthFilter"
      @rangechange="fetchEventsForTimeline"
    />
    <NavigationDrawer v-model="filterDrawer">
      <div class="p-4">
        <TextInput class="mb-2" label="Titel" :value="filter.title" @input="applyFilter({ title: $event })" />
        <PersonField label="Personen" :value="filter.people" @input="applyFilter({ people: $event })" />
      </div>
    </NavigationDrawer>
  </Layout>
</template>

<script>
import debounce from 'debounce-async'
import DateTime from 'luxon/src/datetime'

export default {
  data() {
    return {
      monthFilter: DateTime.local(),
      filterDrawer: false,
      events: [],
      filter: { title: '', people: [], start: null, end: null },
    }
  },
  methods: {
    setMonthFilter({ currentTime }) {
      this.monthFilter = currentTime
    },
    setTimelineTime(monthFilter) {
      this.$refs.timeline.setWindow(
        monthFilter.startOf('month').toJSDate(),
        monthFilter.startOf('month').plus(this.$config.RUNTIME_WINDOW_SPAN).toJSDate(),
      )
    },
    applyFilter(filter) {
      this.filter = { ...this.filter, ...filter }
      this.fetchEventsForTimeline()
    },
    fetchEventsDebounced: debounce(function fetchEventsDebounced(params) {
      return this.$axios.$get('/events/', { params })
    }, 200),
    async fetchEventsForTimeline({ start, end } = {}) {
      this.filter = { ...this.filter, start: start || this.filter.start, end: end || this.filter.end }
      try {
        this.events = (
          await this.fetchEventsDebounced({
            date_after: DateTime.fromJSDate(start).minus(this.$config.FETCH_PADDING).toISODate(),
            date_before: DateTime.fromJSDate(end).plus(this.$config.FETCH_PADDING).toISODate(),
            ordering: '-date',
            ...this.filter,
          })
        ).results
      } catch (error) {
        if (error !== 'canceled') {
          throw error
        }
      }
    },
  },
}
</script>
<style>
.timeline {
  height: calc(100dvh - 3rem);
}
</style>
