<template>
  <Layout>
    <div class="container px-4">
      <h1 class="mb-4 text-xl font-bold">
        Neues Ereignis hinzfügen
      </h1>
      <Form
        v-model:errors="errors"
        class="w-full"
        :save="save"
        :cancel="cancel"
        @success="success"
      >
        <div class="flex flex-wrap gap-x-4">
          <TextInput
            v-model="event.title"
            :errors="errorsForField('title')"
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
            :errors="errorsForField('date')"
            label="Datum"
            class="mb-4 block grow"
          />
        </div>
        <div class="flex flex-wrap gap-x-4">
          <EventField
            v-model="event.relations"
            :errors="errorsForField('relations')"
            label="Verknüpfungen"
            class="mb-4 grow basis-full md:basis-0"
          />
          <PersonField
            v-model="event.people"
            :errors="errorsForField('people')"
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
import { DateTime } from "luxon";
import formErrorMixin from "@/components/form/form-error-mixin";

export default defineNuxtComponent({
  mixins: [formErrorMixin],
  data() {
    return {
      event: {
        title: "",
        description: null,
        date: DateTime.local().toISODate(),
        icon: "",
        people: [],
        relations: [],
        images: [],
      },
    };
  },
  methods: {
    success({ id }) {
      this.$toast.success("Ereignis erstellt");
      this.$router.push({ name: "index", query: { activeEvent: id } });
    },
    save() {
      const images = this.event.images.map(partialRight(omit, "thumbnail"));
      return this.$axios.post("/events/", { ...this.event, images });
    },
    cancel() {
      this.$router.push("/");
    },
  },
});
</script>
