<template>
  <Layout narrow>
    <template #append>
      <nuxt-link
        to="/person/new"
        class="flex h-full items-center px-4 text-white hover:bg-primary-400"
      >
        <Icon name="feather:plus" size="18" />
        <span class="ml-1 hidden sm:block">Hinzufügen</span>
      </nuxt-link>
    </template>
    <div class="container">
      <PersonTabs class="mb-4" />
      <template v-for="person in people" :key="person.id">
        <nuxt-link
          class="flex items-center px-4 py-6 hover:bg-gray-200"
          :to="{ name: 'person-id-edit', params: { id: person.id } }"
        >
          <Gallery
            :images="[person.image]"
            :thumbnail="person.image.thumbnail"
            class="mr-6 rounded-full"
          />
          <div class="flex h-full flex-col place-content-center">
            <span class="text-xl">{{ person.name }}</span>
            <small>{{ person.role.name }}</small>
          </div>
        </nuxt-link>
        <hr />
      </template>
    </div>
  </Layout>
</template>

<script>
export default defineNuxtComponent({
  async asyncData({ $axios }) {
    const { data: people } = await $axios.get("/people/");
    return { people };
  },
});
</script>
