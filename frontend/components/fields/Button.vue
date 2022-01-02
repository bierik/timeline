<template>
  <button
    v-bind="$attrs"
    class="bg-primary-300 rounded-lg py-2 px-4 text-white leading-tight focus:outline-none focus:bg-primary-400"
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
