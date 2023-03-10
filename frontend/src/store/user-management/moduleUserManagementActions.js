import axios from '@/axios.js'

export default {
  fetchUsers ({ commit }) {
    console.log('[STORE] fetchUsers')
    return new Promise((resolve, reject) => {
      axios.get('/profiles/')
        .then((response) => {
          commit('SET_USERS', response.data.results)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  fetchProfileStatistics ({ commit }) {
    console.log('[STORE] fetchUsers')
    return new Promise((resolve, reject) => {
      axios.get('/profile-stats')
        .then((response) => {
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  fetchStatistics ({ commit }) {
    console.log('[STORE] fetchUsers')
    return new Promise((resolve, reject) => {
      axios.get('/stats')
        .then((response) => {
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  fetchUser ({ commit }, userId) {
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
  fetchActiveUser ({ commit }, userId = this.state.AppActiveUser.id) {
    console.log('[STORE] fetchUser', userId)
    return new Promise((resolve, reject) => {
      axios.get(`/profile/${userId}/`)
        .then((response) => {
          commit('UPDATE_USER_INFO', response.data, { root: true })
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
  changePassword ({ commit }, payload) {
    console.log('changePassword')
    return new Promise((resolve, reject) => {
      axios.put('/profile/password-change/', payload)
        .then((response) => {
          // TODO commit token or logout
          // Set accessToken
          localStorage.setItem('accessToken', response.data.key)
          commit('auth/SET_BEARER', response.data.token, { root: true })
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  }
}
