<template>
  <Layout narrow>
    <template #append>
      <nuxt-link
        to="/role/new"
        class="flex h-full items-center px-4 text-white hover:bg-primary-400"
      >
        <Icon
          name="feather:plus"
          size="18"
        />
        <span class="ml-1 hidden sm:block">Hinzufügen</span>
      </nuxt-link>
    </template>
    <div class="container">
      <PersonTabs class="mb-4" />
      <template
        v-for="role in roles"
        :key="role.id"
      >
        <nuxt-link
          class="flex items-center px-4 py-6 hover:bg-gray-200"
          :to="{ name: 'role-id-edit', params: { id: role.id } }"
        >
          {{ role.name }}
        </nuxt-link>
        <hr />
      </template>
    </div>
  </Layout>
</template>

<script>
export default defineNuxtComponent({
  async asyncData({ $axios }) {
    const { data: roles } = await $axios.get("/roles/");
    return { roles };
  },
});
</script>
