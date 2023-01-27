import Vue from 'vue'
import Vuex from 'vuex'
import roles from './modules/roles'
import messages from './modules/messages'
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex)

const debug = true;

export default new Vuex.Store({
  modules: {
    roles,
    messages,
  },
  strict: debug,
  plugins: [
    createPersistedState({
      paths: [],
    }),
],
})