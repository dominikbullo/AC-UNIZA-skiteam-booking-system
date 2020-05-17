/*=========================================================================================
  File Name: moduleCalendarActions.js
  Description: Calendar Module Actions
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
==========================================================================================*/

import axios from '@/axios.js'

export default {
  fetchUsers ({ commit }) {
    console.log('[STORE] fetchUsers')
    return new Promise((resolve, reject) => {
      axios.get('/profile/')
        .then((response) => {
          commit('SET_USERS', response.data.results)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  fetchChildrenStatistics ({ commit }) {
    console.log('[STORE] fetchUsers')
    return new Promise((resolve, reject) => {
      axios.get('/children/stats/')
        .then((response) => {
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  fetchUser (context, userId) {
    console.log('[STORE] fetchUser', userId)
    return new Promise((resolve, reject) => {
      axios.get(`/profile/${userId}/`)
        .then((response) => {
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  editUser ({ commit }, payload) {
    const id = this.state.AppActiveUser.id
    return new Promise((resolve, reject) => {
      axios.patch(`/profile/${id}/`, payload)
        .then((response) => {
          console.log('user', response)
          commit('UPDATE_USER_INFO', response.data, { root: true })
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  resetPassword ({ commit }, payload) {
    console.log('resetPassword')
    return new Promise((resolve, reject) => {
      axios.put('/profile/password-change/', payload)
        .then((response) => {
          // TODO commit token or logout
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  }
}
