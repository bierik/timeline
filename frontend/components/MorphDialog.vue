<template>
  <div
    class="rounded-xl p-2 bg-primary-300 shadow-flat absolute bottom-20 scale-0 origin-bottom opacity-0 transition-all duration-300 w-[90vw] max-w-96 max-h-[90dvh] whitespace-normal drop-shadow-xl"
    :class="activeClass"
    style="z-index: -1"
  >
    <slot />
  </div>
</template>

<script>
export default {
  name: 'MorphDialog',
  props: {
    open: {
      type: Boolean,
      default: () => false,
    },
  },
  computed: {
    activeClass() {
      return this.open ? 'scale-100 opacity-100' : ''
    },
  },
}
</script>
