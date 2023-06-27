<template>
  <Field v-bind="$attrs">
    <div class="flex flex-wrap gap-x-2">
      <div v-for="image in value" :key="`image-preview-${image.id}`" class="relative">
        <button
          class="bg-white flex rounded-full p-1 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
          @click="removeImage(image)"
        >
          <feather type="x" />
        </button>
        <img :src="image.thumbnail" class="w-32 h-32 rounded object-cover" />
      </div>
      <TUSUpload :value="uploadedImage" @input="handleImageUpload" />
    </div>
  </Field>
</template>

<script>
import reject from 'lodash/reject'
import fieldMixin from '@/components/fields/field-mixin'

export default {
  mixins: [fieldMixin],
  data() {
    return {
      uploadedImage: null,
    }
  },
  methods: {
    handleImageUpload(image) {
      this.$emit('input', [...this.value, image])
      this.uploadedImage = null
    },
    removeImage(image) {
      this.$emit(
        'input',
        reject(this.value, ({ id }) => id === image.id),
      )
    },
  },
}
</script>
