<template>
  <Layout>
    <div class="container px-4">
      <h1 class="text-xl mb-4 font-bold">Rolle bearbeiten</h1>
      <Form :errors.sync="errors" class="w-full" :save="save" :cancel="cancel" @success="success">
        <TextInput v-model="role.name" :errors="errorsForField('name')" class="mb-4 block grow" label="Name" />
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
    const role = await $axios.$get(`/roles/${route.params.id}/`)
    return { role }
  },
  methods: {
    success() {
      this.$toast.success('Rolle bearbeitet')
      this.$router.push({ name: 'role', query: this.$route.query })
    },
    async save() {
      await this.$axios.$patch(`/roles/${this.role.id}/`, this.role)
    },
    cancel() {
      this.$router.push({ name: 'role', query: this.$route.query })
    },
    async remove() {
      try {
        if (window.confirm('Rolle wirklich löschen?')) {
          await this.$axios.$delete(`/roles/${this.role.id}/`)
          this.$router.push({ name: 'role' })
          this.$toast.success('Rolle gelöscht')
        }
      } catch (e) {
        this.$toast.error(JSON.stringify(e.response.data))
      }
    },
  },
}
</script>
