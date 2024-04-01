<template>
  <Layout>
    <div class="container px-4">
      <h1 class="text-xl mb-4 font-bold">Ereignis bearbeiten</h1>
      <Form :errors.sync="errors" class="w-full" :save="save" :cancel="cancel" @success="success">
        <div class="flex gap-4">
          <TextInput v-model="event.title" class="mb-4 block grow" label="Titel" />
          <EmojiField v-model="event.icon" label="Icon" :errors="errorsForField('icon')" content-class="mb-4 block" />
          <DateInput v-model="event.date" label="Datum" class="mb-4 block grow" />
        </div>
        <div class="flex gap-4">
          <EventField v-model="event.relations" label="Verknüpfungen" class="mb-4 grow" :exclude="excludeFromSearch" />
          <PersonField v-model="event.people" label="Personen" class="mb-4 grow" />
        </div>
        <div class="flex gap-4">
          <TUSUpload
            v-model="event.images"
            multiple
            class="grow mb-4"
            :errors="errorsForField('images')"
            label="Bilder"
          />
        </div>
        <div class="flex gap-4">
          <label class="grow">
            <span class="block text-gray-500 font-bold">Beschreibung</span>
            <Editor v-model="event.description" />
          </label>
        </div>
        <template #action-before>
          <ButtonDelete @click="remove">Löschen</ButtonDelete>
        </template>
      </Form>
    </div>
  </Layout>
</template>

<script>
import omit from 'lodash/omit'
import partialRight from 'lodash/partialRight'
import formErrorMixin from '@/components/form/form-error-mixin'

export default {
  mixins: [formErrorMixin],
  async asyncData({ $axios, route }) {
    const event = await $axios.$get(`/events/${route.params.id}/`)
    return { event }
  },
  computed: {
    excludeFromSearch() {
      return Number.parseInt(this.$route.params.id)
    },
  },
  mounted() {
    this.event.people = this.event.people.map((person) => person.id)
  },
  methods: {
    success() {
      this.$toast.success('Ereignis bearbeitet')
      this.$router.push({ name: 'event-timeline', query: this.$route.query })
    },
    async save() {
      const images = this.event.images.map(partialRight(omit, 'thumbnail'))
      await this.$axios.$patch(`/events/${this.event.id}/`, { ...this.event, images })
    },
    cancel() {
      this.$router.push({ name: 'event-timeline', query: this.$route.query })
    },
    async remove() {
      try {
        if (window.confirm('Ereignis wirklich löschen?')) {
          await this.$axios.$delete(`/events/${this.event.id}/`)
          this.$router.push({ name: 'event-timeline' })
          this.$toast.success('Ereignis gelöscht')
        }
      } catch (e) {
        this.$toast.error(JSON.stringify(e.response.data))
      }
    },
  },
}
</script>
