<template>
  <Layout narrow>
    <template #append>
      <button
        type="button"
        class="flex h-full items-center px-4 text-white hover:bg-primary-400"
        @click="filterDrawer = true"
      >
        <Icon name="feather:filter" size="18" />
        <span class="ml-1 hidden sm:block">Filter</span>
      </button>
      <Bottomnav>
        <template #activator="{ on }">
          <button
            type="button"
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
      @rangechange="handleRangeChange"
      @ready="handleReady"
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
import throttle from "lodash/throttle";
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
    handleRangeChange({ currentTime, start, end }) {
      this.setMonthFilter(currentTime);
      this.loadEventsThrotteled(start, end);
    },
    async handleReady({ currentTime, start, end }) {
      this.setMonthFilter(currentTime);
      this.loadEvents(start, end);
    },
    setMonthFilter(currentTime) {
      this.monthFilter = currentTime;
    },
    setTimelineTime(monthFilter) {
      this.$refs.timeline.setWindow(
        monthFilter.startOf("month").toJSDate(),
        monthFilter
          .startOf("month")
          .plus(this.$config.RUNTIME_WINDOW_SPAN)
          .toJSDate(),
      );
    },
    applyFilter(filter) {
      this.filter = { ...this.filter, ...filter };
      this.$refs.timeline.reset();
      const { start, end } = this.$refs.timeline.getWindow();
      this.fetchEventsForTimeline(start, end);
    },
    async loadEvents(start, end) {
      const response = await this.$axios.get("/events/", {
        params: {
          date_after: DateTime.fromJSDate(start)
            .minus(this.$config.FETCH_PADDING)
            .toISODate(),
          date_before: DateTime.fromJSDate(end)
            .plus(this.$config.FETCH_PADDING)
            .toISODate(),
          ordering: "-date",
          ...this.filter,
        },
      });
      this.events = response.data.results;
    },
    loadEventsThrotteled: throttle(
      async function fetchEventsThrotteled(start, end) {
        await this.loadEvents(start, end);
      },
      500,
      { leading: false, trailing: true },
    ),
  },
});
</script>
