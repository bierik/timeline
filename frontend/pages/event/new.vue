<template>
  <Layout>
    <div class="container">
      <h1 class="text-xl mb-4 font-bold">Neues Ereignis hinzfügen</h1>
      <form class="w-full" @submit.prevent="save" @reset.prevent="reset">
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <TextInput v-model="event.title" class="mb-4 block" label="Titel" />
          <DateInput v-model="event.date" label="Datum" class="mb-4 block" />
          <TextInput v-model="event.icon" label="Icon" class="mb-4 block" />
          <EventField v-model="event.relations" label="Verknüpfungen" class="mb-4" />
          <PersonField v-model="event.people" label="Personen" class="mb-4" />
          <div>
            <span class="block text-gray-500 font-bold">Dateien</span>
            <MultiTUSUpload @uploaded="files = $event" />
          </div>
        </div>
        <label>
          <span class="block text-gray-500 font-bold">Beschreibung</span>
          <Editor v-model="event.description" />
        </label>
        <Button class="mt-4" type="submit">Speichern</Button>
        <ButtonSecondary class="mt-4" type="reset">Abbrechen</ButtonSecondary>
      </form>
    </div>
  </Layout>
</template>

<script>
import DateTime from 'luxon/src/datetime'

export default {
  data() {
    return {
      files: [],
      event: {
        title: '',
        description: null,
        date: DateTime.local().toISODate(),
        icon: '',
        people: [],
        relations: [],
      },
    }
  },
  methods: {
    async save() {
      try {
        await this.$axios.$post('/events/', { ...this.event, files: this.files })
        this.$router.push('/')
        this.$toast.success('Ereignis erstellt')
      } catch (e) {
        this.$toast.error(JSON.stringify(e.response.data))
      }
    },
    reset() {
      this.$router.push('/')
    },
  },
}
</script>
