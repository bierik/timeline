<template>
  <div
    :id="$options.holderId"
    class="w-full rounded-lg border-2 border-gray-200 bg-gray-200 py-4 text-gray-700"
  />
</template>

<script>
import { v4 as uuidv4 } from "uuid";

export default defineNuxtComponent({
  props: {
    modelValue: {
      type: String,
      default: "",
    },
  },
  holderId: `editor_${uuidv4()}`,
  editor: null,
  async beforeUnmount() {
    await this.destroy();
  },
  async mounted() {
    await this.init();
  },
  methods: {
    async init() {
      await this.destroy();
      const { default: BalloonEditor } = await import(
        "@ckeditor/ckeditor5-build-inline"
      );
      this.$options.editor = await BalloonEditor.create(
        document.getElementById(this.$options.holderId),
        {
          toolbar: ["bold", "italic"],
        },
      );
      this.$options.editor.model.document.on("change:data", () => {
        this.$emit("update:model-value", this.$options.editor.getData());
      });
      this.$options.editor.setData(this.modelValue || "");
    },
    async destroy() {
      if (this.$options.editor && this.$options.editor.state !== "destroyed") {
        await this.$options.editor.destroy();
        this.editor = null;
      }
    },
  },
});
</script>
