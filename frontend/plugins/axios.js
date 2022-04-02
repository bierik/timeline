import qs from 'qs'

export default function ({ $axios }) {
  $axios.defaults.xsrfHeaderName = 'X-CSRFToken'
  $axios.defaults.xsrfCookieName = 'csrftoken'
  $axios.defaults.paramsSerializer = (params) => qs.stringify(params, { arrayFormat: 'repeat' })
}
