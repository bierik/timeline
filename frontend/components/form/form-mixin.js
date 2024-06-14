import get from "lodash/get";
import isEqual from "lodash/isEqual";
import noop from "lodash/noop";

export default {
  props: {
    save: {
      type: Function,
      default: noop,
    },
    remove: {
      type: Function,
      default: noop,
    },
    cancel: {
      type: Function,
      default: noop,
    },
    errors: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      loading: false,
      valid: null,
    };
  },
  computed: {
    disableRemove() {
      return isEqual(this.remove, noop);
    },
  },
  methods: {
    async _remove() {
      try {
        const response = await this.remove();
        this.$emit("success-remove", response);
      } catch (error) {
        const status = get(error, "response.status");
        if (status >= 500) {
          this.$emit("serverError", error);
          this.$toast.error(JSON.stringify(error.response.data));
        } else {
          this.$emit("error", error);
          throw error;
        }
      }
    },
    async _save() {
      this.loading = true;
      try {
        const response = await this.save();
        this.$emit("success", response);
      } catch (error) {
        const status = get(error, "response.status");
        if (status >= 400 && status < 500) {
          this.$emit("update:errors", error.response.data);
          this.$toast.warning("Überprüfen Sie die Eingabefelder auf Fehler.");
          this.$emit("clientError", error);
        } else if (status >= 500) {
          this.$emit("serverError", error);
          this.$toast.error("Es ist ein unerwarteter Fehler aufgetreten.");
        } else {
          this.$emit("error", error);
          throw error;
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
