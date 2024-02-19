<template>
  <div class="group" :class="value ? '' : 'navigation-drawer-close'">
    <div
      class="bg-white z-50 fixed inset-y-0 right-0 group-[.navigation-drawer-close]:translate-x-full transition-transform"
    >
      <slot />
    </div>
    <div
      class="transition-opacity z-40 fixed inset-0 bg-black opacity-60 group-[.navigation-drawer-close]:opacity-0"
      :class="value ? '' : 'pointer-events-none'"
      @click="close"
    />
  </div>
</template>

<script>
import { escapeable, modalable } from '@/mixins/modal'

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
