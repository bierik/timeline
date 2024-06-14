<template>
  <button
    v-bind="$attrs"
    class="flex items-center justify-center rounded-lg bg-gray-500 px-4 py-2 leading-tight text-white hover:bg-gray-400 focus:bg-gray-400 focus:outline-none"
  >
    <slot />
  </button>
</template>

<script>
export default {
  inheritAttrs: false,
};
</script>
