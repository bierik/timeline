<template>
  <div class="pt-12">
    <div class="fixed top-0 right-0 left-0 bg-primary h-12">
      <div class="container items-center mx-auto flex h-full">
        <nuxt-link to="/event/new" class="flex items-center text-white px-4 hover:bg-primary-400 h-full">
          <feather type="plus" size="18" class="mr-1" />
          <span>Ereignis</span>
        </nuxt-link>
      </div>
    </div>
    <Timeline :events="events" class="timeline" @rangechange="fetchEvents" />
  </div>
</template>

<script>
import debounce from 'debounce-async'
import DateTime from 'luxon/src/datetime'

export default {
  data() {
    return {
      events: [],
    }
  },
  methods: {
    fetchEventsDebounced: debounce(async function fetchEventsDebounced({ start, end }) {
      this.events = await this.$axios.$get('/events/', {
        params: {
          date_after: DateTime.fromJSDate(start).minus({ months: 1 }).toISODate(),
          date_before: DateTime.fromJSDate(end).plus({ months: 1 }).toISODate(),
        },
      })
    }, 200),
    async fetchEvents(params) {
      try {
        await this.fetchEventsDebounced(params)
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
  height: calc(100vh - 3rem);
}
</style>
