import { defineNuxtConfig } from "nuxt/config";

const isProduction = process.env.NODE_ENV === "production";

export default defineNuxtConfig({
  devtools: { enabled: true },
  css: [
    "~/assets/css/tailwind.css",
    "vis-timeline/dist/vis-timeline-graph2d.css",
    "photoswipe/dist/photoswipe.css",
  ],
  ssr: false,
  modules: [
    "@nuxt/eslint",
    "@pinia/nuxt",
    "@nuxtjs/google-fonts",
    "nuxt-icon",
    "@vite-pwa/nuxt",
  ],
  pwa: {
    registerType: "autoUpdate",
    manifest: {
      name: "Timeline",
      short_name: "Timeline",
      description: "Capture your memories on a timeline",
      theme_color: "#3b82f6",
    },
    pwaAssets: {
      config: true,
    },
    client: {
      periodicSyncForUpdates: 3600,
    },
    devOptions: {
      enabled: !isProduction,
    },
    workbox: {
      globPatterns: ["**/*.{js,css,html,png,svg,ico}"],
    },
    injectManifest: {
      globPatterns: ["**/*.{js,css,html,png,svg,ico}"],
    },
  },
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
