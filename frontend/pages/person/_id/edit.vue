<template>
  <Layout>
    <div class="container px-4">
      <h1 class="text-xl mb-4 font-bold">Ereignis bearbeiten</h1>
      <Form :errors.sync="errors" class="w-full" :save="save" :cancel="cancel" @success="success">
        <div class="flex gap-x-4 flex-wrap">
          <TextInput
            v-model="person.name"
            :errors="errorsForField('name')"
            class="mb-4 block grow basis-full md:basis-0"
            label="Name"
          />
          <SelectInput
            v-model="person.role"
            :errors="errorsForField('role')"
            class="mb-4 block grow"
            label="Rolle"
            :options="roleChoices"
          />
        </div>
        <TUSUpload v-model="person.image" class="grow" :errors="errorsForField('image')" label="Bild" />
        <template #action-before>
          <ButtonDelete @click="remove">Löschen</ButtonDelete>
        </template>
      </Form>
    </div>
  </Layout>
</template>

<script>
import omit from 'lodash/omit'
import formErrorMixin from '@/components/form/form-error-mixin'

export default {
  mixins: [formErrorMixin],
  async asyncData({ $axios, route }) {
    const person = await $axios.$get(`/people/${route.params.id}/`)
    person.role = person.role.id
    const roles = await $axios.$get('/roles/')
    const roleChoices = roles.map(({ id, name }) => ({ value: id, display_name: name }))
    return { person, roleChoices }
  },
  methods: {
    success() {
      this.$toast.success('Person bearbeitet')
      this.$router.push({ name: 'person', query: this.$route.query })
    },
    async save() {
      await this.$axios.$patch(`/people/${this.person.id}/`, {
        ...this.person,
        image: omit(this.person.image, 'thumbnail'),
      })
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
