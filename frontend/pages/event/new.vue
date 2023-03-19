<template>
  <Layout>
    <div class="container px-4">
      <h1 class="text-xl mb-4 font-bold">Neues Ereignis hinzfügen</h1>
      <Form :errors.sync="errors" class="w-full" :save="save" :cancel="cancel" @success="success">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <TextInput v-model="event.title" :errors="errorsForField('title')" class="mb-4 block" label="Titel" />
          <DateInput v-model="event.date" :errors="errorsForField('date')" label="Datum" class="mb-4 block" />
          <TextInput v-model="event.icon" :errors="errorsForField('icon')" label="Icon" class="mb-4 block" />
          <EventField
            v-model="event.relations"
            :errors="errorsForField('relations')"
            label="Verknüpfungen"
            class="mb-4"
          />
          <PersonField v-model="event.people" :errors="errorsForField('people')" label="Personen" class="mb-4" />
          <MultiTUSUpload v-model="event.images" :errors="errorsForField('images')" label="Bilder" />
        </div>
        <label>
          <span class="block text-gray-500 font-bold">Beschreibung</span>
          <Editor v-model="event.description" />
        </label>
      </Form>
    </div>
  </Layout>
</template>

<script>
import DateTime from 'luxon/src/datetime'
import formErrorMixin from '@/components/form/form-error-mixin'

export default {
  mixins: [formErrorMixin],
  data() {
    return {
      event: {
        title: '',
        description: null,
        date: DateTime.local().toISODate(),
        icon: '',
        people: [],
        relations: [],
        images: [],
      },
    }
  },
  methods: {
    success() {
      this.$toast.success('Ereignis erstellt')
      this.$router.push('/')
    },
    async save() {
      await this.$axios.$post('/events/', this.event)
    },
    cancel() {
      this.$router.push('/')
    },
  },
}
</script>
