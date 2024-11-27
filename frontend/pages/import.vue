<template>
  <Layout>
    <div class="container px-4">
      <h1 class="mb-4 text-xl font-bold">
        Bilder importieren
      </h1>
      <label
        class="flex h-16 cursor-pointer items-center justify-center rounded-lg bg-primary-500 px-4 py-2 leading-tight text-white hover:bg-primary-400 focus:bg-primary-400 focus:outline-none"
      >
        <Icon
          name="feather:file-plus"
          class="mr-1"
        />
        <span>Bilder auswählen</span>
        <input
          class="hidden"
          type="file"
          multiple
          accept=".jpg,.jpeg,.png"
          @change="loadImages"
        />
      </label>
      <swiper-container
        ref="swiper"
        class="pb-28 pt-8"
        auto-height="true"
        navigation-prev-el="#prev-button"
        navigation-next-el="#next-button"
        navigation-disabled-class="!bg-gray-200"
        speed="1"
        @progress="makeProgress"
      >
        <swiper-slide
          v-for="(
            importedImageGroup, index
          ) in groupedImportedImagesWithOriginalDate"
          :key="importedImageGroup.days"
          class="container"
        >
          <div
            class="grid w-full grid-cols-2 gap-2 md:grid-cols-3 xl:grid-cols-4"
          >
            <div
              v-for="importedImage in importedImageGroup.values"
              :key="importedImage.file.name"
              class="relative"
            >
              <img
                class="aspect-square size-full rounded object-cover"
                :src="importedImage.preview"
              />
              <button
                type="button"
                class="absolute left-1/2 top-1/2 flex -translate-x-1/2 -translate-y-1/2 rounded-full bg-white p-1"
                @click="removeImage(importedImage)"
              >
                <Icon name="feather:x" />
              </button>
            </div>
          </div>
          <div class="flex flex-wrap gap-x-4 pt-4">
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
              class="mb-4 block grow basis-full md:basis-0"
            />
            <EventField
              v-model="importedImageGroup.relations"
              :errors="errorsForFieldAndIndex(index, 'relations')"
              label="Verknüpfungen"
              class="mb-4 grow basis-full"
            />
            <PersonField
              v-model="importedImageGroup.people"
              :errors="errorsForFieldAndIndex(index, 'people')"
              label="Personen"
              class="mb-4 grow basis-full"
            />
          </div>
          <label>
            <span class="block font-bold text-gray-500">Beschreibung</span>
            <Editor v-model="importedImageGroup.description" />
          </label>
        </swiper-slide>
        <swiper-slide
          v-for="(
            importedImage, index
          ) in importedImagesWithMissingOriginalDate"
          :key="importedImage.file.name"
          class="container"
        >
          <div
            class="grid w-full grid-cols-2 gap-2 md:grid-cols-3 xl:grid-cols-4"
          >
            <div class="relative">
              <img
                class="aspect-square size-full rounded object-cover"
                :src="importedImage.preview"
              />
              <button
                type="button"
                class="absolute left-1/2 top-1/2 flex -translate-x-1/2 -translate-y-1/2 rounded-full bg-white p-1"
                @click="removeImage(importedImage)"
              >
                <Icon name="feather:x" />
              </button>
            </div>
          </div>
          <div class="flex flex-wrap gap-x-4 pt-4">
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
              class="mb-4 block grow basis-full md:basis-0"
            />
            <EventField
              v-model="importedImage.relations"
              :errors="errorsForFieldAndIndex(index, 'relations')"
              label="Verknüpfungen"
              class="mb-4 grow basis-full"
            />
            <PersonField
              v-model="importedImage.people"
              :errors="errorsForFieldAndIndex(index, 'people')"
              label="Personen"
              class="mb-4 grow basis-full"
            />
          </div>
          <label>
            <span class="block font-bold text-gray-500">Beschreibung</span>
            <Editor v-model="importedImage.description" />
          </label>
        </swiper-slide>
      </swiper-container>
      <div
        v-show="hasImportedImages"
        class="fixed inset-x-0 bottom-0 z-10 bg-primary-50"
      >
        <div class="container flex flex-col p-4">
          <ProgressLinear
            class="mb-4"
            :max="imagesCount"
            :value="activeStep"
          />
          <div class="flex">
            <Button
              id="prev-button"
              class="mr-2"
            >
              Zurück
            </Button>
            <Button id="next-button">
              Weiter
            </Button>
            <div class="grow" />
            <Button
              :loading="loading"
              @click="performImport"
            >
              Importieren
            </Button>
          </div>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script>
