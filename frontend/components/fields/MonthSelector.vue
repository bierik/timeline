<template>
  <div class="flex m-2">
    <SelectInput v-model="month" class="mr-2" :options="monthChoices" />
    <TextInput v-model="year" class="w-20" />
  </div>
</template>

<script>
import range from 'lodash/range'
import DateTime from 'luxon/src/datetime'

export default {
  props: {
    value: {
      type: DateTime,
      default: () => DateTime.local(),
    },
  },
  data() {
    return {
      monthChoices: range(1, 13).map((month) => ({
        display_name: DateTime.fromObject({ month }).setLocale('de-CH').toLocaleString({ month: 'long' }),
        value: month,
      })),
    }
  },
  computed: {
    month: {
      get() {
        return this.value.month
      },
      set(month) {
        this.$emit('input', this.value.set({ month }))
      },
    },
    year: {
      get() {
        return this.value.toFormat('yyyy')
      },
      set(year) {
        if (!/^\d{4}$/.test(year)) {
          return
        }
        this.$emit('input', this.value.set({ year }))
      },
    },
  },
}
</script>
