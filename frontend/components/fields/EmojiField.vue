<template>
  <div>
    <div
      ref="emoji-picker-anchor"
      :class="isOpen ? '' : 'hidden'"
      class="fixed inset-0 z-40 flex items-center justify-center bg-black/60"
      @click="close"
    />
    <div class="flex items-end">
      <TextInput
        v-bind="omit($attrs, 'class')"
        v-model="value"
        readonly
        maxlength="1"
        class="w-14"
        @click="open"
      />
    </div>
  </div>
</template>

<script>
import { Picker } from "emoji-mart";
import omit from "lodash/omit";
import { escapeable, modalable } from "@/mixins/modal";

export default defineNuxtComponent({
  mixins: [escapeable("close"), modalable("isOpen")],
  props: {
    modelValue: {
      type: String,
      default: () => "",
    },
  },
  data() {
    const picker = new Picker({
      theme: "light",
      locale: "de",
      previewPosition: "none",
      onEmojiSelect: this.select,
    });
    picker.addEventListener("click", (event) => {
      event.stopPropagation();
    });
    return {
      isOpen: false,
      picker,
    };
  },
  computed: {
    value: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:model-value", value);
      },
    },
  },
  mounted() {
    document.body.prepend(this.$refs["emoji-picker-anchor"]);
    this.$refs["emoji-picker-anchor"].appendChild(this.picker);
  },
  methods: {
    omit,
    close() {
      this.isOpen = false;
    },
    open() {
      this.isOpen = true;
    },
    select(emoji) {
      this.$emit("update:model-value", emoji.native);
      this.isOpen = false;
    },
    escaped() {
      this.close();
    },
  },
});
</script>
