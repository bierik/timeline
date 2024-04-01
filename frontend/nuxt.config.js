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
      { name: 'viewport', content: 'width=device-width, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no' },
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
    '~/plugins/vuex-persist',
    '~/plugins/theme',
  ],
  buildModules: ['@nuxtjs/tailwindcss', '@nuxtjs/google-fonts'],
  modules: [
    '@nuxtjs/pwa',
    '@nuxtjs/axios',
    'vue-toastification/nuxt',
    '@nuxtjs/auth-next',
    ['@nuxtjs/proxy', { xfwd: true }],
  ],
  axios: {
    baseURL: '/api',
  },
  proxy: [
    'http://backend:8000/api',
    'http://backend:8000/media',
    'http://backend:8000/admin',
    'http://backend:8000/static',
  ],
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
  pwa: {
    meta: {
      lang: 'de',
      nativeUI: true,
      theme_color: '#ffffff',
    },
    manifest: {
      lang: 'de',
      useWebmanifestExtension: true,
    },
    icon: {
      purpose: 'any',
    },
  },
  build: {
    target: 'modern',
    transpile: ['vis-data', 'vis-timeline', 'photoswipe'],
  },
}
