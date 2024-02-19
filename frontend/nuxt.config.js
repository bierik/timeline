export default {
  ssr: false,
  target: 'static',
  loading: false,
  components: [
    {
      path: '~/components',
      pathPrefix: false,
    },
  ],
  router: {
    middleware: ['auth'],
  },
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
  plugins: [
    '~/plugins/dompurify',
    '~/plugins/breakpoints',
    '~/plugins/config',
    '~/plugins/filters',
    '~/plugins/axios',
    '~/plugins/feather',
    '~/plugins/theme',
  ],
  buildModules: ['@nuxtjs/tailwindcss', '@nuxtjs/pwa', '@nuxtjs/google-fonts'],
  modules: ['@nuxtjs/axios', 'vue-toastification/nuxt', '@nuxtjs/auth-next'],
  axios: {
    baseURL: 'http://localhost:5002/api',
  },
  auth: {
    redirect: {
      login: '/login',
      logout: '/login',
      callback: false,
      home: '/event/timeline',
    },
    fullPathRedirect: true,
    strategies: {
      local: {
        token: {
          type: 'Token',
        },
        endpoints: {
          login: { url: '/auth/login/', method: 'post' },
          logout: { url: '/auth/logout/', method: 'post' },
          user: { url: '/auth/user/', method: 'get' },
        },
      },
    },
  },
  googleFonts: {
    families: {
      'Courier Prime': true,
    },
  },
  build: {
    target: 'modern',
    transpile: ['vis-data', 'vis-timeline', 'photoswipe'],
  },
  generate: {
    dir: '/tmp/nuxt_output',
  },
}
