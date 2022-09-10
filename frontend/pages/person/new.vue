<template>
  <Layout>
    <div class="container">
      <h1 class="text-xl mb-4 font-bold">Neue Person hinzfügen</h1>
      <form class="w-full" @submit.prevent="save" @reset.prevent="reset">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <TextInput v-model="person.name" class="mb-4 block" label="Name" />
          <SelectInput
            v-model="person.role"
            class="mb-4 block"
            label="Rolle"
            :options="schema.actions.POST.role.choices"
          />
          <label class="block">
            <span class="block text-gray-500 font-bold">Bild</span>
            <TUSUpload @uploaded="file = $event" @deleted="file = null" />
          </label>
        </div>
        <Button class="mt-4" type="submit">Speichern</Button>
        <ButtonSecondary class="mt-4" type="reset">Abbrechen</ButtonSecondary>
      </form>
    </div>
  </Layout>
</template>

<script>
export default {
  async asyncData({ $axios }) {
    const schema = await $axios.$options('/people/')
    return { schema }
  },
  data() {
    return {
      file: null,
      person: {
        name: '',
        role: 1,
      },
    }
  },
  methods: {
    async save() {
      try {
        await this.$axios.$post('/people/', { ...this.person, file: this.file })
        this.$router.push('/person')
        this.$toast.success('Person erstellt')
      } catch (e) {
        this.$toast.error(JSON.stringify(e.response.data))
      }
    },
    reset() {
      this.$router.push('/')
    },
  },
}
</script>
