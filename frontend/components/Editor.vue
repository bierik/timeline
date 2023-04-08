<template>
  <div :id="holderId" class="bg-gray-200 border-2 border-gray-200 rounded-lg w-full py-4 text-gray-700 flex flex-col" />
</template>

<script>
import EditorJS from '@editorjs/editorjs'
import { v4 as uuidv4 } from 'uuid'

export default {
  props: {
    value: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      editor: null,
      holderId: `editor_${uuidv4()}`,
    }
  },
  mounted() {
    if (this.editor) {
      this.editor.destroy()
      this.editor = null
    }
    this.editor = new EditorJS({
      holder: this.holderId,
      data: this.value,
      onChange: async (api) => {
        const content = await api.saver.save()
        this.$emit('input', content)
      },
    })
  },
}
</script>
