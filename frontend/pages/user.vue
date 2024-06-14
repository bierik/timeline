<template>
  <Layout>
    <div class="container px-4">
      <h2 class="mb-2 font-bold">Theme</h2>
      <label class="flex">
        <input v-model="themeModel" class="mr-1" type="radio" value="sunrise" />
        Sunrise
      </label>
      <label class="flex">
        <input v-model="themeModel" class="mr-1" type="radio" value="ocean" />
        Ocean
      </label>
      <label class="mb-6 flex">
        <input v-model="themeModel" class="mr-1" type="radio" value="grass" />
        Grass
      </label>

      <h2 class="mb-2 font-bold">Security</h2>
      <form
        class="mb-4 max-w-sm"
        @submit.prevent="changePassword(passwordResetData)"
      >
        <TextInput
          v-model="passwordResetData.password"
          type="password"
          label="Passwort"
          class="mb-2"
        />
        <TextInput
          v-model="passwordResetData.password_validation"
          type="password"
          label="Passwort wiederholen"
          class="mb-4"
        />
        <Button :disabled="!passwordResetValid" type="submit"
          >Zurücksetzen</Button
        >
      </form>
      <Button @click="logout()">Ausloggen</Button>
    </div>
  </Layout>
</template>

<script>
import { mapActions, mapState } from "pinia";
import { useThemeStore } from "@/store/theme";
import { useAuthStore } from "@/store/auth";

export default defineNuxtComponent({
  data() {
    return {
      passwordResetData: { password: "", password_validation: "" },
    };
  },
  computed: {
    ...mapState(useThemeStore, ["theme"]),
    passwordResetValid() {
      if (
        !(
          this.passwordResetData.password ||
          this.passwordResetData.password_validation
        )
      ) {
        return false;
      }
      return (
        this.passwordResetData.password ===
        this.passwordResetData.password_validation
      );
    },
    themeModel: {
      get() {
        return this.theme;
      },
      set(theme) {
        this.setTheme(theme);
      },
    },
  },
  methods: {
    ...mapActions(useThemeStore, ["setTheme"]),
    ...mapActions(useAuthStore, ["logout", "changePassword"]),
  },
});
</script>
