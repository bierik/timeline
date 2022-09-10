<template>
  <Layout>
    <template #append>
      <nuxt-link to="/person/new" class="flex items-center text-white px-4 hover:bg-primary-400 h-full">
        <feather type="plus" size="18" class="mr-1" />
        <span class="hidden sm:block">Hinzufügen</span>
      </nuxt-link>
    </template>
    <div class="container">
      <h1 class="text-xl mb-4 font-bold">Personen</h1>
      <template v-for="person in people">
        <div :key="person.id" class="flex items-center">
          <img :src="person.image.thumbnail" class="rounded-full mr-6" />
          <div class="flex flex-col place-content-center h-full">
            <span class="text-xl">{{ person.name }}</span>
            <small>{{ person.role_display }}</small>
          </div>
          <div class="grow" />
          <ButtonDelete class="bg-red-500 p-2 flex items-center rounded" @click="remove(person)">
            <feather type="trash" size="18" stroke="white" />
          </ButtonDelete>
        </div>
        <hr :key="`divider-${person.id}`" class="my-4" />
      </template>
    </div>
  </Layout>
</template>

<script>
export default {
  async asyncData({ $axios }) {
    const people = await $axios.$get('/people/')
    return { people }
  },
  methods: {
    async remove(person) {
      try {
        if (window.confirm('Person wirklich löschen?')) {
          await this.$axios.$delete(`/people/${person.id}/`)
          this.$nuxt.refresh()
          this.$toast.success('Person gelöscht')
        }
      } catch (e) {
        this.$toast.error(JSON.stringify(e.response.data))
      }
    },
  },
}
</script>
