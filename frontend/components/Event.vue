<template>
  <div class="flex flex-col justify-center items-center" :data-event-id="event.id">
    <MorphDialog :open="isActive">
      <div class="flex flex-col h-full pb-10 min-h-16">
        <span v-dompurify-html="event.description" class="text-left text-xs pr-10 max-h-[50dvh] overflow-y-auto" />
        <div class="grow"></div>
        <div class="flex mb-2">
          <span
            v-for="relation in event.relations"
            :key="`relation-${relation.id}`"
            class="hover:bg-primary-200 bg-primary-400 rounded-md px-2 py-1 text-xs mr-1 whitespace-nowrap overflow-x-hidden overflow-ellipsis cursor-pointer"
            @click="focusRelation(relation.id)"
          >
            {{ relation.title }}
          </span>
        </div>
        <div class="flex">
          <span
            v-for="person in event.people"
            :key="`person-${person.id}`"
            class="flex items-center bg-primary-400 rounded-full p-1 pr-3 text-xs mr-1 whitespace-nowrap overflow-x-hidden overflow-ellipsis"
          >
            <img width="100" height="100" class="w-6 h-6 rounded-full mr-2" :src="person.image.thumbnail" />
            {{ person.name }}
          </span>
        </div>
      </div>
      <Gallery
        v-if="event.has_images"
        class="bottom-0 left-0 w-8 h-8 transition-all rounded-full absolute shadow-flat shadow-primary hover:shadow-flat-lg object-cover"
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
      class="rounded-full w-16 h-16 mb-4 flex justify-center items-center text-4xl bg-primary-300 shadow-flat shadow-primary hover:shadow-flat-lg transition-all cursor-pointer"
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
  },
  data() {
    return {
      relations: [],
    }
  },
  computed: {
    isActive() {
      return Number.parseInt(this.$nuxt.$route.query.activeEvent) === this.event.id
    },
  },
  methods: {
    edit() {
      this.$nuxt.$router.push({
        name: 'event-id-edit',
        params: { id: this.event.id },
      })
    },
    focusRelation(relation) {
      this.$nuxt.$router.push({ name: 'event-timeline', query: { activeEvent: relation } })
      this.$nuxt.$router.push({ name: 'event-timeline', query: { activeEvent: relation } })
    },
    openDialog() {
      this.$nuxt.$router.push({ name: 'event-timeline', query: { activeEvent: this.event.id } })
    },
    closeDialog() {
      this.$nuxt.$router.push({ name: 'event-timeline' })
    },
  },
}
</script>
