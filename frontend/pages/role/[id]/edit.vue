<template>
  <Layout>
    <div class="container px-4">
      <h1 class="mb-4 text-xl font-bold">Rolle bearbeiten</h1>
      <Form
        v-model:errors="errors"
        class="w-full"
        :save="save"
        :cancel="cancel"
        :remove="remove"
        @success="success"
        @success-remove="successRemove"
      >
        <TextInput
          v-model="role.name"
          :errors="errorsForField('name')"
          class="mb-4 block grow"
          label="Name"
        />
      </Form>
    </div>
  </Layout>
</template>

<script>
import formErrorMixin from "@/components/form/form-error-mixin";

export default defineNuxtComponent({
  mixins: [formErrorMixin],
  async asyncData({ $axios }) {
    const route = useRoute();
    const { data: role } = await $axios.get(`/roles/${route.params.id}/`);
    return { role };
  },
  methods: {
    success() {
      this.$toast.success("Rolle bearbeitet");
      this.$router.push({ name: "role", query: this.$route.query });
    },
    save() {
      return this.$axios.patch(`/roles/${this.role.id}/`, this.role);
    },
    cancel() {
      this.$router.push({ name: "role", query: this.$route.query });
    },
    successRemove() {
      this.$router.push({ name: "role" });
      this.$toast.success("Rolle gelöscht");
    },
    remove() {
      if (window.confirm("Rolle wirklich löschen?")) {
        return this.$axios.delete(`/roles/${this.role.id}/`);
      }
    },
  },
});
</script>
