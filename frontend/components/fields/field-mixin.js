export default {
  inheritAttrs: false,
  props: {
    modelValue: {
      required: true,
    },
    targetClass: {
      type: String,
      default: () => "",
    },
  },
  computed: {
    value: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:model-value", value);
      },
    },
  },
};
