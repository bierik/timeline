<template>
  <button
    v-bind="$attrs"
    :type="type"
    class="relative flex items-center justify-center rounded-lg px-4 py-2 leading-tight text-white focus:outline-none"
    :disabled="computedDisabled"
    :class="
      disabled
        ? 'bg-gray-200'
        : 'bg-primary-500 focus:bg-primary-400 hover:bg-primary-400'
    "
  >
    <Icon
      v-if="loading"
      class="absolute"
      name="feather:loader"
      size="20"
      animation="spin"
      animation-speed="slow"
    />
    <div :class="{ invisible: loading }" class="flex items-center">
      <slot />
    </div>
  </button>
</template>

<script>
export default {
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
      default: () => "button",
    },
  },
  computed: {
    computedDisabled() {
      return this.loading || this.disabled;
    },
  },
};
</script>
