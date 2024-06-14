<template>
  <div class="relative w-full rounded bg-gray-500">
    <div
      :class="sizeClass"
      class="rounded bg-primary-500"
      :style="barWidthStyle"
    />
    <span class="absolute left-1/2 top-0 -translate-x-1/2 text-xs text-white">{{
      progressText
    }}</span>
  </div>
</template>
<script>
export default {
  name: "ProgressLinear",
  props: {
    max: {
      type: Number,
      default: () => 0,
    },
    value: {
      type: Number,
      default: () => 0,
    },
    size: {
      type: Number,
      default: () => 2,
    },
  },
  computed: {
    sizeClass() {
      return `p-${this.size}`;
    },
    barWidthStyle() {
      return {
        width: `${(this.value / this.max) * 100}%`,
      };
    },
    progressText() {
      return `${this.value} / ${this.max}`;
    },
  },
};
</script>
