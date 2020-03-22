import axios from '@/axios.js'

export default {
  addChild ({ commit }, payload) {
    console.log('add child payload', payload)
    return new Promise((resolve, reject) => {

      axios.post('/children/', { user: payload })
        .then((response) => {
          console.log('response after child added ', response)
          commit('ADD_MEMBER', Object.assign(payload, { user: response.data }))
          resolve(response)
        })
        .catch((error) => {
        })
    })
  },
  fetchFamily ({ commit }, familyId) {
    return new Promise((resolve, reject) => {
      // console.log(payload.filter)
      // axios.get('/families/', {params: {filter: payload.filter}})
      // TODO -> need id of family
      axios.get(`/families/${familyId}/`)
        .then((response) => {
          commit('SET_FAMILY_MEMBERS', response.data.members)
          // commit('UPDATE_FAMILY_INFO', response.data)
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  deleteChild ({ commit }, task) {
    return new Promise((resolve, reject) => {
      axios.post(`/api/apps/todo/task/${task.id}`, { task })
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
