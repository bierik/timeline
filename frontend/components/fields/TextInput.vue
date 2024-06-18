<template>
  <Field>
    <input
      v-bind="$attrs"
      v-model="value"
      class="w-full appearance-none rounded-lg border-2 border-gray-200 bg-gray-200 px-4 py-2 leading-tight text-gray-700 focus:border-primary-300 focus:bg-white focus:outline-none"
      :type="inputType"
    />
  </Field>
</template>

<script>
export default defineNuxtComponent({
  name: "TextInput",
  props: {
    modelValue: {
      type: String,
      default: () => "",
    },
  },
  computed: {
    inputType() {
      return this.$attrs.type || "text";
    },
    value: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:model-value", value);
      },
    },
  },
});
</script>
