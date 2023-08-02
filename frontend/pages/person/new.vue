<template>
  <Layout>
    <div class="container px-4">
      <h1 class="text-xl mb-4 font-bold">Neue Person hinzfügen</h1>
      <Form :errors.sync="errors" :save="save" :cancel="cancel" @success="success">
        <div class="flex gap-4">
          <TextInput v-model="person.name" :errors="errorsForField('name')" class="mb-4 block grow" label="Name" />
          <SelectInput
            v-model="person.role"
            :errors="errorsForField('role')"
            class="mb-4 block grow"
            label="Rolle"
            :options="schema.actions.POST.role.choices"
          />
        </div>
        <div class="flex gap-4">
          <TUSUpload v-model="person.image" class="grow" :errors="errorsForField('image')" label="Bild" />
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
        image: null,
      },
    }
  },
  methods: {
    success() {
      this.$toast.success('Person erstellt')
      this.$router.push({ name: 'person' })
    },
    async save() {
      await this.$axios.$post('/people/', this.person)
    },
    cancel() {
      this.$router.push({ name: 'person' })
    },
  },
}
</script>
