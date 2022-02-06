<template>
  <div>
    <div v-for="field in fields" :key="`upload-field-${field}`" class="flex mb-2">
      <TUSUpload class="grow w-full mr-2" @uploaded="handleUploadSuccess" />
      <Button @click.prevent="removeField(field)">Löschen</Button>
    </div>
    <Button @click.prevent="addField">Weitere Datei hinzufügen</Button>
  </div>
</template>

<script>
import { v4 as uuidv4 } from 'uuid'

export default {
  data() {
    return {
      files: [],
      fields: [uuidv4()],
    }
  },
  methods: {
    handleUploadSuccess(file) {
      this.files = [...this.files, file]
      this.$emit('uploaded', this.files)
    },
    addField() {
      this.fields = [...this.fields, uuidv4()]
    },
    removeField(fieldToRemove) {
      this.fields = this.fields.filter((field) => field !== fieldToRemove)
      this.$emit('uploaded', this.files)
    },
  },
}
</script>
