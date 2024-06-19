import ToastPlugin from "vue-toast-notification";
import "vue-toast-notification/dist/theme-default.css";

export default defineNuxtPlugin(({ vueApp }) => {
  vueApp.use(ToastPlugin, {
    position: "top-right",
  });
});
