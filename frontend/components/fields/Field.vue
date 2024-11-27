<template>
  <component
    :is="tag"
    class="flex flex-col items-start"
  >
    <span class="block font-bold text-gray-500">{{ label }}</span>
    <slot />
    <span class="text-red-600">{{ errorText }}</span>
  </component>
</template>

<script>
export default defineNuxtComponent({
  name: "Field",
  props: {
    errors: {
      type: Array,
      default: () => [],
    },
    label: {
      type: String,
      default: () => "",
    },
    tag: {
      type: String,
      default: () => "label",
    },
  },
  computed: {
    errorText() {
      return this.errors.join("");
    },
  },
});
</script>
