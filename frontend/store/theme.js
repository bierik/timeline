import { defineStore } from "pinia";

export const useThemeStore = defineStore("themeStore", {
  state: () => ({
    theme: "sunrise",
    prevTheme: "sunrise",
  }),
  actions: {
    setTheme(theme) {
      this.prevTheme = this.theme;
      this.theme = theme;
    },
  },
  persist: true,
});
