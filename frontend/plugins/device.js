function isTouchDevice() {
  return window.matchMedia("(pointer: coarse)").matches;
}

export default defineNuxtPlugin(({ $config }) => {
  Object.assign($config, {
    device: {
      isTouchDevice: isTouchDevice(),
    },
  });
});
