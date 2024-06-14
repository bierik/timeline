import { Duration } from "luxon";
import { createApp } from "vue";
import EventComponent from "@/components/Event.vue";
import VueDOMPurifyHTML from "vue-dompurify-html";

export default defineNuxtPlugin(({ $config, $router }) => {
  const FETCH_PADDING = { months: 3 };
  const INITIAL_WINDOW = { months: 1 };
  const RUNTIME_WINDOW_SPAN = { months: 1 };
  const MAX_ZOOM = { months: 2 };
  const MIN_ZOOM = { days: 4 };
  const ZOOM_STEP = 0.5;

  const TIMELINE_OPTIONS = {
    locale: "de",
    template(item) {
      const eventComponent = createApp(EventComponent, { event: item });
      eventComponent.provide("$router", $router);
      eventComponent.use(VueDOMPurifyHTML);
      return eventComponent.mount(document.createElement("div")).$el;
    },
    timeAxis: { scale: "day", step: 1 },
    format: {
      majorLabels(date) {
        return date.format("MMMM yyyy");
      },
    },
    height: "100%",
    showCurrentTime: true,
    showTooltips: false,
    zoomMax: Duration.fromObject(MAX_ZOOM).toMillis(),
    zoomMin: Duration.fromObject(MIN_ZOOM).toMillis(),
    horizontalScroll: true,
  };

  Object.assign($config, {
    FETCH_PADDING,
    MAX_ZOOM,
    MIN_ZOOM,
    INITIAL_WINDOW,
    ZOOM_STEP,
    TIMELINE_OPTIONS,
    RUNTIME_WINDOW_SPAN,
  });
});
