<template>
  <div ref="timeline" class="timeline" @scroll="trackScrollOffset">
    <div class="timeline-ticks">
      <div v-for="tick in ticks" :key="tick.date" class="timeline-tick">
        <div class="timeline-tick-label">{{ tick.date | toLocaleDateString }}</div>
      </div>
      <div class="timeline-line" />
      <Event
        v-for="event in eventStream"
        :key="event.date"
        :title="event.title"
        :icon="event.icon"
        :style="{ left: `${event.offset}px` }"
      />
    </div>
  </div>
</template>

<script>
import { DateTime, Interval } from 'luxon'

const start = DateTime.fromISO('2020-11-09')
const end = DateTime.local()

function getEventOffset(date) {
  const difference = DateTime.fromISO(date).diff(start).shiftTo('days').days
  return difference * 40
}

export default {
  name: 'Timeline',
  props: {
    events: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    ticks() {
      const interval = Interval.fromDateTimes(start, end)
      const ticks = interval.splitBy({ weeks: 1 })
      return ticks.map((tick) => ({ date: tick.start.toISO() }))
    },
    eventStream() {
      return this.events.map((event) => ({ ...event, offset: getEventOffset(event.date) }))
    },
  },
  mounted() {
    this.$refs.timeline.scrollLeft = this.$route.query.scrollOffset
  },
  methods: {
    trackScrollOffset() {
      window.requestAnimationFrame(() => {
        this.$router.replace({ query: { scrollOffset: this.$refs.timeline.scrollLeft } })
      })
    },
  },
}
</script>

<style>
.timeline {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  overflow: auto;
  padding: 0 50px;
}

.timeline-line {
  height: 1px;
  left: 0;
  right: 0;
  background: black;
  position: absolute;
}

.timeline-ticks {
  display: flex;
  position: relative;
}

.timeline-tick {
  background: black;
  width: 1px;
  margin-left: 280px;
  margin-top: -5px;
  height: 11px;
  font-size: 10px;
  white-space: nowrap;
}
.timeline-tick:first-child {
  margin-left: 0;
}

.timeline-tick-label {
  margin-top: 10px;
}
</style>
