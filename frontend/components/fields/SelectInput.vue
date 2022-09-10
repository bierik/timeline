<template>
  <label>
    <span class="block text-gray-500 font-bold">{{ label }}</span>
    <select
      v-model="modelValue"
      v-bind="$attrs"
      :class="targetClass"
      class="bg-gray-200 appearance-none border-2 border-gray-200 rounded-lg w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-primary-300"
    >
      <option v-for="option in options" :key="option.value" :value="option.value">
        {{ option.display_name }}
      </option>
    </select>
  </label>
</template>

<script>
export default {
  inheritAttrs: false,
  props: {
    label: {
      type: String,
      default: () => '',
    },
    value: {
      type: [Number, Array],
      required: true,
    },
    targetClass: {
      type: String,
      default: () => '',
    },
    options: {
      type: Array,
      default: () => [],
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
