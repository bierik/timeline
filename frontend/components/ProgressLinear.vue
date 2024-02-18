<template>
  <div class="w-full bg-gray-500 rounded relative">
    <div :class="sizeClass" class="bg-primary-500 rounded" :style="barWidthStyle" />
    <span class="absolute text-xs left-1/2 -translate-x-1/2 top-0 text-white">{{ progressText }}</span>
  </div>
</template>
<script>
export default {
  name: 'ProgressLinear',
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
      return `p-${this.size}`
    },
    barWidthStyle() {
      return {
        width: `${(this.value / this.max) * 100}%`,
      }
    },
    progressText() {
      return `${this.value} / ${this.max}`
    },
  },
}
</script>
