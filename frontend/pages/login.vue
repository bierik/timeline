<template>
  <div class="flex flex-col justify-center items-center h-screen">
    <form class="bg-slate-50 p-16 rounded" @submit.prevent="login">
      <TextInput v-model="credentials.username" autofocus class="mb-4" type="email" label="E-Mail" />
      <TextInput v-model="credentials.password" class="mb-4" type="password" label="Passwort" />
      <Button type="submit" class="w-full">Login</Button>
    </form>
  </div>
</template>

<script>
import get from 'lodash/get'

export default {
  data() {
    return {
      credentials: {},
    }
  },
  methods: {
    async login() {
      try {
        await this.$auth.loginWith('local', { data: this.credentials })
      } catch (error) {
        const status = get(error, 'response.status')
        if (status >= 400 && status < 500) {
          this.$toast.warning('Die Zugangsdaten stimmen nicht')
          this.credentials.password = ''
        }
      }
    },
  },
}
</script>
