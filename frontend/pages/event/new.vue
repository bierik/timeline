<template>
  <Layout>
    <div class="container px-4">
      <h1 class="text-xl mb-4 font-bold">Neues Ereignis hinzfügen</h1>
      <Form :errors.sync="errors" class="w-full" :save="save" :cancel="cancel" @success="success">
        <div class="flex gap-4">
          <TextInput v-model="event.title" :errors="errorsForField('title')" class="mb-4 block grow" label="Titel" />
          <EmojiField v-model="event.icon" label="Icon" :errors="errorsForField('icon')" content-class="mb-4 block" />
          <DateInput v-model="event.date" :errors="errorsForField('date')" label="Datum" class="mb-4 block grow" />
        </div>
        <div class="flex gap-4">
          <EventField
            v-model="event.relations"
            :errors="errorsForField('relations')"
            label="Verknüpfungen"
            class="mb-4 grow"
          />
          <PersonField v-model="event.people" :errors="errorsForField('people')" label="Personen" class="mb-4 grow" />
        </div>
        <div class="flex gap-4">
          <MultiTUSUpload v-model="event.images" class="grow mb-4" :errors="errorsForField('images')" label="Bilder" />
        </div>
        <div class="flex gap-4">
          <label class="grow">
            <span class="block text-gray-500 font-bold">Beschreibung</span>
            <Editor v-model="event.description" />
          </label>
        </div>
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
