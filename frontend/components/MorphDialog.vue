<template>
  <div
    class="absolute bottom-20 max-h-[90dvh] w-[90vw] max-w-96 origin-bottom scale-0 whitespace-normal rounded-xl bg-primary-300 p-2 opacity-0 shadow-flat drop-shadow-xl transition-all duration-300"
    :class="activeClass"
    style="z-index: -1"
  >
    <slot />
  </div>
</template>

<script>
export default {
  name: "MorphDialog",
  props: {
    open: {
      type: Boolean,
      default: () => false,
    },
  },
  computed: {
    activeClass() {
      return this.open ? "scale-100 opacity-100" : "";
    },
  },
};
</script>
