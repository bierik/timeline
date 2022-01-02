<template>
  <div ref="timeline" />
</template>

<script>
import Vue from 'vue'
import { Timeline } from 'vis-timeline/esnext'
import { DataSet } from 'vis-data/esnext'
import DateTime from 'luxon/src/datetime'
import EventComponent from '@/components/Event.vue'

const EventComponentConstructor = Vue.extend(EventComponent)

export default {
  props: {
    events: {
      type: Array,
      default: () => [],
    },
  },
  mounted() {
    const options = {
      locale: 'de-CH',
      template(item, element, data) {
        const eventComponentInstance = new EventComponentConstructor({
          propsData: { title: item.title, icon: item.icon },
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
  },
}
</script>

<style>
.vis-time-axis .vis-grid.vis-odd {
  background: transparent;
}

.vis-grid.vis-vertical.vis-minor {
  border-color: #fafafa;
}

.vis-grid.vis-vertical.vis-major {
  border-style: dotted;
}
</style>
