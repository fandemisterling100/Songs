// initial state
const state = () => ({
    all: [],
    default_type: 'info',
    position: 'all',
  })
  
  // getters
  const getters = {}
  
  // actions
  const actions = {
    showMessage ({ commit }, {message, type, position = 'all'}) {
      if(message) {
        const id = Math.random().toString(36).substring(2);
        commit('setMessage', {message, type, position, id});
  
        setTimeout(function() {
          commit('removeMessage', id)
        }, 5000)
      }
    },
    cleanMessages ({ commit }) {
      commit('cleanMessages')
    },
    removeMessage ({ commit }, id) {
      commit('removeMessage', id)
    }
  }
  
  // mutations
  const mutations = {
    setMessage (state, message) {
      state.all.push(message)
    },
    cleanMessages (state) {
      state.all = []
    },
    removeMessage (state, id) {
      state.all = state.all.filter(item => item.id !== id)
    },
  }
  
  export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }