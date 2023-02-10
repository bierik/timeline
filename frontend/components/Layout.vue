<template>
  <div>
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
          <feather class="mr-1" size="20" type="calendar" />
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
        <nuxt-link
          to="/settings"
          class="flex items-center text-white px-4 hover:bg-primary-400 h-full"
          active-class="bg-primary-400"
        >
          <feather class="mr-1" size="20" type="settings" />
          <span class="hidden sm:block">Einstellungen</span>
        </nuxt-link>
        <div class="grow" />
        <slot name="append" />
      </div>
    </div>
    <div :class="narrow ? '' : 'py-12'">
      <slot />
    </div>
  </div>
</template>
<script>
export default {
  props: {
    narrow: {
      type: Boolean,
      default: () => false,
    },
  },
}
</script>
