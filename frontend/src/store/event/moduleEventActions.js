import axios from '@/axios.js'

export default {
  // addEvent ({ commit }, payload) {
  //   console.log('add child payload', payload)
  //   return new Promise((resolve, reject) => {
  //
  //     axios.post('/children/', { user: payload })
  //       .then((response) => {
  //         console.log('response after child added ', response)
  //         commit('ADD_MEMBER', Object.assign(payload, { user: response.data }))
  //         resolve(response)
  //       })
  //       .catch((error) => {
  //         reject(error)
  //       })
  //   })
  // },
  // fetchEvents ({ commit }) {
  //   return new Promise((resolve, reject) => {
  //     axios.get('season/events/')
  //       .then((response) => {
  //         console.log(response.data)
  //         commit('SET_EVENTS', response.data.results)
  //         resolve(response)
  //       })
  //       .catch((error) => {
  //         reject(error)
  //       })
  //   })
  // }
  // fetchEvents ({ commit }, payload) {
  //   return new Promise((resolve, reject) => {
  //     console.log('payload in fetchEvents', payload)
  //     axios.get('/season/events/')
  //       .then((response) => {
  //         // commit('SET_EVENTS', response.data.results)
  //         // commit('UPDATE_FAMILY_INFO', response.data)
  //         resolve(response)
  //       })
  //       .catch((error) => {
  //         reject(error)
  //       })
  //   })
  // }
}
