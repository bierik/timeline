<template>
  <Field v-bind="$attrs">
    <div v-if="value" class="relative">
      <img :src="value.thumbnail" class="w-32 h-32 object-cover rounded" />
      <button
        class="bg-white flex rounded-full p-1 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
        @click="remove"
      >
        <feather type="x" />
      </button>
    </div>
    <div v-else-if="loading" class="bg-gray-200 w-32 h-32 flex items-center justify-center rounded">
      <feather type="loader" animation="spin" />
    </div>
    <div v-else class="bg-gray-200 w-32 h-32 relative cursor-pointer rounded">
      <feather type="upload" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
      <input class="hidden" type="file" accept=".jpg,.jpeg,.png" @input="handleImage" />
    </div>
  </Field>
</template>

<script>
import first from 'lodash/first'
import last from 'lodash/last'
import * as tus from 'tus-js-client'
import { v4 as uuidv4 } from 'uuid'
import fieldMixin from '@/components/fields/field-mixin'

export default {
  mixins: [fieldMixin],
  data() {
    return {
      bytesUploaded: 0,
      bytesTotal: 0,
      upload: null,
      error: null,
      image: null,
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
  },
  methods: {
    remove() {
      this.$emit('input', null)
    },
    randomFilename(filename) {
      const extension = last(filename.split('.'))
      return `${uuidv4()}.${extension}`
    },
    handleImage(event) {
      const image = first(event.target.files)
      this.loading = true
      this.error = null
      this.bytesUploaded = 0
      this.bytesTotal = 0

      if (!image) {
        return
      }

      const reader = new FileReader()
      reader.onload = () => {
        this.preview = reader.result
        this.$emit('input', {
          id: Date.now(),
          filename: this.upload.options.metadata.filename,
          thumbnail: reader.result,
        })
      }
      reader.readAsDataURL(image)

      const vm = this
      this.upload = new tus.Upload(image, {
        endpoint: '/api/upload/',
        retryDelays: [0, 3000, 5000, 10000, 20000],
        chunkSize: 5242880,
        metadata: {
          filename: image.name,
          filetype: image.type,
        },
        onError(error) {
          vm.error = error
        },
        onProgress(bytesUploaded, bytesTotal) {
          vm.bytesUploaded = bytesUploaded
          vm.bytesTotal = bytesTotal
        },
        onSuccess() {
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
