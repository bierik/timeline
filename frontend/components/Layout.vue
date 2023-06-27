<template>
  <div class="flex flex-col min-h-screen">
    <div class="bg-primary h-12 sticky top-0 z-10">
      <div class="container items-center flex h-full">
        <nuxt-link
          :to="{ name: 'event-timeline' }"
          class="flex items-center text-white px-4 hover:bg-primary-400 h-full"
          active-class="bg-primary-400"
        >
          <feather class="mr-1" size="20" type="calendar" />
          <span class="hidden sm:block">Timeline</span>
        </nuxt-link>
        <nuxt-link
          :to="{ name: 'event-list' }"
          class="flex items-center text-white px-4 hover:bg-primary-400 h-full"
          active-class="bg-primary-400"
        >
          <feather class="mr-1" size="20" type="list" />
          <span class="hidden sm:block">Ereignisse</span>
        </nuxt-link>
        <nuxt-link
          to="/person"
          class="flex items-center text-white px-4 hover:bg-primary-400 h-full"
          active-class="bg-primary-400"
        >
          <feather class="mr-1" size="20" type="user" />
          <span class="hidden sm:block">Personen</span>
        </nuxt-link>
        <div class="grow" />
        <slot name="append" />
        <nuxt-link
          :to="{ name: 'user' }"
          class="block mx-4 bg-white w-9 h-9 rounded-full flex items-center justify-center"
        >
          {{ userSignature }}
        </nuxt-link>
      </div>
    </div>
    <div :class="narrow ? '' : 'py-4'" class="grow">
      <slot />
    </div>
  </div>
</template>
<script>
import first from 'lodash/first'

export default {
  props: {
    narrow: {
      type: Boolean,
      default: () => false,
    },
  },
  computed: {
    userSignature() {
      return [first(Array.from(this.$auth.user.first_name)), first(Array.from(this.$auth.user.last_name))].join('')
    },
  },
}
</script>
