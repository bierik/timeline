<template>
  <Layout>
    <template #append>
      <button
        class="flex h-full items-center px-4 text-white hover:bg-primary-400"
        @click="filterDrawer = true"
      >
        <Icon name="feather:filter" size="18" />
        <span class="ml-1 hidden sm:block">Filter</span>
      </button>
      <Bottomnav>
        <template #activator="{ on }">
          <button
            class="flex h-full items-center px-4 text-white hover:bg-primary-400"
            v-on="on"
          >
            <Icon name="feather:plus" size="18" />
            <span class="ml-1 hidden sm:block">Hinzufügen</span>
          </button>
        </template>
        <div class="bg-white">
          <nuxt-link
            to="/event/new"
            class="flex h-full items-center p-4 hover:bg-gray-200"
          >
            <Icon name="feather:plus" size="18" />
            <span class="ml-1">Hinzufügen</span>
          </nuxt-link>
          <hr />
          <nuxt-link
            class="flex h-full items-center p-4 hover:bg-gray-200"
            :to="{ name: 'import' }"
          >
            <Icon name="feather:upload" size="18" />
            <span class="ml-1">Import</span>
          </nuxt-link>
        </div>
      </Bottomnav>
    </template>
    <NavigationDrawer v-model="filterDrawer">
      <div class="p-4">
        <TextInput
          class="mb-2"
          label="Titel"
          :model-value="filter.title"
          @update:model-value="applyFilter({ title: $event })"
        />
        <DateInput
          class="mb-2"
          label="Von"
          :model-value="filter.date_after"
          @update:model-value="applyFilter({ date_after: $event })"
        />
        <DateInput
          class="mb-2"
          label="Bis"
          :model-value="filter.date_before"
          @update:model-value="applyFilter({ date_before: $event })"
        />
        <PersonField
          label="Personen"
          :model-value="filter.people"
          @update:model-value="applyFilter({ people: $event })"
        />
      </div>
    </NavigationDrawer>
    <div class="container">
      <ul>
        <li v-for="event in events" :key="event.id">
          <nuxt-link
            class="flex items-center justify-between p-4 hover:bg-gray-200"
            :to="{ name: 'event-id-edit', params: { id: event.id } }"
          >
            <div class="text-3xl">{{ event.icon }}</div>
            <div
              class="flex h-full grow flex-col place-content-center"
              :class="{ 'pl-4': !!event.icon, 'pr-4': !!event.has_images }"
            >
              <span class="break-all">{{ event.title }}</span>
              <small class="text-xs">{{
                $toLocaleDateString(event.date)
              }}</small>
              <div>
                <nuxt-link
                  class="inline-flex items-center text-blue-400 underline"
                  :to="{
                    name: 'index',
                    query: { activeEvent: event.id },
                  }"
                >
                  <Icon class="mr-1" size="15" name="feather:map-pin" />
                  <small>Timeline</small>
                </nuxt-link>
              </div>
            </div>
            <Gallery
              v-if="event.has_images"
              :images="event.images"
              :thumbnail="event.thumbnail"
              class="size-20 rounded-full"
            />
          </nuxt-link>
          <hr />
        </li>
      </ul>
      <div ref="infiniteScrollAnchor" class="invisible" />
    </div>
  </Layout>
</template>

<script>
import debounce from "lodash/debounce";
import isEmpty from "lodash/isEmpty";
import isNull from "lodash/isNull";
import negate from "lodash/negate";
import pickBy from "lodash/pickBy";

export default defineNuxtComponent({
  data() {
    return {
      filterDrawer: false,
      events: [],
      nextLink: undefined,
      filter: {
        ordering: "-date",
        people: [],
        title: "",
        date_after: null,
        date_before: null,
      },
    };
  },
  async mounted() {
    await this.performSearch();
    this.infiniteScrollObserver = new IntersectionObserver(this.nextPage, {
      root: null,
    });
    this.infiniteScrollObserver.observe(this.$refs.infiniteScrollAnchor);
  },
  beforeUnmount() {
    this.infiniteScrollObserver.disconnect();
  },
  methods: {
    nextPage(event) {
      if (!event[0].isIntersecting) {
        return;
      }
      if (isNull(this.nextLink)) {
        return;
      }
      this.performSearch();
    },
    async performSearch() {
      const response = this.nextLink
        ? (await this.$axios.get(this.nextLink)).data
        : (
            await this.$axios.get("/events/", {
              params: pickBy(this.filter, negate(isEmpty)),
            })
          ).data;
      this.events = this.nextLink
        ? [...this.events, ...response.results]
        : response.results;
      this.nextLink = response.next;
    },
    applyFilterDebounced: debounce(
      async function applyFilter(filter) {
        this.nextLink = undefined;
        this.filter = { ...this.filter, ...filter };
        await this.performSearch();
      },
      200,
      { leading: true, trailing: false }
    ),
    async applyFilter(filter) {
      try {
        await this.applyFilterDebounced(filter);
      } catch (error) {
        if (error !== "canceled") {
          throw error;
        }
      }
    },
  },
});
</script>
