import Vue from 'vue'
import Vuex from 'vuex'

import * as getters from './getters'
import * as actions from './actions'
import * as mutations from './mutations'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    currentProject: {
      code: '',
      name: '',
      menu: {},
    },
    user: {
      // name: 'Test test',
      // login: 'root',
    },
    currentPage: '',
    startDate: '',
    endDate: '',
  },
  getters: {
    ...getters
  },
  mutations: {
    ...mutations
  },
  actions: {
    ...actions
  },
  modules: {
  }
})
