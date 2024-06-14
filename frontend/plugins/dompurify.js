import VueDOMPurifyHTML from "vue-dompurify-html";

export default defineNuxtPlugin(({ vueApp }) => {
  vueApp.use(VueDOMPurifyHTML);
});
