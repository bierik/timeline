<template>
  <Field v-bind="$attrs">
    <textarea
      v-model="value"
      class="w-full appearance-none rounded-lg border-2 border-gray-200 bg-gray-200 px-4 py-2 leading-tight text-gray-700 focus:border-primary-300 focus:bg-white focus:outline-none"
      required
      type="text"
    />
  </Field>
</template>

<script>
import fieldMixin from "@/components/fields/field-mixin";

export default {
  mixins: [fieldMixin],
};
</script>
