<template>
  <button
    v-bind="$attrs"
    class="bg-red-500 rounded-lg py-2 px-4 text-white leading-tight focus:outline-none focus:bg-red-600"
    v-on="$listeners"
  >
    <slot />
  </button>
</template>

<script>
export default {
  inheritAttrs: false,
}
</script>
