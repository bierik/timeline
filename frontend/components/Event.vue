<template>
  <div class="flex flex-col justify-center items-center" @click="dialogOpen = !dialogOpen">
    <MorphDialog :open="true">
      <span class="text-xs" v-html="event.description_html" />
      <Gallery v-if="event.thumbnail" :images="event.images" :thumbnail="event.thumbnail" />
      <button
        class="flex rounded-full p-2 absolute -bottom-3 -right-3 bg-white shadow-flat shadow-primary"
        @click="edit"
      >
        <feather type="edit-2" size="20" />
      </button>
    </MorphDialog>
    <div
      class="rounded-full w-16 h-16 mb-4 flex justify-center items-center text-4xl bg-primary-300 shadow-flat shadow-primary hover:shadow-flat-lg transition-all"
    >
      {{ event.icon }}
    </div>
    <div class="bg-black text-white p-2 leading-none text-sm font-dymo">{{ event.title }}</div>
  </div>
</template>

<script>
export default {
  name: 'TimelineEvent',
  props: {
    event: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      dialogOpen: false,
    }
  },
  methods: {
    edit() {
      this.$options.$router.push({ name: 'event-id-edit', params: { id: this.event.id } })
    },
  },
}
</script>
