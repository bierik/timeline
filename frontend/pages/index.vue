<template>
  <Layout narrow>
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
    <MonthSelector
      :model-value="monthFilter"
      class="fixed z-10"
      @update:model-value="setTimelineTime"
    />
    <Timeline
      ref="timeline"
      :events="events"
      class="h-[calc(100dvh_-_3rem)]"
      @rangechanged="setMonthFilter"
      @rangechange="fetchEventsForTimeline"
    />
    <NavigationDrawer v-model="filterDrawer">
      <div class="p-4">
        <TextInput
          class="mb-2"
          label="Titel"
          :model-value="filter.title"
          @update:model-value="applyFilter({ title: $event })"
        />
        <PersonField
          label="Personen"
          :model-value="filter.people"
          @update:model-value="applyFilter({ people: $event })"
        />
      </div>
    </NavigationDrawer>
  </Layout>
</template>

<script>
import debounce from "lodash/debounce";
import { DateTime } from "luxon";

export default defineNuxtComponent({
  data() {
    return {
      events: [],
      monthFilter: DateTime.local(),
      filterDrawer: false,
      filter: { title: "", people: [], start: null, end: null },
    };
  },
  methods: {
    setMonthFilter({ currentTime }) {
      this.monthFilter = currentTime;
    },
    setTimelineTime(monthFilter) {
      this.$refs.timeline.setWindow(
        monthFilter.startOf("month").toJSDate(),
        monthFilter
          .startOf("month")
          .plus(this.$config.RUNTIME_WINDOW_SPAN)
          .toJSDate()
      );
    },
    applyFilter(filter) {
      this.filter = { ...this.filter, ...filter };
      this.$refs.timeline.reset();
      this.fetchEventsForTimeline();
    },
    fetchEventsDebounced: debounce(
      async function fetchEventsDebounced(params) {
        const response = await this.$axios.get("/events/", { params });
        return response;
      },
      200,
      { leading: true, trailing: false }
    ),
    async fetchEventsForTimeline({ start, end } = {}) {
      this.filter = {
        ...this.filter,
        start: start || this.filter.start,
        end: end || this.filter.end,
      };
      try {
        this.events = (
          await this.fetchEventsDebounced({
            date_after: DateTime.fromJSDate(start)
              .minus(this.$config.FETCH_PADDING)
              .toISODate(),
            date_before: DateTime.fromJSDate(end)
              .plus(this.$config.FETCH_PADDING)
              .toISODate(),
            ordering: "-date",
            ...this.filter,
          })
        ).data.results;
      } catch (error) {
        if (error !== "canceled") {
          throw error;
        }
      }
    },
  },
});
</script>
