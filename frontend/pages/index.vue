<template></template>

<script>
export default {
  middleware({ redirect }) {
    redirect({ name: 'event-timeline' })
  },
}
</script>
