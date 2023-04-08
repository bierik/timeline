<template>
  <div class="group" :class="value ? '' : 'navigation-drawer-close'">
    <div
      class="bg-white z-30 fixed inset-y-0 right-0 group-[.navigation-drawer-close]:translate-x-full transition-transform"
    >
      <slot />
    </div>
    <div
      class="transition-opacity z-20 fixed inset-0 bg-black opacity-60 group-[.navigation-drawer-close]:opacity-0"
      :class="value ? '' : 'pointer-events-none'"
      @click="close"
    />
  </div>
</template>

<script>
import { escapeable, modalable } from '@/components/mixins'

export default {
  mixins: [escapeable('close'), modalable('value')],
  props: {
    value: {
      type: Boolean,
      default: () => false,
    },
  },
  methods: {
    close() {
      this.$emit('input', false)
    },
  },
}
</script>
<style>
.navigation-drawer-content {
  background-color: white;
  position: fixed;
  z-index: 30;
  right: 0;
  top: 0;
  bottom: 0;
}

.navigation-drawer-backdrop {
  background-color: rgba(0, 0, 0, 0.4);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 20;
}
</style>
