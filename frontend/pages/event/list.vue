<template>
  <Layout narrow>
    <template #append>
      <nuxt-link to="/event/new" class="flex items-center text-white px-4 hover:bg-primary-400 h-full">
        <feather type="plus" size="18" class="mr-1" />
        <span class="hidden sm:block">Hinzufügen</span>
      </nuxt-link>
      <nuxt-link class="flex items-center text-white px-4 hover:bg-primary-400 h-full" :to="{ name: 'import' }">
        <feather type="upload" size="18" class="mr-1" />
        <span class="hidden sm:block">Import</span>
      </nuxt-link>
      <button class="flex items-center text-white px-4 hover:bg-primary-400 h-full" @click="filterDrawer = true">
        <feather type="filter" size="18" class="mr-1" />
        <span class="hidden sm:block">Filter</span>
      </button>
    </template>
    <NavigationDrawer v-model="filterDrawer">
      <div class="p-4">
        <TextInput class="mb-2" label="Titel" :value="filter.title" @input="applyFilter({ title: $event })" />
        <DateInput class="mb-2" label="Von" :value="filter.date_after" @input="applyFilter({ date_after: $event })" />
        <DateInput class="mb-2" label="Bis" :value="filter.date_before" @input="applyFilter({ date_before: $event })" />
        <PersonField label="Personen" :value="filter.people" @input="applyFilter({ people: $event })" />
      </div>
    </NavigationDrawer>
    <div class="container">
      <ul>
        <template v-for="event in events">
          <nuxt-link
            :key="event.id"
            class="hover:bg-gray-200 block"
            :to="{ name: 'event-id-edit', params: { id: event.id } }"
          >
            <li class="flex items-center justify-between py-6 px-4">
              <div class="text-7xl">{{ event.icon }}</div>
              <div class="flex flex-col place-content-center h-full flex-grow px-8">
                <span class="text-xl">{{ event.title }}</span>
                <small>{{ event.date | toLocaleDateString }}</small>
                <div>
                  <nuxt-link
                    class="underline text-blue-400 inline-flex items-center"
                    :to="{ name: 'event-timeline', query: { activeEvent: event.id } }"
                  >
                    <feather class="mr-1" size="15" type="map-pin" /> <small>Timeline</small>
                  </nuxt-link>
                </div>
              </div>
              <Gallery
                v-if="event.has_images"
                :images="event.images"
                :thumbnail="event.thumbnail"
                class="rounded-full"
              />
            </li>
          </nuxt-link>
          <hr :key="`divider-${event.id}`" />
        </template>
      </ul>
      <div ref="infiniteScrollAnchor" class="invisible" />
    </div>
  </Layout>
</template>

<script>
import debounce from 'debounce-async'
import isEmpty from 'lodash/isEmpty'
import isNull from 'lodash/isNull'
import negate from 'lodash/negate'
import pickBy from 'lodash/pickBy'

export default {
  data() {
    return {
      filterDrawer: false,
      events: [],
      nextLink: undefined,
      filter: { ordering: '-date', people: [], title: '', date_after: null, date_before: null },
    }
  },
  async mounted() {
    await this.performSearch()
    this.infiniteScrollObserver = new IntersectionObserver(this.nextPage, {
      root: null,
    })
    this.infiniteScrollObserver.observe(this.$refs.infiniteScrollAnchor)
  },
  beforeDestroy() {
    this.infiniteScrollObserver.disconnect()
  },
  methods: {
    nextPage(event) {
      if (!event[0].isIntersecting) {
        return
      }
      if (isNull(this.nextLink)) {
        return
      }
      this.performSearch()
    },
    async performSearch() {
      const response = this.nextLink
        ? await this.$axios.$get(this.nextLink)
        : await this.$axios.$get('/events/', { params: pickBy(this.filter, negate(isEmpty)) })
      this.events = this.nextLink ? [...this.events, ...response.results] : response.results
      this.nextLink = response.next
    },
    applyFilterDebounced: debounce(async function applyFilter(filter) {
      this.nextLink = undefined
      this.filter = { ...this.filter, ...filter }
      await this.performSearch()
    }, 200),
    async applyFilter(filter) {
      try {
        await this.applyFilterDebounced(filter)
      } catch (error) {
        if (error !== 'canceled') {
          throw error
        }
      }
    },
  },
}
</script>
