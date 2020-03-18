/*=========================================================================================
  File Name: store.js
  Description: Vuex store
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
==========================================================================================*/


import Vue from 'vue'
import Vuex from 'vuex'

import state from './state'
import getters from './getters'
import mutations from './mutations'
import actions from './actions'

Vue.use(Vuex)

import moduleAuth from './auth/moduleAuth.js'
import moduleFamily from './family/moduleFamily.js'
import moduleCalendar from './calendar/moduleCalendar.js'


export default new Vuex.Store({
  getters,
  mutations,
  state,
  actions,
  modules: {
    auth: moduleAuth,
    family: moduleFamily,
    calendar: moduleCalendar
  },
  strict: process.env.NODE_ENV !== 'production'
})
