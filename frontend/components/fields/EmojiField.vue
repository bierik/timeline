<template>
  <div>
    <div
      ref="emoji-picker-anchor"
      :class="isOpen ? '' : 'hidden'"
      class="z-10 bg-black/60 emoji-picker-anchor flex items-center justify-center fixed inset-0"
      @click="close"
    />
    <div class="flex items-end" :class="contentClass">
      <TextInput maxlength="1" class="mr-2 w-14" v-bind="$attrs" v-on="$listeners" />
      <Button @click="open">
        <feather type="smile" />
      </Button>
    </div>
  </div>
</template>
<script>
import { Picker } from 'emoji-mart'
import { escapeable, modalable } from '@/components/mixins'

export default {
  mixins: [escapeable('close'), modalable('isOpen')],
  props: {
    contentClass: {
      type: String,
      default: () => '',
    },
  },
  data() {
    const picker = new Picker({
      theme: 'light',
      locale: 'de',
      previewPosition: 'none',
      onEmojiSelect: this.select,
    })
    picker.addEventListener('click', (event) => {
      event.stopPropagation()
    })
    return {
      isOpen: false,
      picker,
    }
  },
  mounted() {
    this.$refs['emoji-picker-anchor'].appendChild(this.picker)
  },
  methods: {
    close() {
      this.isOpen = false
    },
    open() {
      this.isOpen = true
    },
    select(emoji) {
      this.$emit('input', emoji.native)
      this.isOpen = false
    },
    escaped() {
      this.close()
    },
  },
}
</script>
