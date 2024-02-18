<template>
  <div>
    <slot name="activator" v-bind="{ on: { click: open } }" />
    <div class="group" :class="isOpen ? '' : 'bottom-nav-close'">
      <div
        class="z-30 fixed bottom-0 left-0 right-0 group-[.bottom-nav-close]:translate-y-full transition-transform"
        @click="close"
      >
        <slot />
      </div>
      <div
        class="transition-opacity z-20 fixed inset-0 bg-black opacity-60 group-[.bottom-nav-close]:opacity-0"
        :class="isOpen ? '' : 'pointer-events-none'"
        @click="close"
      />
    </div>
  </div>
</template>
<script>
import { escapeable, modalable } from '@/components/mixins'

export default {
  name: 'Bottomnav',
  mixins: [escapeable('close'), modalable('isOpen')],
  data() {
    return {
      isOpen: false,
    }
  },
  beforeDestroy() {
    this.unlockModal()
  },
  methods: {
    close() {
      this.isOpen = false
    },
    open() {
      this.isOpen = true
    },
  },
}
</script>
