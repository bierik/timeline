import { useThemeStore } from "@/store/theme";

function setTheme(prevTheme, theme) {
  document.documentElement.classList.remove(`theme-${prevTheme}`);
  document.documentElement.classList.add(`theme-${theme}`);
}

export default defineNuxtPlugin({
  name: "theme",
  dependsOn: ["pinia-persist"],
  setup() {
    const themeStore = useThemeStore();
    setTheme(themeStore.prevTheme, themeStore.theme);
    themeStore.$subscribe((_, { theme, prevTheme }) => {
      setTheme(prevTheme, theme);
    });
  },
});
