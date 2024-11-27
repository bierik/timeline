<template>
  <SelectInput
    multiple
    :options="options"
    v-bind="$attrs"
  />
</template>

<script>
export default defineNuxtComponent({
  data() {
    return {
      options: [],
    };
  },
  async mounted() {
    const { data: people } = await this.$axios.get("/people/");
    this.options = people.map((person) => ({
      display_name: person.name,
      value: person.id,
    }));
  },
});
</script>
