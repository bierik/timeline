<template>
  <div v-bind="$attrs">
    <TextInput
      v-model="query"
      v-bind="omit($attrs, 'class')"
      placeholder="Nach Ereignissen suchen"
      target-class="rounded-bl-none rounded-br-none"
    />
    <div class="rounded-b-md border-x-2 border-b-2">
      <template v-if="items.length">
        <label
          v-for="(item, index) in items"
          :key="`relation-${item.id}`"
          class="block p-4 hover:bg-gray-50"
          :class="{ 'border-b-2': index !== items.length - 1 }"
        >
          <input v-model="selectedItems" type="checkbox" :value="item.id" />
          {{ item.title }}
        </label>
      </template>
      <span v-else class="block p-4">Keine Ergebnisse</span>
    </div>
  </div>
</template>

<script>
import debounce from "lodash/debounce";
import isNumber from "lodash/isNumber";
import uniqBy from "lodash/uniqBy";
import omit from "lodash/omit";
import pick from "lodash/pick";

export default defineNuxtComponent({
  inheritAttrs: false,
  props: {
    exclude: {
      type: Number,
      default: () => null,
    },
    value: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      loading: false,
      items: this.value,
      query: "",
      itemsCache: this.value,
    };
  },
  computed: {
    selectedItems: {
      get() {
        return this.value.map((value) => (isNumber(value) ? value : value.id));
      },
      set(selectedItems) {
        this.$emit("update:model-value", selectedItems);
      },
    },
  },
  watch: {
    query() {
      if (!this.query) {
        this.items = this.itemsCache;
      } else {
        this.search();
      }
    },
  },
  mounted() {
    this.$emit(
      "update:model-value",
      this.value.map((value) => (isNumber(value) ? value : value.id))
    );
  },
  methods: {
    omit,
    pick,
    async search() {
      if (!this.query) {
        return;
      }
      try {
        await this.debouncedSearch();
      } catch (error) {
        if (error !== "canceled") {
          throw error;
        }
      }
    },
    selectItem() {
      this.query = "";
    },
    debouncedSearch: debounce(
      async function debouncedSearch() {
        this.loading = true;
        try {
          this.items = uniqBy(
            [
              ...this.itemsCache,
              ...(
                await this.$axios.get("/events/", {
                  params: { title: this.query },
                })
              ).data.results,
            ],
            "id"
          ).filter((item) => item.id !== this.exclude);
        } catch (e) {
          this.items = [];
          throw e;
        } finally {
          this.loading = false;
        }
      },
      400,
      { leading: true, trailing: false }
    ),
  },
});
</script>
