<template>
  <div class="timeline-tick" :style="tickStyle" />
</template>

<script>
export default {
  name: 'TimelineTick',
  props: {
    major: {
      type: Boolean,
      default: () => false,
    },
  },
  computed: {
    tickHeight() {
      return this.major ? 20 : 10
    },
    tickStyle() {
      return {
        height: `${this.tickHeight}px`,
      }
    },
  },
}
</script>

<style>
.timeline-tick {
  background: black;
  width: 1px;
}
</style>
