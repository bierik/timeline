export default function () {
  document.documentElement.removeAttribute('class')
  document.documentElement.classList.add(`theme-${localStorage.getItem('theme')}`)
}
