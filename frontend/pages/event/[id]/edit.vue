<template>
  <Layout>
    <div class="container px-4">
      <h1 class="mb-4 text-xl font-bold">Ereignis bearbeiten</h1>
      <Form
        v-model:errors="errors"
        class="w-full"
        :save="save"
        :cancel="cancel"
        :remove="remove"
        @success-remove="successRemove"
        @success="success"
      >
        <div class="flex flex-wrap gap-x-4">
          <TextInput
            v-model="event.title"
            class="mb-4 block grow"
            label="Titel"
          />
          <EmojiField
            v-model="event.icon"
            label="Icon"
            :errors="errorsForField('icon')"
            content-class="mb-4 block"
          />
          <DateInput
            v-model="event.date"
            label="Datum"
            class="mb-4 block grow"
          />
        </div>
        <div class="flex flex-wrap gap-x-4">
          <EventField
            v-model="event.relations"
            label="Verknüpfungen"
            class="mb-4 grow basis-full md:basis-0"
            :exclude="excludeFromSearch"
          />
          <PersonField
            v-model="event.people"
            label="Personen"
            class="mb-4 grow"
          />
        </div>
        <TUSUpload
          v-model="event.images"
          multiple
          class="mb-4 grow"
          :errors="errorsForField('images')"
          label="Bilder"
        />
        <label>
          <span class="block font-bold text-gray-500">Beschreibung</span>
          <Editor v-model="event.description" />
        </label>
      </Form>
    </div>
  </Layout>
</template>

<script>
import omit from "lodash/omit";
import partialRight from "lodash/partialRight";
import formErrorMixin from "@/components/form/form-error-mixin";

export default defineNuxtComponent({
  mixins: [formErrorMixin],
  async asyncData({ $axios }) {
    const route = useRoute();
    const { data: event } = await $axios.get(`/events/${route.params.id}/`);
    return { event };
  },
  computed: {
    excludeFromSearch() {
      return Number.parseInt(this.$route.params.id);
    },
  },
  mounted() {
    this.event.people = this.event.people.map((person) => person.id);
  },
  methods: {
    success({ id }) {
      this.$toast.success("Ereignis bearbeitet");
      this.$router.push({ name: "index", query: { activeEvent: id } });
    },
    save() {
      const images = this.event.images.map(partialRight(omit, "thumbnail"));
      return this.$axios.patch(`/events/${this.event.id}/`, {
        ...this.event,
        images,
      });
    },
    cancel() {
      this.$router.push({ name: "index", query: this.$route.query });
    },
    successRemove() {
      this.$router.push({ name: "index" });
      this.$toast.success("Ereignis gelöscht");
    },
    remove() {
      if (window.confirm("Ereignis wirklich löschen?")) {
        return this.$axios.delete(`/events/${this.event.id}/`);
      }
    },
  },
});
</script>
