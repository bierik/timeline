import { defineNuxtConfig } from "nuxt/config";

const isProduction = process.env.NODE_ENV === "production";

export default defineNuxtConfig({
  modules: [
    "@nuxt/eslint",
    "@pinia/nuxt",
    "@nuxtjs/google-fonts",
    "@nuxt/icon",
    "@vite-pwa/nuxt",
  ],

  ssr: false,

  components: [
    {
      path: "~/components",
      pathPrefix: false,
    },
  ],

  devtools: { enabled: true },

  css: [
    "~/assets/css/tailwind.css",
    "vis-timeline/dist/vis-timeline-graph2d.css",
    "photoswipe/dist/photoswipe.css",
  ],

  vue: {
    compilerOptions: {
      isCustomElement(tag) {
        return tag.startsWith("swiper-");
      },
    },
  },

  compatibilityDate: "2024-11-27",

  nitro: {
    devProxy: {
      "/api/": {
        target: `http://backend:8000/api/`,
      },
      "/admin/": {
        target: `http://backend:8000/admin/`,
      },
      "/static/": {
        target: `http://backend:8000/static/`,
      },
    },
  },

  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },

  eslint: {
    config: {
      stylistic: {
        arrowParens: true,
        braceStyle: "1tbs",
        quotes: "double",
        semi: true,
        quoteProps: "as-needed",
      },
    },
  },

  googleFonts: {
    families: {
      "Courier Prime": true,
    },
  },

  icon: {
    serverBundle: "remote",
  },

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
});
