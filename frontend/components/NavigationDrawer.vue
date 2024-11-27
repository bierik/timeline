<template>
  <div
    class="group"
    :class="modelValue ? '' : 'navigation-drawer-close'"
  >
    <div
      class="fixed inset-y-0 right-0 z-50 bg-white transition-transform group-[.navigation-drawer-close]:translate-x-full"
    >
      <slot />
    </div>
    <div
      class="fixed inset-0 z-40 bg-black opacity-60 transition-opacity group-[.navigation-drawer-close]:opacity-0"
      :class="modelValue ? '' : 'pointer-events-none'"
      @click="close"
    />
  </div>
</template>

<script>
import { escapeable, modalable } from "@/mixins/modal";

export default defineNuxtComponent({
  mixins: [escapeable("close"), modalable("modelValue")],
  props: {
    modelValue: {
      type: Boolean,
      default: () => false,
    },
  },
  methods: {
    close() {
      this.$emit("update:model-value", false);
    },
  },
});
</script>
