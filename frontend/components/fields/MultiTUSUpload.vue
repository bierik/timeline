<template>
  <div class="flex flex-wrap">
    <div v-for="image in filteredFiles" :key="`image-preview-${image.id}`" class="relative">
      <button
        class="bg-white flex rounded-full p-1 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
        @click.prevent="removeImage(image.id)"
      >
        <feather type="x" />
      </button>
      <img :src="image.thumbnail" class="w-32 h-32" />
    </div>
    <div v-for="field in fields" :key="`upload-field-${field}`" class="flex mb-2">
      <TUSUpload @uploaded="handleUploadSuccess($event, field)" @deleted="removeField(field)" />
    </div>
  </div>
</template>

<script>
import { v4 as uuidv4 } from 'uuid'

export default {
  props: {
    files: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      uploadedFiles: [],
      deletedFiles: [],
      fields: [uuidv4()],
    }
  },
  computed: {
    filteredFiles() {
      return this.files.filter((file) => !this.deletedFiles.includes(file.id))
    },
  },
  methods: {
    handleUploadSuccess(file, field) {
      this.uploadedFiles = [...this.uploadedFiles, { file, field }]
      this.$emit(
        'uploaded',
        this.uploadedFiles.map((f) => f.file),
      )
      this.addField()
    },
    addField() {
      this.fields = [...this.fields, uuidv4()]
    },
    removeField(fieldToRemove) {
      this.fields = this.fields.filter((field) => field !== fieldToRemove)
      this.uploadedFiles = this.uploadedFiles.filter((file) => file.field !== fieldToRemove)
      this.$emit('uploaded', this.uploadedFiles)
    },
    removeImage(image) {
      this.deletedFiles = [...this.deletedFiles, image]
      this.$emit('deleted', this.deletedFiles)
    },
  },
}
</script>
