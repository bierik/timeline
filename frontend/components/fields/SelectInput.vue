<template>
  <Field v-bind="$attrs">
    <select
      v-model="value"
      v-bind="omit($attrs, 'class')"
      :class="targetClass"
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
import fieldMixin from "@/components/fields/field-mixin";
import omit from "lodash/omit";

export default {
  mixins: [fieldMixin],
  methods: {
    omit,
  },
  props: {
    options: {
      type: Array,
      default: () => [],
    },
  },
};
</script>
