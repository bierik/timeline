<template>
  <div>
    <slot
      name="activator"
      v-bind="{ on: { click: open } }"
    />
    <div
      class="group"
      :class="isOpen ? '' : 'bottom-nav-close'"
    >
      <div
        class="fixed inset-x-0 bottom-0 z-30 transition-transform group-[.bottom-nav-close]:translate-y-full"
        @click="close"
      >
        <slot />
      </div>
      <div
        class="fixed inset-0 z-20 bg-black opacity-60 transition-opacity group-[.bottom-nav-close]:opacity-0"
        :class="isOpen ? '' : 'pointer-events-none'"
        @click="close"
      />
    </div>
  </div>
</template>

<script>
import { escapeable, modalable } from "@/mixins/modal";

export default defineNuxtComponent({
  name: "Bottomnav",
  mixins: [escapeable("close"), modalable("isOpen")],
  data() {
    return {
      isOpen: false,
    };
  },
  beforeUnmount() {
    this.unlockModal();
  },
  methods: {
    close() {
      this.isOpen = false;
    },
    open() {
      this.isOpen = true;
    },
  },
});
</script>
