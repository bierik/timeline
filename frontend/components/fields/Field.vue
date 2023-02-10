<template>
  <label class="flex flex-col items-start">
    <span class="block text-gray-500 font-bold">{{ label }}</span>
    <slot />
    <span class="text-red-600">{{ errorText }}</span>
  </label>
</template>

<script>
export default {
  name: 'Field',
  props: {
    errors: {
      type: Array,
      default: () => [],
    },
    label: {
      type: String,
      default: () => '',
    },
  },
  computed: {
    errorText() {
      return this.errors.join('')
    },
  },
}
</script>
