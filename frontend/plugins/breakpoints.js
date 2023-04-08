import resolveConfig from 'tailwindcss/resolveConfig'
import tailwindConfig from '../tailwind.config'

function matchScreenSize(screens) {
  const width = window.innerWidth
  return Object.entries(screens).reduce((accum, [screen, size]) => {
    const sizeNumber = Number.parseInt(size)
    return Object.assign(accum, {
      [`${screen}AndUp`]: width >= sizeNumber,
      [`${screen}AndDown`]: width <= sizeNumber,
      [screen]: width === sizeNumber,
    })
  }, {})
}

export default function ({ $config }) {
  const {
    theme: { screens },
  } = resolveConfig(tailwindConfig)
  $config.breakpoints = matchScreenSize(screens)
}
