<template>
  <div class="flex min-h-dvh flex-col">
    <div class="sticky top-0 z-30 h-12 bg-primary">
      <div class="container flex h-full items-stretch">
        <nuxt-link
          :to="{ name: 'index' }"
          class="flex h-full items-center px-4 text-white hover:bg-primary-400"
          active-class="bg-primary-400"
        >
          <Icon
            name="feather:calendar"
            size="20"
          />
          <span class="ml-1 hidden sm:block">Timeline</span>
        </nuxt-link>
        <nuxt-link
          :to="{ name: 'event-list' }"
          class="flex h-full items-center px-4 text-white hover:bg-primary-400"
          active-class="bg-primary-400"
        >
          <Icon
            size="20"
            name="feather:list"
          />
          <span class="ml-1 hidden sm:block">Ereignisse</span>
        </nuxt-link>
        <nuxt-link
          :to="{ name: 'person' }"
          :exact="false"
          class="flex h-full items-center px-4 text-white hover:bg-primary-400"
          :class="{
            'bg-primary-400': ['/person', '/role'].includes($route.fullPath),
          }"
        >
          <Icon
            size="20"
            name="feather:user"
          />
          <span class="ml-1 hidden sm:block">Personen</span>
        </nuxt-link>
        <div class="grow" />
        <slot name="append" />
        <div class="flex items-center">
          <nuxt-link
            :to="{ name: 'user' }"
            class="mx-4 flex size-7 items-center justify-center rounded-full bg-white"
          >
            <span v-if="hasSignature">{{ signature }}</span>
            <Icon
              v-else
              size="20"
              name="feather:user"
            />
          </nuxt-link>
        </div>
      </div>
    </div>
    <div
      :class="narrow ? '' : 'py-4'"
      class="grow"
    >
      <slot />
    </div>
  </div>
</template>

<script>
import { mapState } from "pinia";
import { useAuthStore } from "@/store/auth";

export default {
  props: {
    narrow: {
      type: Boolean,
      default: () => false,
    },
  },
  computed: {
    ...mapState(useAuthStore, ["user", "signature"]),
    hasSignature() {
      return !!this.signature;
    },
  },
};
</script>
