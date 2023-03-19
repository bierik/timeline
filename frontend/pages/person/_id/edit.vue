<template>
  <Layout>
    <div class="container">
      <h1 class="text-xl mb-4 font-bold">Ereignis bearbeiten</h1>
      <Form :errors.sync="errors" class="w-full" :save="save" :cancel="cancel" @success="success">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <TextInput v-model="person.name" :errors="errorsForField('name')" class="mb-4 block" label="Name" />
          <SelectInput
            v-model="person.role"
            :errors="errorsForField('role')"
            class="mb-4 block"
            label="Rolle"
            :options="schema.actions.POST.role.choices"
          />
          <TUSUpload v-model="person.image" :errors="errorsForField('image')" label="Bild" />
        </div>
        <template #action-before>
          <ButtonDelete @click="remove">Löschen</ButtonDelete>
        </template>
      </Form>
    </div>
  </Layout>
</template>

<script>
import formErrorMixin from '@/components/form/form-error-mixin'

export default {
  mixins: [formErrorMixin],
  async asyncData({ $axios, route }) {
    const person = await $axios.$get(`/people/${route.params.id}/`)
    const schema = await $axios.$options('/people/')
    return { person, schema }
  },
  methods: {
    success() {
      this.$toast.success('Person bearbeitet')
      this.$router.push({ name: 'person', query: this.$route.query })
    },
    async save() {
      await this.$axios.$patch(`/people/${this.person.id}/`, this.person)
    },
    cancel() {
      this.$router.push({ name: 'person', query: this.$route.query })
    },
    async remove() {
      try {
        if (window.confirm('Person wirklich löschen?')) {
          await this.$axios.$delete(`/people/${this.person.id}/`)
          this.$router.push({ name: 'person' })
          this.$toast.success('Person gelöscht')
        }
      } catch (e) {
        this.$toast.error(JSON.stringify(e.response.data))
      }
    },
  },
}
</script>
