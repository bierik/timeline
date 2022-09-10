<template>
  <SelectInput v-bind="$attrs" v-model="modelValue" multiple :options="options" />
</template>

<script>
export default {
  inheritAttrs: false,
  props: {
    value: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      options: [],
    }
  },
  async fetch() {
    const people = await this.$axios.$get('/people/')
    this.options = people.map((person) => ({ display_name: person.name, value: person.id }))
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
