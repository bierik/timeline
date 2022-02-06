<template>
  <div id="editorjs" />
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
