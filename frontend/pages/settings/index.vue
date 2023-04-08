<template>
  <Layout>
    <div class="container px-4">
      <h2 class="text-md font-bold mb-2">Theme</h2>
      <label class="flex">
        <input v-model="theme" class="mr-1" type="radio" value="sunrise" />
        Sunrise
      </label>
      <label class="flex">
        <input v-model="theme" class="mr-1" type="radio" value="ocean" />
        Ocean
      </label>
      <label class="flex mb-6">
        <input v-model="theme" class="mr-1" type="radio" value="grass" />
        Grass
      </label>

      <nuxt-link
        class="w-20 flex justify-center items-center bg-primary-300 rounded-lg py-2 px-4 text-white leading-tight focus:outline-none focus:bg-primary-400 hover:bg-primary-400"
        :to="{ name: 'import' }"
        >Import</nuxt-link
      >
    </div>
  </Layout>
</template>

<script>
export default {
  data() {
    return {
      theme: localStorage.getItem('theme') || 'sunrise',
    }
  },
  watch: {
    theme(theme) {
      localStorage.setItem('theme', theme)
      document.documentElement.removeAttribute('class')
      document.documentElement.classList.add(`theme-${localStorage.getItem('theme')}`)
    },
  },
}
</script>
