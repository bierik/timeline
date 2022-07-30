<template>
  <div class="w-full h-full flex flex-col bg-white p-3">
    <span>{{ title }}</span>
    <span>{{ description }}</span>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: () => '',
    },
    description: {
      type: String,
      default: () => '',
    },
  },
}
</script>
