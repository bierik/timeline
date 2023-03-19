<template>
  <div class="relative">
    <div ref="timeline" class="h-full" />
    <div class="flex flex-col fixed bottom-0 right-0 pr-5 pb-20">
      <Button v-if="timeline" class="rounded-full px-3 py-3 flex mb-2 justify-center items-center" @click="zoomIn">
        <feather size="20" type="plus" />
      </Button>
      <Button v-if="timeline" class="rounded-full px-3 py-3 flex justify-center items-center mb-2" @click="zoomOut">
        <feather size="20" type="minus" />
      </Button>
      <Button v-if="timeline" class="rounded-full px-3 py-3 flex justify-center items-center" @click="goToToday">
        <feather size="20" type="calendar" />
      </Button>
    </div>
  </div>
</template>

<script>
import DateTime from 'luxon/src/datetime'
import Duration from 'luxon/src/duration'
import { DataSet } from 'vis-data/esnext'
import { Timeline } from 'vis-timeline/esnext'
import Vue from 'vue'
import EventComponent from '@/components/Event.vue'

const EventComponentConstructor = Vue.extend(EventComponent)

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
      this.timeline.itemsData.update(events)
    },
    $route: {
      async handler({ query: { activeEvent } }) {
        await this.initTimeline()
        if (!activeEvent) {
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
      const self = this
      const options = {
        locale: 'de-CH',
        template(item) {
          const eventComponentInstance = new EventComponentConstructor({
            propsData: {
              event: item,
              $router: self.$router,
            },
          })
          eventComponentInstance.$mount()
          return eventComponentInstance.$el
        },
        timeAxis: { scale: 'day', step: 1 },
        format: {
          majorLabels(date) {
            return date.format('MMMM yyyy')
          },
        },
        height: '100%',
        showCurrentTime: false,
        showTooltips: false,
        zoomMax: Duration.fromObject({ months: 2 }).toMillis(),
        zoomMin: Duration.fromObject({ days: 4 }).toMillis(),
        horizontalScroll: true,
        zoomable: false,
      }
      this.timeline = new Timeline(this.$refs.timeline, new DataSet(this.events), options)
      const now = DateTime.local()
      this.timeline.setWindow(now.minus({ months: 1 }).toISODate(), now.plus({ months: 1 }).toISODate())
      this.timeline.on('rangechange', (args) => {
        this.$emit('rangechange', args)
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
      this.timeline.zoomIn(0.5)
    },
    zoomOut() {
      this.timeline.zoomOut(0.5)
    },
    goToToday() {
      this.timeline.moveTo(DateTime.local().toJSDate())
    },
  },
}
</script>
