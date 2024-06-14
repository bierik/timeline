<template>
  <Field v-bind="$attrs" tag="div">
    <div class="grid w-full grid-cols-2 gap-2 md:grid-cols-3 xl:grid-cols-4">
      <div
        v-for="(image, index) in files"
        :key="image.name"
        class="relative aspect-square"
      >
        <img
          :src="image.thumbnail"
          width="100"
          height="100"
          class="size-full rounded object-cover"
        />
        <div
          v-if="image.loading"
          class="absolute left-1/2 top-1/2 flex -translate-x-1/2 -translate-y-1/2"
        >
          <Icon name="feather:loader" animation="spin" />
        </div>
        <button
          v-else
          class="absolute left-1/2 top-1/2 flex -translate-x-1/2 -translate-y-1/2 rounded-full bg-white p-1"
          @click.stop.prevent="remove(index)"
        >
          <Icon name="feather:x" />
        </button>
      </div>

      <label class="relative aspect-square cursor-pointer rounded bg-gray-200">
        <Icon
          name="feather:upload"
          class="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2"
        />
        <input
          class="hidden"
          :multiple="multiple"
          type="file"
          accept=".jpg,.jpeg,.png"
          @input="handleFiles"
        />
      </label>
    </div>
  </Field>
</template>

<script>
import differenceBy from "lodash/differenceBy";
import first from "lodash/first";
import isEmpty from "lodash/isEmpty";
import reject from "lodash/reject";
import * as tus from "tus-js-client";
import fieldMixin from "@/components/fields/field-mixin";
import { readImage, randomFilename } from "@/lib/file";

function createPendingFile(file) {
  file.loading = true;
  return file;
}

export default defineNuxtComponent({
  mixins: [fieldMixin],
  props: {
    multiple: {
      type: Boolean,
      default: () => false,
    },
    modelValue: {
      type: [Array, Object, File],
      default: () => [],
    },
  },
  data() {
    return {
      uploadedFiles: [],
    };
  },
  computed: {
    files() {
      return this.multiple
        ? [...this.modelValue, ...this.uploadedFiles]
        : reject([this.modelValue].flat(), isEmpty);
    },
  },
  methods: {
    async handleFiles(event) {
      if (isEmpty(event.target.files)) {
        return;
      }
      this.uploadedFiles = (
        await Promise.all(
          differenceBy(event.target.files, this.files, "name").map(readImage)
        )
      ).map(createPendingFile);
      const uploads = this.uploadedFiles.map((file, index) => {
        const filename = randomFilename(file);
        file.filename = filename;
        file.id = Date.now();
        return new Promise((resolve) => {
          const upload = new tus.Upload(file, {
            endpoint: "/api/upload/",
            retryDelays: [0, 3000, 5000, 10000, 20000],
            chunkSize: 1000000,
            metadata: {
              filename,
              filetype: file.type,
            },
            onSuccess: () => {
              file.loading = false;
              this.uploadedFiles[index] = file;
              resolve();
            },
          });
          upload.options.metadata.filename = filename;
          upload.start();
        });
      });
      await Promise.all(uploads);
      this.$emit(
        "update:model-value",
        this.multiple
          ? [...this.modelValue, ...this.uploadedFiles]
          : first(this.uploadedFiles)
      );
      this.uploadedFiles = [];
    },
    remove(indexToRemove) {
      this.$emit(
        "update:model-value",
        this.files.filter((_, index) => index !== indexToRemove)
      );
    },
  },
});
</script>
