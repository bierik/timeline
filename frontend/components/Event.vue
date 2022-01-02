<template>
  <div class="flex flex-col justify-center items-center" @click="dialogOpen = !dialogOpen">
    <MorphDialog :open="dialogOpen" />
    <div
      class="rounded-full w-16 h-16 mb-4 flex justify-center items-center text-4xl bg-primary-300 shadow-flat shadow-primary hover:shadow-flat-lg transition-all"
    >
      {{ icon }}
    </div>
    <div class="bg-black text-white p-2 leading-none text-sm font-dymo">{{ title }}</div>
  </div>
</template>

<script>
export default {
  name: 'TimelineEvent',
  props: {
    title: {
      type: String,
      default: () => '',
    },
    icon: {
      type: String,
      default: () => '',
    },
  },
  data() {
    return {
      dialogOpen: false,
    }
  },
}
</script>
