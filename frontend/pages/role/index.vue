<template>
  <Layout narrow>
    <template #append>
      <nuxt-link to="/role/new" class="flex items-center text-white px-4 hover:bg-primary-400 h-full">
        <feather type="plus" size="18" />
        <span class="hidden sm:block ml-1">Hinzufügen</span>
      </nuxt-link>
    </template>
    <div class="container">
      <PersonTabs class="mb-4" />
      <template v-for="role in roles">
        <nuxt-link
          :key="role.id"
          class="flex items-center hover:bg-gray-200 py-6 px-4"
          :to="{ name: 'role-id-edit', params: { id: role.id } }"
        >
          {{ role.name }}
        </nuxt-link>
        <hr :key="`divider-${role.id}`" />
      </template>
    </div>
  </Layout>
</template>

<script>
export default {
  async asyncData({ $axios }) {
    const roles = await $axios.$get('/roles/')
    return { roles }
  },
}
</script>
