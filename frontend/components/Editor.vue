<template>
  <div :id="holderId" />
</template>

<script>
import BalloonEditor from '@ckeditor/ckeditor5-build-inline'
import { v4 as uuidv4 } from 'uuid'

export default {
  props: {
    value: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      editor: Promise.resolve(null),
      holderId: `editor_${uuidv4()}`,
    }
  },
  async beforeDestroy() {
    await this.destroy()
  },
  async mounted() {
    await this.init()
  },
  methods: {
    async init() {
      await this.destroy()
      this.editor = await BalloonEditor.create(document.getElementById(this.holderId), {
        toolbar: ['bold', 'italic'],
      })
      this.editor.model.document.on('change:data', () => {
        this.$emit('input', this.editor.getData())
      })
    },
    async destroy() {
      if (await this.editor) {
        await this.editor.destroy()
        this.editor = Promise.resolve(null)
      }
    },
  },
}
</script>
