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
      <swiper-container
        ref="swiper"
        class="mt-8 mb-4"
        navigation-prev-el="#prev-button"
        navigation-next-el="#next-button"
        navigation-disabled-class="!bg-gray-200"
        speed="1"
        @progress="makeProgress"
      >
        <swiper-slide
          v-for="(importedImageGroup, index) in groupedImportedImagesWithOriginalDate"
          :key="importedImageGroup.days"
          class="container"
        >
          <div class="flex flex-wrap mb-4">
            <div
              v-for="importedImage in importedImageGroup.values"
              :key="importedImage.file.name"
              class="relative w-32 h-32"
            >
              <img class="w-32 h-32 object-cover rounded" :src="importedImage.preview" />
              <button
                class="bg-white flex rounded-full p-1 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
                @click="removeImage(importedImage)"
              >
                <feather type="x" />
              </button>
            </div>
          </div>
          <div class="flex gap-4">
            <TextInput
              v-model="importedImageGroup.title"
              :errors="errorsForFieldAndIndex(index, 'title')"
              label="Titel"
              class="mb-4 grow"
            />
            <EmojiField
              v-model="importedImageGroup.icon"
              :errors="errorsForFieldAndIndex(index, 'icon')"
              label="Icon"
              class="mb-4 block"
            />
            <DateInput
              v-model="importedImageGroup.dateTimeOriginal"
              :errors="errorsForFieldAndIndex(index, 'date')"
              label="Datum"
              class="mb-4 block grow"
            />
          </div>
          <label>
            <span class="block text-gray-500 font-bold">Beschreibung</span>
            <Editor v-model="importedImageGroup.description" />
          </label>
        </swiper-slide>
        <swiper-slide
          v-for="(importedImage, index) in importedImagesWithMissingOriginalDate"
          :key="importedImage.file.name"
          class="container"
        >
          <div class="flex flex-wrap mb-4">
            <div class="relative w-32 h-32">
              <img class="w-32 h-32 object-cover rounded" :src="importedImage.preview" />
              <button
                class="bg-white flex rounded-full p-1 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
                @click="removeImage(importedImage)"
              >
                <feather type="x" />
              </button>
            </div>
          </div>
          <div class="flex gap-4">
            <TextInput
              v-model="importedImage.title"
              :errors="errorsForFieldAndIndex(index, 'title', true)"
              label="Titel"
              class="mb-4 grow"
            />
            <EmojiField
              v-model="importedImage.icon"
              :errors="errorsForFieldAndIndex(index, 'title', true)"
              label="Icon"
              class="mb-4 block"
            />
            <DateInput
              v-model="importedImage.dateTimeOriginal"
              :errors="errorsForFieldAndIndex(index, 'title', true)"
              label="Datum"
              class="mb-4 block grow"
            />
          </div>
          <label>
            <span class="block text-gray-500 font-bold">Beschreibung</span>
            <Editor v-model="importedImage.description" />
          </label>
        </swiper-slide>
      </swiper-container>
      <div v-show="hasImportedImages" class="flex flex-col">
        <ProgressLinear class="mb-4" :max="imagesCount" :value="activeStep" />
        <div class="flex">
          <Button id="prev-button" class="mr-2">Zurück</Button>
          <Button id="next-button">Weiter</Button>
          <div class="grow" />
          <Button :loading="loading" @click="performImport">Importieren</Button>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script>
import EXIF from 'exif-js'
import find from 'lodash/find'
import findIndex from 'lodash/findIndex'
import get from 'lodash/get'
import isEmpty from 'lodash/isEmpty'
import last from 'lodash/last'
import pick from 'lodash/pick'
import property from 'lodash/property'
import reject from 'lodash/reject'
import size from 'lodash/size'
import DateTime from 'luxon/src/datetime'
import { register } from 'swiper/swiper-element-bundle'

import * as tus from 'tus-js-client'
import { v4 as uuidv4 } from 'uuid'

register()

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
    return null
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

