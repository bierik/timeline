<template>
  <div
    class="flex flex-col items-center justify-center"
    :data-event-id="event.id"
  >
    <MorphDialog :open="isActive">
      <div class="flex h-full min-h-16 flex-col pb-10">
        <span
          v-dompurify-html="event.description"
          class="max-h-[50dvh] overflow-y-auto pr-10 text-left text-xs"
        />
        <div class="grow" />
        <div class="mb-2 flex">
          <span
            v-for="relation in event.relations"
            :key="`relation-${relation.id}`"
            class="mr-1 cursor-pointer overflow-x-hidden text-ellipsis whitespace-nowrap rounded-md bg-primary-400 px-2 py-1 text-xs hover:bg-primary-200"
            @click="focusRelation(relation.id)"
          >
            {{ relation.title }}
          </span>
        </div>
        <div class="flex">
          <span
            v-for="person in event.people"
            :key="`person-${person.id}`"
            class="mr-1 flex items-center overflow-x-hidden text-ellipsis whitespace-nowrap rounded-full bg-primary-400 p-1 pr-3 text-xs"
          >
            <img
              width="100"
              height="100"
              class="mr-2 size-6 rounded-full"
              :src="person.image.thumbnail"
            />
            {{ person.name }}
          </span>
        </div>
      </div>
      <Gallery
        v-if="event.has_images"
        class="absolute bottom-0 left-0 size-8 rounded-full object-cover shadow-flat shadow-primary transition-all hover:shadow-flat-lg"
        :images="event.images"
        :thumbnail="event.thumbnail"
      />
      <button
        class="absolute bottom-0 right-0 flex size-8 items-center justify-center rounded-full bg-white p-2 shadow-flat shadow-primary transition-all hover:shadow-flat-lg"
        @click="edit"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="1em"
          height="1em"
          viewBox="0 0 24 24"
        >
          <path
            fill="currentColor"
            fill-rule="evenodd"
            d="M3 18L15 6l3 3L6 21H3zM16 5l2-2l3 3l-2.001 2.001z"
          />
        </svg>
      </button>
      <button
        class="absolute right-0 top-0 flex size-8 items-center justify-center rounded-full bg-white p-2 shadow-flat shadow-primary transition-all hover:shadow-flat-lg"
        @click="closeDialog"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="1em"
          height="1em"
          viewBox="0 0 24 24"
        >
          <path
            fill="currentColor"
            fill-rule="evenodd"
            d="M10.657 12.071L5 6.414L6.414 5l5.657 5.657L17.728 5l1.414 1.414l-5.657 5.657l5.657 5.657l-1.414 1.414l-5.657-5.657l-5.657 5.657L5 17.728z"
          />
        </svg>
      </button>
    </MorphDialog>
    <div
      class="mb-4 flex size-16 cursor-pointer items-center justify-center rounded-full bg-primary-300 text-4xl shadow-flat shadow-primary transition-all hover:shadow-flat-lg"
      @click="openDialog"
    >
      {{ event.icon }}
    </div>
    <div class="bg-black p-2 font-dymo text-sm leading-none text-white">
      {{ event.title }}
    </div>
  </div>
</template>

<script>
export default {
  name: "TimelineEvent",
  inject: ["$router"],
  props: {
    event: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      relations: [],
    };
  },
  computed: {
    isActive() {
      return (
        Number.parseInt(this.$router.currentRoute.value.query.activeEvent) ===
        this.event.id
      );
    },
  },
  methods: {
    edit() {
      this.$router.push({
        name: "event-id-edit",
        params: { id: this.event.id },
      });
    },
    focusRelation(relation) {
      this.$router.push({
        name: "index",
        query: { activeEvent: relation },
      });
      this.$router.push({
        name: "index",
        query: { activeEvent: relation },
      });
    },
    openDialog() {
      this.$router.push({
        name: "index",
        query: { activeEvent: this.event.id },
      });
    },
    closeDialog() {
      this.$router.push({ name: "index" });
    },
  },
};
</script>
