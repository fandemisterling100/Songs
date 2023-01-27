import Api from '../../utils/api'

// initial state
const state = () => ({
    roles: []
  })

// getters
const getters = {
}

// actions
const actions = {
  getRoles({ state, commit }) {
    let url = "/api/v1/roles/"
    Api.get(url)
      .then((response) => {
        commit('setRoles', response.data)
      })
      .catch(error => {
        throw error
      })
  },
}

// mutations
const mutations = {
  setRoles (state, value) {
    state.roles = value
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
