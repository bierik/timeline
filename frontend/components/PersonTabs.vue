<template>
  <div class="grid grid-cols-2">
    <nuxt-link
      :to="{ name: 'person' }"
      active-class="border-b-primary-500"
      class="flex items-center justify-center border-b-2 border-b-primary-200 bg-slate-100 p-4 hover:bg-slate-300"
      >Personen</nuxt-link
    >
    <nuxt-link
      :to="{ name: 'role' }"
      active-class="border-b-primary-500"
      class="flex items-center justify-center border-b-2 border-b-primary-200 bg-slate-100 p-4 hover:bg-slate-300"
      >Rollen</nuxt-link
    >
  </div>
</template>
<script>
export default {
  name: "PersonTabs",
};
</script>
