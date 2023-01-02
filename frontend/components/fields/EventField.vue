<template>
  <div>
    <TextInput
      v-model="query"
      :label="label"
      placeholder="Nach Ereignissen suchen"
      target-class="rounded-bl-none rounded-br-none"
    />
    <div class="border-l-2 border-r-2 border-b-2 rounded-bl-md rounded-br-md">
      <template v-if="items.length">
        <label
          v-for="(item, index) in items"
          :key="`relation-${item.id}`"
          class="p-4 block hover:bg-gray-50"
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
import debounceAsync from 'debounce-async'
import isNumber from 'lodash/isNumber'
import uniqBy from 'lodash/uniqBy'

export default {
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
    label: {
      type: String,
      default: () => '',
    },
  },
  data() {
    return {
      loading: false,
      items: this.value,
      query: '',
      itemsCache: this.value,
    }
  },
  computed: {
    selectedItems: {
      get() {
        return this.value.map((value) => (isNumber(value) ? value : value.id))
      },
      set(selectedItems) {
        this.$emit('input', selectedItems)
      },
    },
  },
  watch: {
    query() {
      if (!this.query) {
        this.items = this.itemsCache
      } else {
        this.search()
      }
    },
  },
  mounted() {
    this.$emit(
      'input',
      this.value.map((value) => (isNumber(value) ? value : value.id)),
    )
  },
  methods: {
    async search() {
      if (!this.query) {
        return
      }
      try {
        await this.debouncedSearch()
      } catch (error) {
        if (error !== 'canceled') {
          throw error
        }
      }
    },
    selectItem() {
      this.query = ''
    },
    debouncedSearch: debounceAsync(async function debouncedSearch() {
      this.loading = true
      try {
        this.items = uniqBy(
          [...this.itemsCache, ...(await this.$axios.$get('/events/', { params: { title: this.query } })).results],
          'id',
        ).filter((item) => item.id !== this.exclude)
      } catch (e) {
        this.items = []
        throw e
      } finally {
        this.loading = false
      }
    }, 400),
  },
}
</script>
