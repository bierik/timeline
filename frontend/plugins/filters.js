import { DateTime } from "luxon";

function toLocaleDateString(isoDateString) {
  const datetime = DateTime.fromISO(isoDateString);
  if (datetime.isValid) {
    return datetime.toLocaleString(DateTime.DATE_MED);
  }
  return isoDateString.toLocaleString(DateTime.DATE_MED);
}

export default defineNuxtPlugin(() => {
  return {
    provide: {
      toLocaleDateString: toLocaleDateString,
    },
  };
});
