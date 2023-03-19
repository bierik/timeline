<template>
  <img :src="thumbnail" class="cursor-zoom-in" @click.prevent.stop="openGallery" />
</template>

<script>
import PhotoSwipeLightbox from 'photoswipe/dist/photoswipe-lightbox.esm.js'
import Vue from 'vue'

import GalleryCaptionComponent from '@/components/GalleryCaption.vue'

const GalleryCaptionComponentConstructor = Vue.extend(GalleryCaptionComponent)

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
    }
  },
  mounted() {
    this.initGallery()
  },
  methods: {
    buildCaption({ title, description }) {
      const galleryCaptionComponentInstance = new GalleryCaptionComponentConstructor({
        propsData: {
          title,
          description,
        },
      })
      galleryCaptionComponentInstance.$mount()
      return galleryCaptionComponentInstance.$el.outerHTML
    },
    buildDataSource() {
      return this.images.map((image) => ({
        src: image.image,
        width: image.dimensions.width,
        height: image.dimensions.height,
        alt: `${image.title} — ${image.description}`,
        title: image.title,
        description: image.description,
      }))
    },
    openGallery() {
      this.gallery.loadAndOpen(0)
    },
    initGallery() {
      const options = {
        dataSource: this.buildDataSource(),
        pswpModule: () => import('photoswipe/dist/photoswipe.esm.js'),
      }
      this.gallery = new PhotoSwipeLightbox(options)
      this.gallery.on('uiRegister', () => {
        this.gallery.pswp.ui.registerElement({
          name: 'caption',
          isButton: false,
          appendTo: 'root',
          onInit: (el, pswp) => {
            this.gallery.pswp.on('change', () => {
              el.innerHTML = this.buildCaption(pswp.currSlide.data)
            })
          },
        })
      })
      this.gallery.init()
    },
  },
}
</script>