import EXIF from "exif-js";
import find from "lodash/find";
import findIndex from "lodash/findIndex";
import get from "lodash/get";
import isEmpty from "lodash/isEmpty";
import last from "lodash/last";
import pick from "lodash/pick";
import property from "lodash/property";
import reject from "lodash/reject";
import size from "lodash/size";
import { DateTime } from "luxon";
import { register } from "swiper/element-bundle";

import * as tus from "tus-js-client";
import { v4 as uuidv4 } from "uuid";

register();

function readFileAsArrayBuffer(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      resolve([file, reader.result]);
    };
    reader.onerror = reject;
    reader.readAsArrayBuffer(file);
  });
}

function parseEXIFDateTime(str) {
  if (!str) {
    return null;
  }
  const dateTime = DateTime.fromFormat(str, "yyyy:MM:dd hh:mm:ss");
  return dateTime.isValid ? dateTime : null;
}

async function extractCreatedDate(files = []) {
  const arrayBuffers = await Promise.all(
    Array.from(files).map((f) => readFileAsArrayBuffer(f)),
  );
  return arrayBuffers.map(([file, buffer]) => {
    const dateTimeOriginal = parseEXIFDateTime(
      get(EXIF.readFromBinaryFile(buffer), "DateTimeOriginal"),
    );
    return {
      buffer,
      preview: URL.createObjectURL(new Blob([buffer], { type: file.type })),
      dateTimeOriginal:
        dateTimeOriginal || DateTime.fromMillis(file.lastModified),
      file,
    };
  });
}

function dateTimeToDays(datetime) {
  return Math.floor(datetime.toSeconds() / 60 / 60 / 24);
}

function randomFilename(filename) {
  const extension = last(filename.split("."));
  return `${uuidv4()}.${extension}`;
}

function extractImagesWithOriginalDate(images) {
  const group = [];
  images.filter(property("dateTimeOriginal")).forEach((importedImage) => {
    const days = dateTimeToDays(importedImage.dateTimeOriginal);
    const index = findIndex(group, (groupEntry) => groupEntry.days === days);
    if (index < 0) {
      group.push({
        days,
        dateTimeOriginal: importedImage.dateTimeOriginal.toISODate(),
        values: [importedImage],
        title: "",
        icon: "",
        description: null,
        relations: [],
        people: [],
      });
    } else {
      group[index].values.push(importedImage);
    }
  });
  return group;
}

function extractImagesWithMissingOriginalDate(images) {
  return reject(images, property("dateTimeOriginal")).map((importedImage) => ({
    ...importedImage,
    title: "",
    icon: "",
    description: null,
    relations: [],
    people: [],
  }));
}

