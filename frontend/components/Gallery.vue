<template>
  <div class="relative" style="width: fit-content">
    <img :src="thumbnail" />
    <div
      class="group bg-black bg-opacity-0 absolute inset-0 hover:bg-opacity-25 transition-all flex items-center justify-items-center"
      @click="openGallery"
    >
      <div class="opacity-0 transition-opacity group-hover:opacity-100 flex-grow">🔍</div>
    </div>
  </div>
</template>

<script>
import PhotoSwipe from 'photoswipe'
import PhotoSwipeUIDefault from 'photoswipe/dist/photoswipe-ui-default'
export default {
  props: {
    images: {
      type: Array,
      default: () => [],
    },
    thumbnail: {
      type: String,
      required: true,
    },
  },
  computed: {
    items() {
      return this.images.map((image) => ({
        src: image.file,
        w: image.dimensions.width,
        h: image.dimensions.height,
        title: `${image.title} — ${image.description}`,
      }))
    },
  },
  methods: {
    openGallery() {
      const photoSwipeRoot = document.querySelector('#pswp')
      const options = {}
      const gallery = new PhotoSwipe(photoSwipeRoot, PhotoSwipeUIDefault, this.items, options)
      gallery.init()
    },
  },
}
</script>
