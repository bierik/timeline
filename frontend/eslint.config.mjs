import tailwind from "eslint-plugin-tailwindcss";
import withNuxt from "./.nuxt/eslint.config.mjs";

export default withNuxt(tailwind.configs["flat/recommended"], {
  rules: {
    "vue/multi-word-component-names": "off",
    "vue/html-self-closing": [
      "off",
      {
        html: {
          normal: "never",
          void: "always",
        },
      },
    ],
  },
});
