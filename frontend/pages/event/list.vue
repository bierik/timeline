<template>
  <Layout narrow>
    <template #append>
      <nuxt-link to="/event/new" class="flex items-center text-white px-4 hover:bg-primary-400 h-full">
        <feather type="plus" size="18" class="mr-1" />
        <span class="hidden sm:block">Hinzufügen</span>
      </nuxt-link>
    </template>
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
import isNull from 'lodash/isNull'
import isUndefined from 'lodash/isUndefined'

export default {
  data() {
    return {
      events: [],
      nextLink: undefined,
    }
  },
  mounted() {
    this.infiniteScrollObserver = new IntersectionObserver(this.loadMoreEvents, {
      root: null,
    })
    this.infiniteScrollObserver.observe(this.$refs.infiniteScrollAnchor)
  },
  beforeDestroy() {
    this.infiniteScrollObserver.disconnect()
  },
  methods: {
    async loadMoreEvents(event) {
      if (!event[0].isIntersecting) {
        return
      }
      if (isUndefined(this.nextLink)) {
        const response = await this.$axios.$get('/events/', { params: { ordering: '-date' } })
        this.nextLink = response.next
        this.events = [...this.events, ...response.results]
      } else if (!isNull(this.nextLink)) {
        const response = await this.$axios.$get(this.nextLink)
        this.nextLink = response.next
        this.events = [...this.events, ...response.results]
      }
    },
  },
}
</script>