export default defineNuxtComponent({
  data() {
    return {
      importedImages: [],
      groupedImportedImagesWithOriginalDate: [],
      importedImagesWithMissingOriginalDate: [],
      activeStep: 1,
      loading: false,
      errors: [],
    };
  },
  computed: {
    hasImportedImages() {
      return !isEmpty(this.importedImages);
    },
    imagesCount() {
      return (
        size(this.groupedImportedImagesWithOriginalDate)
        + size(this.importedImagesWithMissingOriginalDate)
      );
    },
  },
  beforeUnmount() {
    this.importedImages.forEach((importedImage) =>
      URL.revokeObjectURL(importedImage.buffer),
    );
  },
  methods: {
    errorsForFieldAndIndex(index, field, offsetIndex = false) {
      const finalIndex = offsetIndex
        ? index + size(this.groupedImportedImagesWithOriginalDate)
        : index;
      return get(this.errors[finalIndex], field);
    },
    makeProgress({ detail }) {
      this.activeStep = Math.min(
        this.imagesCount,
        1 + detail[1] * (this.imagesCount - 1),
      );
    },
    async loadImages(event) {
      this.importedImages = await extractCreatedDate(event.target.files);
      this.groupedImportedImagesWithOriginalDate
        = extractImagesWithOriginalDate(this.importedImages);
      this.importedImagesWithMissingOriginalDate
        = extractImagesWithMissingOriginalDate(this.importedImages);
      setTimeout(() => {
        this.$refs.swiper.swiper.update();
      }, 0);
    },
    removeImage(importedImage) {
      this.importedImages = this.importedImages.filter(
        (i) => i.file.name !== importedImage.file.name,
      );
      this.groupedImportedImagesWithOriginalDate
        = extractImagesWithOriginalDate(this.importedImages);
      this.importedImagesWithMissingOriginalDate
        = extractImagesWithMissingOriginalDate(this.importedImages);
    },
    async performImport() {
      const imagesToUpload = this.importedImages.map((importedImage) => {
        const uploadFilename = randomFilename(importedImage.file.name);
        return new Promise((resolve, reject) => {
          const upload = new tus.Upload(importedImage.file, {
            endpoint: "/api/upload/",
            retryDelays: [0, 3000, 5000, 10000, 20000],
            chunkSize: 1000000,
            metadata: {
              filename: uploadFilename,
              filetype: importedImage.file.type,
            },
            onError(error) {
              reject(error);
            },
            onSuccess() {
              resolve({ filename: importedImage.file.name, uploadFilename });
            },
          });
          upload.options.metadata.filename = uploadFilename;
          upload.start();
        });
      });
      this.loading = true;
      try {
        const uploadedImages = await Promise.all(imagesToUpload);
        const payload = [
          ...this.groupedImportedImagesWithOriginalDate.map(
            (groupedUploadedImage) => ({
              ...pick(groupedUploadedImage, [
                "title",
                "icon",
                "description",
                "relations",
                "people",
              ]),
              date: groupedUploadedImage.dateTimeOriginal,
              images: groupedUploadedImage.values.map(
                (uploadedImage) =>
                  find(uploadedImages, { filename: uploadedImage.file.name })
                    .uploadFilename,
              ),
            }),
          ),
          ...this.importedImagesWithMissingOriginalDate.map(
            (uploadedImage) => ({
              ...pick(uploadedImage, [
                "title",
                "icon",
                "description",
                "relations",
                "people",
              ]),
              date: uploadedImage.dateTimeOriginal,
              images: [
                find(uploadedImages, { filename: uploadedImage.file.name })
                  .uploadFilename,
              ],
            }),
          ),
        ];
        try {
          await this.$axios.post("/events/bulk_create/", payload);
          this.$router.push({ name: "index" });
        } catch (error) {
          const status = get(error, "response.status");
          if (status >= 400 && status < 500) {
            this.errors = error.response.data;
            this.$toast.warning("Überprüfen Sie die Eingabefelder auf Fehler.");
          } else if (error >= 500) {
            this.$toast.error("Es ist ein unerwarteter Fehler aufgetreten.");
          } else {
            throw error;
          }
        } finally {
          this.loading = false;
        }
      } catch {
        this.$toast.error(
          "Beim Hochladen der Bilder ist ein unerwarteter Fehler aufgetreten.",
        );
        return;
      } finally {
        this.loading = false;
      }
    },
  },
});
</script>

<style>
::range-thumb {
  border-radius: 1px;
  cursor: pointer;
}
</style>
