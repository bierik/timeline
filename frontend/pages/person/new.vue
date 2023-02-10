<template>
  <Layout>
    <div class="container">
      <h1 class="text-xl mb-4 font-bold">Neue Person hinzfügen</h1>
      <Form :errors.sync="errors" :save="save" :cancel="cancel" @success="success">
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
      </Form>
    </div>
  </Layout>
</template>

<script>
import formErrorMixin from '@/components/form/form-error-mixin'

export default {
  mixins: [formErrorMixin],
  async asyncData({ $axios }) {
    const schema = await $axios.$options('/people/')
    return { schema }
  },
  data() {
    return {
      person: {
        name: '',
        role: 1,
        file: null,
      },
    }
  },
  methods: {
    success() {
      this.$toast.success('Person erstellt')
      this.$router.push('/')
    },
    async save() {
      await this.$axios.$post('/people/', this.person)
    },
    cancel() {
      this.$router.push('/')
    },
  },
}
</script>
