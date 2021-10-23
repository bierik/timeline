// eslint-disable-next-line nuxt/no-cjs-in-config
const path = require('path')

export default {
  rootDir: path.join(__dirname, 'frontend'),
  ssr: false,
  target: 'static',
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
  css: [],
  plugins: [],
  buildModules: ['@nuxtjs/tailwindcss', '@nuxtjs/pwa'],
  modules: ['@nuxtjs/axios'],
  axios: {
    baseURL: '/api',
  },
  build: {},
  vue: {
    config: {
      productionTip: false,
      devtools: true,
    },
  },
}
