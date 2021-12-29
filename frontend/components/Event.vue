<template>
  <div class="event">
    <div class="event-line" />
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
}
</script>

<style>
.event {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  position: absolute;
  transform: translateX(-50%);
  top: -120px;
  cursor: pointer;
}

.event-icon {
  border-radius: 50%;
  background-color: #f4c2c2;
  padding: 30px;
  font-size: 40px;
  box-shadow: 0 0 0 6px #f4c2c280;
  width: 50px;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  margin-bottom: 10px;
  transition: box-shadow 0.2s ease-in-out;
}

.event-icon:hover {
  box-shadow: 0 0 0 10px #f4c2c280;
}

.event-text {
  background-color: black;
  color: white;
  padding: 5px;
  font-family: 'Courier Prime';
  font-size: 12px;
  line-height: normal;
}

.event-line {
  width: 1px;
  background: black;
  height: 60px;
  position: absolute;
  top: 60px;
  z-index: -1;
}
</style>
