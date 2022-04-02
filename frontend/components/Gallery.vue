<template>
  <img
    :src="thumbnail"
    class="transition-all rounded-full absolute shadow-flat shadow-primary hover:shadow-flat-lg object-cover"
    @click="openGallery"
  />
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
