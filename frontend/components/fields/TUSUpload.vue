<template>
  <label class="bg-gray-200 border-2 border-gray-200 rounded-lg w-full py-2 px-4 text-gray-700 flex flex-col">
    <input class="hidden" type="file" :disabled="success" @input="handleFile" />
    <span v-if="!hasFile" class="block mb-2">Datei auswählen…</span>
    <span v-else-if="success" class="block mb-2">Erfolgreich uploaded</span>
    <span v-else-if="error" class="block mb-2">Beim upload ist ein Fehler aufgetreten</span>
    <progress class="w-full h-1" max="100" :value="progress" />
  </label>
</template>

<script>
import first from 'lodash/first'
import last from 'lodash/last'
import * as tus from 'tus-js-client'
import { v4 as uuidv4 } from 'uuid'

export default {
  inheritAttrs: false,
  data() {
    return {
      bytesUploaded: 0,
      bytesTotal: 0,
      upload: null,
      success: false,
      error: null,
      file: null,
    }
  },
  computed: {
    errorMessages() {
      return [this.error].filter(Boolean)
    },
    progress() {
      const fraction = (this.bytesUploaded / this.bytesTotal) * 100
      return Number.isNaN(fraction) ? 0 : fraction
    },
    hasFile() {
      return !!this.file
    },
  },
  methods: {
    randomFilename(filename) {
      const extension = last(filename.split('.'))
      return `${uuidv4()}.${extension}`
    },
    handleFile(event) {
      const file = first(event.target.files)
      this.success = false
      this.error = null
      this.bytesUploaded = 0
      this.bytesTotal = 0
      this.file = file

      if (!file) {
        return
      }

      const vm = this
      this.upload = new tus.Upload(file, {
        endpoint: '/api/upload/',
        retryDelays: [0, 3000, 5000, 10000, 20000],
        chunkSize: 5242880,
        metadata: {
          filename: file.name,
          filetype: file.type,
        },
        onError(error) {
          vm.error = error
          vm.success = false
        },
        onProgress(bytesUploaded, bytesTotal) {
          vm.bytesUploaded = bytesUploaded
          vm.bytesTotal = bytesTotal
        },
        onSuccess() {
          vm.$emit('uploaded', vm.upload.options.metadata.filename)
          vm.success = true
        },
      })
      this.upload.findPreviousUploads().then((previousUploads) => {
        if (previousUploads.length) {
          this.upload.resumeFromPreviousUpload(previousUploads[0])
        }
      })
      this.upload.options.metadata.filename = this.randomFilename(this.upload.options.metadata.filename)
      this.upload.start()
    },
  },
}
</script>