function extractImagesWithOriginalDate(images) {
  const group = []
  images.filter(property('dateTimeOriginal')).forEach((importedImage) => {
    const days = dateTimeToDays(importedImage.dateTimeOriginal)
    const index = findIndex(group, (groupEntry) => groupEntry.days === days)
    if (index < 0) {
      group.push({
        days,
        dateTimeOriginal: importedImage.dateTimeOriginal.toISODate(),
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
}

function extractImagesWithMissingOriginalDate(images) {
  return reject(images, property('dateTimeOriginal')).map((importedImage) => ({
    ...importedImage,
    title: '',
    icon: '',
    description: null,
  }))
}

export default {
  data() {
    return {
      importedImages: [],
      groupedImportedImagesWithOriginalDate: [],
      importedImagesWithMissingOriginalDate: [],
      activeStep: 1,
      loading: false,
      errors: [],
    }
  },
  computed: {
    hasImportedImages() {
      return !isEmpty(this.importedImages)
    },
    imagesCount() {
      return size(this.groupedImportedImagesWithOriginalDate) + size(this.importedImagesWithMissingOriginalDate)
    },
  },
  beforeDestroy() {
    this.importedImages.forEach((importedImage) => URL.revokeObjectURL(importedImage.buffer))
  },
  methods: {
    errorsForFieldAndIndex(index, field, offsetIndex = false) {
      const finalIndex = offsetIndex ? index + size(this.groupedImportedImagesWithOriginalDate) : index
      return get(this.errors[finalIndex], field)
    },
    makeProgress({ detail: [_, progress] }) {
      this.activeStep = Math.min(this.imagesCount, 1 + progress * (this.imagesCount - 1))
    },
    async loadImages(event) {
      this.importedImages = await extractCreatedDate(event.target.files)
      this.groupedImportedImagesWithOriginalDate = extractImagesWithOriginalDate(this.importedImages)
      this.importedImagesWithMissingOriginalDate = extractImagesWithMissingOriginalDate(this.importedImages)
      setTimeout(() => {
        this.$refs.swiper.swiper.update()
      }, 0)
    },
    removeImage(importedImage) {
      this.importedImages = this.importedImages.filter((i) => i.file.name !== importedImage.file.name)
      this.groupedImportedImagesWithOriginalDate = extractImagesWithOriginalDate(this.importedImages)
      this.importedImagesWithMissingOriginalDate = extractImagesWithMissingOriginalDate(this.importedImages)
    },
    async performImport() {
      const imagesToUpload = this.importedImages.map((importedImage) => {
        const uploadFilename = randomFilename(importedImage.file.name)
        return new Promise((resolve, reject) => {
          const upload = new tus.Upload(importedImage.file, {
            endpoint: '/api/upload/',
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
              resolve({ filename: importedImage.file.name, uploadFilename })
            },
          })
          upload.options.metadata.filename = uploadFilename
          upload.start()
        })
      })
      this.loading = true
      try {
        const uploadedImages = await Promise.all(imagesToUpload)
        const payload = [
          ...this.groupedImportedImagesWithOriginalDate.map((groupedUploadedImage) => ({
            ...pick(groupedUploadedImage, ['title', 'icon', 'description']),
            date: groupedUploadedImage.dateTimeOriginal,
            images: groupedUploadedImage.values.map(
              (uploadedImage) => find(uploadedImages, { filename: uploadedImage.file.name }).uploadFilename,
            ),
          })),
          ...this.importedImagesWithMissingOriginalDate.map((uploadedImage) => ({
            ...pick(uploadedImage, ['title', 'icon', 'description']),
            date: uploadedImage.dateTimeOriginal,
            images: [find(uploadedImages, { filename: uploadedImage.file.name }).uploadFilename],
          })),
        ]
        try {
          await this.$axios.$post('/events/bulk_create/', payload)
          this.$router.push({ name: 'event-timeline' })
        } catch (error) {
          const status = get(error, 'response.status')
          if (status >= 400 && status < 500) {
            this.errors = error.response.data
            this.$toast.warning('Überprüfen Sie die Eingabefelder auf Fehler.')
          } else if (error >= 500) {
            this.$toast.error('Es ist ein unerwarteter Fehler aufgetreten.')
          } else {
            throw error
          }
        } finally {
          this.loading = false
        }
      } catch (error) {
        this.$toast.error('Beim Hochladen der Bilder ist ein unerwarteter Fehler aufgetreten.')
        return
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
<style>
::range-thumb {
  border-radius: 1px;
  cursor: pointer;
}
</style>
