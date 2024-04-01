<template>
  <Layout>
    <div class="container px-4">
      <h1 class="text-xl mb-4 font-bold">Neues Ereignis hinzfügen</h1>
      <Form :errors.sync="errors" class="w-full" :save="save" :cancel="cancel" @success="success">
        <div class="flex gap-x-4 flex-wrap">
          <TextInput v-model="event.title" :errors="errorsForField('title')" class="mb-4 block grow" label="Titel" />
          <EmojiField v-model="event.icon" label="Icon" :errors="errorsForField('icon')" content-class="mb-4 block" />
          <DateInput v-model="event.date" :errors="errorsForField('date')" label="Datum" class="mb-4 block grow" />
        </div>
        <div class="flex gap-x-4 flex-wrap">
          <EventField
            v-model="event.relations"
            :errors="errorsForField('relations')"
            label="Verknüpfungen"
            class="mb-4 grow basis-full md:basis-0"
          />
          <PersonField v-model="event.people" :errors="errorsForField('people')" label="Personen" class="mb-4 grow" />
        </div>
        <TUSUpload
          v-model="event.images"
          multiple
          class="grow mb-4"
          :errors="errorsForField('images')"
          label="Bilder"
        />
        <label>
          <span class="block text-gray-500 font-bold">Beschreibung</span>
          <Editor v-model="event.description" />
        </label>
      </Form>
    </div>
  </Layout>
</template>

<script>
import omit from 'lodash/omit'
import partialRight from 'lodash/partialRight'
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
      const images = this.event.images.map(partialRight(omit, 'thumbnail'))
      await this.$axios.$post('/events/', { ...this.event, images })
    },
    cancel() {
      this.$router.push('/')
    },
  },
}
</script>
