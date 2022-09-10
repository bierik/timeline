<template>
  <div :class="narrow ? 'pt-12' : 'py-20'">
    <div class="fixed top-0 right-0 left-0 bg-primary h-12">
      <div class="container items-center mx-auto flex h-full">
        <nuxt-link to="/" class="flex items-center text-white px-4 hover:bg-primary-400 h-full">
          <span>Ereignisse</span>
        </nuxt-link>
        <nuxt-link to="/person" class="flex items-center text-white px-4 hover:bg-primary-400 h-full">
          Personen
        </nuxt-link>
        <div class="grow" />
        <slot name="append" />
      </div>
    </div>
    <slot />
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
