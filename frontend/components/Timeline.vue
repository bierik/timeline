<template>
  <div class="relative">
    <div
      ref="timeline"
      :style="{ visibility: timeline ? 'visible' : 'hidden' }"
      class="h-full"
    />
    <Icon
      class="absolute bottom-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
      name="feather:loader"
      size="50"
      :style="{ visibility: timeline ? 'hidden' : 'visible' }"
    />
    <div class="fixed bottom-0 right-0 flex flex-col pb-20 pr-5">
      <Button
        v-if="timeline"
        class="mb-2 hidden items-center justify-center rounded-full p-3 drop-shadow-lg md:flex"
        @click="zoomIn"
      >
        <Icon size="20" name="feather:zoom-in" />
      </Button>
      <Button
        v-if="timeline"
        class="mb-2 hidden items-center justify-center rounded-full p-3 drop-shadow-lg md:flex"
        @click="zoomOut"
      >
        <Icon size="20" name="feather:zoom-out" />
      </Button>
      <Button
        v-if="timeline"
        class="flex items-center justify-center rounded-full p-3 drop-shadow-lg"
        @click="goToToday"
      >
        <Icon size="20" name="feather:calendar" />
      </Button>
    </div>
  </div>
</template>

<script>
import { DateTime, Interval } from "luxon";
import { Timeline } from "vis-timeline/esnext";

export default defineNuxtComponent({
  props: {
    events: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      timeline: null,
    };
  },
  watch: {
    events(events) {
      this.timeline.itemsData.update(events);
    },
    "$route.query.activeEvent": {
      async handler(event) {
        this.selectEvent(event);
      },
    },
  },
  async mounted() {
    await this.initTimeline();
    this.selectEvent(this.$route.query.activeEvent);
  },
  methods: {
    async selectEvent(event) {
      if (!event) {
        this.timeline.setSelection([]);
        this.timeline.setOptions({ horizontalScroll: true });
        return;
      }
      await this.addEvent(event);
      this.selectActiveEvent();
      this.timeline.setOptions({ horizontalScroll: false });
      setTimeout(() => {
        this.timeline.focus(Number.parseInt(event), { zoom: false });
      }, 0);
    },
    async initTimeline() {
      await this.$nextTick();
      if (this.timeline) {
        return;
      }
      this.timeline = new Timeline(
        this.$refs.timeline,
        this.events,
        this.$config.TIMELINE_OPTIONS
      );
      this.timeline.setOptions({
        zoomable: this.$config.device.isTouchDevice,
      });
      const now = DateTime.local();
      this.timeline.setWindow(
        now.minus(this.$config.INITIAL_WINDOW).toISODate(),
        now.plus(this.$config.INITIAL_WINDOW).toISODate()
      );
      this.timeline.on("rangechange", (args) => {
        this.$emit("rangechange", args);
      });
      this.timeline.on("rangechanged", (args) => {
        const interval = Interval.fromDateTimes(
          DateTime.fromJSDate(args.start),
          DateTime.fromJSDate(args.end)
        );
        const currentTime = interval.divideEqually(2)[0].end;
        this.$emit("rangechanged", { ...args, currentTime });
      });
      this.timeline.on("changed", () => this.selectActiveEvent());
    },
    hasEvent(id) {
      return this.timeline.itemsData.getIds().includes(Number.parseInt(id));
    },
    async addEvent(id) {
      if (this.hasEvent(id)) {
        return;
      }
      const { data: event } = await this.$axios.get(`/events/${id}/`);
      this.timeline.itemsData.add(event);
    },
    selectActiveEvent() {
      Array.from(document.querySelectorAll(".vis-item")).forEach((item) =>
        item.classList.remove("vis-selected")
      );
      const eventEl = document.querySelector(
        `[data-event-id="${this.$route.query.activeEvent}"]`
      );
      if (eventEl) {
        eventEl.closest(".vis-item").classList.add("vis-selected");
      }
    },
    zoomIn() {
      this.timeline.zoomIn(this.$config.ZOOM_STEP);
    },
    zoomOut() {
      this.timeline.zoomOut(this.$config.ZOOM_STEP);
    },
    goToToday() {
      this.timeline.moveTo(DateTime.local().toJSDate());
    },
    setWindow(...args) {
      this.timeline.setWindow(...args);
    },
    reset() {
      this.timeline.itemsData.clear();
    },
  },
});
</script>
