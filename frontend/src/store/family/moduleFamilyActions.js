import axios from '@/axios.js'

export default {
  addChild ({ commit }, payload) {
    payload.profile.user_role = 'child'
    console.log('add child payload', payload)

    return new Promise((resolve, reject) => {
      axios.post('/child/', { user: payload })
        .then((response) => {
          console.log('response after child added ', response)
          commit('ADD_MEMBER', Object.assign(payload, { user: response.data }))
          resolve(response)
        })
        .catch((error) => {
          reject(error)
        })
    })
  },
  fetchFamily ({ commit }, familyId) {
    console.log('payload in fetchFamily', familyId)

    return new Promise((resolve, reject) => {
      axios.get(`/family/${familyId}/`)
        .then((response) => {
          commit('UPDATE_FAMILY', response.data)
          // TODO IDEA: set only children
          // TODO FIXME: UPDATE_FAMILY_INFO
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
