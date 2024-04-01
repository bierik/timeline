export const state = () => ({
  theme: 'sunrise',
  prevTheme: 'sunrise',
})

export const mutations = {
  setTheme(state, theme) {
    state.prevTheme = state.theme
    state.theme = theme
  },
}
