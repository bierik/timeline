export default {
  inheritAttrs: false,
  props: {
    value: {
      required: true,
    },
    targetClass: {
      type: String,
      default: () => '',
    },
  },
  computed: {
    modelValue: {
      get() {
        return this.value
      },
      set(modelValue) {
        this.$emit('input', modelValue)
      },
    },
  },
}
