import { defineStore } from "pinia";
import first from "lodash/first";

export const useAuthStore = defineStore("authStore", {
  state: () => ({
    token: null,
    user: {},
  }),
  actions: {
    async login(credentials) {
      const { $axios } = useNuxtApp();
      const {
        data: { token, user },
      } = await $axios.post("/auth/login/", credentials);
      this.token = token;
      this.user = user;
    },
    async logout() {
      const { $axios } = useNuxtApp();
      const router = useRouter();
      await $axios.post("/auth/logout/");
      this.token = null;
      this.user = {};
      router.push({ name: "login" });
    },
    async changePassword(credentials) {
      const { $axios } = useNuxtApp();
      const router = useRouter();
      await $axios.post("/auth/change_password/", credentials);
      router.push({ name: "login" });
    },
  },
  getters: {
    signature() {
      return [
        first(Array.from(this.user.first_name || "")),
        first(Array.from(this.user.last_name || "")),
      ].join("");
    },
  },
  persist: true,
});
