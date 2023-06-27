<template>
  <Layout>
    <div class="container px-4">
      <h1 class="text-xl mb-4 font-bold">Bilder importieren</h1>
      <label
        class="cursor-pointer bg-primary-300 h-16 rounded-lg py-2 px-4 text-white leading-tight focus:outline-none flex items-center justify-center hover:bg-primary-400"
      >
        <feather type="file-plus" class="mr-1" />
        <span>Bilder auswählen</span>
        <input class="hidden" type="file" multiple accept=".jpg,.jpeg,.png" @change="loadImages" />
      </label>
      <agile
        ref="agile"
        class="mt-8 mb-4"
        :infinite="false"
        :dots="false"
        :nav-buttons="false"
        :speed="0"
        :swipe-distance="Infinity"
        :throttle-delay="0"
        @after-change="handleSlideChanged"
      >
        <div v-for="importedImageGroup in groupedImportedImages" :key="importedImageGroup.days" class="container">
          <h2 class="text-md mb-4 font-bold">
            Bilder vom {{ importedImageGroup.dateTimeOriginal | toLocaleDateString }}
          </h2>
          <div class="flex flex-wrap mb-4">
            <div
              v-for="importedImage in importedImageGroup.values"
              :key="importedImage.file.name"
              class="relative w-32 h-32"
            >
              <img class="w-32 h-32 object-cover" :src="importedImage.preview" />
              <button
                class="bg-white flex rounded-full p-1 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
                @click="removeImage(importedImage)"
              >
                <feather type="x" />
              </button>
            </div>
          </div>
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <TextInput v-model="importedImageGroup.title" label="Titel" class="mb-4" />
            <EmojiField v-model="importedImageGroup.icon" label="Icon" class="mb-4 block" />
          </div>
          <label>
            <span class="block text-gray-500 font-bold">Beschreibung</span>
            <Editor v-model="importedImageGroup.description" />
          </label>
        </div>
      </agile>
      <div v-if="hasImportedImages" class="flex">
        <Button class="mr-2" :disabled="!hasPrev" @click="prev">Zurück</Button>
        <Button :disabled="!hasNext" @click="next">Weiter</Button>
        <div class="grow" />
        <Button @click="performImport">Importieren</Button>
      </div>
    </div>
  </Layout>
</template>

<script>
import EXIF from 'exif-js'
import findIndex from 'lodash/findIndex'
import get from 'lodash/get'
import isEmpty from 'lodash/isEmpty'
import last from 'lodash/last'
import size from 'lodash/size'
import DateTime from 'luxon/src/datetime'
import * as tus from 'tus-js-client'
import { v4 as uuidv4 } from 'uuid'

function readFileAsArrayBuffer(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => {
      resolve([file, reader.result])
    }
    reader.onerror = reject
    reader.readAsArrayBuffer(file)
  })
}

function parseEXIFDateTime(str) {
  if (!str) {
    return DateTime.local()
  }
  const dateTime = DateTime.fromFormat(str, 'yyyy:MM:dd hh:mm:ss')
  return dateTime.isValid ? dateTime : null
}

async function extractCreatedDate(files = []) {
  const arrayBuffers = await Promise.all(Array.from(files).map((f) => readFileAsArrayBuffer(f)))
  return arrayBuffers.map(([file, buffer]) => {
    const dateTimeOriginal = parseEXIFDateTime(get(EXIF.readFromBinaryFile(buffer), 'DateTimeOriginal'))
    return {
      buffer,
      preview: URL.createObjectURL(new Blob([buffer], { type: file.type })),
      dateTimeOriginal,
      file,
      uploadFilename: null,
    }
  })
}

function dateTimeToDays(datetime) {
  return Math.floor(datetime.toSeconds() / 60 / 60 / 24)
}

function randomFilename(filename) {
  const extension = last(filename.split('.'))
  return `${uuidv4()}.${extension}`
}

export default {
  data() {
    return {
      importedImages: [],
      currentSlide: 0,
    }
  },
  computed: {
    groupedImportedImages() {
      const group = []
      this.importedImages.forEach((importedImage) => {
        const days = dateTimeToDays(importedImage.dateTimeOriginal)
        const index = findIndex(group, (groupEntry) => groupEntry.days === days)
        if (index < 0) {
          group.push({
            days,
            dateTimeOriginal: importedImage.dateTimeOriginal,
            values: [importedImage],
            title: '',
            icon: '',
            description: null,
          })
        } else {
          group[index].values.push(importedImage)
        }
      })
      return group
    },
    hasImportedImages() {
      return !isEmpty(this.importedImages)
    },
    slideCount() {
      return size(this.groupedImportedImages)
    },
    hasNext() {
      return this.slideCount !== 0 && this.currentSlide < this.slideCount - 1
    },
    hasPrev() {
      return this.currentSlide > 0
    },
  },
  watch: {
    importedImages() {
      this.reloadSlider()
    },
  },
  beforeDestroy() {
    this.importedImages.forEach((importedImage) => URL.revokeObjectURL(importedImage.buffer))
  },
  methods: {
    async loadImages(event) {
      this.importedImages = await extractCreatedDate(event.target.files)
    },
    reloadSlider() {
      setTimeout(this.$refs.agile.reload, 0)
    },
    prev() {
      this.$refs.agile.goToPrev()
    },
    next() {
      this.$refs.agile.goToNext()
    },
    removeImage(importedImage) {
      this.importedImages = this.importedImages.filter((i) => i.file.name !== importedImage.file.name)
    },
    handleSlideChanged({ currentSlide }) {
      this.currentSlide = currentSlide
    },
    async performImport() {
      const uploads = Promise.all(
        this.importedImages.map((importedImage) => {
          const uploadFilename = randomFilename(importedImage.file.name)
          return new Promise((resolve, reject) => {
            const upload = new tus.Upload(importedImage.file, {
              endpoint: 'api/upload/',
              retryDelays: [0, 3000, 5000, 10000, 20000],
              chunkSize: 5242880,
              metadata: {
                filename: uploadFilename,
                filetype: importedImage.file.type,
              },
              onError(error) {
                reject(error)
              },
              onSuccess() {
                importedImage.uploadFilename = uploadFilename
                resolve()
              },
            })
            upload.options.metadata.filename = uploadFilename
            upload.start()
          })
        }),
      )
      await uploads
      await this.$axios.$post(
        '/events/bulk_create/',
        this.groupedImportedImages.map((groupedUploadedImage) => ({
          title: groupedUploadedImage.title,
          description: groupedUploadedImage.description,
          icon: groupedUploadedImage.icon,
          date: groupedUploadedImage.dateTimeOriginal.toISODate(),
          images: groupedUploadedImage.values.map((uploadedImage) => uploadedImage.uploadFilename),
        })),
      )
      this.$router.push({ name: 'event-timeline' })
    },
  },
}
</script>
