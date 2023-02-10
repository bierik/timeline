<template>
  <Field v-bind="$attrs">
    <textarea
      v-model="modelValue"
      class="bg-gray-200 appearance-none border-2 border-gray-200 rounded-lg w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-primary-300"
      required
      type="text"
    />
  </Field>
</template>

<script>
import fieldMixin from '@/components/fields/field-mixin'

export default {
  mixins: [fieldMixin],
}
</script>
