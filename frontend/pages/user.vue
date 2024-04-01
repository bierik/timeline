<template>
  <Layout>
    <div class="container px-4">
      <h2 class="text-md font-bold mb-2">Theme</h2>
      <label class="flex">
        <input v-model="themeModel" class="mr-1" type="radio" value="sunrise" />
        Sunrise
      </label>
      <label class="flex">
        <input v-model="themeModel" class="mr-1" type="radio" value="ocean" />
        Ocean
      </label>
      <label class="flex mb-6">
        <input v-model="themeModel" class="mr-1" type="radio" value="grass" />
        Grass
      </label>

      <h2 class="text-md font-bold mb-2">Security</h2>
      <form class="mb-4 max-w-sm" @submit.prevent="resetPassowrd">
        <TextInput v-model="passwordResetData.password" type="password" label="Passwort" class="mb-2" />
        <TextInput
          v-model="passwordResetData.password_validation"
          type="password"
          label="Passwort wiederholen"
          class="mb-4"
        />
        <Button :disabled="!passwordResetValid" type="submit">Zurücksetzen</Button>
      </form>
      <Button @click="$auth.logout()">Ausloggen</Button>
    </div>
  </Layout>
</template>

<script>
import { mapState, mapMutations } from 'vuex'

export default {
  data() {
    return {
      passwordResetData: { password: '', password_validation: '' },
    }
  },
  computed: {
    ...mapState('theme', ['theme']),
    passwordResetValid() {
      if (!(this.passwordResetData.password || this.passwordResetData.password_validation)) {
        return false
      }
      return this.passwordResetData.password === this.passwordResetData.password_validation
    },
    themeModel: {
      get() {
        return this.theme
      },
      set(theme) {
        this.setTheme(theme)
      },
    },
  },
  methods: {
    ...mapMutations('theme', ['setTheme']),
    async resetPassowrd() {
      try {
        await this.$axios.$post('/auth/change_password/', this.passwordResetData)
        this.$toast.success('Passwort zurückgesetzt')
        this.$auth.logout()
      } catch (error) {}
    },
  },
}
</script>
