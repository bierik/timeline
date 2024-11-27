<template>
  <Layout>
    <div class="container px-4">
      <h1 class="mb-4 text-xl font-bold">
        Neue Person hinzfügen
      </h1>
      <Form
        v-model:errors="errors"
        :save="save"
        :cancel="cancel"
        @success="success"
      >
        <div class="flex flex-wrap gap-x-4">
          <TextInput
            v-model="person.name"
            :errors="errorsForField('name')"
            class="mb-4 block grow basis-full md:basis-0"
            label="Name"
          />
          <SelectInput
            v-model="person.role"
            :errors="errorsForField('role')"
            class="mb-4 block grow"
            label="Rolle"
            :options="roleChoices"
          />
        </div>
        <TUSUpload
          v-model="person.image"
          class="grow"
          :errors="errorsForField('image')"
          label="Bild"
        />
      </Form>
    </div>
  </Layout>
</template>

<script>
import omit from "lodash/omit";
import formErrorMixin from "@/components/form/form-error-mixin";

export default defineNuxtComponent({
  mixins: [formErrorMixin],
  async asyncData({ $axios }) {
    const { data: roles } = await $axios.get("/roles/");
    const roleChoices = roles.map(({ id, name }) => ({
      value: id,
      display_name: name,
    }));
    return { roleChoices };
  },
  data() {
    return {
      person: {
        name: "",
        role: null,
        image: {},
      },
    };
  },
  methods: {
    success() {
      this.$toast.success("Person erstellt");
      this.$router.push({ name: "person" });
    },
    save() {
      return this.$axios.post("/people/", {
        ...this.person,
        image: omit(this.person.image, "thumbnail"),
      });
    },
    cancel() {
      this.$router.push({ name: "person" });
    },
  },
});
</script>
