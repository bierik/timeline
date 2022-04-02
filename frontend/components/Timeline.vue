<template>
  <div ref="timeline" />
</template>

<script>
import DateTime from 'luxon/src/datetime'
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
  watch: {
    events(events) {
      this.timeline.setItems(new DataSet(events))
    },
    $route: {
      handler({ query: { activeEvent } }) {
        setTimeout(() => {
          this.timeline.focus(Number.parseInt(activeEvent), { zoom: false })
        }, 0)
      },
      immediate: true,
    },
  },
  mounted() {
    const $router = this.$router
    const $axios = this.$axios
    const options = {
      locale: 'de-CH',
      template(item) {
        const eventComponentInstance = new EventComponentConstructor({
          $router,
          $axios,
          propsData: {
            event: item,
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
    }
    this.timeline = new Timeline(this.$refs.timeline, new DataSet(this.events), options)
    const now = DateTime.local()
    this.timeline.setWindow(now.minus({ months: 1 }).toISODate(), now.plus({ months: 1 }).toISODate())
    this.timeline.on('rangechange', (args) => {
      this.$emit('rangechange', args)
    })
    this.timeline.on('changed', () => this.selectActiveEvent())
  },
  methods: {
    selectActiveEvent() {
      const eventEl = document.querySelector(`[data-event-id="${this.$route.query.activeEvent}"]`)
      if (eventEl) {
        eventEl.closest('.vis-item').classList.add('vis-selected')
      }
    },
  },
}
</script>
