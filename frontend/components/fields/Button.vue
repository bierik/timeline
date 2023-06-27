<template>
  <button
    v-bind="$attrs"
    :type="type"
    class="relative flex justify-center items-center rounded-lg py-2 px-4 text-white leading-tight focus:outline-none"
    :disabled="computedDisabled"
    :class="disabled ? 'bg-gray-200' : 'bg-primary-500 focus:bg-primary-400 hover:bg-primary-400'"
    v-on="$listeners"
  >
    <feather v-if="loading" class="absolute" type="loader" size="20" animation="spin" animation-speed="slow" />
    <div :class="{ invisible: loading }" class="flex items-center">
      <slot />
    </div>
  </button>
</template>

<script>
export default {
  inheritAttrs: false,
  props: {
    loading: {
      type: Boolean,
      default: () => false,
    },
    disabled: {
      type: Boolean,
      default: () => false,
    },
    type: {
      type: String,
      default: () => 'button',
    },
  },
  computed: {
    computedDisabled() {
      return this.loading || this.disabled
    },
  },
}
</script>
