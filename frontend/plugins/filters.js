import { DateTime } from 'luxon'
import Vue from 'vue'

function toLocaleDateString(isoDateString) {
  const datetime = DateTime.fromISO(isoDateString)
  if (datetime.isValid) {
    return datetime.toLocaleString(DateTime.DATE_MED)
  }
  return isoDateString.toLocaleString(DateTime.DATE_MED)
}

Vue.filter('toLocaleDateString', toLocaleDateString)
