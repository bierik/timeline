import Duration from 'luxon/src/duration'
import Vue from 'vue'
import EventComponent from '@/components/Event.vue'

const EventComponentConstructor = Vue.extend(EventComponent)

export default function ({ $config }) {
  const FETCH_PADDING = $config.breakpoints.mdAndDown ? { weeks: 3 } : { months: 3 }
  const MAX_ZOOM = { months: 2 }
  const MIN_ZOOM = { days: 4 }
  const INITIAL_WINDOW = $config.breakpoints.mdAndDown ? { weeks: 1 } : { months: 1 }
  const ZOOM_STEP = 0.5
  const RUNTIME_WINDOW_SPAN = $config.breakpoints.mdAndDown ? { weeks: 1 } : { months: 1 }

  const TIMELINE_OPTIONS = {
    locale: 'de',
    template(item) {
      const eventComponentInstance = new EventComponentConstructor({
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
    showCurrentTime: true,
    showTooltips: false,
    zoomMax: Duration.fromObject(MAX_ZOOM).toMillis(),
    zoomMin: Duration.fromObject(MIN_ZOOM).toMillis(),
    horizontalScroll: true,
    zoomable: $config.breakpoints.mdAndDown,
  }

  Object.assign($config, {
    FETCH_PADDING,
    MAX_ZOOM,
    MIN_ZOOM,
    INITIAL_WINDOW,
    ZOOM_STEP,
    TIMELINE_OPTIONS,
    RUNTIME_WINDOW_SPAN,
  })
}
