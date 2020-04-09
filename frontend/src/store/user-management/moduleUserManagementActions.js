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
      axios.get('/user/')
        .then((response) => {
          commit('SET_USERS', response.data.results)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  fetchUser (context, userId) {
    return new Promise((resolve, reject) => {
      axios.get(`/user/${userId}`)
        .then((response) => {
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  fetchDefaultUser (context, userId) {
    return new Promise((resolve, reject) => {
      axios.get(`/api/user-management/user/268`)
        .then((response) => {
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  removeUser ({ commit }, userId) {
    return new Promise((resolve, reject) => {
      axios.delete(`/api/user-management/user/${userId}/`)
        .then((response) => {
          commit('REMOVE_RECORD', userId)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  fetchProfiles ({ commit }) {
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
  fetchProfile (context, userId) {
    return new Promise((resolve, reject) => {
      axios.get(`/profile/${userId}`)
        .then((response) => {
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  }
}
