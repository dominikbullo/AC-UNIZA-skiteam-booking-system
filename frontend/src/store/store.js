import Vue from 'vue'
import Vuex from 'vuex'

import state from './state'
import getters from './getters'
import mutations from './mutations'
import actions from './actions'

import moduleAuth from './auth/moduleAuth.js'
import moduleFamily from './family/moduleFamily.js'
import moduleEvent from './event/moduleEvent.js'
import moduleCalendar from './calendar/moduleCalendar.js'

Vue.use(Vuex)


export default new Vuex.Store({
  getters,
  mutations,
  state,
  actions,
  modules: {
    auth: moduleAuth,
    family: moduleFamily,
    event: moduleEvent,
    calendar: moduleCalendar
  },
  strict: process.env.NODE_ENV !== 'production'
})
