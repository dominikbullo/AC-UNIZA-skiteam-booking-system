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
    return new Promise((resolve, reject) => {
      axios.get('/users/')
        .then((response) => {
          commit('SET_USERS', response.data.results)
          resolve(response)
        })
        .catch((error) => { reject(error) })
    })
  },
  fetchUser (context, userId) {
    return new Promise((resolve, reject) => {
      axios.get(`/users/${userId}`)
        .then((response) => {
          resolve(response)
        })
        .catch((error) => { reject(error) })
    })
  },
  fetchProfiles ({ commit }) {
    return new Promise((resolve, reject) => {
      axios.get('/profiles/')
        .then((response) => {
          commit('SET_USERS', response.data.results)
          resolve(response)
        })
        .catch((error) => { reject(error) })
    })
  },
  fetchProfile (context, userId) {
    return new Promise((resolve, reject) => {
      axios.get(`/profiles/${userId}`)
        .then((response) => {
          resolve(response)
        })
        .catch((error) => { reject(error) })
    })
  },
  removeRecord ({ commit }, userId) {
    return new Promise((resolve, reject) => {
      axios.delete(`/api/user-management/users/${userId}/`)
        .then((response) => {
          commit('REMOVE_RECORD', userId)
          resolve(response)
        })
        .catch((error) => { reject(error) })
    })
  }
}
