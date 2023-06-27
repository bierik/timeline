<template>
  <Field v-bind="$attrs">
    <input
      v-model="modelValue"
      v-bind="$attrs"
      :class="targetClass"
      class="bg-gray-200 appearance-none border-2 border-gray-200 rounded-lg w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-primary-300"
      :type="inputType"
      v-on="omit($listeners, ['input'])"
    />
  </Field>
</template>

<script>
import omit from 'lodash/omit'
import fieldMixin from '@/components/fields/field-mixin'

export default {
  name: 'TextInput',
  mixins: [fieldMixin],
  computed: {
    inputType() {
      return this.$attrs.type || 'text'
    },
  },
  methods: {
    omit,
  },
}
</script>
