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
  addChild ({commit}, payload) {
    console.log(payload)
    return new Promise((resolve, reject) => {

      axios.post('/children/', {user: payload})
        .then((response) => {
          commit('ADD_MEMBER', Object.assign(payload, {id: response.data.id}))
          resolve(response)
        })
        .catch((error) => {
        })
    })
  },
  fetchFamily ({commit}, payload) {
    return new Promise((resolve, reject) => {
      // console.log(payload.filter)
      // axios.get('/families/', {params: {filter: payload.filter}})
      // TODO family id
      axios.get('/families/23/')
        .then((response) => {
          console.log(response.data)
          commit('SET_FAMILY_MEMBERS', response.data)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  deleteChild ({commit}, task) {
    return new Promise((resolve, reject) => {
      axios.post(`/api/apps/todo/task/${task.id}`, {task})
        .then((response) => {
          commit('UPDATE_TASK', response.data)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  }
}
