<template>
  <Layout>
    <div class="container px-4">
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
export default {
  data() {
    return {
      passwordResetData: { password: '', password_validation: '' },
    }
  },
  computed: {
    passwordResetValid() {
      if (!(this.passwordResetData.password || this.passwordResetData.password_validation)) {
        return false
      }
      return this.passwordResetData.password === this.passwordResetData.password_validation
    },
  },
  methods: {
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
