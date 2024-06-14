import piniaPluginPersistedstate from "pinia-plugin-persistedstate";

export default defineNuxtPlugin({
  name: "pinia-persist",
  setup({ $pinia }) {
    $pinia.use(piniaPluginPersistedstate);
  },
});
