<template>
  <Field>
    <select
      v-bind="$attrs"
      v-model="value"
      class="w-full appearance-none rounded-lg border-2 border-gray-200 bg-gray-200 px-4 py-2 leading-tight text-gray-700 focus:border-primary-300 focus:bg-white focus:outline-none"
    >
      <option
        v-for="option in options"
        :key="option.value"
        :value="option.value"
      >
        {{ option.display_name }}
      </option>
    </select>
  </Field>
</template>

<script>
export default defineNuxtComponent({
  props: {
    modelValue: {
      type: [String, Number, Array],
      default: () => [],
    },
    options: {
      type: Array,
      default: () => [],
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
