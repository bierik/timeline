<template>
  <TextInput v-model="modelValue" type="date" v-bind="$attrs" />
</template>

<script>
export default {
  inheritAttrs: false,
  props: {
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
