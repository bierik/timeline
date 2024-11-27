<template>
  <div class="flex h-screen flex-col items-center justify-center">
    <form
      class="rounded bg-slate-50 p-16"
      @submit.prevent="login"
    >
      <TextInput
        v-model="credentials.username"
        autofocus
        class="mb-4"
        type="text"
        autocapitalize="none"
        label="Benutzername"
      />
      <TextInput
        v-model="credentials.password"
        class="mb-4"
        type="password"
        label="Passwort"
      />
      <Button
        type="submit"
        class="w-full"
      >
        Login
      </Button>
    </form>
  </div>
</template>

<script>
import get from "lodash/get";
import { useAuthStore } from "@/store/auth";

export default defineNuxtComponent({
  data() {
    return {
      credentials: {},
    };
  },
  methods: {
    async login() {
      const authStore = useAuthStore();
      try {
        await authStore.login(this.credentials);
        this.$router.push({ name: "index" });
      } catch (error) {
        const status = get(error, "response.status");
        if (status >= 400 && status < 500) {
          this.$toast.warning("Die Zugangsdaten stimmen nicht");
          this.credentials.password = "";
        } else {
          throw error;
        }
      }
    },
  },
});
</script>
