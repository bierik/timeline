import get from "lodash/get";

export default {
  data() {
    return {
      errors: {},
      valid: null,
    };
  },
  methods: {
    errorsForField(field) {
      return get(this.errors, field);
    },
  },
};
