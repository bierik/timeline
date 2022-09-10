<template>
  <div class="flex">
    <div v-if="success" class="relative">
      <img :src="preview" class="w-32 h-32 object-cover" />
      <button
        class="bg-white flex rounded-full p-1 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
        @click="remove"
      >
        <feather type="x" />
      </button>
    </div>
    <div v-else-if="loading" class="bg-gray-200 w-32 h-32 flex items-center justify-center">
      <feather type="loader" animation="spin" />
    </div>
    <label v-else class="bg-gray-200 w-32 h-32 relative">
      <feather type="upload" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
      <input class="hidden" type="file" :disabled="success" @input="handleFile" />
    </label>
  </div>
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
      preview: null,
      loading: false,
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
    remove() {
      this.$emit('deleted')
      this.success = false
    },
    randomFilename(filename) {
      const extension = last(filename.split('.'))
      return `${uuidv4()}.${extension}`
    },
    handleFile(event) {
      const file = first(event.target.files)
      this.loading = true
      this.success = false
      this.error = null
      this.bytesUploaded = 0
      this.bytesTotal = 0
      this.file = file

      if (!file) {
        return
      }

      const reader = new FileReader()
      reader.onload = () => {
        this.preview = reader.result
      }
      reader.readAsDataURL(file)

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
          vm.loading = false
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
