export default defineNuxtPlugin(() => {
  return {
    provide: {
      toast: {
        success: () => {},
        error: () => {},
        warning: () => {},
      },
    },
  };
});
