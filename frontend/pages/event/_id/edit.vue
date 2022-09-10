<template>
  <Layout>
    <div class="container mx-auto flex flex-col pt-6 pb-10">
      <h1 class="text-xl mb-4 font-bold">Ereignis bearbeiten</h1>
      <form class="w-full" @submit.prevent="save" @reset.prevent="reset">
        <TextInput v-model="event.title" class="mb-4 block" label="Titel" />
        <DateInput v-model="event.date" label="Datum" class="mb-4 block" />
        <TextInput v-model="event.icon" label="Icon" class="mb-4 block" />
        <EventField v-model="event.relations" label="Verknüpfungen" class="mb-4" :exclude="excludeFromSearch" />
        <PersonField v-model="event.people" label="Personen" class="mb-4" />
        <label>
          <span class="block text-gray-500 font-bold">Beschreibung</span>
          <Editor v-model="event.description" />
        </label>
        <span class="block text-gray-500 font-bold">Dateien</span>
        <MultiTUSUpload :files="event.images" @uploaded="handleUploadedFiles" @deleted="handleFilesDeleted" />
        <div class="flex mt-4">
          <Button class="mr-2" type="submit">Speichern</Button>
          <ButtonSecondary type="reset">Abbrechen</ButtonSecondary>
          <div class="grow" />
          <ButtonDelete @click="remove">Löschen</ButtonDelete>
        </div>
      </form>
    </div>
  </Layout>
</template>

<script>
export default {
  async asyncData({ $axios, route }) {
    const event = await $axios.$get(`/events/${route.params.id}/`)
    return { event }
  },
  data() {
    return {
      files: [],
      deletedFiles: [],
    }
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
    async save() {
      await this.$axios.$patch(`/events/${this.event.id}/`, {
        ...this.event,
        files: this.files,
        deleted_files: this.deletedFiles,
      })
      this.$router.push({ name: 'index', query: this.$route.query })
    },
    reset() {
      this.$router.push({ name: 'index', query: this.$route.query })
    },
    async remove() {
      await this.$axios.$delete(`/events/${this.event.id}/`)
      this.$router.push({ name: 'index', query: this.$route.query })
    },
    handleUploadedFiles(files) {
      this.files = files
    },
    handleFilesDeleted(files) {
      this.deletedFiles = files
    },
  },
}
</script>
