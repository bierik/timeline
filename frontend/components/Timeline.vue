<template>
  <div class="relative">
    <div ref="timeline" class="h-full" />
    <div class="flex flex-col fixed bottom-0 right-0 pr-5 pb-20">
      <Button
        v-if="timeline"
        class="rounded-full px-3 py-3 flex mb-2 justify-center items-center drop-shadow-lg"
        @click="zoomIn"
      >
        <feather size="20" type="zoom-in" />
      </Button>
      <Button
        v-if="timeline"
        class="rounded-full px-3 py-3 flex justify-center items-center mb-2 drop-shadow-lg"
        @click="zoomOut"
      >
        <feather size="20" type="zoom-out" />
      </Button>
      <Button
        v-if="timeline"
        class="rounded-full px-3 py-3 flex justify-center items-center drop-shadow-lg"
        @click="goToToday"
      >
        <feather size="20" type="calendar" />
      </Button>
    </div>
  </div>
</template>

<script>
import DateTime from 'luxon/src/datetime'
import Interval from 'luxon/src/interval'
import { DataSet } from 'vis-data/esnext'
import { Timeline } from 'vis-timeline/esnext'

export default {
  props: {
    events: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      timeline: null,
    }
  },
  watch: {
    events(events) {
      this.timeline.itemsData.clear()
      this.timeline.itemsData.add(events)
    },
    $route: {
      async handler({ query: { activeEvent } }) {
        await this.initTimeline()
        if (!activeEvent) {
          this.timeline.setSelection([])
          return
        }
        await this.addEvent(activeEvent)
        setTimeout(() => {
          this.timeline.focus(Number.parseInt(activeEvent), { zoom: false })
        }, 0)
      },
      immediate: true,
    },
  },
  methods: {
    async initTimeline() {
      await this.$nextTick()
      if (this.timeline) {
        return
      }
      this.timeline = new Timeline(this.$refs.timeline, new DataSet(this.events), this.$config.TIMELINE_OPTIONS)
      const now = DateTime.local()
      this.timeline.setWindow(
        now.minus(this.$config.INITIAL_WINDOW).toISODate(),
        now.plus(this.$config.INITIAL_WINDOW).toISODate(),
      )
      this.timeline.on('rangechange', (args) => {
        this.$emit('rangechange', args)
      })
      this.timeline.on('rangechanged', (args) => {
        const interval = Interval.fromDateTimes(DateTime.fromJSDate(args.start), DateTime.fromJSDate(args.end))
        const currentTime = interval.divideEqually(2)[0].end
        this.$emit('rangechanged', { ...args, currentTime })
      })
      this.timeline.on('changed', () => this.selectActiveEvent())
    },
    hasEvent(id) {
      return this.timeline.itemsData.getIds().includes(Number.parseInt(id))
    },
    async addEvent(id) {
      if (this.hasEvent(id)) {
        return
      }
      const event = await this.$axios.$get(`/events/${id}/`)
      this.timeline.itemsData.add(event)
    },
    selectActiveEvent() {
      const eventEl = document.querySelector(`[data-event-id="${this.$route.query.activeEvent}"]`)
      if (eventEl) {
        eventEl.closest('.vis-item').classList.add('vis-selected')
      }
    },
    zoomIn() {
      this.timeline.zoomIn(this.$config.ZOOM_STEP)
    },
    zoomOut() {
      this.timeline.zoomOut(this.$config.ZOOM_STEP)
    },
    goToToday() {
      this.timeline.moveTo(DateTime.local().toJSDate())
    },
    setWindow(...args) {
      this.timeline.setWindow(...args)
    },
  },
}
</script>
