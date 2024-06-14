<template>
  <Layout>
    <div class="container px-4">
      <h1 class="mb-4 text-xl font-bold">Neue Rolle hinzfügen</h1>
      <Form
        v-model:errors="errors"
        :save="save"
        :cancel="cancel"
        @success="success"
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
  data() {
    return {
      role: {
        name: "",
      },
    };
  },
  methods: {
    success() {
      this.$toast.success("Rolle erstellt");
      this.$router.push({ name: "role" });
    },
    save() {
      return this.$axios.post("/roles/", this.role);
    },
    cancel() {
      this.$router.push({ name: "role" });
    },
  },
});
</script>
