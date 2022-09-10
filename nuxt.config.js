// eslint-disable-next-line nuxt/no-cjs-in-config
const path = require('path')

export default {
  rootDir: path.join(__dirname, 'frontend'),
  ssr: false,
  target: 'static',
  loading: false,
  components: [
    {
      path: '~/components',
      pathPrefix: false,
    },
  ],
  telemetry: false,
  head: {
    title: 'timeline',
    htmlAttrs: {
      lang: 'de',
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
  },
  css: ['vis-timeline/dist/vis-timeline-graph2d.css', 'photoswipe/dist/photoswipe.css'],
  plugins: ['~/plugins/filters', '~/plugins/axios', '~/plugins/feather'],
  buildModules: ['@nuxtjs/tailwindcss', '@nuxtjs/pwa', '@nuxtjs/google-fonts'],
  modules: ['@nuxtjs/axios', '@nuxtjs/proxy'],
  axios: {
    baseURL: '/api',
  },
  proxy: ['http://localhost:8000/api', 'http://localhost:8000/media'],
  vue: {
    config: {
      productionTip: false,
      devtools: true,
    },
  },
  googleFonts: {
    families: {
      'Courier Prime': true,
    },
  },
  build: {
    transpile: ['vis-data', 'vis-timeline'],
  },
  generate: {
    dir: '../staticfiles',
  },
}
