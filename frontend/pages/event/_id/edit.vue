<template>
  <div class="container mx-auto max-w-screen-md min-h-screen flex flex-col pt-6 pb-10">
    <h1 class="text-xl mb-4 font-bold">Ereignis bearbeiten</h1>
    <form class="w-full" @submit.prevent="save" @reset.prevent="reset">
      <TextInput v-model="event.title" class="mb-4 block" label="Titel" />
      <DateInput v-model="event.date" label="Datum" class="mb-4 block" />
      <TextInput v-model="event.icon" label="Icon" class="mb-4 block" />
      <label>
        <span class="block text-gray-500 font-bold">Beschreibung</span>
        <Editor v-model="event.description" />
      </label>
      <span class="block text-gray-500 font-bold">Dateien</span>
      <MultiTUSUpload :files="event.images" @uploaded="handleUploadedFiles" @deleted="handleFilesDeleted" />
      <Button class="mt-4" type="submit">Speichern</Button>
      <ButtonSecondary class="mt-4" type="reset">Abbrechen</ButtonSecondary>
    </form>
  </div>
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
  methods: {
    async save() {
      try {
        await this.$axios.$patch(`/events/${this.event.id}/`, {
          ...this.event,
          files: this.files,
          deleted_files: this.deletedFiles,
        })
        this.$router.push('/')
      } catch (error) {}
    },
    reset() {
      this.$router.push('/')
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
