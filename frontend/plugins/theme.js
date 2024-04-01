export default function ({ store }) {
  store.subscribe(({ type }, { theme }) => {
    if (type === 'theme/setTheme') {
      document.documentElement.classList.replace(`theme-${theme.prevTheme}`, `theme-${theme.theme}`)
    }
    document.documentElement.classList.add(`theme-${store.state.theme.theme}`)
  })
}
