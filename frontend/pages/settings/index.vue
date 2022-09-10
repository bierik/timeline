<template>
  <Layout>
    <div class="container">
      <h1 class="text-xl mb-4 font-bold">Einstellungen</h1>
      <h2 class="text-md font-bold">Theme</h2>
      <label class="flex">
        <input v-model="theme" class="mr-1" type="radio" value="sunrise" />
        Sunrise
      </label>
      <label class="flex">
        <input v-model="theme" class="mr-1" type="radio" value="ocean" />
        Ocean
      </label>
      <label class="flex">
        <input v-model="theme" class="mr-1" type="radio" value="grass" />
        Grass
      </label>
    </div>
  </Layout>
</template>

<script>
export default {
  data() {
    return { chooser: false, theme: localStorage.getItem('theme') }
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
