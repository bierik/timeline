<template>
  <div class="m-2 flex">
    <SelectInput
      v-model="month"
      class="mr-2"
      :options="monthChoices"
    />
    <TextInput
      v-model="year"
      class="w-20"
    />
  </div>
</template>

<script>
import range from "lodash/range";
import { DateTime } from "luxon";

export default defineNuxtComponent({
  props: {
    modelValue: {
      type: DateTime,
      default: () => DateTime.local(),
    },
  },
  data() {
    return {
      monthChoices: range(1, 13).map((month) => ({
        display_name: DateTime.fromObject({ month })
          .setLocale("de-CH")
          .toLocaleString({ month: "long" }),
        value: month,
      })),
    };
  },
  computed: {
    month: {
      get() {
        return this.modelValue.month;
      },
      set(month) {
        this.$emit("update:model-value", this.modelValue.set({ month }));
      },
    },
    year: {
      get() {
        return this.modelValue.toFormat("yyyy");
      },
      set(year) {
        if (!/^\d{4}$/.test(year)) {
          return;
        }
        this.$emit("update:model-value", this.modelValue.set({ year }));
      },
    },
  },
});
</script>
