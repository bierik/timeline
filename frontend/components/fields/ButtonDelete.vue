<template>
  <button
    v-bind="$attrs"
    class="bg-red-500 rounded-lg py-2 px-4 text-white leading-tight focus:outline-none focus:bg-red-400 hover:bg-red-400 flex items-center justify-center"
    type="button"
    v-on="$listeners"
  >
    <feather size="20" type="trash" />
  </button>
</template>

<script>
export default {
  inheritAttrs: false,
}
</script>
