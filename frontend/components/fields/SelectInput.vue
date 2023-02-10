<template>
  <Field v-bind="$attrs">
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
  </Field>
</template>

<script>
import fieldMixin from '@/components/fields/field-mixin'

export default {
  mixins: [fieldMixin],
  props: {
    options: {
      type: Array,
      default: () => [],
    },
  },
}
</script>
