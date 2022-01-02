<template>
  <div class="event" @click="dialogOpen = !dialogOpen">
    <MorphDialog :open="dialogOpen" />
    <div class="event-icon">
      {{ icon }}
    </div>
    <div class="event-text">{{ title }}</div>
  </div>
</template>

<script>
export default {
  name: 'TimelineEvent',
  props: {
    title: {
      type: String,
      default: () => '',
    },
    icon: {
      type: String,
      default: () => '',
    },
  },
  data() {
    return {
      dialogOpen: false,
    }
  },
}
</script>

<style>
.vis-item.vis-box {
  border-color: transparent;
  background-color: transparent;
}

.vis-item.vis-dot {
  border-color: black;
  background-color: black;
}

.vis-item.vis-line {
  border-color: black;
  background-color: black;
}

.vis-item .vis-item-content {
  padding: 0;
}

.event {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.event-icon {
  transition: box-shadow 0.2s ease-in-out;
  border-radius: 50%;
  background-color: #f4c2c2;
  box-shadow: 0 0 0 6px #f5dddc;
  width: 50px;
  height: 50px;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
}

.vis-item.vis-box:hover .event-icon {
  box-shadow: 0 0 0 10px #f5dddc;
}

.event-text {
  background-color: black;
  color: white;
  padding: 5px;
  font-family: 'Courier Prime';
  font-size: 12px;
  line-height: normal;
}
</style>
