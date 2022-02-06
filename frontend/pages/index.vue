<template>
  <div>
    <Timeline :events="events" class="timeline" @rangechange="fetchEvents" />
    <nuxt-link
      to="/event/new"
      class="
        rounded-full
        w-16
        h-16
        flex
        items-center
        justify-center
        text-white
        fixed
        bottom-8
        right-8
        drop-shadow-lg
        bg-primary-300
        text-2xl
      "
      >+</nuxt-link
    >
  </div>
</template>

<script>
import throttle from 'lodash/throttle'
import DateTime from 'luxon/src/datetime'

export default {
  data() {
    return {
      events: [],
    }
  },
  methods: {
    fetchEvents: throttle(async function fetchEvents({ start, end }) {
      this.events = await this.$axios.$get('/events/', {
        params: {
          date_after: DateTime.fromJSDate(start).minus({ months: 1 }).toISODate(),
          date_before: DateTime.fromJSDate(end).plus({ months: 1 }).toISODate(),
        },
      })
    }, 500),
  },
}
</script>
<style>
.timeline {
  height: 50vh;
}
</style>
