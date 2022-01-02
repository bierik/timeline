<template>
  <div class="morph-dialog" :class="{ open }">
    Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's
    standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a
    type specimen book.
  </div>
</template>

<script>
export default {
  name: 'MorphDialog',
  props: {
    open: {
      type: Boolean,
      default: () => false,
    },
  },
}
</script>

<style>
.morph-dialog {
  border-radius: 10px;
  padding: 10px;
  z-index: -1;
  width: 300px;
  height: 300px;
  background: #f4c2c2;
  box-shadow: 0 0 0 6px #f5dddc;
  position: absolute;
  bottom: 65px;
  transform: scale(0);
  transform-origin: bottom;
  opacity: 0;
  transition: all 0.5s ease-in-out;
}

.morph-dialog.open {
  transform: scale(1);
  opacity: 1;
}
</style>
