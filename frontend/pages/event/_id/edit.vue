<template>
  <Layout>
    <div class="container px-4">
      <h1 class="text-xl mb-4 font-bold">Ereignis bearbeiten</h1>
      <Form :errors.sync="errors" class="w-full" :save="save" :cancel="cancel" @success="success">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <TextInput v-model="event.title" class="mb-4 block" label="Titel" />
          <DateInput v-model="event.date" label="Datum" class="mb-4 block" />
          <EmojiField v-model="event.icon" label="Icon" :errors="errorsForField('icon')" content-class="mb-4 block" />
          <EventField v-model="event.relations" label="Verknüpfungen" class="mb-4" :exclude="excludeFromSearch" />
          <PersonField v-model="event.people" label="Personen" class="mb-4" />
          <div>
            <span class="block text-gray-500 font-bold">Dateien</span>
            <MultiTUSUpload v-model="event.images" />
          </div>
        </div>
        <label>
          <span class="block text-gray-500 font-bold">Beschreibung</span>
          <Editor v-model="event.description" />
        </label>
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
      await this.$axios.$patch(`/events/${this.event.id}/`, this.event)
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
