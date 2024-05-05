<template>
  <Field v-bind="$attrs" tag="div">
    <div class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-x-2 gap-y-2 w-full">
      <div v-for="(image, index) in files" :key="image.name" class="relative aspect-square">
        <img :src="image.thumbnail" width="100" height="100" class="object-cover rounded w-full h-full" />
        <div v-if="image.loading" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 flex">
          <feather type="loader" animation="spin" />
        </div>
        <button
          v-else
          class="bg-white flex rounded-full p-1 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
          @click.stop.prevent="remove(index)"
        >
          <feather type="x" />
        </button>
      </div>

      <label class="bg-gray-200 relative cursor-pointer rounded aspect-square">
        <feather type="upload" class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2" />
        <input class="hidden" :multiple="multiple" type="file" accept=".jpg,.jpeg,.png" @input="handleFiles" />
      </label>
    </div>
  </Field>
</template>

<script>
import differenceBy from 'lodash/differenceBy'
import first from 'lodash/first'
import isEmpty from 'lodash/isEmpty'
import reject from 'lodash/reject'
import * as tus from 'tus-js-client'
import fieldMixin from '@/components/fields/field-mixin'
import { readImage, randomFilename } from '@/lib/file'

function createPendingFile(file) {
  file.loading = true
  return file
}

export default {
  mixins: [fieldMixin],
  props: {
    multiple: {
      type: Boolean,
      default: () => false,
    },
    value: {
      type: [Array, Object, File],
      default: () => [],
    },
  },
  data() {
    return {
      uploadedFiles: [],
    }
  },
  computed: {
    files() {
      return this.multiple ? [...this.value, ...this.uploadedFiles] : reject([this.value].flat(), isEmpty)
    },
  },
  methods: {
    async handleFiles(event) {
      if (isEmpty(event.target.files)) {
        return
      }
      this.uploadedFiles = (await Promise.all(differenceBy(event.target.files, this.files, 'name').map(readImage))).map(
        createPendingFile,
      )
      const uploads = this.uploadedFiles.map((file, index) => {
        const filename = randomFilename(file)
        file.filename = filename
        file.id = Date.now()
        return new Promise((resolve) => {
          const upload = new tus.Upload(file, {
            endpoint: '/api/upload/',
            retryDelays: [0, 3000, 5000, 10000, 20000],
            chunkSize: 1000000,
            metadata: {
              filename,
              filetype: file.type,
            },
            onSuccess: () => {
              file.loading = false
              this.$set(this.uploadedFiles, index, file)
              resolve()
            },
          })
          upload.options.metadata.filename = filename
          upload.start()
        })
      })
      await Promise.all(uploads)
      this.$emit('input', this.multiple ? [...this.value, ...this.uploadedFiles] : first(this.uploadedFiles))
      this.uploadedFiles = []
    },
    remove(indexToRemove) {
      this.$emit(
        'input',
        this.files.filter((_, index) => index !== indexToRemove),
      )
    },
  },
}
</script>
