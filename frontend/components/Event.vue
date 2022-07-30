<template>
  <div
    class="flex flex-col justify-center items-center"
    :class="{ 'active-event': isActive }"
    :data-event-id="event.id"
  >
    <MorphDialog :open="isActive">
      <div class="flex flex-col h-full pb-10">
        <span class="text-xs flex-grow" v-html="event.description_html" />
        <div class="flex">
          <span
            v-for="relation in event.relations"
            :key="`relation-${relation.id}`"
            class="bg-primary-400 rounded-md px-2 py-1 text-xs mr-1 whitespace-nowrap overflow-x-hidden overflow-ellipsis"
            @click="focusRelation(relation.id)"
          >
            {{ relation.title }}
          </span>
        </div>
      </div>
      <Gallery
        v-if="event.has_images"
        class="bottom-0 left-0 w-8 h-8"
        :images="event.images"
        :thumbnail="event.thumbnail"
      />
      <button
        class="flex transition-all rounded-full p-2 absolute w-8 h-8 bottom-0 right-0 bg-white shadow-flat shadow-primary justify-center items-center hover:shadow-flat-lg bg-primary-300"
        @click="edit"
      >
        <feather type="edit-2" size="15" />
      </button>
      <button
        class="flex transition-all rounded-full p-2 absolute w-8 h-8 top-0 right-0 bg-white shadow-flat shadow-primary justify-center items-center hover:shadow-flat-lg bg-primary-300"
        @click="closeDialog"
      >
        <feather type="x" size="15" />
      </button>
    </MorphDialog>
    <div
      class="rounded-full w-16 h-16 mb-4 flex justify-center items-center text-4xl bg-primary-300 shadow-flat shadow-primary hover:shadow-flat-lg transition-all"
      @click="openDialog"
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
    $router: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      relations: [],
    }
  },
  computed: {
    isActive() {
      return Number.parseInt(this.$router.currentRoute.query.activeEvent) === this.event.id
    },
  },
  methods: {
    edit() {
      this.$router.push({
        name: 'event-id-edit',
        params: { id: this.event.id },
      })
    },
    focusRelation(relation) {
      this.$router.push({ name: 'index', query: { activeEvent: relation } })
      this.$router.push({ name: 'index', query: { activeEvent: relation } })
    },
    openDialog() {
      this.$router.push({ name: 'index', query: { activeEvent: this.event.id } })
    },
    closeDialog() {
      this.$router.push({ name: 'index' })
    },
  },
}
</script>
