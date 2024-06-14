<template>
  <img
    width="100"
    height="100"
    :src="thumbnail"
    class="cursor-zoom-in"
    @click.prevent.stop="openGallery"
  />
</template>

<script>
import PhotoSwipeLightbox from "photoswipe/lightbox";

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
  data() {
    return {
      gallery: null,
    };
  },
  mounted() {
    this.initGallery();
  },
  methods: {
    buildDataSource() {
      return this.images.map((image) => ({
        src: image.image,
        width: image.dimensions.width,
        height: image.dimensions.height,
        description: image.description,
      }));
    },
    openGallery() {
      this.gallery.loadAndOpen(0);
    },
    initGallery() {
      const options = {
        dataSource: this.buildDataSource(),
        pswpModule: () => import("photoswipe"),
      };
      this.gallery = new PhotoSwipeLightbox(options);
      this.gallery.init();
    },
  },
};
</script>
