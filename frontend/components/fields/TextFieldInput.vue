<template>
  <label>
    <span class="block text-gray-500 font-bold">{{ label }}</span>
    <textarea
      v-model="modelValue"
      class="bg-gray-200 appearance-none border-2 border-gray-200 rounded-lg w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-primary-300"
      required
      type="text"
    />
  </label>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
      default: () => '',
    },
    value: {
      type: String,
      required: true,
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
</script>
