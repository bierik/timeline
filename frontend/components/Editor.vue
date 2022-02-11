<template>
  <div id="editorjs" class="bg-gray-200 border-2 border-gray-200 rounded-lg w-full py-4 text-gray-700 flex flex-col" />
</template>

<script>
import EditorJS from '@editorjs/editorjs'

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
    }
  },
  mounted() {
    if (this.editor) {
      this.editor.destroy()
      this.editor = null
    }
    this.editor = new EditorJS({
      data: this.value,
      onChange: async (api) => {
        const content = await api.saver.save()
        this.$emit('input', content)
      },
    })
  },
}
</script>
