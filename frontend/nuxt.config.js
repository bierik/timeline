import { defineNuxtConfig } from "nuxt/config";

export default defineNuxtConfig({
  devtools: { enabled: true },
  css: [
    "~/assets/css/tailwind.css",
    "vis-timeline/dist/vis-timeline-graph2d.css",
    "photoswipe/dist/photoswipe.css",
  ],
  ssr: false,
  modules: ["@nuxt/eslint", "@pinia/nuxt", "@nuxtjs/google-fonts", "nuxt-icon"],
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  components: [
    {
      path: "~/components",
      pathPrefix: false,
    },
  ],
  vue: {
    compilerOptions: {
      isCustomElement(tag) {
        return tag.startsWith("swiper-");
      },
    },
  },
  googleFonts: {
    families: {
      "Courier Prime": true,
      Quicksand: [300, 400, 500, 600, 700],
    },
  },
  nitro: {
    devProxy: {
      "/api/": {
        target: `http://backend:8000/api/`,
      },
      "/media/": {
        target: `http://backend:8000/media/`,
      },
      "/admin/": {
        target: `http://backend:8000/admin/`,
      },
      "/static/": {
        target: `http://backend:8000/static/`,
      },
    },
  },
});
