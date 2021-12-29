import Vue from 'vue'
import { DateTime } from 'luxon'

function toLocaleDateString(isoDateString) {
  return DateTime.fromISO(isoDateString).toLocaleString(DateTime.DATE_MED)
}

Vue.filter('toLocaleDateString', toLocaleDateString)
