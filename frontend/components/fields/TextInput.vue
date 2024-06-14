<template>
  <Field v-bind="$attrs">
    <input
      v-model="value"
      v-bind="omit($attrs, 'class')"
      :class="targetClass"
      class="w-full appearance-none rounded-lg border-2 border-gray-200 bg-gray-200 px-4 py-2 leading-tight text-gray-700 focus:border-primary-300 focus:bg-white focus:outline-none"
      :type="inputType"
    />
  </Field>
</template>

<script>
import omit from "lodash/omit";
import fieldMixin from "@/components/fields/field-mixin";

export default {
  name: "TextInput",
  mixins: [fieldMixin],
  computed: {
    inputType() {
      return this.$attrs.type || "text";
    },
  },
  methods: {
    omit,
  },
};
</script>
