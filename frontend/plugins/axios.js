import qs from "qs";
import axios from "axios";
import { useAuthStore } from "@/store/auth";

export default defineNuxtPlugin({
  name: "axios",
  dependsOn: ["pinia-persist"],
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    const client = axios.create({
      xsrfHeaderName: "X-CSRFToken",
      xsrfCookieName: "csrftoken",
      paramsSerializer: (params) =>
        qs.stringify(params, { arrayFormat: "repeat" }),
      baseURL: "/api",
    });

    client.interceptors.request.use(
      (config) => {
        if (authStore.token) {
          config.headers.Authorization = `Token ${authStore.token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    client.interceptors.response.use(
      (res) => Promise.resolve(res),
      (error) => {
        if (error?.response?.status == 401) {
          router.push({ name: "login" });
        }
        return Promise.reject(error);
      }
    );
    return {
      provide: {
        axios: client,
      },
    };
  },
});
