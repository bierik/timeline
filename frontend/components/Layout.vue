<template>
  <div class="flex flex-col min-h-dvh">
    <div class="bg-primary h-12 sticky top-0 z-30">
      <div class="container items-stretch flex h-full">
        <nuxt-link
          :to="{ name: 'event-timeline' }"
          class="flex items-center text-white px-4 hover:bg-primary-400 h-full"
          active-class="bg-primary-400"
        >
          <feather size="20" type="calendar" />
          <span class="hidden sm:block ml-1">Timeline</span>
        </nuxt-link>
        <nuxt-link
          :to="{ name: 'event-list' }"
          class="flex items-center text-white px-4 hover:bg-primary-400 h-full"
          active-class="bg-primary-400"
        >
          <feather size="20" type="list" />
          <span class="hidden sm:block ml-1">Ereignisse</span>
        </nuxt-link>
        <nuxt-link
          :to="{ name: 'person' }"
          :exact="false"
          class="flex items-center text-white px-4 hover:bg-primary-400 h-full"
          :class="{ 'bg-primary-400': ['/person', '/role'].includes($route.fullPath) }"
        >
          <feather size="20" type="user" />
          <span class="hidden sm:block ml-1">Personen</span>
        </nuxt-link>
        <div class="grow" />
        <slot name="append" />
        <div class="flex items-center">
          <nuxt-link :to="{ name: 'user' }" class="mx-4 bg-white w-7 h-7 rounded-full flex items-center justify-center">
            <span v-if="hasSignature">{{ userSignature }}</span>
            <feather v-else size="20" type="user" />
          </nuxt-link>
        </div>
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
      return [
        first(Array.from(this.$auth.user.first_name || '')),
        first(Array.from(this.$auth.user.last_name || '')),
      ].join('')
    },
    hasSignature() {
      return !!this.userSignature
    },
  },
}
</script>
