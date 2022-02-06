<template>
  <div class="container mx-auto max-w-screen-md h-screen flex flex-col pt-6">
    <h1 class="text-xl mb-4 font-bold">Neues Ereignis hinzfügen</h1>
    <form class="w-full" @submit.prevent="save" @reset.prevent="reset">
      <TextInput v-model="event.title" class="mb-4 block" label="Titel" />
      <DateInput v-model="event.date" label="Datum" class="mb-4 block" />
      <TextInput v-model="event.icon" label="Icon" class="mb-4 block" />
      <Editor v-model="event.description" />
      <label>
        <span class="block text-gray-500 font-bold">Dateien</span>
        <MultiTUSUpload @uploaded="handleUploadedFiles" />
      </label>
      <Button class="mt-4" type="submit">Speichern</Button>
      <ButtonSecondary class="mt-4" type="reset">Abbrechen</ButtonSecondary>
    </form>
  </div>
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
      },
    }
  },
  methods: {
    async save() {
      try {
        await this.$axios.$post('/events/', { ...this.event, files: this.files })
        this.$router.push('/')
      } catch (error) {}
    },
    reset() {
      this.$router.push('/')
    },
    handleUploadedFiles(files) {
      this.files = files
    },
  },
}
</script>
