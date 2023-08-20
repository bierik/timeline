<template>
  <Layout narrow>
    <template #append>
      <nuxt-link to="/person/new" class="flex items-center text-white px-4 hover:bg-primary-400 h-full">
        <feather type="plus" size="18" />
        <span class="hidden sm:block ml-1">Hinzufügen</span>
      </nuxt-link>
    </template>
    <div class="container">
      <template v-for="person in people">
        <nuxt-link
          :key="person.id"
          class="flex items-center hover:bg-gray-200 block py-6 px-4"
          :to="{ name: 'person-id-edit', params: { id: person.id } }"
        >
          <img :src="person.image.thumbnail" class="rounded-full mr-6" />
          <div class="flex flex-col place-content-center h-full">
            <span class="text-xl">{{ person.name }}</span>
            <small>{{ person.role_display }}</small>
          </div>
        </nuxt-link>
        <hr :key="`divider-${person.id}`" />
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
}
</script>
