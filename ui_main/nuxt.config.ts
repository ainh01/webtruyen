export default defineNuxtConfig({
  ssr: true,

  modules: [
    '@nuxtjs/tailwindcss',
    'nuxt-icon',
    'nuxt-swiper',
    'nuxt-simple-robots',
  ],

  runtimeConfig: {
    public: {
      // baseURL: 'https://otruyenapi.com/v1/api',
      baseURL: process.env.VITE_OTRUYEN_API_BASE_URL,
    },
  },

  compatibilityDate: '2025-01-05',
});