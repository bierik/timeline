import get from 'lodash/get'
import noop from 'lodash/noop'

export function escapeable(method) {
  return {
    mounted() {
      window.addEventListener('keyup', (event) => {
        if (event.key === 'Escape') {
          get(this, method, noop)()
        }
      })
    },
    beforeDestroy() {
      window.removeEventListener('keyup', get(this, method))
    },
  }
}

function lockModal() {
  window.document.documentElement.classList.add('overflow-hidden')
}
function unlockModal() {
  window.document.documentElement.classList.remove('overflow-hidden')
}
export function modalable(value) {
  return {
    methods: {
      lockModal,
      unlockModal,
    },
    watch: {
      [value](v) {
        v ? lockModal() : unlockModal()
      },
    },
  }
}
